#Import package

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px 
import datetime
from datetime import datetime
from streamlit_folium import folium_static
import folium
from haversine import haversine
from PIL import Image 
import inflection
import plotly.graph_objects as go

st.set_page_config(page_title='Countries',page_icon="📊",layout='wide')

#====================================================================
# Funções
#====================================================================
def avg_by_country(df,var):
            df_aux = round(df.loc[:,[var,'country_name']]
                           .groupby(['country_name'])
                           .mean().reset_index()
                           .sort_values(var,ascending=False),2)
            fig = px.bar(df_aux , x='country_name',y= var, text_auto='.5s', color='country_name')
            return fig

def qty_by_country(df,var):
    df_aux = (df.loc[:,[var,'country_name']]
              .groupby('country_name')
              .count()
              .reset_index()
              .sort_values(var,ascending=False))
    fig = px.bar(df_aux, x='country_name', y= var, text_auto='.5s', color='country_name')
    return fig



def dataframe_clean(df):    
    df.drop_duplicates(inplace=True)
    df = df.dropna(axis=0,how='any')
    df = df.reset_index(drop=True)
    df["Cuisines"] = df.loc[:,"Cuisines"].apply(lambda x: x.replace(' ','_').split(",")[0])
    df["Currency"] = df.loc[:,"Currency"].apply(lambda x: x.replace(' ','_'))
    return df


def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
    return COUNTRIES[country_id]


def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred"
}
def color_name(color_code):
    return COLORS[color_code]


def rename_columns(df):
    df = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
#---------------------------- Inicio da Estrutura lógica do código ------------
#====================
# Import dataset
#====================
df_raw = pd.read_csv('zomato.csv')

#====================
#Copy Dataset
#====================
df = df_raw.copy()

#====================
# Cleaning Dataset
#====================
df = dataframe_clean(df)

#===========================
#Create new dataset columns
#==========================
df['Country Name']=df['Country Code'].apply(lambda x:country_name(x))

df['Category Meal']= df['Price range'].apply(lambda x: create_price_type(x))

df['Rating color']=df['Rating color'].apply(lambda x:color_name(x))

#===============================
# Rename columns of the dataset  
#==============================
df = rename_columns(df)


#==========================================================================
# Barra Lateral
#==========================================================================
st.header('Marketplace - Countries')



image_path ='logo1.png'
image = Image.open(image_path)
st.sidebar.image(image, width=320)


#st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('#### **Found your Favority Restaurant in the World Now !!**')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Filters')

countries_select = st.sidebar.multiselect(
    "How would you like to choose the Countries?",
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])

df=df.loc[df['country_name'].isin(countries_select),:]
   
    
    
#=========================================================================
# Layout no Streamlit
#=========================================================================
with st.container():
    st.markdown('##### Restaurants  Quantity  By  Country')   
    fig = qty_by_country(df,'restaurant_name')
    st.plotly_chart(fig, use_container_width=True )
    
    
with st.container():
    st.markdown('##### Cities  Quantity  By  Country')
    fig = qty_by_country(df,'city')
    st.plotly_chart(fig, use_container_width=True )

    

with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Average  Rating  By  Country')
            fig = avg_by_country(df,'votes')
            st.plotly_chart(fig, use_container_width=True)
               

        with col2:              
            st.markdown('##### Meal Average  Cost  For  Two  By  Country')
            fig = avg_by_country(df,'average_cost_for_two')
            st.plotly_chart(fig,use_container_width = True)


    
    
                    