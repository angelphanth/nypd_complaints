import streamlit as st
import numpy as np 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

st.markdown("""
<style>
body {
    background-color: darkgray;
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

st.sidebar.title('NYPD Quick Lookup :sleuth_or_spy:')
st.sidebar.write("On this page you can further explore NYPD's force complaint cases by precinct.")
st.sidebar.markdown('-------')
st.sidebar.write('Year(s)')

min_year = int(df_force['year_received'].min())
max_year = int(df_force['year_received'].max())

year_filter_min, year_filter_max = st.sidebar.slider('(Select a range or single year)', min_year, max_year, [max_year-1, max_year])

df_exp_set = df_force[(df_force['year_received'] <= year_filter_max) & (df_force['year_received'] >= year_filter_min)]
df_exp = df_exp_set.groupby(['precinct','complainant_ethnicity','complainant_gender']).size().rename('cases').reset_index()

# df_mos = df_force[(df_force['year_received'] <= year_filter_max) & (df_force['year_received'] >= year_filter_min)]
df_mos = df_exp_set.groupby(['precinct','mos_ethnicity','mos_gender']).size().rename('cases').reset_index()

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
st.sidebar.write('Would you like to group the cases by the race of the Subjects or Officers?')
side = st.sidebar.selectbox("", ('Subjects', 'Officers'))
st.sidebar.markdown('-------')
st.sidebar.write('Would you like to see a breakdown of the cases by gender of the subjects/officers?')
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

df_info = df_force[df_force['precinct']== selected_precinct]

df_census = pd.read_csv('nypd_pop_2010.csv', index_col=0)
df_income = pd.read_csv('borough_income_2018.csv', index_col=0)

st.title('Census Data')
if selected_precinct in df_census.columns:
    ok = df_census[str(selected_precinct)]
    other = ok.reset_index()[2:-1]
    other.columns = ['Race', 'Population']

    pop = go.Figure(data=[go.Pie(labels=other['Race'], values=other['Population'])])

    pop.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title=f"Precinct {selected_precinct} Population 2010",
            yaxis_title="",
            xaxis_title="",
            font=dict(family="Arial Black",
                size=14,
                color="black"
            ), showlegend=True, legend=dict(
    orientation="h",
    yanchor="bottom",
    xanchor="right",
    x=3))
    st.plotly_chart(pop)

    so = df_income[ok[-1]]
    income = so.reset_index()
    income.columns = ['Household','Median Income']
    
    st.title(f'Borough: {ok[-1]}')

    fig = px.bar(income, y ='Household', x='Median Income', orientation='h', text='Median Income', width=800, height=400)

    fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
        # title=f"Median Income for Borough: {ok[-1]}",
        xaxis_title="Median Income ($)",
        yaxis_title="Household Type",
        font=dict(family="Arial Black",
            size=18,
            color="white"
        ), 
    )

    fig.update_traces(marker_color='white')
    fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
    fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig)



if selected_precinct not in df_census.columns:
    st.write(f'No census data for precinct {selected_precinct}')


if st.sidebar.checkbox(f'NYPD-specific Extra Features'):

    st.markdown('-------')
    st.title(f' :police_car: Precinct {selected_precinct} Continued :police_car: \n\n\n ')

    this = df_exp_set[['shield_no','rank_incident','mos_ethnicity','mos_gender','mos_age_incident','complainant_ethnicity','complainant_gender','complainant_age_incident','allegation','board_disposition']]

    this.columns = ['Shield Number','Officer Rank','Officer Race','Officer Gender','Officer Age','Subject Race','Subject Gender','Subject Age','Allegation','Board Decision']

    this['Board Decision'] = this['Board Decision'].str.split(n=1, expand=True)[0]

    ya = this.groupby(['Officer Race', 'Board Decision']).size().rename('Percentage')

    decision = ya.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
    decision = decision.reset_index()

    st.sidebar.write('Select Extra')
    option_again = st.sidebar.selectbox("", ('Precinct Complaint Outcomes', 'Officer Search'))
    st.sidebar.markdown('-------')

    if option_again == 'Precinct Complaint Outcomes':

        fig = px.bar(decision, x="Percentage", y="Officer Race", orientation='h', text='Board Decision', color='Board Decision',width=1000)
        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Board Decision Percentages by Officer Race",
            yaxis_title="",
            xaxis_title="",
            font=dict(family="Arial Black",
                size=14,
                color="black"
            ), showlegend=False
        )
        fig.update_traces(textfont_size=12)
        fig.update_xaxes(showgrid=False, zeroline=False, gridcolor='white', showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig) 

    if option_again == 'Officer Search':


        df_force = df_force[['shield_no','first_name','last_name','rank_incident','mos_ethnicity','mos_gender','mos_age_incident','complainant_ethnicity','complainant_gender','complainant_age_incident','allegation','year_received','board_disposition']]

        df_force.columns = ['Shield Number','Officer First Name','Officer Last Name','Officer Rank','Officer Race','Officer Gender','Officer Age','Subject Race','Subject Gender','Subject Age','Allegation','Year Complaint Received','Board Decision']

        st.sidebar.write('Enter Shield (Badge) Number for Complaint History')
        user_input = st.sidebar.selectbox('', list(this['Shield Number'].unique()), 0)

        st.dataframe(df_force[df_force['Shield Number'] == user_input])


