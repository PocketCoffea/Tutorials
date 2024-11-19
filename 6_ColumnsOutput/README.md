# Columns output

PocketCoffea can export histograms, but also arrays. This is necessary for example to prepare the training dataset for
machine learning models. 

There are 2 main way of exporing arrays from PocketCoffea:
1. as numpy arrays directly in the output file
2. as awkward arrays exported as parquet files for each chunk. 

In both cases the arrays to export are configured with a dictionary of `ColOut` objects in the analysis configuration
file. 
Full details in the [docs](https://pocketcoffea.readthedocs.io/en/stable/configuration.html#columns-output).

```python 

cfg = Configurator(
   # columns output configuration
   columns = {
        "common": {
             "inclusive": [ColOut("LeptonGood",["pt","eta","phi"])],
             "bycategory": {}
        },
        "bysample": {
            "TTTo2L2Nu" :{ "inclusive":  [ColOut("JetGood",["pt","eta","phi"])]},
        }
    }
)
```

As usual the configuration is done by category or by sample. 

The `ColOut` object has many options: 

```python
@dataclass
class ColOut:
    collection: str  # Collection
    columns: List[str]  # list of columns to export
    flatten: bool = True  # Flatten by defaul
    store_size: bool = True
    fill_none: bool = True
    fill_value: float = -999.0  # by default the None elements are filled
    pos_start: int = None  # First position in the collection to export. If None export from the first element
    pos_end: int = None  # Last position in the collection to export. If None export until the last element
```

In case the arrays are saved and accumulated in the output file directly, it is necessary to flatten out the arrays. if
`ColOut(flatten=True)` is used, an additional column `nCollection` is saved to be able to unflatten the array later. 

It is also possible to pad the arrays by specifying a `pos_end` and `fill_none` option. 

### Exercises
1. Have a look at the `config_baseline.py`
2. Add a new column output for the `LeptonGood` collection
3. Add a new column output for the `JetGood` collection only for 1 sample
4. Run the analysis and check the output file
   

## Exporting Awkward arrays in parquet file
It is often more useful to export a parquet file with awkward arrays output for each chunk of processing. This procedure
helps reducing the problem of memory usage when exporting large datasets to a single output file. Moreover collections
do not need to be flattened to numpy as we can export directly the awkward arrays. Full docs [here](https://pocketcoffea.readthedocs.io/en/stable/configuration.html#exporting-chunks-in-separate-files).

This is done just by setting a `workflow_option` with the output target folder used to store the output. 
```python
cfg = Configurator(
   workflow_options = {
        "dump_columns_as_arrays_per_chunk": "root://eosuser.cern.ch//eos/user/y/yourusername/output_folder/"
        },
)
```

