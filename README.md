# EO-vs-CMIP-GHG-forcings-comparison

This repository contains all code for creating a figure that compares ground-based CIMP7 v1.0.0 data with 
satellite OBS4MIPs data. 

### Workflow
Current idea of preprocessing data is explained in [tutorial: getting-started_ch4](tutorials/getting-started_ch4.ipynb) 
and [tutorial: getting-started_co2](tutorials/getting-started_co2.ipynb)

In summary:

+ download $CH_4$ and $CO_2$ data products retrieved from 
  + CIMP7 v1.0.0 as provided via esgf (see [pseudo MAKEFILE](data/MAKEFILE) for workflow)
  + OBS4MIPs v4.5 as provided via CDS (see [CO2](https://cds.climate.copernicus.eu/datasets/satellite-carbon-dioxide?tab=overview)
  & [CH4](https://cds.climate.copernicus.eu/datasets/satellite-methane?tab=overview))
+ analyse missing values
+ average over longitudes
+ compute weighted average for each latitude band
+ resize grid if needed by averaging the weighted averages of each latitude band

### Questions/Notes

+ why do we focus only on latitude bands? Regional aspects are ignored?
+ validity of approach for resizing grid should be discussed  

### Note
Work on this repo is currently in progress. 