# Variations

Systematic variations are usually Weights variations or Shape variations: 

- Weight variations: just different weights that are applied alternatively when filling histograms
- Shape variations: variations of the object calibrations which make necessary to rerun multiple times the analysis
  workflow on varied collections. 
  
## Weight variations

In PocketCoffea Weights can have variations: either just an up/down single variation, or multiple named variations. 
Have a look at the previous step of the tutorial [Weights](../4_Weights) for more details. 

The variations to include in the histogram outputs are specified by sample and by category with a dictionary in the
configuration file. 

```python

cfg = Configurator(
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
                    "2jets_C": ["my_custom_weight_withvar"],
                }
            },
            "bysample": {
                "TTTo2L2Nu": {
                    "bycategory": {
                        "1btag": ["sf_mu_trigger"],
                        "2jets_D": ["my_custom_weight_multivar"]
                    }
            }
            }
        },
    },
)
```

Each variation defines a new axis in the histogram output for that sample. 

When multiple variations are defined, it is
sufficient to specify the general weight name and all the variations will be included. 
This allows the framework to customize the available variations for different data taking periods. 
For an example, have a look at the btagSF
[implementation](https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/weights/common/common.py#L106)

The output of the configuration will look like: 


```python

'TTTo2L2Nu': {'TTTo2L2Nu_2018': Hist(
                  StrCategory(['1btag', '2btag', '2jets', '2jets_B', '2jets_C', '2jets_D', 'baseline'], name='cat', label='Category'),
                  StrCategory(['my_custom_weight_multivar_statDown', 'my_custom_weight_multivar_statUp', 
                  'my_custom_weight_multivar_systDown', 'my_custom_weight_multivar_systUp', 
                  'my_custom_weight_withvarDown', 'my_custom_weight_withvarUp', 
                  'nominal', 'pileupDown', 'pileupUp', 'sf_btag_cferr1Down', 'sf_btag_cferr1Up', 
                  'sf_btag_cferr2Down', 'sf_btag_cferr2Up', 'sf_btag_hfDown', 'sf_btag_hfUp', 
                  'sf_btag_hfstats1Down', 'sf_btag_hfstats1Up', 'sf_btag_hfstats2Down', 
                  'sf_btag_hfstats2Up', 'sf_btag_lfDown', 'sf_btag_lfUp', 'sf_btag_lfstats1Down', 
                  'sf_btag_lfstats1Up', 'sf_btag_lfstats2Down', 'sf_btag_lfstats2Up', 'sf_ele_idDown',
                  'sf_ele_idUp', 'sf_ele_recoDown', 'sf_ele_recoUp', 'sf_mu_idDown', 'sf_mu_idUp', 
                  'sf_mu_isoDown', 'sf_mu_isoUp', 'sf_mu_triggerDown', 'sf_mu_triggerUp'], name='variation', label='Variation'),
                  Regular(50, -2.5, 2.5, name='JetGood.eta', label='$\\eta_{j}$'),
                  
In [11]: output["variables"]["nJetGood"]["TTTo2L2Nu"]["TTTo2L2Nu_2018"][{"cat": "1btag","variation":"sf_btag_hfstats2Up"}].values()
Out[11]: 
array([      0.        ,  523178.55490659, 1440712.13801668,
       1331449.24633987,  719456.14197037,  291536.5644295 ,
        100138.56199999,   29658.35231088,    8087.11802913,
             0.        ])

```


## Shape variations

In PocketCoffea shape variations are applied after the skimming step. The full workflow from preselection to histogram
output is run for different shape variations. 

The customization of shape variations is under development at the ongoing CAT hackathon. **Please refer back to this
tutorial in the near future :)** 
