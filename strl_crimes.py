import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import wget


df = pd.read_csv('/Users/kitsuyomi/Desktop/crimedata.csv')



st.write("""
# Introductory analysis of crime data

The dashboard based on the Crimes in US Communities Dataset from Kaggle
""")


st.subheader('1. Which state is most dangerous for the location of American communities?')

st.write("""Mean Violent сrimes per population in states""")

number = 0
selection1 = st.multiselect('You can specify the information on the desired state', sorted(df['state'].unique()), sorted(df['state'].unique()), key = number)
df_subh1 = df.groupby('state').agg({'ViolentCrimesPerPop': 'mean'}).reset_index()

subh1 = alt.Chart(df_subh1[df_subh1.state.isin(selection1)]).mark_bar().encode(x = 'state', y = 'ViolentCrimesPerPop')
st.write(subh1)

st.write(""" As we can see, communities located, for example, in Washington, D.C., 
are more dangerous - on average, more violent crimes are committed in them. 
At the same time, in communities located in the state of North Dakota, there are 
fewer such crimes on average""")



st.subheader('2. Correlation of rental cost and average number of robberies')
number = 1
selection2 = st.multiselect('You can specify the information on the desired state', sorted(df['state'].unique()), sorted(df['state'].unique()), key = number)

fig = px.scatter(df[df.state.isin(selection2)], x="MedRent", y="robberies", labels={
                     "MedRent": "Median rental cost",
                     "robberies": "Robberies"
                 }, title = 'Correlation of rental cost and average number of robberies')
fig.update_layout(yaxis_range=[0,1000])
fig.update_layout(margin = dict(r = 0, t = 30))
st.plotly_chart(fig, use_container_width=True)
st.write(""" My hypothesis was not confirmed: there is no correlation on the graph between the cost of rent and the number of robberies""")



st.subheader('3. Are divorced men more dangerous for women?')

number = 2
selection3 = st.multiselect('You can specify the information on the desired state', sorted(df['state'].unique()), sorted(df['state'].unique()), key = number)

fig = px.scatter(df[df.state.isin(selection3)], x="MalePctDivorce", y="rapesPerPop", labels={
                     "MalePctDivorce": "Percentage of divorced men",
                     "rapesPerPop": "Rapes per population"
                 }, title = 'Correlation of the percentage of divorced men and the number of rapes in state')
fig.update_layout(margin = dict(t = 30))
fig.update_layout(yaxis_range=[-1,200])
st.plotly_chart(fig, use_container_width=True)
st.write(""" There is a linear relation between the number of divorced men and rapes.
Perhaps in such communities it is worth paying more attention to psychological assistance to vulnerable segments of the population""")



st.subheader("4. Successes (?) of the Government's policy of supporting racial minorities")

number = 3
selection4 = st.selectbox('You can specify the information on the desired state by set max percantage of the whites', sorted(range(51, 101), reverse=True), key = number)


df_murders = df.groupby('state').agg({'murdPerPop': 'mean', 'racePctWhite': 'mean'}).reset_index()
fig = px.bar(df_murders[(df_murders['murdPerPop'] > 5) & (df['racePctWhite'] <= selection4)], y='state', x='murdPerPop', color='racePctWhite', color_continuous_scale='Viridis', 
             labels={'state': 'State', 'murdPerPop':'Murders per population', 'racePctWhite': 'Percentage of the whites'},
            title = 'The number of murders by state')
fig.update_layout(height=500, margin = dict(t = 30))
st.plotly_chart(fig, use_container_width=True)

st.write(""" Let's look at the graph without an outlier (Washington State, DC)""")

number = 4
selection5 = st.selectbox('You can specify the information on the desired state by set max percantage of the whites', sorted(range(51, 101), reverse=True), key = number)

df_murders = df.groupby('state').agg({'murdPerPop': 'mean', 'racePctWhite': 'mean'}).reset_index()
df_murders = df_murders[df_murders['state'] != 'DC']
fig = px.bar(df_murders[(df_murders['murdPerPop'] > 5) & (df['racePctWhite'] <= selection5)], y='state', x='murdPerPop', color='racePctWhite', color_continuous_scale='Viridis', 
             labels={'state': 'State', 'murdPerPop':'Murders per population', 'racePctWhite': 'percentage of the whites'},
                        title = 'The number of murders by state')
fig.update_layout(height=500, margin = dict(t = 30))
st.plotly_chart(fig, use_container_width=True)

st.write(""" In most states, there is no linear relationship between racial diversity 
and the number of murders. But at the same time, in some states there is a big problem
 of non-inclusion of racial minorities in American society, which results in a large 
 number of crimes. The American government should pay more attention to racial politics 
 in certain states """)



st.subheader('5. Uneducated thieves')

number = 5
selection6 = st.multiselect('You can specify the information on the desired state', sorted(df['state'].unique()), sorted(df['state'].unique()), key = number)

fig = px.scatter(df[df.state.isin(selection6)], x="larcPerPop", y="PctLess9thGrade", labels={
                     "larcPerPop": "Larcenies per population",
                     "PctLess9thGrade": "Percentage of uneducated people"
                 }, title = 'Correlation between the number of people with education less than grade 9 and the number of theft')
fig.update_layout(xaxis_range=[10,12000])
fig.update_layout(yaxis_range=[0,40])
fig.update_layout(margin = dict(t = 30))
st.plotly_chart(fig, use_container_width=True)
st.write(""" There is indeed a connection between ignorance and theft. Lack of education often entails a lack of stable earnings and, 
as a result, forces to steal. The Government should allocate more funds to finance schools in communities, especially in poor ones""")