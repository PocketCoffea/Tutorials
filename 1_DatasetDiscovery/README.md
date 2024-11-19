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
```
