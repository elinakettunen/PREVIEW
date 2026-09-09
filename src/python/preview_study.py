from repo_paths import DATA_PATH
import pandas as pd
import numpy as np
from collections import defaultdict
import aivo

def read_preview_study_csv(fname, **kwargs):
    """Read CSV files with Windows-specific encoding and formatting."""
    default_params = {
        'encoding': 'cp1252',
        'delimiter': ';',
        'decimal': ',',
    }
    return pd.read_csv(fname, **{**default_params, **kwargs}).replace('999999', np.nan).replace(999999, np.nan)

def load_preview_data(raw_path):
    """Load and preprocess PREVIEW data files."""
    # Reading files
    dfs = [
        read_preview_study_csv(
            fname, 
            usecols=lambda c: not c.startswith('NvStat'),
            dtype=defaultdict(lambda: np.float64, aivo.dtypes_explicit)
        ).drop_duplicates()
        for fname 
        in (f'{raw_path}/cid1batch{i}_EK_21Nov2023.csv' for i in range(1,6))
    ]

    # Handle CoFormel column
    for df in dfs:
        if 'CoFormel' in df.columns:
            df.CoFormel = df.CoFormel.str.replace(',','.').astype(np.float64)

    # Finding common column names
    clists = [df.columns for df in dfs]
    common_columns = list(set(clists[0]).intersection(*clists[1:]))

    # Merging data from all files to a single dataframe
    preview_data = dfs[0]
    for df in dfs[1:]:
        preview_data = preview_data.merge(
            df,
            on=common_columns,
            how='inner'
        )

    # Data cleanup
    # Combining date and time to timestamp
    preview_data.insert(
        0,
        'timestamp',
        pd.to_datetime(
            preview_data.DaDate.str.cat(
                preview_data.MaTime,
                sep = ' '
            ),
            format='%d.%m.%Y %H:%M:%S'
        )
    )
    preview_data['date'] = preview_data.timestamp.dt.date

    preview_data.drop(
        columns=['DaDate','MaTime'],
        inplace=True
    )

    # Assuming fineli codes where they are integers, zero-padding and identifying them with an F
    preview_data['code'] = preview_data.Code.apply(
        lambda code: 'F' + code.zfill(6) if code[0].isdigit() else code
    )

    #Renaming sodium col
    preview_data.rename(columns={'NA.':'NA'}, inplace=True)

    return preview_data

def load_recipes():
    """Load recipe data from Excel file."""
    recipes = pd.read_excel(
        f'{DATA_PATH}/products_to_ingredients.xlsx',
        sheet_name='Tutkimusraportti',
        usecols=[
            'Reseptiryhmä', 'Tuoteryhmä', 'Reseptin/tuotteen tunnus',
            'Reseptin/tuotteen nimi', 'Kulutettu määrä',
            'Kulutetun ruuan mittayksikkö', 'Käyttömäärä',
            'Käyttömäärän yksikkö', 'Resepti/tuote kommentit',
            'Reseptin/tuotteen tyyppi', 'Tuotetunnus', 'Ainesosan nimi',
            'ENERC', 'FAT', 'CHOAVL', 'PROT', 'ALC', 'SUGOH', 'SUGAR',
            'FRUS', 'SUCS', 'STARCH', 'FIBC', 'FOL', 'NIAEQ', 'VITB6',
            'RIBF', 'THIA', 'VITA', 'CAROTENS', 'VITB12', 'VITC', 'VITD',
            'VITE', 'VITK', 'CA', 'FE', 'ID', 'K', 'MG', 'NA', 'NACL',
            'P', 'SE', 'ZN', 'FAPU', 'FASAT', 'FAMCIS', 'FATRN', 'FAPUN3',
            'FAPUN6', 'F18D2CN6', 'F18D3N3', 'F20D5N3', 'F22D6N3',
            'CHOLE', 'STERT', 'TRP',
        ]
    )
    recipes['recipe_fineli_code'] = recipes['Reseptin/tuotteen tunnus'].str.replace('RE','F')
    return recipes

def process_recipes(preview_data, recipes):
    """Process recipes and return expanded intakes."""
    is_recipe_row = preview_data.code.isin(recipes.recipe_fineli_code)
    recipe_rows = preview_data[is_recipe_row]
    intakes = preview_data[~is_recipe_row]

    aromi2aivo_rename = {
        'CAROTENS': 'CAROT',
        'CHOAVL': 'CHO',
        'CHOLE': 'CHOL',
        'Tuotetunnus': 'code',
        'Kulutettu määrä': 'CoFormel',
        'Käyttömäärä': 'CoWeight',
        'ENERC': 'ENERJ',
        'FAMCIS': 'FAMS',
        'Ainesosan nimi': 'Name',
    }

    columns_to_copy = {
        'DaDay', 'IvSocSec', 'MaMeal', 'MaName', 'MaType', 'MainGroup',
        'MgName', 'PdName', 'PdPeriod', 'SgName', 'SubGroup', 'subject_id',
        'timestamp'
    }

    def scale(v, factor):
        try: return v*factor
        except TypeError: return v

    def ingredient_intakes(recipe_code, intake_grams):
        scale_factor = intake_grams/100.0
        return recipes[
            (recipes.recipe_fineli_code==recipe_code)
            &
            (recipes['Reseptin/tuotteen tyyppi']=='Ainesosa')
        ].copy().map(
            lambda x: scale(x,scale_factor),
            na_action='ignore'
        ).rename(
            columns=aromi2aivo_rename
        )

    def expand_recipe_to_ingredients(row):
        df = ingredient_intakes(row.code, row.CoWeight)
        for c in columns_to_copy:
            df[c] = getattr(row, c)
        df['CoRow'] = range(1,len(df)+1)
        df['CoFormel'] = row.CoWeight
        df.recipe_fineli_code = row.code
        return df

    expanded_rows = pd.concat(
        [expand_recipe_to_ingredients(row) for row in recipe_rows.itertuples()]
    )
    return pd.concat([intakes, expanded_rows])

def get_intakes(raw_path):
    """Main function to load and process all data."""
    preview_data = load_preview_data(raw_path)
    recipes = load_recipes()
    return process_recipes(preview_data, recipes)