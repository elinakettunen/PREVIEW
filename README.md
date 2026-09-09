This repository contains the data analysis code for

_Intake of animal-source foods varies widely across individuals and is linked to distinct dietary characteristics: A PREVIEW sub-study_

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