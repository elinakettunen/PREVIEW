This repository contains the data analysis code for the following article:

_Kettunen, E., Freese, R., Hovinen, T. et al. Intake of animal-source foods varies widely across individuals and is linked to distinct dietary characteristics: a PREVIEW sub-study. BMC Nutr (2026). https://doi.org/10.1186/s40795-026-01482-2_

`src/data`
- `food_properties.csv` classifying food codes to food groups, and estimating their animal proportion

`src/python`
- `aivo.py` defines some constants about the file format produced by Aivo diet software.
- `article_exhibits.ipynb` the main python code producing figures, tables, and computed values used in the manuscript.
- `fao_groups.ipynb` parses FAO's public food group coding from their published PDF to CSV
- `local_paths.py.example` an example of the python file needed to set local paths outside this repository, pointing at the research dataset
- `preprocessing.ipynb` code that parses and preprocesses the data files
- `preview_study.py` contains some data parsing functions specific to naming and format used in the PREVIEW study
- `repo_paths.py` intra-repository path constants shared by the notebooks
- `requirements.txt` the exact versions used when generating the figures and tables in the published article. Run `pip install -r requirements.txt` in a fresh environment to reproduce the results.
