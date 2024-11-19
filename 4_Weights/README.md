# Weights

Weights are applied to MC events to correct for efficiencies, scale factors, and XS. 

In PocketCoffea, weights can be configured by category or by sample using the configuration file. 


```python

from pocket_coffea.lib.weights.common import common_weights

cfg = Configurator(

    weights_classes = common_weights,

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                          "pileup",
                          "sf_ele_reco", "sf_ele_id",
                          "sf_mu_id","sf_mu_iso",
                          "sf_btag", "sf_jet_puId", 
                          ],

            "bycategory" : {
                "2jets_20pt" : [.....]
            }

        },
        "bysample": {
             "TTToSemiLeptonic": {
                  "inclusive": [...],
                  "bycategory": { 
                       "2jets_20pt": [....]
                   }
             }
        }
    },
    weights_classes = common_weights

)
```

Weights are conveniently identified with a name. Weights are made available to the analysis workflow using the
`weights_classes` parameter of the configurator. The Weight classes define the code which compute the weight and define
uniquely the name of the weight. PocketCoffea has an internal mechanism to avoid the duplication of the same weight name
in an analysis configuration.

The user can include the commonly defined weights or define custom one. The available common weights are defined in
[pocket_coffea/lib/weights/common](https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/weights/common/common.py). 

A full explanation and documention is available in the
[docs](https://pocketcoffea.readthedocs.io/en/stable/configuration.html#weights).

N.B.: Weights are never applied to Data samples (`isMC=True` in the dataset metadata).

## Custom weights

Custom weights are very easy to define. An utility to wrap lambda function as Weights is available in the library. 

```python
from pocket_coffea.lib.weights.weights import WeightLambda


my_custom_sf  = WeightLambda.wrap_func(
    name="sf_custom",

    function=lambda params, metadata, events, size, shape_variations:
        call_to_my_fancy_function(events, params, metadata, shape_variations)

    has_variations=True
)
```

If the lambda returns more than 1 arrays, Weights variations are considered. For example: 

```python 

my_custom_weight = WeightLambda.wrap_func(
    name="my_custom_weight",
    function=lambda params, metadata, events, size, shape_variations:
         np.ones(size) * 2.0,
    has_variations=False
    )


my_custom_weight_variations = WeightLambda.wrap_func(
    name="my_custom_weight_withvar",
    function=lambda params, metadata, events, size, shape_variations:
         (np.ones(size) * 2.0, np.ones(size) * 3.0, np.ones(size) * 0.5),
    has_variations=True
    )
```

Sometimes is necessary to define multiple named variations of the same weight (think about the btagSF variations). It is
possible to do it with a WeightLambda:

```python

my_custom_weight_multivariations = WeightLambda.wrap_func(
    name="my_custom_weight_multivar",
    function=lambda params, metadata, events, size, shape_variations:
         (
             np.ones(size) * 2.0,
             ["stat", "syst"], # name of the variations
             [np.ones(size) * 3.0, np.ones(size) * 4.0], # up
             [np.ones(size) * 0.5, np.ones(size) * 0.25] # down
          ),
    has_variations=True,
    variations=["stat", "syst"]
    )
```

To make the custom Weight available in the configuration, it is necessary to include it in the `weights_classes`
parameter. The weight name becomes available to be used as a string. 

```python
weights_classes = common_weights + [my_custom_weight, my_custom_weight_variations, my_custom_weight_multivariations]
```

### Exercises
1. Have a look at the common weights defined in the library.
2. Customize the configuration to modify the weights applied to different samples. 
3. Run the configuration and have a look at the results
4. Define a custom weight depending on the pt of the leading jet.
5. Add the custom weight in a category and apply it to the analysis.


## More complicated Weights implementations

In some cases, the weight computation is more complicated and requires a more complex implementation. In this case, it
is possible to define a custom class that inherits from the `Weight` class directly. 
This is necessary when the weight computation requires a more complex logic, or when the weight computation is based on
different parameters depending on the sample or data taking period. 

In fact, the Weight object is recreated for each chunk, and the dataset metadata is passed to the constructor of the
weight, alongside with the analysis parameters. 

```python
from pocket_coffea.lib.weights_manager import WeightWrapper


# example of WeightWrapper definition

class CustomTopSF(WeightWrapper):

    name = "top_sf"
    has_variations = True

    def __init__(self, params, metadata):
        super().__init__(params, metadata)
        self.sf_file = params["top_sf"]["json_file"]
        # custom variations from config
        self._variations = params["top_sf"]["variations"]


    def compute(self, events, size, shape_variation):

        if shape_variation == "nominal":
            sf_data = sf_function.compute(self.sf_file, events)
            return WeightDataMultiVariation(
                name = self.name, 
                nominal = sf_data["nominal"],
                up = [sf_data[var] for var in self._variations["up"]],
                down = [sf_data[var] for var in self._variations["down"]]
            )
        else:
            return WeightData(
                name = self.name, 
                nominal = np.ones(size),
            )
```


### Exercises
1. Have a look at the `Weight` class definition in the library
   [code](https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/weights/weights.py#L91)
2. Have a look at the definition of common weights in the library
   [code](https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/weights/common/common.py)
3. Define a custom weight class that computes a weights based on the number of jets in the event.
4. Add the custom weight in the configuration and apply it to the analysis.
