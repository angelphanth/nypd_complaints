import streamlit as st
import numpy as np 
import pandas as pd 
import plotly.express as px

st.markdown("""
<style>
body {
    background-color: #cce6ff;
}
</style>
    """, unsafe_allow_html=True)


# Path to dataset
path = 'cleaned_nypd_complaints.csv'

# Loading in and cleaning the data
@st.cache
def load_data():
    df = pd.read_csv(path, index_col=0)
    force_complaints = df[df['fado_type'] == 'Force']
    return force_complaints

# Run our function and save the cleaned df to 'df_nyc'
df_force = load_data()

df_exp = df_force.groupby(['precinct','complainant_ethnicity','complainant_gender']).size().rename('cases').reset_index()
df_mos = df_force.groupby(['precinct','mos_ethnicity','mos_gender']).size().rename('cases').reset_index()

st.sidebar.title('Settings')
st.sidebar.write('Check it out')
st.sidebar.markdown('-------')


st.sidebar.write('Select a Precinct')

# Creating the selectbox and giving the dropdown options to choose from
precinct_most_to_least = df_exp.groupby(['precinct']).sum().sort_values(by='cases', ascending=False).index
selected_precinct = st.sidebar.selectbox('(Sorted from most to least cases)', precinct_most_to_least)

df_tot = df_exp[df_exp['precinct']==selected_precinct]


f'''
# NYPD #

# :oncoming_police_car: Precinct {selected_precinct} :oncoming_police_car: 

## Total Excessive Force Reports: **{df_tot['cases'].sum()}**


 
#
'''

st.sidebar.markdown('-------')
st.sidebar.write('Cases by:')
side = st.sidebar.selectbox("", ('Subjects', 'Officers'))
st.sidebar.markdown('-------')
st.sidebar.write('Group Cases by Gender?')
option = st.sidebar.selectbox("", ('No', 'Yes'))
st.sidebar.markdown('-------')

if option == 'No':

    if side == 'Subjects':
    
        df_complainant = df_exp[df_exp['precinct']==selected_precinct].groupby(['complainant_ethnicity']).sum().reset_index().sort_values(by='cases', ascending=False)
        df_complainant['Percentage'] = df_complainant['cases']/(df_complainant['cases'].sum())*100

        fig = px.bar(df_complainant, y ='complainant_ethnicity', x='Percentage', orientation='h', text='cases', width=800, height=600)

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Subject Ethnicity",
            xaxis_title="Percentage of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), 
        )

        fig.update_traces(marker_color='white')
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)

    if side == 'Officers':

        df_officers = df_mos[df_mos['precinct']==selected_precinct].groupby(['mos_ethnicity']).sum().reset_index().sort_values(by='cases', ascending=False)
        df_officers['Percentage'] = df_officers['cases']/(df_officers['cases'].sum())*100

        fig = px.bar(df_officers, y ='mos_ethnicity', x='Percentage', orientation='h', text='cases', width=800, height=600)

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Officer Ethnicity",
            xaxis_title="Percentage of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), 
        )

        fig.update_traces(marker_color='white')
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)


if option == 'Yes':

    if side == 'Subjects':

        df_complainant = df_exp[df_exp['precinct']==selected_precinct].groupby(['complainant_ethnicity','complainant_gender']).sum()
        df_complainant['Percentage'] = df_complainant.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_complainant = df_complainant.reset_index().sort_values(by='cases', ascending=False)

        fig = px.bar(df_complainant, x="cases", y="complainant_ethnicity",
                    color='complainant_gender', orientation='h', text='complainant_gender', 
                    hover_data=["complainant_gender", "Percentage"])

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Cases by subject ethnicity",
            xaxis_title="Number of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), showlegend=False
        )

        fig.update_traces(textfont_size=12)
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)    

    if side == 'Officers':

        df_officers = df_mos[df_mos['precinct']==selected_precinct].groupby(['mos_ethnicity','mos_gender']).sum()
        df_officers['Percentage'] = df_officers.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_officers = df_officers.reset_index().sort_values(by='cases', ascending=False)

        fig = px.bar(df_officers, x="cases", y="mos_ethnicity",
                    color='mos_gender', orientation='h', text='mos_gender', 
                    hover_data=["mos_gender", "Percentage"])

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Officer Ethnicity",
            xaxis_title="Number of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), showlegend=False
        )

        fig.update_traces(textfont_size=12)
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)


if st.sidebar.checkbox(f'Precinct {selected_precinct} Case Details'):

    st.markdown('-------')
    st.title(f'Precinct {selected_precinct} Cases')

    st.dataframe(df_force[df_force['precinct'] == selected_precinct])