import streamlit as st
import lasio
import pandas as pd
from io import StringIO
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title='Multi-Well LAS Explorer')

st.sidebar.write('# Multi-Well LAS Data Viewer\n **North Carolina Geological Survey**')
st.sidebar.write('\nUpload multiple LAS files to compare well curves.')

@st.cache_data
def load_data(uploaded_files):
    las_files = []
    well_data_list = []

    for uploaded_file in uploaded_files:
        try:
            bytes_data = uploaded_file.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las_file = lasio.read(str_io)
            well_data = las_file.df()
            well_data['DEPTH'] = well_data.index
            las_files.append(las_file)
            well_data_list.append(well_data)
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {e}")

    return las_files, well_data_list

def plot_multi_wells(las_files, well_data_list):
    st.title('Multi-Well Curve Comparison')

    if not las_files:
        st.warning('No files have been uploaded')
        return

    # Select curves to compare across wells
    curves_to_plot = st.multiselect(
        'Select Curves to Compare', 
        options=list(set([curve.mnemonic for las in las_files for curve in las.curves]))
    )

    if not curves_to_plot:
        st.warning('Please select at least one curve to plot.')
        return

    fig = make_subplots(rows=1, cols=len(curves_to_plot), shared_yaxes=True, 
                        subplot_titles=curves_to_plot, horizontal_spacing=0.02)

    for i, curve in enumerate(curves_to_plot, start=1):
        for las_file, well_data in zip(las_files, well_data_list):
            well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
            if curve in well_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=well_data[curve], y=well_data['DEPTH'], 
                        mode='lines', name=f"{well_name} - {curve}"
                    ),
                    row=1, col=i
                )

        fig.update_xaxes(title_text=curve, row=1, col=i)

    fig.update_layout(
        height=800,
        yaxis=dict(title='DEPTH', autorange='reversed'),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

uploaded_files = st.sidebar.file_uploader(
    'Upload LAS Files', type=['.las'], accept_multiple_files=True
)

las_files, well_data_list = load_data(uploaded_files)

if las_files:
    plot_multi_wells(las_files, well_data_list)

st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a page:', 
    ['Home', 'Header Information', 'Data Information', 'Curve Comparison'])

def home():
    st.title('Log ASCII Standard (LAS) - Well Geophysical Data Viewer')
    st.write('Explore well log geophysical data using LAS files from multiple wells.')

def header(las_files):
    st.title('LAS File Header Info')

    if not las_files:
        st.warning('No files have been uploaded')
    else:
        for las in las_files:
            st.write(f"### Well: {las.well.WELL.value if 'WELL' in las.well else 'Unnamed Well'}")
            for item in las.well:
                st.write(f"<b>{item.descr.capitalize()} ({item.mnemonic}):</b> {item.value}", 
                         unsafe_allow_html=True)

def raw_data(las_files, well_data_list):
    st.title('Raw Data Information')

    if not las_files:
        st.warning('No files have been uploaded')
    else:
        for las, well_data in zip(las_files, well_data_list):
            st.write(f"### Well: {las.well.WELL.value if 'WELL' in las.well else 'Unnamed Well'}")
            for curve in las.curves:
                st.write(f"{curve.mnemonic} ({curve.unit}): {curve.descr}", unsafe_allow_html=True)
            st.dataframe(well_data)

if options == 'Home':
    home()
elif options == 'Header Information':
    header(las_files)
elif options == 'Data Information':
    raw_data(las_files, well_data_list)
elif options == 'Curve Comparison':
    plot_multi_wells(las_files, well_data_list)
