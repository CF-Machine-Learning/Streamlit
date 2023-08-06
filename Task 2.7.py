import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit import components
import plotly.graph_objects as go



data = pd.read_csv("Random32MainData.csv")
weather=pd.read_csv("weather data.csv")
columns_to_drop = [7,8,9,11,13,15,17,19,21,23,25,27,29,31,32,33,34,35,36,37,38,39,40,41,43,44,45]
weather = weather.drop(weather.columns[columns_to_drop], axis=1)

# Define the pages for presenting findings
pages = ['Introduction', 'Dual Axis Line Chart', 'Most Popular Station',"Kepler.gl Map","Misc",'Recommendations, Insights']  # You can add more pages as needed

# Create a sidebar to select pages
selected_page = st.sidebar.selectbox('Select Page:', pages)

# Load the reduced sample data using the load_data function
#data = load_data()

# Display different content based on the selected page
if selected_page == 'Introduction':
    st.image("Dashboard Image.jpeg", use_column_width=True)

    # Add text to introduce the viewer to the dashboard's purpose
    st.title('Welcome to Your Dashboard')


    st.subheader('Purpose of the Dashboard')
    st.write("""

**Introduction:**

Welcome to the Citibike Trip Data Analysis Dashboard! This dashboard presents an in-depth analysis of Citibike trip data in New York City. Our goal is to explore and gain insights into bike usage patterns, popular bike stations, and the relationship between bike trips and temperature.

**Dual-Axis Line Chart Page:**

On this page, we have a dual-axis line chart that showcases the trends of bike trip counts and temperatures over time. By analyzing this chart, we can understand how temperature variations impact bike usage in the city.

**Most Popular Stations Bar Chart Page:**

Here, we present a bar chart highlighting the top 10 most popular Citibike stations in New York City. This chart provides insights into the stations that witness the highest bike trip volumes, helping us identify areas with high demand.

**Kepler.gl Map Page:**

Explore the interactive Kepler.gl map, which displays the geographic distribution of bike trips across the city. The map visually represents bike movement patterns, helping us uncover hotspot areas and popular routes.

**Solution for Citibike's Supply Problem:**

We have included an additional chart that stands out in finding a solution for Citibike's supply problem. This chart provides crucial metrics and insights to address the supply-demand balance and optimize bike availability.

**Recommendations Page:**

In the final section, we present our recommendations and insights extracted from the overall analysis. Based on the data-driven findings, we propose strategies to improve bike availability, expand stations, and enhance the user experience.

**How to Use the Dashboard:**

To navigate through the dashboard, simply use the sidebar on the left to select the page of interest. Each page contains visualizations and analyses related to its specific topic. Feel free to interact with the charts and map for a more detailed exploration of the data.""")

    st.subheader('Data Source')
    st.write('The bike trip data is sourced from the Citi Bike sharing system, and temperature data is sourced from the National Weather Service. The data has been combined and preprocessed for analysis.')

    st.subheader('Instructions')
    st.write('Please use the sidebar to navigate between different sections of the dashboard. You can select specific pages to view various visualizations and insights.')

    #st.write('This is Page 1')
    # You can add plots, tables, or any other content specific to Page 1 here

elif selected_page == 'Dual Axis Line Chart':
    #merged_df = prepare_data(data)
    data['started_at']=pd.to_datetime(data['started_at']).dt.date
    #st.write(data)
    trips_per_day = data.groupby('started_at').size().reset_index(name='trip_count')
    trips_per_day['started_at'] = pd.to_datetime(trips_per_day['started_at'])
    #st.write(trips_per_day)
    weather['DATE'] = pd.to_datetime(weather['DATE'])
    merged_df = pd.merge(weather,trips_per_day, left_on='DATE', right_on='started_at', how='left')


    merged_df.drop(columns=['started_at'], inplace=True)



    merged_df['temperatures_F'] = (merged_df['TAVG'] * 9/5) + 32
    #st.write(merged_df)

    # Step 4: Create the dual-axis line chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot bike trip counts on the first axis (left)
    sns.lineplot(x='DATE', y='trip_count', data=merged_df, ax=ax1, color='b')
    ax1.set_ylabel('Bike_trip_count', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Create a second axis (right) for temperature
    ax2 = ax1.twinx()
    sns.lineplot(x='DATE', y='temperatures_F', data=merged_df, ax=ax2, color='r')
    ax2.set_ylabel('Temperature (Fahrenheit)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')



    # Customize the chart
    plt.title('trip_count and Temperatures')
    plt.xlabel('Date')
    plt.legend(labels=['Bike_trip_count', 'Temperature'], loc='upper left')

    # Show the plot
    plt.tight_layout()
    st.pyplot(fig)
    # You can add different content specific to Dual Axis Line Chart here
    st.subheader("Dual axis Line Chart for Bike Trip and Temp")

    markdown_text=''' Using this sample, we counted the number of bike trips on a daily basis and plotted it in plot 1. Next, we gathered temperature data per day and created plot 2 to visualize the temperature trends.

Upon merging both plots, we presented a dual-axis line chart to compare bike trips and temperatures and observed that the line chart of bike trip counts over time shows that there is a consistent pattern in the number of bike trips. There are fluctuations in the daily bike trip counts, but overall, the number of bike trips remains relatively stable.

The line chart of temperature variation over time indicates that there are seasonal changes in temperature. The temperature tends to be higher during the summer months and lower during the winter months.

The consistent bike trip counts despite temperature variations could suggest that bike-sharing is popular year-round in the region, regardless of weather conditions. This finding might indicate that bike-sharing infrastructure is well-utilized and could potentially support tourism and recreational activities in the area.'''
    st.markdown(markdown_text)

elif selected_page == 'Most Popular Station':
    station_counts = data.groupby('start_station_name').size().reset_index(name='Trip Count')

    station_counts_sorted = station_counts.sort_values(by='Trip Count', ascending=False)

    top_10_stations = station_counts_sorted.head(10)

    fig = px.bar(
        top_10_stations,
        x='Trip Count',
        y='start_station_name',
        orientation='h',
        title='Top 10 Most Popular Citi Bike Stations in New York',
        labels={'start_station_name': 'Station', 'Trip Count': 'Number of Trips'},
        text='Trip Count',  # Data labels: Display trip counts on the bars
    )

    # Customize the chart layout and design
    fig.update_layout(
        xaxis_title='Number of Trips',
        yaxis_title='Station',
        yaxis_categoryorder='total ascending',  # Order the stations by trip counts
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color
        paper_bgcolor='rgba(0,0,0,0)',  # Set the chart background color
        font=dict(size=12),  # Adjust the font size
        margin=dict(l=50, r=50, t=80, b=50),  # Adjust the margins
    )

    # Show the plot using Streamlit
    st.plotly_chart(fig)
    # You can add different content specific to Most Popular Station here

    st.subheader("Most Popular station")

    markdown_text=''' In this analysis, our approach involved counting the number of bike trips between the starting and ending stations. Based on this information, we identified the top 10 most popular stations and presented them using a bar plot. This bar plot visually represents the popularity of these stations, making it easier to understand which stations are frequented the most.'''
    st.markdown(markdown_text)

elif selected_page == 'Kepler.gl Map':
    html_file = open("custom_map.html", 'r', encoding='utf-8').read()

    # Render the .html file using st.components.v1.html
    st.components.v1.html(html_file, height=500)

    st.subheader("Kepler.gl Map for station and arc connecting them")

    markdown_text=''' In this analysis we have taken the trips on the basis of starting and the ending station with an arc connecting them with the help of kepler.gl map where if we want you can customize the maps , find the arc between the most common stations. changing of colour options is also available. '''
    st.markdown(markdown_text)



elif selected_page == 'Misc':

    rider_counts = data['rideable_type'].value_counts()

    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=rider_counts.index, values=rider_counts.values)])

    # Customize the chart layout
    fig.update_layout(title='Rider Types Distribution')

    # Show the chart using Streamlit
    st.plotly_chart(fig)

    st.subheader("Pie chart for Rider Type")

    markdown_text=''' This is an simple pie chart which we have tried to plot on Rider type category from the citi Bike trip data  and we finds that the  classic bike is compared to electric bike and docked bike as the percentage is 73.3.8% for the classic bike,25.9% for the electric bike and 0.85% for docked bike

we can also concludes from the above chart the preferences of customers for taking a ride in classic bike is more.'''
    st.markdown(markdown_text)


    html_file = open("commontripmap.html", 'r', encoding='utf-8').read()

    # Render the .html file using st.components.v1.html
    st.components.v1.html(html_file, height=500)
    st.subheader("Kepler.gl Map for 10 most popular station and arc connecting them")

    markdown_text=''' We have taken the top 10 most popular station on the basis of trip count and with the help of kepler.gl map and tries to use an arc which connects them'''
    st.markdown(markdown_text)


elif selected_page == 'Recommendations, Insights':
    markdown_text=''' We can mention some of the insights by performing analsysis on citi bike trip data  and Weather data from New york.

1.  We identified the top 10 most popular stations, which are consistently attracting a high number of bike trips. These stations can be considered prime locations for bike-sharing services and may require more attention in terms of bike availability and maintenance.

2. Line chart of bike trip counts over time shows that there is a consistent pattern in the number of bike trips. There are fluctuations in the daily bike trip counts, but overall, the number of bike trips remains relatively stable.

3. The line chart of temperature variation over time indicates that there are seasonal changes in temperature. The temperature tends to be higher during the summer months and lower during the winter months.

4. We observed that bike trip counts vary across different months. There seems to be a seasonal pattern, with higher bike usage during certain months, which could be influenced by factors such as weather, tourist influx, or local events.

5. The analysis can help understand user preferences and behaviors, guiding marketing strategies and service improvements to cater to customer needs where we have seen that the choice of rider type for classic bike is more as compared to electric and docked bike so we can take this under preferences and try to improve the availablity of classic bike based on their demand.

6. We have seen from the number of bike trip the most popular stations that we have found states that these stations such as Central Avenue Road, Avenue Road etc which comes under the manhattan zone of new york and then we came to know that the most tourits places and recreational centres are mostly in these zone as comapred to other zones so the data offer insights into how tourism affects bike usage in specific areas.'''

    st.markdown(markdown_text)





# Finally, run the Streamlit app
if __name__ == '__main__':
    st.title("")
