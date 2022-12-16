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

st.set_page_config(page_title='Cuisines',page_icon="🥗",layout='wide')

#====================================================================
# Funções
#====================================================================
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
df_raw = pd.read_csv('dataset/zomato.csv')

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
st.header('Marketplace - Cuisines Types')

st.subheader('Best Restaurants of the Main Cuisines Types')

image_path ='logo1.png'
image = Image.open(image_path)
st.sidebar.image(image, width=320)


#st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('#### **Found your Favority Restaurant in the World Now !!**')
st.sidebar.markdown("""___""")

#=============================
#Filtros
#=============================
st.sidebar.markdown('## Filters')

#============================
#Filtro de seleção de paises
#============================
countries_select = st.sidebar.multiselect(
    "would you like to choose the Countries?",
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Brazil','England', 'Qatar','South Africa','Canada','Australia'])

#===============================================
#Filtro deslizante de qumtidade de restaurantes
#===============================================
restaurants_qty = st.sidebar.slider("Would you like to select the restaurants quantity?",value = 10, min_value = 1 ,max_value = 20) 

#============================
# Filtro de tipo de cozinha
#============================
cuisines_select = st.sidebar.multiselect(
    "would you like to choose the Cuisine Type?",['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin_American', 'Healthy_Food',
       'Cafe', 'Fast_Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar_Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North_Eastern',
       'Ice_Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet_Fast_Food', 'Lebanese', 'Modern_Australian',
       'African', 'Coffee_and_Tea', 'Australian', 'Middle_Eastern',
       'Malaysian', 'Tapas', 'New_American', 'Pub_Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe_Food', 'Korean_BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New_Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern_European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum_Cha', 'Pacific_Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim_Sum', 'Crepes', 'Fish_and_Chips', 'Russian',
       'Continental', 'South_Indian', 'North_Indian', 'Salad',
       'Finger_Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street_Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern_Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal_Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast_Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian_Fusion', 'Pan_Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri_Lankan', 'Khaleeji',
       'South_African', 'Drinks_Only', 'Durban', 'World_Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh_Fish', 'Restaurant_Cafe',
       'Kumpir', 'Döner', 'Turkish_Pizza', 'Ottoman', 'Old_Turkish_Bars',
       'Kokoreç'],default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian','American','Italian'])


#===================
# Filtered Dataset
#===================

df2 = df.copy()

df = df.loc[df['country_name'].isin(countries_select),:]

df =(df.loc[df['cuisines']
            .isin(cuisines_select),:]
     .head(restaurants_qty))    


#=========================================================================
# Layout no Streamlit
#=========================================================================
with st.container():
    col1,col2,col3,col4,col5 =st.columns(5)
    
    with col1: 
        valor=str( df2.loc[df2['cuisines'] == 'Italian','aggregate_rating'].max())+ '/'+ str(5.0) 
        df_aux=(df2.loc[(df2['cuisines']=='Italian'),['aggregate_rating','restaurant_id','cuisines','restaurant_name']]
                .groupby(['restaurant_id','cuisines','restaurant_name'])
                .max()
                .reset_index()
                .sort_values('aggregate_rating',ascending=False) 
                .head(1))
        name = df_aux['restaurant_name'].max()
        teste = 'Italian : ' +  name
        col1.metric(teste,valor)
  

    with col2:
        valor=str( df2.loc[df2['cuisines'] == 'American','aggregate_rating'].max())+ '/'+ str(5.0)
        df_aux=(df2.loc[(df2['cuisines']=='American'),['aggregate_rating','restaurant_id','cuisines','restaurant_name']]
                .groupby(['restaurant_id','cuisines','restaurant_name'])
                .max()
                .reset_index()
                .sort_values('aggregate_rating',ascending=False) 
                .head(1))
        name = df_aux['restaurant_name'].max()
        teste = 'American : ' + name
        col2.metric(teste,valor)
     

    with col3:
        valor=str( df2.loc[df2['cuisines'] == 'Arabian','aggregate_rating'].max())+ '/'+ str(5.0) 
        df_aux=(df2.loc[(df2['cuisines']=='Arabian'),['aggregate_rating','restaurant_id','cuisines','restaurant_name']]
                .groupby(['restaurant_id','cuisines','restaurant_name'])
                .max()
                .reset_index()
                .sort_values('aggregate_rating',ascending=False) 
                .head(1))
        name = df_aux['restaurant_name'].max()
        teste = 'Arabian : ' + name
        col3.metric(teste,valor)
        

    with col4:
        valor=str( df2.loc[df2['cuisines'] == 'Japanese','aggregate_rating'].max())+ '/'+ str(5.0)
        df_aux=(df2.loc[(df2['cuisines']=='Japanese'),['aggregate_rating','restaurant_id','cuisines','restaurant_name']]
                .groupby(['restaurant_id','cuisines','restaurant_name'])
                .max()
                .reset_index()
                .sort_values('aggregate_rating',ascending=False)
                .head(1))
        name = df_aux['restaurant_name'].max()
        teste = 'Japanese : ' + name
        col4.metric(teste,valor)
      

    with col5:
        valor=str( df2.loc[df2['cuisines'] == 'Home-made','aggregate_rating'].max())+ '/'+ str(5.0)
        df_aux=(df2.loc[(df2['cuisines']=='Home-made'),['aggregate_rating','restaurant_id','cuisines','restaurant_name']]
                .groupby(['restaurant_id','cuisines','restaurant_name'])
                .max()
                .reset_index()
                .sort_values('aggregate_rating',ascending=False)
                .head(1))
        name = df_aux['restaurant_name'].max()
        teste = 'Home-made : ' + name
        col5.metric(teste,valor)
        
       
       
with st.container():
    st.subheader(f'Top {restaurants_qty} Restaurants' )
    df1 =(df.loc[df['cuisines'].isin(cuisines_select),['aggregate_rating','restaurant_id','restaurant_name','country_name','city','cuisines','average_cost_for_two','votes']]
          .groupby(['restaurant_id','restaurant_name','country_name','city','cuisines','average_cost_for_two','aggregate_rating','votes'])
          .max('aggregate_rating')
          .sort_values('aggregate_rating',ascending=False)
          .reset_index())          
    st.dataframe(df1)


with st.container():
        col1, col2 = st.columns(2)        

        with col1:
            st.markdown(f'##### Top {restaurants_qty} Best Types of Cuisines')
            df_aux = (df2.loc[:,['aggregate_rating','cuisines']]
                      .groupby(['cuisines'])
                      .mean()
                      .reset_index()
                      .sort_values('aggregate_rating',ascending=False)
                      .head(restaurants_qty))          
            fig=px.bar(df_aux,x='cuisines',y='aggregate_rating',text_auto='.4s',labels={'cuisines':'Cuisines','aggregate_rating':'Average of Average Rating'},color='aggregate_rating')
            st.plotly_chart(fig,use_container_width=True)            

        with col2:              
            st.markdown(f'##### Top {restaurants_qty} Worst Types of Cuisines') 
            df_aux = (df2.loc[:,['aggregate_rating','cuisines']]
                      .groupby(['cuisines'])
                      .mean()
                      .reset_index()
                      .sort_values('aggregate_rating',ascending=True) 
                      .head(restaurants_qty)) 
            fig=px.bar(df_aux,x='cuisines',y='aggregate_rating',text_auto='.4s',labels={'cuisines':'Cuisines','aggregate_rating':'Average of Average Rating'},color='aggregate_rating')
            st.plotly_chart(fig,use_container_width=True)            
