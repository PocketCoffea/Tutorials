# Analysis Facilities setup

## Lxplus
Lxplus can be used to submit jobs to condor using dask as a scheduler. 

Example to submit an analysis using the dask scheduler on lxplus. 

```bash
# Setup grid certificate
voms-proxy-init -voms cms -rfc --valid 168:0

# Load the apptainer image
apptainer shell -B /eos -B /afs -B /cvmfs/cms.cern.ch  -B /tmp -B /eos/cms/  \
               -B /etc/sysconfig/ngbauth-submit   -B ${XDG_RUNTIME_DIR} \
               --env KRB5CCNAME="FILE:${XDG_RUNTIME_DIR}/krb5cc" \
               /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/pocketcoffea:lxplus-el9-latest 

Singularity> pocket-coffea run --cfg config.py --executor dask@lxplus --scaleout 100 --chunksize 400000 \
             --worker-image
             /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/pocketcoffea:lxplus-el9-latest \
             --queue microcentury
             
```
The dask scheduler monitoring page is available at the post 8787. You can open a SSH tunnel to lxplus with port forwarding to access the monitoring page. 

```bash
ssh -L 8787:localhost:8787 lxplus.cern.ch

# Open a browser and go to http://localhost:8787/status
```

Cons:
- the lxplus session needs to remain open for the job to run
- once the processing is done the jobs are killed

## CERN SWAN Analysis Facility
The CERN SWAN analysis facility can be used to use a nice Jupyterlab interface to run the analysis.
In this case the dask scheduler is running on the SWAN infrastructure and the workers stay alive even between different
analysis runs. 

To setup the SWAN environment to use PocketCoffea, few steps are needed. 

1. Create a startup script in your EOS base folder to setup some environment variables in SWAN. Assuming your user name
is `username`
```bash

cat << 'EOF' > /eos/user/u/username/setup_swan.sh
#!/bin/sh

export X509_USER_PROXY=/eos/user/u/username/my_x509_user_proxy
export PATH=/eos/user/u/username/.local/bin:$PATH
export PYTHONPATH=/eos/user/u/username/.local/lib/python3.11/site-packages:$PYTHONPATH
EOF
```
This is needed only once, the first time you setup the SWAN environment.

2. Copy your grid certificate secrets to EOS
```bash
# from lxplus
cp ~/.globus /eos/user/u/username/
```
This is needed only once, the first time you setup the SWAN environment.

3. Go to https://swan.cern.ch:
   - Select "Try new Jupyterlab interface"
   - In environment script put `$CERNBOX_HOME/setup_swan.sh`
   - In the "External computing resources", for HTcondor pool select `CERN HTcondor pool`
   - Click start


4. Once inside Swan, open a terminal and run the following commands
```bash
# setup authentication for swan and grid-certificate
voms-proxy-init -voms cms -rfc --valid 168:0

kinit 
```
This is needed all the time. The CMS grid certificate should be valid for 168 hours. `kinit` is needed to access condor,
without it the kerberos ticket will expire and the dask scheduler won't be able to start.

5. Install PocketCoffea in the local python environment located in the EOS folder at `/eos/user/u/username/.local`
   **N.B.**: Note that the `--editable` option (-e) does not work in Swan.
```bash
pip install --user pocket-coffea
```
This is only needed when you want to update PocketCoffea.


6. Open the Dask tab on the left and click on `New` to start a dask scheduler
7. Click on "Scale" to start the workers

To run the PocketCoffea analysis, one needs to pass the scheduler url (visible in the Scheduler tab) to the `pocket-coffea` command. 

```bash
pocket-coffea run --cfg config.py -e dask@swan --sched-url <scheduler-url> --chunksize 400000
```

In the Swan AF the workers will use the same package version as the one installed locally in the EOS python folder.


## INFN Analysis Facility
