import streamlit as st
import lasio
import pandas as pd
from io import StringIO
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title='LAS Explorer')

st.sidebar.write('# LAS Data Viewer\n **North Carolina Geological Survey**')
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

def display_well_location(las_file):
    well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
    latitude, longitude = None, None

    for key in ['LAT', 'SLAT']:
        if key in las_file.well:
            latitude = las_file.well[key].value
            break
    for key in ['LONG', 'SLON']:
        if key in las_file.well:
            longitude = las_file.well[key].value
            break

    if latitude and longitude:
        fig = px.scatter_mapbox(
            lat=[latitude], lon=[longitude], text=[well_name],
            zoom=6, height=500, mapbox_style="open-street-map",
            title="Well Location"
        )
        fig.update_traces(
            marker=dict(size=12, color="red"),
            hovertemplate=f"well: {well_name}<br>lat: {latitude}<br>lon: {longitude}<extra></extra>"
        )
        st.plotly_chart(fig)
    else:
        st.warning("No valid well location found in the uploaded LAS file.")

def plot_multi_wells(las_files, well_data_list):
    st.title('Multi-Well Curve Comparison')

    if not las_files:
        st.warning('No files have been uploaded')
        return

    all_curves = list(set([curve.mnemonic for las in las_files for curve in las.curves]))
    curves_to_plot = st.multiselect('Select Curves to Compare', all_curves)
    overlay = st.checkbox("Overlay wells on same axis instead of separate subplots", value=False)

    if not curves_to_plot:
        st.warning('Please select at least one curve to plot.')
        return

    if overlay:
        fig = make_subplots(rows=1, cols=1, shared_yaxes=True)
        for curve in curves_to_plot:
            for las_file, well_data in zip(las_files, well_data_list):
                well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
                if curve in well_data.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=well_data[curve], y=well_data['DEPTH'],
                            mode='lines', name=f"{well_name} - {curve}"
                        )
                    )
        fig.update_layout(
            height=800,
            yaxis=dict(title='DEPTH', autorange='reversed'),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
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

    with st.expander("Optional: Show Histograms for Selected Curves"):
        for curve in curves_to_plot:
            st.subheader(f"Histogram: {curve}")
            hist_fig = go.Figure()
            for las_file, well_data in zip(las_files, well_data_list):
                well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
                if curve in well_data.columns:
                    hist_fig.add_trace(go.Histogram(
                        x=well_data[curve], name=well_name, opacity=0.6
                    ))
            hist_fig.update_layout(
                barmode='overlay',
                title=f"Histogram of {curve}",
                xaxis_title=curve,
                yaxis_title="Count"
            )
            st.plotly_chart(hist_fig, use_container_width=True)

    with st.expander("Optional: Crossplot Between Two Curves"):
        x_curve = st.selectbox("Select X-axis Curve", all_curves, index=0)
        y_curve = st.selectbox("Select Y-axis Curve", all_curves, index=1)
        cross_fig = go.Figure()
        for las_file, well_data in zip(las_files, well_data_list):
            well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
            if x_curve in well_data.columns and y_curve in well_data.columns:
                cross_fig.add_trace(go.Scatter(
                    x=well_data[x_curve], y=well_data[y_curve],
                    mode='markers', name=well_name,
                    marker=dict(size=6), opacity=0.7
                ))
        cross_fig.update_layout(
            title=f"Crossplot: {x_curve} vs {y_curve}",
            xaxis_title=x_curve,
            yaxis_title=y_curve
        )
        st.plotly_chart(cross_fig, use_container_width=True)

    with st.expander("Optional: Curve Statistics Summary"):
        for curve in curves_to_plot:
            st.subheader(f"Statistics: {curve}")
            stats = {}
            for las_file, well_data in zip(las_files, well_data_list):
                well_name = las_file.well.WELL.value if 'WELL' in las_file.well else "Unnamed Well"
                if curve in well_data.columns:
                    stats[well_name] = well_data[curve].describe()
            df_stats = pd.DataFrame(stats)
            st.dataframe(df_stats)

def missing_data(las_files, well_data_list):
    st.title('Missing Data Visualization')

    if not las_files:
        st.warning('No files have been uploaded')
        return

    well_names = [
        las.well.WELL.value if 'WELL' in las.well else f"Well {i+1}"
        for i, las in enumerate(las_files)
    ]
    selected_well = st.selectbox("Select Well", well_names)
    selected_idx = well_names.index(selected_well)
    selected_data = well_data_list[selected_idx]

    curves = st.multiselect('Select Curves to Check for Missing Data', selected_data.columns[:-1], default=selected_data.columns[:-1])

    if not curves:
        st.warning('Please select at least one curve.')
        return

    data_nan = selected_data.notnull().astype(int)

    fig = make_subplots(rows=1, cols=len(curves), shared_yaxes=True, subplot_titles=curves)

    for i, curve in enumerate(curves, start=1):
        fig.add_trace(
            go.Scatter(
                x=data_nan[curve],
                y=selected_data['DEPTH'],
                mode='lines',
                fill='tozerox',
                name=curve
            ),
            row=1, col=i
        )
        fig.update_xaxes(range=[0, 1], visible=False, row=1, col=i)

    fig.update_layout(
        height=700,
        yaxis=dict(title="DEPTH", autorange='reversed'),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

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

uploaded_files = st.sidebar.file_uploader(
    'Upload LAS Files', type=['.las'], accept_multiple_files=True
)

las_files, well_data_list = load_data(uploaded_files)

if las_files:
    st.sidebar.success(f"{len(las_files)} files uploaded successfully")
    display_well_location(las_files[-1])

st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a page:', 
    ['Home', 'Header Information', 'Data Information', 'Curve Comparison', 'Missing Data Visualization'])

def home():
    st.title('Log ASCII Standard (LAS) - Well Geophysical Data Viewer')
    st.write('Explore and compare well log geophysical curves from multiple LAS files.')

if options == 'Home':
    home()
elif options == 'Header Information':
    header(las_files)
elif options == 'Data Information':
    raw_data(las_files, well_data_list)
elif options == 'Curve Comparison':
    plot_multi_wells(las_files, well_data_list)
elif options == 'Missing Data Visualization':
    missing_data(las_files, well_data_list)
