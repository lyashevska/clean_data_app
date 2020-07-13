# coding: utf-8
# data exploration and cleaning

import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.title("Downtime machine analysis")
st.markdown(
    "Data exploration app to gain insight into the frequency, duration, and distribution of the downtime events"
)

# st.date_input("Date", datetime.now())
# st.header('Built with Streamlit')
# st.subheader('App')
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# if uploaded_file is not None:
#      data = pd.read_csv(uploaded_file)
#      st.write(data)

DIR_NAME = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR_NAME, "input_data/")

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

# use
# for name in glob.glob('dir/file?.txt'):
# instead of filename[0]


@st.cache
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
    data["prodtype"] = data["prodtype"].str.replace(r"[\s_]", "-").str.lower()
    data["prodfam"] = data["prodfam"].str.replace(r"[\s_]", "-").str.lower()
    data["reason"] = data["reason"].str.replace(" ", "")
    return data


data = load_data()

st.markdown("Loading data...done!")  # include progress bar

st.markdown("Average monthly downtime, min")
st.area_chart(data.resample("M").mean())
st.text("Total number of entries: %s" % len(data))

# select columns to subset
ALLCOLS = data.columns.tolist()
DEFAULTCOLS = [
    "equip",
    "equiptype",
    "dept",
    "area",
    "shifts",
    "scheduled",
    "reason",
    "min",
]
selectedcols = st.multiselect(
    "Select columns of interest", options=ALLCOLS, default=DEFAULTCOLS
)
data_cols = data[selectedcols]

# select a year
YEAR = data_cols.index.year
year = st.sidebar.selectbox("Select year", tuple(range(YEAR.min(), YEAR.max() + 1, 1)))
data_year = data_cols[str(year)]

# select a dept
DEPT = data_year.dept.unique()
dept = st.sidebar.selectbox("Select department", DEPT)
data_dept = data_year[data_year.dept == str(dept)]

# select a dept
SCHED = data_dept.scheduled.unique()
sched = st.sidebar.selectbox("Select type", SCHED)
data_sched = data_dept[data_dept.scheduled == str(sched)]

# display data
st.dataframe(data_sched)
st.text("Number of rows: %s" % len(data_sched))

selectedcols = [s for s in selectedcols if s not in ("scheduled", "min", "dept")]
selectedcol = st.selectbox("Select a column to display", selectedcols)
st.bar_chart(data_sched.groupby(selectedcol)["min"].sum().sort_values())
st.text("Shown cumulative downtime for column: %s" % (selectedcol))
st.text("Number of %ss: %s" % (selectedcol, len(data_sched.groupby(selectedcol))))

MAX = data_sched["min"].max()
MINMIN, MAXMIN = st.sidebar.slider(
    "Select range for %s, min" % selectedcol, 0, int(MAX), [0, int(MAX)], 10
)

st.sidebar.text("Distribution of downtime, min ")
data_sched["min"][(data_sched["min"] > MINMIN) & (data_sched["min"] < MAXMIN)].hist(
    grid=False, bins=25, color="r"
)
st.sidebar.pyplot()


NEW_DATA_DIR = "output_data"
if not os.path.exists(NEW_DATA_DIR):
    os.makedirs(NEW_DATA_DIR)

if st.button("Save clean data"):
    NEW_FILENAME = "clean_" + FILENAME[0]
    data.to_csv(os.path.join(NEW_DATA_DIR, NEW_FILENAME))
    st.text("Data has been sucessfully saved")

# Buttons
if st.button("About us"):
    st.text("Data exploration app build with https://www.streamlit.io/")
