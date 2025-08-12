# Example configuration with shape variations for the 5_Variations tutorial
from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_definition import Cut
from pocket_coffea.lib.cut_functions import get_nObj_min, get_HLTsel, get_nPVgood, goldenJson, eventFlags
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.parameters.histograms import *

import workflow
from workflow import BasicProcessor

# Import calibrators for shape variations
from pocket_coffea.lib.calibrators.common import JetsCalibrator, METCalibrator, ElectronsScaleCalibrator

# Register custom modules in cloudpickle to propagate them to dask workers
import cloudpickle
import custom_cut_functions
cloudpickle.register_pickle_by_value(workflow)
cloudpickle.register_pickle_by_value(custom_cut_functions)

from custom_cut_functions import *
import os
localdir = os.path.dirname(os.path.abspath(__file__))

# Creating weights configuration
from pocket_coffea.lib.weights.common import common_weights

# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

parameters = defaults.merge_parameters_from_files(default_parameters,
                                                    f"{localdir}/params/object_preselection.yaml",
                                                    f"{localdir}/params/triggers.yaml",
                                                   update=True)

cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": ['datasets/datasets_redirector.json'],
        "filter" : {
            "samples": ['TTTo2L2Nu', "DATA_SingleMuon"],
            "samples_exclude" : [],
            "year": ['2018']
        }
    },

    workflow = BasicProcessor,

    # Configure calibrators for shape variations
    calibrators = [
        JetsCalibrator,         # Applies JEC/JER corrections and systematic variations
        METCalibrator,          # Propagates jet corrections to MET
        ElectronsScaleCalibrator, # Applies electron energy scale/smearing corrections
    ],

    skim = [get_nPVgood(1), eventFlags, goldenJson], 

    preselections = [passthrough],
    categories = {
        "baseline": [passthrough],
        "1btag": [get_nObj_min(1, coll="BJetGood")],
        "2btag": [get_nObj_min(2, coll="BJetGood")],
        "2jets": [get_nObj_min(2, coll="JetGood")],
    },

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS","pileup",
                          "sf_ele_id","sf_ele_reco",
                          "sf_mu_id","sf_mu_iso",
                          ],
            "bycategory": {
                "1btag": ["sf_btag"],
                "2btag": ["sf_btag"],
            },
       },
        "bysample": {
            "TTTo2L2Nu": {
                "bycategory": {
                    "1btag": ["sf_mu_trigger"],
                    "2btag": ["sf_mu_trigger"],
                }
            }
        }
    },
    # Using default common weights
    weights_classes = common_weights,

    variations = {
        "weights": {
            "common": {
                "inclusive": [ "pileup",
                               "sf_ele_id", "sf_ele_reco", 
                               "sf_mu_id", "sf_mu_iso",
                               ],
                "bycategory" : {
                    "1btag": ["sf_btag"],
                    "2btag": ["sf_btag"],
                }
            },
            "bysample": {
                "TTTo2L2Nu": {
                    "bycategory": {
                        "1btag": ["sf_mu_trigger"],
                        "2btag": ["sf_mu_trigger"],
                    }
                }
            }
        },
        # Shape variations configuration
        "shape": {
            "common": {
                "inclusive": [
                    "jet_calibration",              # All JEC/JER variations from JetsCalibrator
                    "electron_scale_and_smearing",  # All electron energy scale variations
                ],
            },
        }
    },

    variables = {
        **ele_hists(),      # Electron histograms - will include ele_scale and ele_smear variations
        **jet_hists(),      # Jet histograms - will include JEC and JER variations
        **count_hist("JetGood"),  # Jet multiplicity - affected by JEC variations
        **count_hist("BJetGood"), # B-jet multiplicity - affected by JEC variations
        "MET_pt": HistConf([Axis(coll="MET", field="pt", label="MET pT [GeV]", bins=50, start=0, stop=200)]),
    },

    columns = {
        # Can export columns for all variations - useful for detailed studies
    },
)
