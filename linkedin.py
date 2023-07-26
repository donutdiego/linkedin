import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(
    page_title="Visualize Your Connections", 
    page_icon="💽", 
    layout="wide",
    initial_sidebar_state="collapsed")

instructions = Image.open('images/inst.png')

# \\\ Sidebar /// #

@st.cache_data
def load_data(csv, dataset):
    if csv is not None: # if file is uploaded
        df = pd.read_csv(csv, skiprows=3, parse_dates=['Connected On'])
        df['year'] = df['Connected On'].dt.year
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')

    else:               # if no file is uploaded or removed
        df = pd.read_csv(f'data/{dataset}.csv', skiprows=3, parse_dates=['Connected On'])
        df['year'] = df['Connected On'].dt.year
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')

    return df

def bar_px(df):
    year = df['year'].value_counts().reset_index()

    bar = px.bar(
    year,
    y='year',
    x='count',
    orientation='h',
    text_auto=True,
    color='count',
    height=200,
    color_continuous_scale=px.colors.sequential.Aggrnyl,
    labels={'year':'','count':''}
    )
    bar.update_traces(textfont_size=14, textposition='outside', 
                    marker_line_width=0, hovertemplate=None, hoverinfo='skip')

    bar.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)')
    
    bar.update_coloraxes(showscale=False)

    bar.update_xaxes(color='#03b5aa',
                    gridcolor='white',
                    linecolor='rgba(0,0,0,0)')

    bar.update_yaxes(color='#03b5aa',
                    linecolor='rgba(0,0,0,0)',
                    dtick=1)

    return bar 

def treemap_px(df, px_height):
    fig = px.treemap(
    df,
    height=px_height,
    path=['Company','Position'],
    color='Company',
    color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), 
                    font=dict(family='Arial', size=14),
                    plot_bgcolor='rgba(0,0,0,0)')

    fig.update_traces(root_color='rgba(0,0,0,0)',  # to match background color of app
                    marker=dict(cornerradius=10),
                    hovertemplate='%{value} Connection(s) <br> at %{label}')
    
    return fig

def polar_px(df):
    df['month'] = df['Connected On'].dt.month_name()
    month = df['month'].value_counts().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    chart = px.bar_polar(
    month,
    theta='month',
    r='count',
    color='count',
    template='plotly_dark',
    color_discrete_map=px.colors.sequential.Redor,
    category_orders={'month': month_order})

    return chart

# \\\ Header /// #

st.title("LinkedIn connections")

with st.container():
    left, right = st.columns((3, 2))
    with left:
        st.subheader("the visual: ")
        st.write("""
        

        my goal was to make this app interactive and allow users to create their own visualization by using their data
        """)
        st.subheader("couple notes:")
        st.write("""
        big thanks to my brother [alberto](https://www.linkedin.com/in/albertoreyes2021/) for letting me use his data 
        
        and want to give credit to [isaac](https://www.linkedin.com/in/tuckerrasbury/) and his project that I took inspiration from
        """)
    with right:
        st.subheader("")
        st.write("")
        dataset = st.selectbox('choose a sample dataset ', ('diego','alberto'))
        csv_file = st.file_uploader('upload your file here 👇 ')
        df = load_data(csv_file, dataset)
        tree_height = st.slider("increase the size of the chart 🔍", 500, 2000, 1000)

with st.container():

    left, right = st.columns((3, 2))
    with left:
        st.subheader("how to get your own data")
        how_to = st.expander("steps: ")
        how_to.write("""
        [click on this link](https://www.linkedin.com/mypreferences/d/download-my-data) and select "request archive" of your data

        then, you will receive an email in about 5 minutes with a link to download your data

        after that, just extract the file from the zipped folder and you are ready to visualize your connections!  
        """)
        how_to.image(instructions, width=500, use_column_width='auto', output_format='PNG')
        

st.write("##")        

# \\\ Treemap /// #

treemap = treemap_px(df, tree_height)

with st.container():
    st.plotly_chart(treemap, use_container_width=True)

# \\\ Bar Chart /// #

st.write("##")

st.subheader("break it down! 🤸")

bar = bar_px(df)

with st.container():
    st.write("by year:")
    st.plotly_chart(bar, use_container_width=True)
