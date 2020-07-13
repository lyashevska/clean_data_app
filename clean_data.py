# coding: utf-8
# data exploration and cleaning

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

DIR_NAME = os.path.dirname(__file__)

DATA_DIR = os.path.join(DIR_NAME, "input_data/")

# look for files with csv extension
FILENAME = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

MISSING_VALUES = ["xx", "nan", "0", "???"]
COLNAMES = [
    "equip",
    "equiptype",
    "dept",
    "area",
    "date",
    "shifts",
    "reason",
    "min",
    "prodfix",
    "enginfix",
    "scheduled",
    "prodfam",
    "prodtype",
    "comment",
    "downtimetype",
]
DATE_COLUMN = "date"


def load_data(nrows=None):
    """
    Load data and do predefined type of cleaning

    Args:
        nrows (int): Limit a number of rows to be read in. Can be useful for large datasets. Defaults to None.

    Returns:
        dataframe: Clean data
    """
    data = pd.read_csv(
        os.path.join(DATA_DIR, FILENAME[0]), nrows=nrows, na_values=MISSING_VALUES
    )
    data.columns = COLNAMES
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data.index = pd.to_datetime(data[DATE_COLUMN])
    data["equip"] = data["equip"].str.replace(r'[\s_" "-]', "").str.lower()
    data["equiptype"] = data["equiptype"].str.replace(r"[\s_]", "-").str.lower()
    data["dept"] = data["dept"].str.replace(" ", "").str.lower()
    data["area"] = data["area"].str.replace(r'[\s|_|" "]', "").str.lower()
    data["shifts"] = data["shifts"].str.lower().str.replace(" ", "")
    di = {
        "evening": "eve",
        "evenings": "eve",
        "wkend": "wknd",
        "days": "day",
        "weekend": "wknd",
        "o/t": "overtime",
    }
    data = data.replace({"shifts": di})
    # replace all other values to NaN
    allowed_values = list(set(di.values()))
    data.loc[~data["shifts"].isin(allowed_values), "shifts"] = "NaN"
    # data['area'] = data['area'].str.replace(r'cell2' 'cell-2')
    #TODO check data types with isinstance
    data["prodtype"] = data["prodtype"].str.replace(r"[\s_]", "-").str.lower()
    data["prodfam"] = data["prodfam"].str.replace(r"[\s_]", "-").str.lower()
    data["reason"] = data["reason"].str.replace(" ", "")
    return data


data = load_data()

NEW_DATA_DIR = "output_data"

if not os.path.exists(NEW_DATA_DIR):
    os.makedirs(NEW_DATA_DIR)

NEW_FILENAME = "clean_" + FILENAME[0]
data.to_csv(os.path.join(NEW_DATA_DIR, NEW_FILENAME))
