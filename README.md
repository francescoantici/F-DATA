# F-DATA
F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems

This repository contains the scripts and documentation for the F-DATA, available in Zenodo [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11467483.svg)](https://doi.org/10.5281/zenodo.11467483).

## Instruction on how to load the data 

The files of F-DATA are saved as `.parquet` files. It is possible to load such files as dataframes by leveraging the `pandas` APIs, after installing `pyarrow` (`pip install pyarrow`). A single file can be loaded as follows:

```
# Importing pandas library
import pandas as pd 

# Read the 21_01.parquet file in a dataframe format
df = pd.read_parquet("21_01.parquet")
df.head()
```

## Repository structure 

- `baseline_experiments.py`: The script to execute ML predictive modelling on the F-DATA.
- `generate_plots.py`: The script to generate a series of plots.
- `requirements.txt`: The python dependencies to execute all the scripts in the repository.
- `docs`: The folder contains some documentation of the final dataset, such as the job feature list and description.
- `plots` : The folder contains the plots of the whole F-DATA, as well as of the single splits that can be found in Zenodo.
- `generation_scripts`: The folder contains the scripts used to anonymize the data and generate the derived features.

## Contact us 

For any information on F-DATA don't hesitate to contact us at: francesco.antici98[at]gmail.com.

## Cite us 

Please cite the work as 

```
@dataset{antici_2024_11467483,
  author       = {Antici, Francesco and
                  Bartolini, Andrea and
                  Domke, Jens and
                  Kiziltan, Zeynep and
                  Yamamoto, Keiji},
  title        = {{F-DATA: A Fugaku Workload Dataset for Job-centric 
                   Predictive Modelling in HPC Systems}},
  month        = jun,
  year         = 2024,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.11467483},
  url          = {https://doi.org/10.5281/zenodo.11467483}
}
```