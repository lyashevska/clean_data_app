# clean_data_app
## Description

The purpose of this app is to explore data and to produce a clean version of it. An open-source app framework [streamlit](https://www.streamlit.io/) is used to build this app.


## Usage
### 1. Clone the repository locally

In your terminal, use `git` to clone the repository locally.

```bash
git clone https://github.com/lyashevska/clean-data-app
```

Alternatively, you can download the zip file of the repository at the top of the main page of the repository. 

### 2. Download Anaconda (if you haven't already)

If you do not already have the [Anaconda distribution](https://www.anaconda.com/download/) of Python 3,  get it (note: you can also set up your project environment w/out Anaconda using `pip` to install the required packages).

### 3. Set up your environment

Use the `conda` package manager to **install all the necessary packages** 
from the provided `environment.yml` file.

```bash
conda env create --prefix ./env --file environment.yml
```
To **activate the environment**, use the `conda activate` command on macOS and Linux.

```bash
conda activate ./env
```
On Windows:

```bash
activate ./env
```
Install `streamlit` package

```bash
pip install streamlit
```

To verify the package was installed run 

```bash
conda list | grep streamlit
```

### 4. To execute run in the terminal

```bash
streamlit run [filename]
```

The app should automatically open in a new tab in your browser.

# clean-data

## Description

This version of the code does not contain `streamlit` app. It can be used for data cleaning. No data exploration.

## Usage
Repeat steps 1-3, exept for `streamlit` installation. 
To execute in terminal run:

```bash
python [filename]
```
Clean version of the data can be found in folder `output_data`, file name is the same as original, prefixed by `clean_`.

## Author
Olga Lyashevska

