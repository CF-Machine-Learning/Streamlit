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
    st.image("Dashboard Image.jpg", use_column_width=True)
    st.write("Source: https://www.istockphoto.com/photo/bicycles-for-rent-in-public-park-gm1128037622-297537720")

    # Add text to introduce the viewer to the dashboard's purpose
    st.title('Dashboard For CitiBike Trip Data Analysis')



    st.subheader("Introduction:")
    st.write("""

Welcome to the Citibike Trip Data Analysis Dashboard! This dashboard presents an in-depth analysis of Citibike trip data in New York City and to explore and gain insights into bike usage patterns, popular bike stations, and the relationship between bike trips and temperature.""")

    st.subheader("How to Use the Dashboard:")
    st.write("""

To navigate through the dashboard, simply use the sidebar on the left to select the page of interest. Each page contains visualizations and analyses related to its specific topic. Feel free to interact with the charts and map for a more detailed exploration of the data.""")

    st.subheader("Dual-Axis Line Chart Page:")
    st.write("""

On this page, we have a dual-axis line chart that showcases the trends of bike trip counts and temperatures over time. By analyzing this chart, we can understand how temperature variations impact bike usage in the city.""")

    st.subheader("Most Popular Stations Bar Chart Page:")
    st.write("""

Here, we present a bar chart highlighting the top 10 most popular Citibike stations in New York City. This chart provides insights into the stations that witness the highest bike trip volumes, helping us identify areas with high demand.""")

    st.subheader("Kepler.gl Map Page:")
    st.write("""

Explore the interactive Kepler.gl map, which displays the geographic distribution of bike trips across the city. The map visually represents bike movement patterns, helping us uncover hotspot areas and popular routes.""")



    st.subheader("Recommendations Page:")
    st.write("""

In the final section, we present our recommendations and insights extracted from the overall analysis. Based on the data-driven findings, we propose strategies to improve bike availability, expand stations, and enhance the user experience.

""")

    st.subheader('Assumptions')
    st.write("""A random seed comprising 32 records and constituting 0.01% of the primary dataframe has been selected. This decision was made to ensure that the subset data employed for the analysis remains within the confines of 25 MB.

The primary dataset is of considerable magnitude, involving the amalgamation of Citibike trip data for the year 2022 with weather-related information. This confluence has resulted in a dataset encompassing 30,689,921 records and 34 variables, thereby amounting to a data size of approximately 9 to 10 gigabytes. Consequently, the act of loading the entire dataset in one instance necessitates a memory allocation of 7 gigabytes, and during subsequent data manipulations, this usage can peak at 32 gigabytes.

In the context of visualizing the data through the utilization of the kepler.gl mapping framework, a methodical approach has been adopted. Specifically, a representative subset of the dataset, comprising 10,000 records randomly selected from each month, has been chosen. This equates to a cumulative selection of 120,000 records, forming the foundation for the ensuing analysis and visualization endeavors conducted within the kepler.gl mapping framework.""")

    st.subheader('Data Source')
    st.write('The bike trip data is sourced from the Citi Bike sharing system, and temperature data is sourced from the National Weather Service.')
    text_new="""Citi Bike Data Source: https://s3.amazonaws.com/tripdata/index.html <br>Weather Data Source: https://www.ncdc.noaa.gov/cdo-web/datasets"""
    st.write(text_new, unsafe_allow_html=True)

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

    st.subheader("Dual axis Line Chart for Bike Trip and Temp")

    # Create the first plot for bike trip counts
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='DATE', y='trip_count', data=merged_df, ax=ax1, color='b')
    ax1.set_ylabel('Bike Trip Count', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    plt.title('Bike Trip Counts')
    plt.xlabel('Date')

    st.subheader('Plot 1: Bike Trip Count')
    st.write("""

The initial visual representation, depicted in Figure 1, delves into the temporal evolution of bike trip counts over the observed period. Employing a line plot, the analysis reveals the fluctuation in bike trip counts in relation to dates. This visualization provides a fundamental insight into the usage patterns of the bike-sharing system, offering an immediate grasp of how trip counts have evolved.""")

    # Show the plot
    st.pyplot(fig1)

    # Create the second plot for temperature
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='DATE', y='temperatures_F', data=merged_df, ax=ax2, color='r')
    ax2.set_ylabel('Temperature (Fahrenheit)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title('Temperature')
    plt.xlabel('Date')

    # Show the plot
    st.pyplot(fig2)

    st.subheader('Plot 2: Temperature')
    st.write("""

In Figure 2, the illustration centers on the variations in temperature, measured in Fahrenheit, throughout the same period of observation. This plot employs a line chart to graphically depict the shifts in temperature over time. This depiction of temperature trends serves as a contextual backdrop, potentially aiding in the interpretation of trends observed in other aspects of the analysis.""")

    # Create the dual-axis line chart
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    # Plot bike trip counts on the first axis (left)
    sns.lineplot(x='DATE', y='trip_count', data=merged_df, ax=ax3, color='b')
    ax3.set_ylabel('Bike Trip Count', color='b')
    ax3.tick_params(axis='y', labelcolor='b')

    # Create a second axis (right) for temperature
    ax4 = ax3.twinx()
    sns.lineplot(x='DATE', y='temperatures_F', data=merged_df, ax=ax4, color='r')
    ax4.set_ylabel('Temperature (Fahrenheit)', color='r')
    ax4.tick_params(axis='y', labelcolor='r')

    # Customize the chart
    plt.title('Bike Trip Count and Temperatures')
    plt.xlabel('Date')
    plt.legend(labels=['Bike Trip Count', 'Temperature'], loc='upper left')

    # Show the plot
    plt.tight_layout()
    st.pyplot(fig3)

    st.subheader('Plot 3: Dual-Axis Line Chart')
    st.write("""

The culmination of this visualization exercise is realized through the dual-axis line chart showcased in Figure 3. This sophisticated chart amalgamates the previous two visualizations, affording the viewer a holistic view of the interplay between bike trip counts and ambient temperatures. On the left axis, the line plot denotes the progression of bike trip counts, while on the right axis, the temperature trends are elegantly presented. This coalescence of data enables a comprehensive understanding of how temperature dynamics intertwine with bike trip patterns.""")

    markdown_text='''The chart depicting bike trip counts over a temporal continuum reveals a discernible and recurring pattern in the frequency of bike trips. Within this pattern, variations in daily bike trip counts are observable; however, there exists an overarching trend of consistency in the total number of bike trips.

Notably, distinct drops and spikes are discernible at specific junctures, notably during the 5th, 9th, and 10th months of the year. This recurrent occurrence aligns with the seasonality inherent to New York's climate.

The graphical representation offers insights into intermittent elevations in bike trip counts, which plausibly correspond to instances of heightened demand. These peaks in bike usage are aptly associated with temporal junctures characterized by escalated demand, such as weekends, holidays, and targeted events.'''
    st.markdown(markdown_text)

elif selected_page == 'Most Popular Station':
    station_counts = data.groupby('start_station_name').size().reset_index(name='Trip Count')

    station_counts_sorted = station_counts.sort_values(by='Trip Count', ascending=False)

    top_10_stations = station_counts_sorted.head(10)

    st.subheader("Most Popular station")

    fig = px.bar(
        top_10_stations,
        x='Trip Count',
        y='start_station_name',
        orientation='h',
        #title='Top 10 Most Popular Citi Bike Stations in New York',
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



    markdown_text=''' The analysis utilizes a random seed to select a subset of 32 records from the primary dataset. This selection was made based on a percentage criterion of 0.01%, a decision prompted by the data's overall size remaining below the 25 MB threshold.

To commence the analysis, the number of bike trip counts was initially computed, considering the origin station as the primary criterion. Subsequently, a filtering process was applied to identify the ten most frequented stations. This filtering was executed based on descending trip count values, resulting in the prioritization of stations with higher trip counts. The insights derived from this process were visualized through a bar chart representation.'''
    st.markdown(markdown_text)

elif selected_page == 'Kepler.gl Map':

    st.subheader("Kepler.gl Map for station and arc connecting them")
    html_file = open("custom_map.html", 'r', encoding='utf-8').read()

    # Render the .html file using st.components.v1.html
    st.components.v1.html(html_file, height=500)

    #st.subheader("Kepler.gl Map for station and arc connecting them")

    markdown_text='''
The analysis pertains to the utilization of an identical dataframe comprising 32 randomly selected seed records. Notably, the data volume adheres to a constraint of less than 25 MB, ensuring data manageability.

The methodology employed involves the utilization of latitude and longitude coordinates of both the starting and ending stations. This information is employed to generate a kepler.gl map, enriched with connecting arcs. Each arc on the map symbolizes an individual trip, thereby providing a visual representation of the journey between the specified stations. Furthermore, the map is interactive, enabling users to hover over arcs to acquire pertinent details, including the time of commencement, station names, and conclusion time.

The customization of the visualization extends beyond the default settings. Color options, for instance, can be tailored to align with user preferences. The coloration of arcs connecting stations can be adjusted for clarity and enhanced interpretability.

Considering the extensive data volume and potential graph complexity, facilitating informed insights demands a strategic approach. To address this, a filtering mechanism is positioned on the left-hand side of the map. Users have the liberty to filter results based on desired starting and ending stations. Additionally, this mechanism assists in pinpointing the most frequently used stations by visualizing connecting arcs between them.





 '''
    st.markdown(markdown_text)



elif selected_page == 'Misc':

    rider_counts = data['rideable_type'].value_counts()
    st.subheader("Pie chart for Rider Type")
    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=rider_counts.index, values=rider_counts.values)])

    # Customize the chart layout
    fig.update_layout(title='Rider Types Distribution')

    # Show the chart using Streamlit
    st.plotly_chart(fig)



    markdown_text=''' The insights drawn from the aforementioned chart suggest a discernible preference among customers for opting for the classic bike type for their rides.

The preponderance of classic bikes, constituting 73.38% of the total rider types, indicates a pronounced preference among users for this bike category. This could be attributed to factors such as familiarity, comfort, and ease of use associated with classic bikes.

The representation of electric bikes at 25.9% signifies a notable presence and growing adoption of this eco-friendly option. This suggests an increasing awareness and interest in sustainable transportation alternatives among riders.

Recognizing the popularity of classic and electric bikes, the service provider could consider optimizing the availability and maintenance of these bikes to meet user demand effectively.

The insights from this analysis could guide the allocation of resources towards the most favored bike categories, influencing infrastructure planning and resource allocation for bike stations and charging facilities.'''
    st.markdown(markdown_text)

    st.subheader("Kepler.gl Map for 10 most popular station and arc connecting them")
    html_file = open("commontripmap.html", 'r', encoding='utf-8').read()

    # Render the .html file using st.components.v1.html
    st.components.v1.html(html_file, height=500)


    markdown_text=''' Presented herewith is the kepler.gl map meticulously crafted to illustrate the ten most frequented stations within the specified context. Notably, the map is complemented by an array of filtering functionalities thoughtfully positioned on the left-hand segment. Noteworthy is the prominent visual representation featured within this map, depicting interconnected arcs that establish connections based on the originating and culminating stations. Further enhancing the user experience, hovering over specific points on the map provides insightful details such as trip commencement information, originating station, and final destination station.'''
    st.markdown(markdown_text)


elif selected_page == 'Recommendations, Insights':
    st.subheader("Recommendations, Insights")
    markdown_text=''' Several insights can be highlighted through the analysis conducted on the Citibike trip data in conjunction with New York's weather data.

1.  The research team has successfully identified the ten prominent stations that consistently attract a significant volume of bike trips. These stations inherently possess the potential to become focal points for bike-sharing services, necessitating increased attention toward bike availability and maintenance endeavors. The comprehensive execution of this analysis mandates the incorporation of maintenance data, which plays a pivotal role in facilitating an extensive evaluation. This dataset will serve as a crucial resource, enabling a thorough assessment and, subsequently, the formulation of data-driven solutions.

2. The line chart depicting bike trip counts over time reveals a consistent pattern in the frequency of bike trips. Noteworthy is the presence of fluctuations in daily trip counts; however, the overarching trend indicates a stable volume of bike trips.

3. The temperature variation line chart underscores distinct seasonal temperature fluctuations over time, with higher temperatures during summer and lower temperatures during winter months.

4. Concurrently, the bike trip count chart indicates variations in trip counts across different months, with notable drops during the 5th, 9th, and 10th months.

5. Plausible factors contributing to this decline include seasonal variations, local events such as road closures and ongoing construction, shifts in the academic calendar, and the influence of public holidays.

6. Determining the precise cause of the reduced bike trip counts necessitates a comprehensive analysis involving historical data, correlation with local events, consideration of prevailing weather conditions, and a comprehensive assessment of contextual factors.

7. This analysis provides valuable insights into user preferences and behaviors, thereby informing strategic marketing initiatives and service enhancements that align with customer requirements. Notably, the analysis reveals a pronounced inclination towards the classic bike rider type, in contrast to the relatively lower preference for electric and docked bike options. This observation underscores the significance of user preferences and sets the groundwork for optimizing the availability of classic bikes to address the evident demand among riders.

8. The examination of the bike trip count data has unveiled a list of highly frequented stations, notably including locations such as Central Avenue Road and Avenue Road. Notably, these stations are situated within the Manhattan zone of New York. This finding has led to the realization that the Manhattan zone harbors a concentration of popular tourist destinations and recreational hubs when contrasted with other zones. This dataset's revelations offer valuable insights into the intricate interplay between tourism dynamics and bike utilization within specific geographical areas.'''

    st.markdown(markdown_text)





# Finally, run the Streamlit app
if __name__ == '__main__':
    st.title("")
