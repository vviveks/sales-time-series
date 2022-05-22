import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as mpl
import calendar

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from streamlit_option_menu import option_menu

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sales Dahboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# --------- Colors -----------
colors={}
def colorFader(c1,c2,mix=0): 
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
c1='#FAA831' 
c2='#9A4800' 
n=9
for x in range(n+1):
    colors['level'+ str(n-x+1)] = colorFader(c1,c2,x/n) 
colors['background'] = '#232425'
colors['text'] = '#fff'

# --------- READ EXXCEL --------
data = pd.read_csv('ldata.csv')

# -------- NAVBAR ------------

selected = option_menu(
    menu_title = "Sales Dashboard", 
    options=["Home", "Timely Sales", 'Filter'], 
    icons=['building', 'calendar3', 'filter-circle-fill'], 
    menu_icon="bar-chart-line-fill", 
    default_index=0, 
    orientation="horizontal",
    styles="text-align-center"
)

# ---- SIDEBAR ----

if selected=='Filter':
    st.sidebar.header("Please Filter Here:")

    city = st.sidebar.multiselect(
        "Select the city:",
        options = data['city'].unique(),
        default = data['city'].unique()
    )

    state = st.sidebar.multiselect(
        "Select the state:",
        options = data['state'].unique(),
        default = data['state'].unique()
    )

    store_type = st.sidebar.multiselect(
        "Select the type:",
        options = data['store_type'].unique(),
        default = data['store_type'].unique()
    )

    data = data.query(
        "city == @city & state == @state & store_type == @store_type"
    )

# -------- Main Page ----------

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# TOP KPI's
stores = int(data["store_nbr"].nunique())
cities = int(data["city"].nunique())
states = int(data["state"].nunique())
store_types = int(data["store_type"].nunique())
products = int(data["family"].nunique())
cluster = int(data["cluster"].nunique())

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.subheader("STORES")
    st.subheader(f"{stores}")
with col2:
    st.subheader("CITIES")
    st.subheader(f"{cities}")
with col3:
    st.subheader("STATES")
    st.subheader(f"{states}")
with col4:
    st.subheader("TYPES")
    st.subheader(f"{store_types}")
with col5:
    st.subheader("PRODUCTS")
    st.subheader(f"{products}")
with col6:
    st.subheader("CLUSTER")
    st.subheader(f"{cluster}")

# ------ BEST SELLING PRODUCTS --------

df_fa_sa = data.groupby('family').agg({"sales" : "mean"}).reset_index().sort_values(by='sales', ascending=False)[:10]
df_fa_sa['color'] = colors['level10']
df_fa_sa['color'][:1] = colors['level1']
df_fa_sa['color'][1:2] = colors['level2']
df_fa_sa['color'][2:3] = colors['level3']
df_fa_sa['color'][3:4] = colors['level4']
df_fa_sa['color'][4:5] = colors['level5']

fig1 = go.Figure(data=[go.Bar(x=df_fa_sa['sales'],
                             y=df_fa_sa['family'], 
                             marker=dict(color= df_fa_sa['color']),
                             name='Family', orientation='h',
                             text=df_fa_sa['sales'].astype(int),
                             textposition='auto',
                             hoverinfo='text',
                             hovertext=
                            '<b>Family</b>:'+ df_fa_sa['family'] +'<br>' +
                            '<b>Sales</b>:'+ df_fa_sa['sales'].astype(int).astype(str) +'<br>' ,
                            # hovertemplate='Family: %{y}'+'<br>Sales: $%{x:.0f}'
                            )])
fig1.update_layout(title_text='The 10 Best-Selling Products ',paper_bgcolor=colors['background'],plot_bgcolor=colors['background'],
                font=dict(
                size=14,
                color='white'))

fig1.update_yaxes(showgrid=False, categoryorder='total ascending')

# -------- AVERAGE SALES VS STORE TYPES -------------

df_st_sa = data.groupby('store_type').agg({"sales" : "mean"}).reset_index().sort_values(by='sales', ascending=False)
fig2=go.Figure(data=[go.Pie(values=df_st_sa['sales'], labels=df_st_sa['store_type'], name='Store type',
                     marker=dict(colors=[colors['level1'],colors['level3'],colors['level5'],colors['level7'],colors['level9']]), hole=0.7,
                     hoverinfo='label+percent+value', textinfo='label'
                    )])
fig2.update_layout(title_text='The Average Sales Vs Store Types',paper_bgcolor=colors['background'],plot_bgcolor='#1f2c56',
                font=dict(
                size=14,
                color='white'))
fig2.update_yaxes(showgrid=False, categoryorder='total ascending')

# ------------- CLUSTER VS SALES ---------------
df_cl_sa = data.groupby('cluster').agg({"sales" : "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_cl_sa['color'] = colors['level10']
df_cl_sa['color'][:1] = colors['level1']
df_cl_sa['color'][1:2] = colors['level2']
df_cl_sa['color'][2:3] = colors['level3']
df_cl_sa['color'][3:4] = colors['level4']
df_cl_sa['color'][4:5] = colors['level5']
fig3 = go.Figure(data=[go.Bar(y=df_cl_sa['sales'],
                             x=df_cl_sa['cluster'], 
                             marker=dict(color= df_cl_sa['color']),
                             name='Cluster',
                             text=df_cl_sa['sales'].astype(int),
                             textposition='auto',
                             hoverinfo='text',
                             hovertext=
                            '<b>Cluster</b>:'+ df_cl_sa['cluster'].astype(str) +'<br>' +
                            '<b>Sales</b>:'+ df_cl_sa['sales'].astype(int).astype(str) +'<br>' ,
                            # hovertemplate='Family: %{y}'+'<br>Sales: $%{x:.0f}'
                            )])
fig3.update_layout(title_text='Clusters Vs Sales',paper_bgcolor=colors['background'],plot_bgcolor=colors['background'],
                font=dict(
                size=14,
                color='white'))

fig3.update_xaxes(tickmode = 'array', tickvals=df_cl_sa.cluster)
fig3.update_yaxes(showgrid=False)

# ------------ AVERAGE SALES VS CITIES -------------

df_city_sa = data.groupby('city').agg({"sales" : "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_city_sa['color'] = colors['level10']
df_city_sa['color'][:1] = colors['level1']
df_city_sa['color'][1:2] = colors['level2']
df_city_sa['color'][2:3] = colors['level3']
df_city_sa['color'][3:4] = colors['level4']
df_city_sa['color'][4:5] = colors['level5']

fig4 = go.Figure(data=[go.Bar(y=df_city_sa['sales'],
                             x=df_city_sa['city'], 
                             marker=dict(color= df_city_sa['color']),
                             name='State',
                             text=df_city_sa['sales'].astype(int),
                             textposition='auto',
                             hoverinfo='text',
                             hovertext=
                            '<b>City</b>:'+ df_city_sa['city'] +'<br>' +
                            '<b>Sales</b>:'+ df_city_sa['sales'].astype(int).astype(str) +'<br>' ,
                            # hovertemplate='Family: %{y}'+'<br>Sales: $%{x:.0f}'
                            )])
fig4.update_layout(title_text='The Average Sales Vs Cities',paper_bgcolor=colors['background'],plot_bgcolor=colors['background'],
                font=dict(
                size=14,
                color='white'))

fig4.update_yaxes(showgrid=False, categoryorder='total ascending')

# ---------- AVERAGE SALES VS STATES ---------------

df_state_sa = data.groupby('state').agg({"sales" : "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_state_sa['color'] = colors['level10']
df_state_sa['color'][:1] = colors['level1']
df_state_sa['color'][1:2] = colors['level2']
df_state_sa['color'][2:3] = colors['level3']
df_state_sa['color'][3:4] = colors['level4']
df_state_sa['color'][4:5] = colors['level5']

fig5 = go.Figure(data=[go.Bar(y=df_state_sa['sales'],
                             x=df_state_sa['state'], 
                             marker=dict(color= df_state_sa['color']),
                             name='State',
                             text=df_state_sa['sales'].astype(int),
                             textposition='auto',
                             hoverinfo='text',
                             hovertext=
                            '<b>State</b>:'+ df_state_sa['state'] +'<br>' +
                            '<b>Sales</b>:'+ df_state_sa['sales'].astype(int).astype(str) +'<br>' ,
                            # hovertemplate='Family: %{y}'+'<br>Sales: $%{x:.0f}'
                            )])
fig5.update_layout(title_text='The Average Sales Vs States',paper_bgcolor=colors['background'],plot_bgcolor=colors['background'],
                font=dict(
                size=14,
                color='white'))

fig5.update_yaxes(showgrid=False, categoryorder='total ascending')

# ---------- AVERAGE DAILY SALES --------------

df_day_sa = data.groupby('date').agg({"sales" : "mean"}).reset_index()
fig6 = go.Figure(data=[go.Scatter(x=df_day_sa['date'], y=df_day_sa['sales'], fill='tozeroy', fillcolor='#FAA831', line_color='#bA6800')])
fig6.update_layout(title_text='The Average Daily Sales',height=300,paper_bgcolor='#232425',plot_bgcolor='#232425',
                font=dict(
                size=12,
                color='white'))
fig6.update_xaxes(showgrid=False)
fig6.update_yaxes(showgrid=False)

# ---------- Quarter-wise avg sale ------------

df_q_sa = data.groupby('quarter').agg({"sales" : "mean"}).reset_index() 



fig7 = go.Figure(data=[go.Pie(values=df_q_sa['sales'], labels=df_q_sa['quarter'], name='Quarter',
                     marker=dict(colors=[colors['level1'],colors['level3'],colors['level5'],colors['level7'],colors['level9']]), hole=0.7,
                     hoverinfo='label+percent+value', textinfo='label'
                    )])

# styling
fig7.update_layout(title_text='Quarter wise Avg Sales Analysis',height=300,paper_bgcolor='#232425',plot_bgcolor='#232425',
                font=dict(
                size=12,
                color='white'))
fig7.update_xaxes(showgrid=False)
fig7.update_yaxes(showgrid=False)

# ---------- AVERAGE MONTHLY SALES -------------

df_mon_sa = data.groupby('month').agg({"sales" : "mean"}).reset_index()
fig8 = go.Figure(data=[go.Scatter(x=df_mon_sa['month'], y=df_mon_sa['sales'], fill='tozeroy', fillcolor='#FAA831', line_color='#bA6800'
                                  ,mode='lines+markers')])


fig8.update_layout(title_text='The Average Monthly Sales',height=300,paper_bgcolor='#232425',plot_bgcolor='#232425',
                font=dict(
                size=12,
                color='white'))
fig8.update_yaxes(showgrid=False)
fig8.update_xaxes(showgrid=False,tickmode = 'array', tickvals=df_mon_sa.month)

# ------------ AVERAGE QUARTERLY SALES ----------------

df_qu_sa = data.groupby('quarter').agg({"sales" : "mean"}).reset_index()
fig9 = go.Figure(data=[go.Scatter(x=df_qu_sa['quarter'], y=df_mon_sa['sales'], fill='tozeroy', fillcolor='#FAA831', line_color='#bA6800'
                                  ,mode='lines+markers')])


fig9.update_layout(title_text='The Average Quarterly Sales',height=300,paper_bgcolor='#232425',plot_bgcolor='#232425',
                font=dict(
                size=12,
                color='white'))
fig9.update_yaxes(showgrid=False)
fig9.update_xaxes(showgrid=False,tickmode = 'array', tickvals=df_qu_sa.quarter)

# ------------ AVERAGE ANNUAL SALES -----------------


df_y_sa = data.groupby('year').agg({"sales" : "mean"}).reset_index()
fig10= go.Figure(data=[go.Scatter(x=df_y_sa['year'], y=df_y_sa['sales'], fill='tozeroy', fillcolor='#FAA831', line_color='#bA6800'
                                  ,mode='lines+markers')])


fig10.update_layout(title_text='The Average Annual Sales',height=300,paper_bgcolor='#232425',plot_bgcolor='#232425',
                font=dict(
                size=12,
                color='white'))
fig10.update_yaxes(showgrid=False)
fig10.update_xaxes(showgrid=False,tickmode = 'array', tickvals=df_y_sa.year)

# ----------- SALES - STATES & CITIES ---------------

df_c_s_sa = data.groupby(['state','city']).agg({"sales" : "mean"}).reset_index()
df_c_s_sa=df_c_s_sa[df_c_s_sa.sales>0]
fig11 = px.sunburst(df_c_s_sa, path=['state', 'city' ], 
                    values='sales',color='sales',
                    color_continuous_scale=[colors['level1'], colors['level10']])

fig11.update_layout(title_text='States & Cities',width=500,paper_bgcolor='#232425',plot_bgcolor='#232425',font=dict(color=colors['text']))

# ------------- BOARDS -----------------

if selected=='Home' or selected=='Filter':
    col7, col8 = st.columns([1,2])

    with col7:
        st.plotly_chart(fig2, True)
    with col8:
        st.plotly_chart(fig1, True)

    col9, col10 = st.columns([3,2])

    with col9 :
        st.plotly_chart(fig5, True)
    with col10:
        st.plotly_chart(fig11, True)

    st.plotly_chart(fig4, True)

if selected=='Timely Sales':
    col11, col12 = st.columns([1,2])

    with col11:
        st.plotly_chart(fig7, True)
    with col12:
        st.plotly_chart(fig9, True)
    
    st.plotly_chart(fig10, True)
    st.plotly_chart(fig8, True)
    st.plotly_chart(fig6, True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
