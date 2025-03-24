# Log Ascii Standard files<br>
<p>Log Ascii Standard (LAS) is the primary file storage format for geophysical data gleaned from exploratory and observation wells, be it from oil or natural gas wells from the petroleum industry or water monitoring wells from the environmental industry. Researchers use the information stored in LAS files to visualize the numerical data stored in the files which are converted to digital geophysical lines (curves) and viewed on a monitor. Easy curve comparison and contrasting from visualization is crucial for use as a subsurface geological investigation tool. In order to convert curves from numerical data, typically a specialized software package is required. These software packages can be cost prohibitive to the independent or student researcher. This LAS Viewer is an alternative to cost-prohibitive specialized software packages.</p><br>
<p></p>Geophysical well logs are an invaluable tool for many subsurface geological interpretations. Although first developed for the petroleum industry, geophysical well logging has proven to be an invaluable technique in many other geological sub-disciplines. In the mineral industry, geophysical logging is widely used both for exploration activities and for monitoring grade control in working mines. In groundwater assessment, geophysical well logging is also central to the delineation of aquifers and producing zones. In regolith studies, the technique can provide unique insights into the composition, structure and variability of the subsurface. Additionally, the technique is widely used for ground truthing airborne geophysical data sets, such as airborne electromagnetics. In geophysical well logging, many different physical properties (represented by the different down-hole sensing tools used) can be used together to characterize the geology surrounding a borehole.</p><br>
<p>The Log Ascii Standard (LAS) formatting system was developed in 1989 (version 1.0) by the Canadian Well Logging Society (CWLS) in an effort to standardize well log geophysical data (often referred to as “curves” in graphic representations) for ease of use in the petroleum industry. In 1992, LAS, version 2.0 was released in an effort to address formatting issues with the first version. Although a version 3.0 was released in 1999 to accommodate some complex, but sparsely used, well curve parameters, <strong>version 2.0 is still the most common version used today</strong>. The formatting is a simple text file that begins with a header containing a well’s name, location, and other well identification specifics, followed by a subsection containing the geophysical curve parameters measured for the individual well. The header information is followed by horizontally aligned vertical columns of numerical data representing the parameter data at a specifically defined depth interval. The depth interval is traditionally the leftmost vertical column of numerical data. The numerical columns are traditionally arranged left -to- right on the page in the same order they are listed vertically (top -to- bottom) in the header. This formatting standard allows an end-user to pull a LAS file into most well geophysical software packages (and this LAS Viewer) and perform numerous subsurface geological analyses.</p><br>
<strong>This LAS Viewer will read LAS versions 1 and 2, but will potentially have difficulty with LAS version 3 files.</strong>


# LAS Viewer

This repository hosts the LAS Viewer, a web-based application built using **Streamlit** to visualize Log ASCII Standard (LAS) well log data.

## Features
- Upload and read LAS files
- Display well log curve information
- Interactive visualizations
- Histogram and crossplot analysis
- Identify missing data ranges

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

