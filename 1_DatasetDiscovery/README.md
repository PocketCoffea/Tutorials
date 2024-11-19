# Dataset discovery

The first step of the analysis is usually gathering the necessary data and MC samples. The NanoAOD samples are stored in
different CMS grid sites around the world. 

A central database, called `DBS`, stores the metadata related to the datasets and the files inside them. The files are
replicated in different sites to ensure their availability. In coffea, it is useful to access directly to the file
location without using any redirector in order to avoid xrootd issues.

The files replicas are handled by the `rucio` system. 

In PocketCoffea, datasets are grouped and their metadata are stored in a dictionary saved in `json` format: this is
usually called the `dataset_definitions.json`. This file containes the general dataset names and metadata info: the
`pocket-coffea build-datasets` script can be used to build the full filelist with the file locations, which is then
passed to the analysis processor. 

Moreover a CLI is provided to explore the dataset dynamically and to build the dataset definitions file on the
fly. Different sites can be selected for different datasets. 

Let's play with the CLI, but first let's initialize the environment with the grid-certificate and  the apptainer images
for PocketCoffea. 


```bash
# Enter in the apptainer
voms-proxy-init -voms cms -rfc --valid 168:0

# Load the apptainer image
apptainer shell -B /eos -B /afs -B /cvmfs/cms.cern.ch  -B /tmp -B /eos/cms/  \
               -B /etc/sysconfig/ngbauth-submit   -B ${XDG_RUNTIME_DIR} \
               --env KRB5CCNAME="FILE:${XDG_RUNTIME_DIR}/krb5cc" \
               /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/pocketcoffea:lxplus-el9-latest 

```

Now we can play with the CLI. 

```bash
Singularity> pocket-coffea dataset-discovery-cli

    ____             __        __  ______      ________
   / __ \____  _____/ /_____  / /_/ ____/___  / __/ __/__  ____ _
  / /_/ / __ \/ ___/ //_/ _ \/ __/ /   / __ \/ /_/ /_/ _ \/ __ `/
 / ____/ /_/ / /__/ ,< /  __/ /_/ /___/ /_/ / __/ __/  __/ /_/ /
/_/    \____/\___/_/|_|\___/\__/\____/\____/_/ /_/  \___/\__,_/


> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:
```

The CLI will ask you to select the dataset you want to explore. 
Let's start with a `query`:

```bash
> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:
query (enter)
query for: /SingleMuon/Run201*MiniAODv2_NanoAODv9*/NANOAOD (enter)

Query for: /SingleMuon/Run2018*MiniAODv2_NanoAODv9*/NANOAOD
                 Query: /SingleMuon/Run201*MiniAODv2_NanoAODv9*/NANOAOD                 
Query for: /SingleMuon/Run2018*MiniAODv2_NanoAODv9*/NANOAOD
              Query: /SingleMuon/Run2018*MiniAODv2_NanoAODv9*/NANOAOD              
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Name       ┃ Tag                                                     ┃ Selected ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ SingleMuon │ (1) Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD      │    N     │
│            │ (2) Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD │    N     │
│            │ (3) Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD      │    N     │
│            │ (4) Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD │    N     │
│            │ (5) Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD      │    N     │
│            │ (6) Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD │    N     │
│            │ (7) Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD      │    N     │
│            │ (8) Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD │    N     │
└────────────┴─────────────────────────────────────────────────────────┴──────────┘

> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:

```

Now we can select the dataset we want to explore:

```bash
> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:select (enter)
Select datasets indices (e.g 1 4 6-10) (all): 1
Selected datasets:
- (1) /SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD
```

Now we can list the replicas of the dataset:

```bash
>[help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:replicas (enter)
Select datasets indices (e.g 1 4 6-10) (all): 1
Loading SITECONF info
Sites availability for dataset: /SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD
                 Available replicas                 
┏━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Index ┃ Site            ┃ Files   ┃ Availability ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
│   0   │ T1_US_FNAL_Disk │ 92 / 92 │    100.0%    │
│   1   │ T2_DE_DESY      │ 92 / 92 │    100.0%    │
│   2   │ T1_DE_KIT_Disk  │ 92 / 92 │    100.0%    │
│   3   │ T3_KR_KISTI     │ 92 / 92 │    100.0%    │
│   4   │ T2_IT_Legnaro   │ 92 / 92 │    100.0%    │
│   5   │ T2_CH_CERN      │ 92 / 92 │    100.0%    │
│   6   │ T2_US_Wisconsin │ 92 / 92 │    100.0%    │
│   7   │ T2_BE_IIHE      │ 92 / 92 │    100.0%    │
│   8   │ T2_US_Purdue    │ 92 / 92 │    100.0%    │
│   9   │ T2_ES_CIEMAT    │ 92 / 92 │    100.0%    │
│  10   │ T3_US_NotreDame │ 92 / 92 │    100.0%    │
│  11   │ T3_CH_PSI       │ 92 / 92 │    100.0%    │
│  12   │ T2_DE_RWTH      │ 92 / 92 │    100.0%    │
│  13   │ T3_KR_UOS       │ 92 / 92 │    100.0%    │
│  14   │ T3_US_FNALLPC   │ 91 / 92 │    98.9%     │
│  15   │ T2_UA_KIPT      │ 73 / 92 │    79.3%     │
│  16   │ T2_RU_JINR      │ 73 / 92 │    79.3%     │
│  17   │ T2_US_Caltech   │ 19 / 92 │    20.7%     │
│  18   │ T1_RU_JINR_Disk │ 19 / 92 │    20.7%     │
│  19   │ T1_IT_CNAF_Disk │ 1 / 92  │     1.1%     │
└───────┴─────────────────┴─────────┴──────────────┘

Select sites [round-robin/choose/first/quit] (round-robin): 

```

The files of this dataset are available in many sites. You have the option to select the sites you want to use for the
analysis or to use the round-robin option. 

```bash
Select sites [round-robin/choose/first/quit] (round-robin): choose
Enter list of sites index to be used (0): 5
Filtering replicas with : T2_CH_CERN
Replicas for /SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD
└── T2_CH_CERN
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/00EBBD1F-032C-9B49-A998-7645C9966432.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/02D6A1FE-C8EB-1A48-8B31-149FDFB64893.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/049D7B08-979F-E743-B9BE-4B37EEFD1B47.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/092EE9D3-83AD-FA4D-8443-B97E38F64E6A.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/0A16AAB8-B190-694F-9B25-9789D75E438D.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/0EC110C4-967D-AE49-A2F5-DD7C0369FCBA.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/171C5530-5150-7C44-9029-40794C1FDBF5.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/18CA020F-42A7-FC49-93D2-A828E075A6F4.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/19F638F9-D583-A64C-A524-F99EB99D265B.root
    ├── root://eoscms.cern.ch//eos/cms/store/data/Run2018A/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2550000/1A637715-C2DE-4649-8654-EE35342FEFC4.root
.....
```bash

Now you can check what you have selected until now:

```bash
> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]: list-selected
Selected datasets:
                                           Selected datasets                                            
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Index ┃ Dataset                                                    ┃ Replicas selected ┃ N. of files ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1     │ /SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD │         Y         │     92      │
└───────┴────────────────────────────────────────────────────────────┴───────────────────┴─────────────┘
```

One can proceed to query for more datasets and select them. 

When you are done, you can save the dataset definitions in a json file:

```bash
> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]: save
Output file name (.yaml or .json) (output.json): datasets_from_cli.json
File datasets_from_cli.json saved!
Do you want to empty your selected samples list? [y/n] (n): n
>[help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]

```

### More options
One can filter the sites by using regular expressions, block some sites, or allow only some sites. 

```bash
> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]:regex-sites
Enter regex to filter sites (e.g. T2_.*): T2
New sites regex: T2


> [help/login/query/query-results/select/list-selected/replicas/list-replicas/save/clear/allow-sites/block-sites/regex-sites/sites-filters/quit]: replicas
Select datasets indices (e.g 1 4 6-10) (all): 
Sites availability for dataset: /SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD
                 Available replicas                 
┏━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Index ┃ Site            ┃ Files   ┃ Availability ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
│   0   │ T2_DE_DESY      │ 92 / 92 │    100.0%    │
│   1   │ T2_IT_Legnaro   │ 92 / 92 │    100.0%    │
│   2   │ T2_CH_CERN      │ 92 / 92 │    100.0%    │
│   3   │ T2_US_Wisconsin │ 92 / 92 │    100.0%    │
│   4   │ T2_BE_IIHE      │ 92 / 92 │    100.0%    │
│   5   │ T2_US_Purdue    │ 92 / 92 │    100.0%    │
│   6   │ T2_ES_CIEMAT    │ 92 / 92 │    100.0%    │
│   7   │ T2_DE_RWTH      │ 92 / 92 │    100.0%    │
│   8   │ T2_UA_KIPT      │ 73 / 92 │    79.3%     │
│   9   │ T2_RU_JINR      │ 73 / 92 │    79.3%     │
│  10   │ T2_US_Caltech   │ 19 / 92 │    20.7%     │
└───────┴─────────────────┴─────────┴──────────────┘

```

---

# Build dataset script.

 Once you have built your dataset definition file, either manually or using the CLI, you can use the
`build-datasets` script to build the full filelist with the file locations.  The full format of the dataset definition
file is explained in the [docs](https://pocketcoffea.readthedocs.io/en/stable/datasets.html#datasets-definition-files)

```bash
Singularity> pocket-coffea build-datasets --help

    ____             __        __  ______      ________
   / __ \____  _____/ /_____  / /_/ ____/___  / __/ __/__  ____ _
  / /_/ / __ \/ ___/ //_/ _ \/ __/ /   / __ \/ /_/ /_/ _ \/ __ `/
 / ____/ /_/ / /__/ ,< /  __/ /_/ /___/ /_/ / __/ __/  __/ /_/ /
/_/    \____/\___/_/|_|\___/\__/\____/\____/_/ /_/  \___/\__,_/


Usage: pocket-coffea build-datasets [OPTIONS]

  Build dataset fileset in json format

Options:
  --cfg TEXT                   Config file with parameters specific to the
                               current run  [required]
  -k, --keys TEXT              Keys of the datasets to be created. If None,
                               the keys are read from the datasets definition
                               file.
  -d, --download               Download datasets from DAS
  -o, --overwrite              Overwrite existing .json datasets
  -c, --check                  Check existence of the datasets
  -s, --split-by-year          Split datasets by year
  -l, --local-prefix TEXT
  -ws, --allowlist-sites TEXT  List of sites in whitelist
  -bs, --blocklist-sites TEXT  List of sites in blacklist
  -rs, --regex-sites TEXT      example: -rs 'T[123]_(FR|IT|DE|BE|CH|UK)_\w+'
                               to serve data from sites in Europe.
  -ir, --include-redirector    Use the redirector path if no site is available
                               after the specified whitelist, blacklist and
                               regexes are applied for sites.
  -p, --parallelize INTEGER
  --help                       Show this message and exit.
```
  
As an exercise let's build the datasets for the dataset definition file in this folder. 
  
```bash
Singularity> pocket-coffea build-datasets --cfg datasets_definitions.json --overwrite -rs 'T[0,1,2]' -p 4

    ____             __        __  ______      ________
   / __ \____  _____/ /_____  / /_/ ____/___  / __/ __/__  ____ _
  / /_/ / __ \/ ___/ //_/ _ \/ __/ /   / __ \/ /_/ /_/ _ \/ __ `/
 / ____/ /_/ / /__/ ,< /  __/ /_/ /___/ /_/ / __/ __/  __/ /_/ /
/_/    \____/\___/_/|_|\___/\__/\____/\____/_/ /_/  \___/\__,_/


Building datasets...
Allowlist sites:
()
Blocklist sites:
()
Dataset keys: ['DYJetsToLL_M-50', 'DATA_SingleMuon']
****************************************
> Working on dataset:  DYJetsToLL_M-50
>> Query for sample: DYJetsToLL,  das_name: ['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM']
****************************************
> Working on dataset:  DATA_SingleMuon
>> Query for sample: DATA_SingleMuon,  das_name: ['/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD']
>> Query for sample: DATA_SingleMuon,  das_name: ['/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD']
>> Query for sample: DATA_SingleMuon,  das_name: ['/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD']
>> Query for sample: DATA_SingleMuon,  das_name: ['/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD']
>> Query for sample: DATA_SingleMuon,  das_name: ['/SingleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD']
Saving datasets DYJetsToLL_M-50 to datasets/DYJetsToLL_M-50.json
Saving datasets DYJetsToLL_M-50 to datasets/DYJetsToLL_M-50_redirector.json
Saving datasets DATA_SingleMuon to datasets/DATA_SingleMuon.json
Saving datasets DATA_SingleMuon to datasets/DATA_SingleMuon_redirector.json
```

Let's have a look at the datasets we have created:

```bash
Singularity> cat datasets/DJetsToLL_M-50.json
{    
"DYJetsToLL_M-50_2018": {
        "metadata": {
            "das_names": "['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM']",
            "sample": "DYJetsToLL",
            "year": "2018",
            "isMC": "True",
            "xsec": "6077.22",
            "nevents": "195510810",
            "size": "257265865671"
        },
        "files": [
            "root://cmsdcadisk.fnal.gov//dcache/uscmsdisk/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/13D0AD97-6B32-CB4C-BA87-5E37BA4CF20E.root",
            "root://dcache-cms-xrootd.desy.de:1094//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/00C9792D-ACD2-2547-BB04-097F0C4E47E3.root",
            "root://dcache-cms-xrootd.desy.de:1094//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/00EA9563-5449-D24E-9566-98AE8E2A61AE.root",
            ....
```

Metadata are included in the fileset for each dataset (takes from your dataset definition file).  The explicit dataset
location for each file is also included. You can spot some files from FNAL and some from DESY dCache. 


In PocketCoffea samples and datasets are not synonymous.

- Sample: groups events of the same type that are considered together for the analysis.
- Dataset: a collection of files that are grouped together for the analysis. They have a specific sample name. They have
  metadata information specifying the sample name, the year, the cross-section, the number of events, and the size.
