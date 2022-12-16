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
from folium import IFrame

st.set_page_config( page_title="Main Page",page_icon="📚")  

#====================================================================
# Funções
#====================================================================
def  restaurants_maps(df): 
    #6. A localização central de cada cidade por tipo de tráfego
    data_plot = (df.loc[:,['city','restaurant_name','average_cost_for_two','aggregate_rating','cuisines','latitude','longitude']]
                 .groupby(['city','restaurant_name','average_cost_for_two','cuisines','aggregate_rating'])
                 .median()
                 .reset_index())
    map =folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
    
    df_aux = data_plot.sample(900)
    
    for i in range(0,len(df_aux)):
        folium.Circle(
            location=[df_aux.iloc[i]['latitude'], df_aux.iloc[i]['longitude']],
            popup=df_aux.iloc[i][['cuisines','average_cost_for_two','aggregate_rating']],
            radius=float(df_aux.iloc[i]['aggregate_rating'])*20,
            color='#69b3a2',
            fill=True,
            fill_color='#69b3a2'
        ).add_to(map)
        
    for index , location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'],
                       location_info['longitude']],
                      icon=folium.Icon(icolor='green', icon='glyphicon-home'),
                      popup=location_info[['city','restaurant_name']]).add_to(map)


    folium_static(map, width = 1024, height = 600 ) 
    
    return None           
                      

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

#==============================
# Rename columns of the dataset  
#==============================
df = rename_columns(df)

#================================
# Main Page
#================================
st.title('Fome Zero!')
st.markdown('# Found  your  Favority  Restaurant  in  the  World  Now !')
st.markdown("""---""")
st.markdown( "## Find the restaurants on the platform")


#==========================================================================
# Barra Lateral
#==========================================================================

image_path ='logo1.png'
image = Image.open(image_path)
st.sidebar.image(image, width=320)

st.sidebar.markdown('## Found your Favority Restaurant in the World Now !!')
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
    col1,col2,col3,col4,col5 =st.columns(5)
    
    rest_regs = df['restaurant_name'].count()
    col1.metric('Registered Restaurants',rest_regs)
    
    country_regs = df['country_code'].nunique()
    col2.metric('Registered Country',country_regs)
    
    city_regs = df['city'].nunique()
    col3.metric('Registered City',city_regs)
    
    rev_plat = df['votes'].sum()
    col4.metric('Reviews Made on the Platform',rev_plat)
    
    cuisines_offer = df['cuisines'].nunique()
    col5.metric('Types of Cuisine Offered',cuisines_offer)

    
    

with st.container():
    st.markdown('##### Platform Maps')
    restaurants_maps(df)                 
                      
    #fig = maker_map(df)
    #st.plotly_chart( fig )                  
                    
                      
  

    
    
    
