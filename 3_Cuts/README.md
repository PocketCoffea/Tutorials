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
1. Define a new cartesian selection by combining N. Leptons and Jet pt cuts
2. Add this selection to the categories dictionary
3. Run the analysis and check the output

## Subsamples
Subsamples are a way to define a set of cuts that are applied to a specific sample. 

```python


## Primary Datasets duplicates cross-cleaning
