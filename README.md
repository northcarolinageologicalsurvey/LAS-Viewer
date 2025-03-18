# LAS Viewer

This repository hosts the LAS Viewer, a web-based application built using **Streamlit** to visualize Log ASCII Standard (LAS) well log data.

## Features
- Upload and read LAS files.
- Display well log curve information.
- Interactive visualizations using Plotly.
- Histogram and crossplot analysis.
- Identify missing data ranges.

## Installation
To run the LAS Viewer locally, first, clone the repository:
```sh
git clone https://github.com/northcarolinageologicalsurvey/LAS-Viewer.git
cd LAS-Viewer
```

Then, install the dependencies:
```sh
pip install -r requirements.txt
```

## Running the App
To launch the app, use the following command:
```sh
streamlit run app.py
```

## Deployment
This application can be deployed using **Streamlit Sharing**, **GitHub Actions**, or other cloud platforms.

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

## Contributing
Feel free to fork the repository, create a feature branch, and submit a pull request!

