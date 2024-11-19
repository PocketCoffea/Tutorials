# Cuts customization in PocketCoffea

Cuts are one of the fundamental operation in performing an analysis. 
In PocketCoffea, we provide a simple way to customize the cuts that you want to apply to your analysis.

A Cut object is a simple wrapper that contains a cut function, a name for the cut to be used in the configuration,
and the parameters to be passed to the cut function. This allows the user to define multiple cuts without duplicating
the cut function.

Cut object can be defined alongside the user configuration and used inside the `skim`, `preselection`, and `categories`
arguments of the configurator. 

The cut functions needs to have a specific signature, that is:

```python
def cut_function(events, params, year, sample, **kwargs):
    # Put here your selection logic
    return boolean_mask 
```

As an example

```python 
import awkward as ak
from pocket_coffea.lib.cut_definition import Cut

def min_jet_pt(events, params, year, sample, **kwargs):
    mask = ak.sum(events.Jet.pt > params["jet_pt"], axis=1)>0
    return mask
    

cut = Cut(
    name="my_first_cut",
    params={
        "param2": 2,
    },
    function=min_jet_pt,
)
```

Many common cuts are already implemented in PocketCoffea: have a look at
https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/cut_functions.py


---
## Categories
Categories are by default expressed as a dictionary of cuts. Each category is defined by the AND of the list of cuts
associated with it. 

```python 
categories = {
        "baseline": [passthrough],
        "1btag": [get_nObj_min(1, coll="BJetGood")],
        "1btag_B": [get_nObj_min(1, coll="BJetGood")],
        "2btag": [get_nObj_min(2, coll="BJetGood")],
    },
```
If a cut object is duplicated, its related function will be executed only once, avoiding unnecessary computation.
Factory functions returning a Cut objects can also be used: if the weight name, parameters, and function are the same,
the cut will be also cached. 

This configuration has the limitation that only 64 categories can be defined. If you need more categories, you can
look at the following section.

The weights and variations can be customized for each category. Have a look at the
[config_baseline.py](./config_baseline.py) configuration file. 

### Exercise
1. Define a new cut that selects events with at least 2 jets with pt > 30 GeV
2. Add this cut to the categories dictionary
3. Run the analysis and check the output


## Cartesian selection
Sometimes it is necessary to create many categories, for example combining different binning in different observables.
This is a quite common use case in the analysis of differential cross-sections.

In PocketCoffea, we provide a way to define a cartesian selection. A `MultiCut` object is a simple wrapper that contains
a list of cuts, and names to assign to each "bin". Multiple `MultiCut` objects can be combined in a
`CartesianSelection`, which will generate all the possible combinations of the cuts.
Moreover, a set of common cuts can be defined and combined with the cartesian selection.


```python
from pocket_coffea.lib.categorization import StandardSelection, CartesianSelection, MultiCut

 categories = CartesianSelection(
        multicuts = [
            MultiCut(name="Njets",
                     cuts=[
                         get_nObj_eq(1, 30., "JetGood"),
                         get_nObj_eq(2, 30., "JetGood"),
                         get_nObj_min(3, 30., "JetGood"),
                     ],
                     cuts_names=["1j","2j","3j"]),
            MultiCut(name="Nbjet",
                    cuts=[
                         get_nObj_eq(0, 15., "BJetGood"),
                         get_nObj_eq(1, 15., "BJetGood"),
                         get_nObj_eq(2, 15., "BJetGood"),
                         get_nObj_min(3, coll="BJetGood"),
                     ],
                     cuts_names=["0b","1b","2b","3b"])
        ],
        common_cats = {
            "inclusive": [passthrough],
            "4jets_40pt" : [get_nObj_min(4, 40., "JetGood")]
        }
    ),
```

This configuration will generate the following categories:

- inclusive
- 4jets_40pt
- 1j_0b
- 1j_1b
- 1j_2b
- 1j_3b
- 2j_0b
- 2j_1b

and so on.

This configuration is internally implemented to be fast and to avoid waste of memory and CPU time.
This allows PocketCoffea to overcome the 64 categories limitation of the `PackedSelection` coffea object.

### Exercise
0. Have a look at the [config_cartesian.py](./config_cartesian_categories.py) configuration file
1. Define a new cartesian selection by combining N. Leptons and Jet pt cuts
2. Add this selection to the categories dictionary
3. Run the analysis and check the output

## Subsamples
Subsamples are a way to define a set of cuts that are applied to a specific sample. 
Subsamples are a special kind of cut because they are applied on top of the rest of the skim/preselection/categorization
and the end of the workflow. In practice subsamples cuts are used to split the events before the final histogramming /
output step. 

Subsamples are defined with Cuts in the `datasets` entry of the Configurator. 

```python
cfg = Configurator(
    datasets = {
        "jsons": ['datasets/datasets_cern.json'],
        "filter" : {
            "samples": ['TTTo2L2Nu', "DATA_SingleMuon", "DATA_SingleEle"],
            "samples_exclude" : [],
            "year": ['2018']
        },
        "subsamples": {
            "TTTo2L2Nu": {
                "ele": [get_nObj_min(1, coll="ElectronGood"), get_nObj_eq(0, coll="MuonGood")],
                "mu":  [get_nObj_eq(0, coll="ElectronGood"), get_nObj_min(1, coll="MuonGood")],
            },
            "DATA_SingleMuon": {
                "clean": [get_HLTsel(primaryDatasets=["SingleEle"], invert=True)], # crosscleaning SingleELe trigger on SIngleMuon
            }
        }
    },

```
Subsamples are visible in the output file as a separate Sample entry, e.g. `TTTo2L2Nu_ele`, `TTTo2L2Nu_mu`,
`DATA_SingleMuon_clean`.

Samples for which no subsamples have been defined are internally considered as a subsample with no cuts.


### Exercise
1. Have a look at the [config_subsamples.py](./config_subsamples.py) configuration file
2. Define a new subsample for the TTTo2L2Nu sample that selects events with at least 2 jets with pt > 30 GeV
3. Run the analysis and check the output


## Primary Datasets duplicates cross-cleaning
The subsample mechanism can be used to implement a cross-cleaning between primary datasets for the Data samples. 
This is needed to remove events passing a certain trigger used to define a primary dataset from another primary dataset.

Have a look at the [config_crosscleaning.py](./config_crosscleaning.py) configuration file.

```python 
    datasets = {
        "jsons": ['datasets/datasets_cern.json'],
        "filter" : {
            "samples": [ "DATA_SingleMuon", "DATA_SingleEle"],
            "samples_exclude" : [],
            "year": ['2018']
        },
        "subsamples": {
            "DATA_SingleEle": {
                "clean": [get_HLTsel(primaryDatasets=["SingleElectron"])],
            },
            "DATA_SingleMuon": {
                "clean": [get_HLTsel(primaryDatasets=["SingleEle"], invert=True)], # crosscleaning SingleELe trigger on SIngleMuon
            }
        }
    },
```

The `get_HLTsel` cut is a factory function that returns a Cut object that applies the HLT selection on the events.
The trigger applied for each primaryDataset are defined in the `params/triggers.yaml` file.

```yam
HLT_triggers:
  "2016_PostVFP":
    SingleEle:
        - Ele32_WPTight_Gsf

    SingleMuon:
        - IsoMu24

  "2018":
    SingleEle:
        - Ele32_WPTight_Gsf
        - Ele28_eta2p1_WPTight_Gsf_HT150

    SingleMuon:
        - IsoMu24
        - IsoTkMu24
```

This mechanism is used to remove events that pass the `Ele32_WPTight_Gsf` trigger from the `DATA_SingleMuon` sample.

Later in the `skim` cuts the full HLT selection for both primary datasets is applied. The `skim` cuts are applied on
both data and MC samples, so that a full OR of all the HLT triggers is applied to the MC samples.
The subsamples mechanism is used to apply the cross-cleaning only to the data samples.

### Exercise
1. Have a look at the [config_crosscleaning.py](./config_crosscleaning.py) configuration file
2. Define a new primary dataset and a new trigger in the `params/triggers.yaml` file
3. Define a new cross-cleaning subsample for the new primary dataset0
