from platform import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


#import data
reach_data = 'Platform Reach.csv'
rdf = pd.read_csv(reach_data)

platform_data = 'Platform Datarama Data1.csv'
pdf = pd.read_csv(platform_data)

#add CPM to performance table
pdf['CPM'] = (pdf['Spend']/pdf['Impressions'])*1000

#merging the CPM column with the reach table
df_merged = rdf.merge(pdf, on=['Platform', 'Ad Type'], how='left')

#duplicating each row by 100 rows for random ad spend to be added
pdf2 = pd.concat([df_merged]*100, ignore_index=True)

#adding random spend to empty rows
pdf2['Random_Spend'] = np.random.randint(1, 200000, pdf2.shape[0])

#add in the reach per line
pdf2['Reach'] = ((pdf2['Random_Spend']/pdf2['CPM'])*1000)

#set size values to max
pdf2.loc[pdf2['Reach'] > pdf2['Size'], 'Reach'] = pdf2['Size']

#display df
#st.write(pdf2)

#create new df with only necessary columns
pdf3 = pdf2[['Platform', 'Ad Type', 'Audience', 'Random_Spend', 'Reach']]
pdf3 = pdf3.rename(columns={'Random_Spend': 'Spend ($)'})

#Create st df
#st.write(pdf3)

#Sort the random spend values to display properly in the line charts
pdf3.sort_values(by='Platform', ascending=True, inplace=True)


#create a function for creating the line chart
def display_line_charts(pdf3, selected_options_col_name, selected_options_col_1, selected_options_col_2):
    
    # Loop through each selected value for each value column
    for option_col_name in selected_options_col_name:
        for option_col_1 in selected_options_col_1:
            for option_col_2 in selected_options_col_2:
                
                # Filter the data based on the selected values
                column_name_col = 'Platform'
                value_col_1 = 'Audience'
                value_col_2 = 'Ad Type'
            
                option_df = pdf3[(pdf3[column_name_col] ==option_col_name) &
                             (pdf3[value_col_1] == option_col_1) &
                             (pdf3[value_col_2] == option_col_2)].sort_values('Spend ($)')
                
                
                # Only plot the filtered data set as a line chart if there is data
                if not option_df.empty:
                    fig = px.line(option_df, x="Spend ($)", y="Reach", title= option_col_name + ' - ' + option_col_1)
                    st.plotly_chart(fig)


def app():
    st.title('Platform Reach Generator')

    column_name_col = 'Platform'
    value_col_1 = 'Audience'
    value_col_2 = 'Ad Type'
    options_col_name = list(pdf3[column_name_col].unique())
    options_col_1 = list(pdf3[value_col_1].unique())
    options_col_2 = list(pdf3[value_col_2].unique())

    selected_options_col_name = st.multiselect('Select Your Platform:', options_col_name)
    selected_options_col_1 = st.multiselect('Select Your Audience:', options_col_1)
    selected_options_col_2 = st.multiselect('Select Your Ad Type:', options_col_2)

    if st.button('Filter and Plot'):
        display_line_charts(pdf3, selected_options_col_name, selected_options_col_1, selected_options_col_2)
    
if __name__ == '__main__':
    app()
