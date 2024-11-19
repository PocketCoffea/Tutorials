# Simple Config

In this part of the tuturial we will run a very basic analysis to look for the Zmumu peak in data and MC. 

Let's look at the content of the folder:
```bash
-rw-r--r--. 1 user zh   3.4K Nov 19 10:08 example_config.py
-rw-r--r--. 1 user zh   2.6K Nov 19 10:08 workflow.py
-rw-r--r--. 1 user zh    763 Nov 19 10:08 custom_cut_functions.py
-rw-r--r--. 1 user zh     48 Nov 19 10:08 custom_run_options.yaml
drwxr-xr-x. 2 user zh   2.0K Nov 19 10:07 datasets
drwxr-xr-x. 2 user zh   2.0K Nov 19 10:08 params
    -rw-r--r--. 1 dvalsecc zh 194 Nov 19 10:08 triggers.yaml
    -rw-r--r--. 1 dvalsecc zh  47 Nov 19 10:08 plotting.yaml
    -rw-r--r--. 1 dvalsecc zh 316 Nov 19 10:08 object_preselection.yaml

-rw-r--r--. 1 user 1000   17 Nov 19 10:08 README.md

```

- `example_config.py` is the main configuration file for the analysis. It contains the definition of the datasets, the
  cuts, the variables to plot, etc.
- `workflow.py` contains the code customizing the analysis workflow. It is used to define the custom object cleaning
  steps and other custom analysis steps. In this particular example it is minimal.
  
- `params` is a folder containing the parameter files for the analysis. The files defining the object preselections, the
  triggers and the plotting configuration
  
- `datasets` is a folder containing the datasets used in the analysis. The datasets are defined in json files defined in
  the first part of the tutorial. 
  
- `custom_cut_functions.py` contains the custom cut functions used in the analysis.
- `custom_run_options.yaml` contains the custom run options for the analysis. It is used to define the number of events
  to process, the number of threads to use, etc.
  
## The config file

In PocketCoffea the analysis is steered by a configuration file. The configuration file is a python file that defines
a `Configurator` object. The configurator contains all the information necessary to customize: 

- the workflow applied to the events: `worflow`
- the datasets used in the analysis: `datasets`
- the skim and preselection cuts applied to the events: `skim`, `preselection`
- the categories in which events will be splitted: `cuts`
- the weights are applied to the events: `weights`
- the variables plotted as histograms: `variables`
- the systematic variations applied to the events: `variations`
- the columns exported from the analysis: `columns`

For a full explanation of the configuration file see the
[documentation](https://pocketcoffea.readthedocs.io/en/stable/configuration.html).

In this example we are going to look for 2 muons and compute their invariant mass. 
We will select events with 2 muons with opposite charge. 

The datasets used for the analysis are defined in the `datasets` dictionary. The datasets are defined in json files.
```python
cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": [f"{localdir}/datasets/DATA_SingleMuon_xc2.json",
                  f"{localdir}/datasets/DYJetsToLL_M-50_xc2.json"
                    ],
        "filter" : {
            "samples": ["DATA_SingleMuon",
                        "DYJetsToLL"],
            "samples_exclude" : [],
            "year": ['2018']
        }
    },

    workflow = ZmumuBaseProcessor,
    )
```

The `workflow` is defined in the `workflow.py` file. It is a class that inherits from `BaseProcessor` and defines the
custom steps of the analysis. In this case the `ZmumuBaseProcessor` is a minimal class that does not define any custom
step, a part from the object cleaning (and object counting) which is compulsory for each different analysis. 

```python 
class ZmumuBaseProcessor(BaseProcessorABC):
    def __init__(self, cfg: Configurator):
        super().__init__(cfg)


    def apply_object_preselection(self, variation):
        '''
        The ttHbb processor cleans
          - Electrons
          - Muons
          - Jets -> JetGood
          - BJet -> BJetGood

        '''
        # Include the supercluster pseudorapidity variable
        electron_etaSC = self.events.Electron.eta + self.events.Electron.deltaEtaSC
        self.events["Electron"] = ak.with_field(
            self.events.Electron, electron_etaSC, "etaSC"
        )
        # Build masks for selection of muons, electrons, jets, fatjets
        self.events["MuonGood"] = lepton_selection(
            self.events, "Muon", self.params
        )
        self.events["ElectronGood"] = lepton_selection(
            self.events, "Electron", self.params
        )
        leptons = ak.with_name(
            ak.concatenate((self.events.MuonGood, self.events.ElectronGood), axis=1),
            name='PtEtaPhiMCandidate',
        )
        self.events["LeptonGood"] = leptons[ak.argsort(leptons.pt, ascending=False)]

        self.events["JetGood"], self.jetGoodMask = jet_selection(
            self.events, "Jet", self.params, "LeptonGood"
        )
        self.events["BJetGood"] = btagging(
            self.events["JetGood"], self.params.btagging.working_point[self._year], wp=self.params.object_preselection.Jet.btag.wp)

        self.events["ll"] = get_dilepton(
            self.events.ElectronGood, self.events.MuonGood
        )
```

The `apply_object_preselection` method is used to clean the objects in the event. In this case we are selecting the
muons and electrons that pass the loose ID and the loose isolation. We are also selecting the jets that pass the loose
jet ID and the loose jet isolation. 

The functions applied to clean the object are defined in the PocketCoffea library, as they are considered general and
common to many CMS analysis. The **parameters** are taken from the `parameters` yaml configuration, and they follow the
format that these common functions expect. There is not formal restriction on the format of the parameters, but it is
recommended to follow the format of the parameters used in the PocketCoffea library, if the user wants to use the
functions defined in the library. Otherwise, the user is free to define locally more function, import them in the script
and use custom parameters schema. **It is strongly recommended to avoid any hardcoding in the analysis script**, but to
define all the parameters in the `parameters` yaml configuration file, so that many groups can share the same analysis
setup and the configuration is easily maintainable.
