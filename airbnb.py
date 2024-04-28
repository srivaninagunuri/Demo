import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

airbnb = pd.read_csv("C:/Users/admin/Downloads/AB_NYC_2019.csv")
# For exploring and analyzing the data, I am deleting some columns

airbnb.drop(['latitude','longitude','reviews_per_month','last_review'], axis=1, inplace=True)

# Analysis-1
room_price_area_wise = airbnb.groupby(['neighbourhood_group','room_type'])['price'].max().reset_index()
room_price_area_wise.sort_values('price', ascending=False).head(10)

# Analysis-2
area_reviews = airbnb.groupby(['neighbourhood_group'])['number_of_reviews'].max().reset_index()

# Analysis-3
price_area = airbnb.groupby(['price'])['number_of_reviews'].max().reset_index()

# Analysis-4
busy_host = airbnb.groupby(['host_id', 'host_name', 'room_type'])['number_of_reviews'].max().reset_index()
busy_host = busy_host.sort_values('number_of_reviews', ascending=False).head(10)

# Analysis-5
highest_price = airbnb.groupby(['host_id', 'host_name', 'room_type','neighbourhood_group'])['price'].max().reset_index()
highest_price = highest_price.sort_values('price', ascending=False).head(10)

# Analysis-6
trafic_areas = airbnb.groupby(['neighbourhood_group', 'room_type'])['minimum_nights'].count().reset_index()
trafic_areas = trafic_areas.sort_values('minimum_nights', ascending=False).head(10)

def airb_plot_1(df,neighbourhood):
    airb= df[df["neighbourhood"]==neighbourhood]
    airb.reset_index(drop= True, inplace= True)

    airbg= pd.DataFrame(airb.groupby(["neighbourhood","price"])["host_name"].sum())
    airbg.reset_index(inplace=True)


    plot_1 = px.bar(airb, y= "price",  x= "host_name",  title= "host_name and price")
    plot_1.update_traces(marker_color= 'yellowgreen')

    st.plotly_chart(plot_1)



#Streamlit

st.title("AirBnb-Analysis")

select = option_menu(menu_title=None, options=["Home", "Explore Data", "Contact"], default_index=0, orientation="horizontal")

if select == "Home":
    st.subheader("Data Analysis")
    st.write("Airbnb is an american San Francisco-based companey operating an oline marketplace for short- and") 
    st.write("long-term homestays and experiences.The Companey acts as a broker and charges a commision from ")
    st.write("each booking. The companey was Founded in 2008 by Brain Chesky,Nathan Blecharczyk, and joi gebbia.") 
    st.write("Airbnb is a shortend version of its original name,AirBedandBreakfast.com The companey is")
    st.write("credited with revolutionizing the tourism industry,while also having been the subject of intense") 
    st.write("creticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an")
    st.write("unofferdable increase in home rents, and for a lack of regulation.")
    st.markdown("<hr>", unsafe_allow_html=True) 
    


    st.write(" ")
    st.write(" ")
    
    st.subheader("Skill Take Away From This Project:")

    st.write("python scripting Data peprocesing, Visualization , EDA, Streamlit, MongoDB or Tableau.")

    st.write("DOMINE:")

    st.write("Travel Industry, Property management and Tourism")

elif select == "Explore Data":
    

        method = st.radio("Choose Your Filters", ["The view of room types", "Number of reviews in terms of Area",
                                                  "Busiest host in terms of Reviews",
                                                  "Top 10 Traffic Areas Based on Minimum Nights Booked",
                                                  "Hosts with maximum price charges",
                                                  "Top 10 Traffic Areas Based on Minimum Nights Booked",
                                                  "Heatmap","The view of hostname with price"])
        if method == "The view of room types":
            # Plot_1
            neighbourhood_group = ['Queens', 'Manhattan', 'Manhattan', 'Brooklyn', 'Brooklyn',
                                    'Queens', 'Manhattan', 'Staten Island', 'Bronx', 'Queens']

            room_type = ['Private room', 'Entire home/apt', 'Private room', 'Entire home/apt', 'Private room',
                        'Shared room', 'Shared room', 'Entire home/apt', 'Private room', 'Entire home/apt',]

            room_dict = {}  # Initialize as a dictionary

            for room in room_type:
                room_dict[room] = room_dict.get(room, 0) + 1  # Increase the count for each room type

            df = px.bar(room_price_area_wise, x='room_type', y='price', title='The view of Room Types', height=400, width=350)
            st.plotly_chart(df)

        if method == "Number of reviews in terms of Area":
            # Plot_2
            df2 = px.bar(area_reviews, x="neighbourhood_group", y="number_of_reviews", title="Number of reviews in terms of Area", height=400, width=350)
            df2.update_traces(marker_color='pink')  # Setting the color of bar graph

            st.plotly_chart(df2)

        if method == "Busiest host in terms of Reviews":
            # Plot3
            price_list = price_area['price']
            review = price_area['number_of_reviews']
            
            df3 = px.scatter(price_area, x="price", y="number_of_reviews")
            df3.update_traces(marker_color='red')  # Setting the color of bar graph

            st.plotly_chart(df3)

        if method == "Top 10 Traffic Areas Based on Minimum Nights Booked":
            # Plot_4
            df4 = px.bar(busy_host, y="host_name", x="number_of_reviews", orientation="h", height=400, title="Busiest host in terms of Reviews")
            df4.update_traces(marker_color='purple')
            st.plotly_chart(df4)

        if method == "Hosts with maximum price charges":
            # Plot_5
            df5 = px.bar(highest_price, x="host_name", y="price", title="Hosts with maximum price charges")
            df5.update_traces(marker_color='orange')
            st.plotly_chart(df5)

        if method == "Top 10 Traffic Areas Based on Minimum Nights Booked":
            # Plot_6
            df6 = px.bar(trafic_areas, x="minimum_nights", y="room_type", orientation="h", height=400, title="Top 10 Traffic Areas Based on Minimum Nights Booked")
            df6.update_traces(marker_color='yellow')
            st.plotly_chart(df6)

        if method == "Heatmap":
            # Plot-7
            numeric_columns = airbnb.select_dtypes(include=['float64', 'int64']).columns
            corr = airbnb[numeric_columns].corr(method='kendall')

            plt.figure(figsize=(12, 6))
            sns.heatmap(corr, annot=True)
            plt.title('Correlation Heatmap (Kendall)')
            plt.xlabel('Features')
            plt.ylabel('Features')

            # Display the Matplotlib figure using Streamlit
            st.pyplot(plt.gcf())

            # Close the Matplotlib figure to suppress the warning
            plt.close()

        if method == "The view of hostname with price":
            
            neighbourhood = st.selectbox("Select the neghberhood to view the Price and Name",airbnb["neighbourhood"].unique())

            airb_plot_1(airbnb, neighbourhood)


elif select == "Contact":
    st.title("Data Analysis")
    st.markdown("This Project aims to analysis data ,perform data cleaning and preparation, develop interactive geospatialvisualizations, and  ")
    
    st.markdown("create dynamic plots to gain insights into pricing variables, availability")
    st.markdown("patterns and location-based trends.")

    st.header("SRIVANI_NAGUNURI")

    st.write("Mail: nagunurisrivani01@gmail.com")
