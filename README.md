# LAS Viewer

This repository hosts the LAS Viewer, a web-based application built using **Streamlit** to visualize Log ASCII Standard (LAS) well log data.

## Features
- Upload and read LAS files.
- Display well log curve information.
- Interactive visualizations using.
- Histogram and crossplot analysis.
- Identify missing data ranges.

# **Use the App Online**
You can access the NCGS LAS Viewer directly without installing anything:
[NCGS LAS Viewer App](https://las-viewer-ncgs.streamlit.app)

## Installation
To run the LAS Viewer locally you must have a Python language compiler on your computer: [to install Python compiler](https://www.python.org/).
First, clone the repository:

```sh
git clone https://github.com/northcarolinageologicalsurvey/LAS-Viewer.git
cd LAS-Viewer
```

Then, install the dependencies:
```sh
pip install -r requirements.txt
```

## Running the App Locally
To launch the app, use the following command:
```sh
streamlit run app.py
```
This app will open in yoour web browser.

## Deployment

## Repository Structure
```
LAS-Viewer/
│── app.py                # Main application file
│── requirements.txt      # Dependencies
│── README.md             # Documentation
│── .streamlit/
│   └── config.toml       # Streamlit configurations
│── .github/workflows/
│   └── deploy.yml        # GitHub Actions deployment
```

