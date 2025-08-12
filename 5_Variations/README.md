# Variations

Systematic variations in PocketCoffea are classified into two main categories:

- **Weight variations**: Alternative weights applied when filling histograms (e.g., scale factor variations)
- **Shape variations**: Variations that modify the physics objects themselves (e.g., jet energy scale uncertainties)

Both types of variations are managed through the PocketCoffea configuration system and create additional axes in the output histograms.

## Weight variations

In PocketCoffea weights can have variations: either just an up/down single variation, or multiple named variations. 
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

Each variation defines a new axis in the histogram output for that sample. When multiple variations are defined, it is
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

Shape variations modify the physics objects themselves and require re-running the full analysis workflow with corrected object collections. These variations are handled through the **Calibrators** system in PocketCoffea.

### The Calibrators System

The Calibrators system provides a modular framework for applying object corrections and systematic variations. Each calibrator:
- Applies corrections to physics objects (jets, leptons, MET, etc.)  
- Provides systematic variations of those corrections
- Manages dependencies between different corrections

### Built-in Calibrators

PocketCoffea provides several ready-to-use calibrators:

#### JetsCalibrator
- **Purpose**: Applies Jet Energy Corrections (JEC) and Jet Energy Resolution (JER) smearing
- **Collections**: Configurable jet collections (e.g., `Jet`, `FatJet`) 
- **Variations**: JEC uncertainties and JER variations (e.g., `AK4PFchs_jecUp`, `AK4PFchs_jerDown`)
- **Configuration**: Controlled through `jets_calibration` parameters

#### METCalibrator  
- **Purpose**: Propagates jet corrections to Missing Energy (MET)
- **Collections**: MET pt and phi
- **Dependencies**: Must run after `JetsCalibrator`
- **No variations**: Inherits variations from jet corrections

#### ElectronsScaleCalibrator
- **Purpose**: Applies electron energy scale and resolution corrections
- **Collections**: `Electron.pt`, `Electron.pt_original`
- **Variations**: `ele_scaleUp/Down`, `ele_smearUp/Down` (MC only)
- **Configuration**: Controlled through `lepton_scale_factors` parameters

### Configuring Calibrators

Calibrators are configured in the `Configurator`:

```python
from pocket_coffea.lib.calibrators.common import JetsCalibrator, METCalibrator, ElectronsScaleCalibrator

cfg = Configurator(
    # Specify the calibrator sequence
    calibrators = [JetsCalibrator, METCalibrator, ElectronsScaleCalibrator],
    
    # Configure shape variations
    variations = {
        "weights": {
            # ... weight variations
        },
        "shape": {
            "common": {
                "inclusive": [
                    "jet_calibration",              # All JEC/JER variations  
                    "electron_scale_and_smearing"   # All electron variations
                ],
            },
            "bysample": {
                "TTbar": {
                    "inclusive": ["custom_calibrator"]  # Sample-specific variations
                }
            }
        }
    },
)
```

### Shape Variation Workflow

When shape variations are configured, PocketCoffea automatically:

1. **Initialize calibrators** with the original events
2. **Loop over variations**: For each requested systematic variation:
   - Apply calibrators in sequence to produce corrected objects
   - Run the full analysis (preselection, categories, histograms) 
   - Reset events to original state for next variation
3. **Collect results** with separate histogram axes for each variation

### Available JEC/JER Variations

The jet calibration system supports various systematic uncertainties:

- **JEC uncertainties**: `JES_Absolute`, `JES_FlavorQCD`, `JES_BBEC1`, etc.
- **JER uncertainties**: `JER` (jet energy resolution)
- **Total variations**: `JES_Total` (combined JEC uncertainty)

The specific variations available depend on the data-taking year and jet collection, configured in `jets_calibration.yaml`:

```yaml
jets_calibration:
  collection:
    2022:
      AK4PFPuppi: "Jet"
      AK8PFPuppi: "FatJet"
  
  variations:
    total_variation:    # Use total JEC uncertainty  
      2022_preEE:
        AK4PFPuppi: ["JES_Total", "JER"]
    
    full_variations:    # Use individual JEC sources
      2022_preEE:  
        AK4PFPuppi:
          - JES_Absolute
          - JES_FlavorQCD
          - JES_BBEC1
          - JER
```

### Naming Convention

Shape variations follow the naming pattern: `{calibrator_name}_{source}_{direction}`:

- **jet_calibration**: `AK4PFPuppi_jecUp`, `AK4PFPuppi_jerDown`
- **electron_scale_and_smearing**: `ele_scaleUp`, `ele_smearDown`

### Advanced Features

#### Jet pT Regression
PocketCoffea supports ML-based jet pT regression using ParticleNet or UParTAK4:

```python
from pocket_coffea.lib.calibrators.common import JetsPtRegressionCalibrator

cfg = Configurator(
    calibrators = [JetsPtRegressionCalibrator, METCalibrator],
)
```

This applies regression corrections before standard JEC, useful for analyses requiring improved jet energy resolution.

#### Custom Calibrators
Users can create custom calibrators by inheriting from the base `Calibrator` class:

```python
from pocket_coffea.lib.calibrators.calibrator import Calibrator

class MyCustomCalibrator(Calibrator):
    name = "my_calibrator"
    has_variations = True
    isMC_only = True
    calibrated_collections = ["MyObject"]
    
    def initialize(self, events):
        # Initialize calibrator with events
        self._variations = ["my_systematic_Up", "my_systematic_Down"]
    
    def calibrate(self, events, orig_colls, variation, already_applied_calibrators=None):
        # Apply corrections based on variation
        if variation == "my_systematic_Up":
            return {"MyObject.pt": events.MyObject.pt * 1.1}
        # ... handle other variations
```

### Example Configuration

Here's a complete example showing both weight and shape variations:

```python
cfg = Configurator(
    calibrators = [JetsCalibrator, METCalibrator, ElectronsScaleCalibrator],
    
    variations = {
        "weights": {
            "common": {
                "inclusive": ["pileup", "sf_ele_id", "sf_mu_id"],
                "bycategory": {
                    "1btag": ["sf_btag"]
                }
            }
        },
        "shape": {
            "common": {
                "inclusive": ["jet_calibration", "electron_scale_and_smearing"]
            }
        }
    },
    
    variables = {
        **jet_hists(),    # Jet histograms will include all variations
        **ele_hists(),    # Electron histograms will include scale variations  
    }
)
```

This configuration will produce histograms with systematic variations from both weight uncertainties (pileup, scale factors) and shape uncertainties (JEC, JER, electron energy scale).

### Output Structure

The resulting histograms will have a variation axis containing all requested systematics:

```python
# Example histogram with combined variations
output["variables"]["jet_pt"]["TTbar"]["TTbar_2022"][
    {"cat": "1btag", "variation": "AK4PFPuppi_jecUp"}
].values()
```
