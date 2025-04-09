# EO-vs-CMIP-GHG-forcings-comparison

This repository contains all code for creating a figure that compares ground-based CIMP7 v1.0.0 data with 
satellite OBS4MIPs data. 

### Workflow

+ download $CH_4$ and $CO_2$ data products retrieved from 
  + CIMP7 v1.0.0 as provided via esgf (see [pseudo MAKEFILE](data/MAKEFILE) for workflow)
  + OBS4MIPs v4.5 as provided via CDS (see [CO2](https://cds.climate.copernicus.eu/datasets/satellite-carbon-dioxide?tab=overview)
  & [CH4](https://cds.climate.copernicus.eu/datasets/satellite-methane?tab=overview))
+ exploratory analysis of CIMP7 data 
  + see [tutorial: CIMP7 data](tutorials/CMIP7-v1.0.0.ipynb)
  + blocker: I'm uncertain when to apply the cosine-weighting to ensure correct weighting
+ preprocessing OBS4MIPS data
  + merge latitudinal grids of OBS4MIPs data to be consistent with 15° gridding of CIMP7 data
+ check missing data when comparing CIMP7 and OBS4MIPs data on a monthly basis (see [tutorial: missing data](tutorials/missing-data.ipynb))

### Note
Work on this repo is currently in progress. 