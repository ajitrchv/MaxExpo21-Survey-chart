import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Chart') #page title setting up
st.header('Survey Chart MaxExpo Dec21')
st.subheader('The chart from the survey results for "MaxExpo Dec21."')


###----- Loading Data --------
excel_file = 'data/Survey_Results.xlsx'
sheet_name='DATA'

df = pd.read_excel(excel_file,sheet_name=sheet_name,usecols='B:D',header=3)
df_participants = pd.read_excel(excel_file, sheet_name= sheet_name, usecols='F:G', header=3)
df_participants.dropna(inplace=True) #=====Droppping null values in table

#------- Streamlit selection -------------

dept = df['Department'].unique().tolist()

ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value = min(ages),
                        max_value = max(ages), 
                        value=(min(ages),max(ages))
                        )

dept_selection = st.multiselect('Department:',
                                    dept,
                                    default=dept
                                    )



#-------- filter ---------------

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(dept_selection))

number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results:{number_of_result}*')

df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()


#---------------plotting bar chart -----------------------------

bar_chart = px.bar  (df_grouped,
                     x = 'Rating',
                     y = 'Votes',
                     text = 'Votes',
                     color_discrete_sequence= ['#F63366']*len(df_grouped),
                     template= 'plotly_white'     
                    )

st.plotly_chart(bar_chart)



#------Displaying the tables from excel-------------

#col1,col2 = st.columns(2) #--------adding as columns

st.dataframe(df)
#st.dataframe(df_participants)


pie_chart = px.pie(df_participants,title='Total Participants',values='Participants',names='Departments')
st.plotly_chart(pie_chart)

#=-------- for displaying image

#image = Image.open('data/rnd.png')
#st.image(image,caption='Random image from web',width=200)



