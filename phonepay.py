import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image


# Fetching data from the table and dataframe creation
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CHARY@sri#",
    database="phonepe",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

# Creating agg_insur_df
mycursor.execute("SELECT * FROM aggregated_insurance")
table1 = mycursor.fetchall()
Agg_insurance = pd.DataFrame(table1, columns=("Transaction_type","Transaction_count","Transaction_amount","States","Year","Quarter"))


# Creating agg_trans_df
mycursor.execute("SELECT * FROM aggregated_Transaction")
table2 = mycursor.fetchall()
Agg_transaction = pd.DataFrame(table2, columns=("States","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


# Creating agg_insur_df
mycursor.execute("SELECT * FROM aggregated_Users")
table3 = mycursor.fetchall()
Agg_user = pd.DataFrame(table3, columns=("States","Year","Quarter","Brands","percentage","Transaction_count"))


# Creating map_insur_df
mycursor.execute("SELECT * FROM Map_insurance")
table4 = mycursor.fetchall()
Map_insur = pd.DataFrame(table4, columns=("States","Year","Quarter","Districts","Transaction_amount","Transaction_count"))


# Creating map_trans_df
mycursor.execute("SELECT * FROM Map_Transaction")
table5 = mycursor.fetchall()
Map_Trans = pd.DataFrame(table5, columns=("States","Year","Quarter","Districts","Transaction_amount","Transaction_count"))



# Creating map_user_df
mycursor.execute("SELECT * FROM Map_users")
table6 = mycursor.fetchall()
Map_users = pd.DataFrame(table6, columns=("States","Year","Quarter","Districts","registeredUsers","AppOpens"))



# Creating top_insur_df
mycursor.execute("SELECT * FROM Top_insurance ")
table7 = mycursor.fetchall()
Top_insur = pd.DataFrame(table7, columns=("States","Year","Quarter","pincodes","Transaction_count","Transaction_amount"))


# Creating top_trans_df
mycursor.execute("SELECT * FROM Top_Transactions")
table8 = mycursor.fetchall()
Top_trans = pd.DataFrame(table8, columns=("States","Year","Quarter","pincodes","Transaction_count","Transaction_amount"))


# Creating top_users_df
mycursor.execute("SELECT * FROM Top_Transactions")
table8 = mycursor.fetchall()
Top_trans = pd.DataFrame(table8, columns=("States","Year","Quarter","pincodes","Transaction_count","Transaction_amount"))


# Creating top_users_df
mycursor.execute("SELECT * FROM Top_users")
table9 = mycursor.fetchall()
Top_users= pd.DataFrame(table9, columns=("States","Year","Quarter","pincodes","registeredUsers"))


def Transaction_amount_count_Y(df,Year):
    df['Year'] = df['Year'].astype(int)
    trany = df[df["Year"] == Year]
    trany.reset_index(drop = True, inplace= True)

    tranygrp = trany.groupby("States")[["Transaction_amount","Transaction_count"]].sum()
    tranygrp.reset_index(inplace= True)
    
    col1, col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(trany, x="States", y="Transaction_amount", title=f"{Year} TRANSACTION AMOUNT",height = 650, width=600)
        fig_amount.update_traces(marker_color='darkblue')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)

    
    with col2:

        fig_count = px.bar(trany, x="States", y="Transaction_count", title=f"{Year}TRANSACTION COUNT",height = 650, width=600)
        fig_count.update_traces(marker_color='red')  # Setting the color of bargraph
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        tranygrp = trany.groupby("States")[["Transaction_amount"]].sum().reset_index()
        response = requests.get(url)
        data = json.loads(response.content)

        fig_india = px.choropleth(tranygrp, 
                                geojson=data, 
                                locations="States", 
                                featureidkey="properties.ST_NM",
                                color= "Transaction_amount",
                                color_continuous_scale="Rainbow",
                                range_color=(tranygrp["Transaction_amount"].min(), tranygrp["Transaction_amount"].max()),
                                hover_name="States", 
                                title=f"{Year} TRANSACTION AMOUNT", 
                                height=500, 
                                width=450)
        fig_india.update_geos(fitbounds="locations")
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)
    
    with col2:
        
        tranygrp = trany.groupby("States")[["Transaction_count"]].sum().reset_index()
        fig_india2 = px.choropleth(tranygrp, 
                                geojson=data, 
                                locations="States", 
                                featureidkey="properties.ST_NM",
                                color= "Transaction_count",
                                color_continuous_scale="Rainbow",
                                range_color=(tranygrp["Transaction_count"].min(), tranygrp["Transaction_count"].max()),
                                hover_name="States", 
                                title=f"{Year} TRANSACTION COUNT", 
                                height=500, 
                                width=450)
        fig_india2.update_geos(fitbounds="locations")
        fig_india2.update_geos(visible=False)
        st.plotly_chart(fig_india2)

    return trany


def Transaction_amount_count_Y_Q(df, Quarter):
    tranc = df[df["Quarter"] == Quarter]
    tranc.reset_index(drop = True, inplace= True)

    tranygrp = tranc.groupby("States")[["Transaction_amount","Transaction_count"]].sum()
    tranygrp.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tranc, x="States", y="Transaction_amount", title=f"{tranc["Year"].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT")
        fig_amount.update_traces(marker_color='darkblue')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tranc, x="States", y="Transaction_count", title=f"{tranc["Year"].min()} YEAR {Quarter}QUARTER TRANSACTION COUNT")
        fig_count.update_traces(marker_color='red')  # Setting the color of bargraph
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        tranygrp = tranc.groupby("States")[["Transaction_amount"]].sum().reset_index()
        response = requests.get(url)
        data = json.loads(response.content)
        fig_india = px.choropleth(tranygrp, 
                                geojson=data, 
                                locations="States", 
                                featureidkey="properties.ST_NM",
                                color= "Transaction_amount",
                                color_continuous_scale="Rainbow",
                                range_color=(tranygrp["Transaction_amount"].min(), tranygrp["Transaction_amount"].max()),
                                hover_name="States", 
                                title= f"{tranc["Year"].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT", 
                                height=500, 
                                width=450)
        fig_india.update_geos(fitbounds="locations")
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)

    with col2:
        tranygrp = tranc.groupby("States")[["Transaction_count"]].sum().reset_index()
        fig_india2 = px.choropleth(tranygrp, 
                                geojson=data, 
                                locations="States", 
                                featureidkey="properties.ST_NM",
                                color= "Transaction_count",
                                color_continuous_scale="Rainbow",
                                range_color=(tranygrp["Transaction_count"].min(), tranygrp["Transaction_count"].max()),
                                hover_name="States", 
                                title=f"{tranc["Year"].min()} YEAR {Quarter} QUARTER TRANSACTION COUNT", 
                                height=500, 
                                width=450)
        fig_india2.update_geos(fitbounds="locations")
        fig_india2.update_geos(visible=False)
        st.plotly_chart(fig_india2)


    return tranc

#Aggregation Transaction Analysis
def Aggre_tran_taransaction_type(df, States):
    tracs = df[df["States"] == "Westbengal"]
    tracs.reset_index(drop = True, inplace= True)

    tracsg = tracs.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tracsg.reset_index(inplace= True)


    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame=tracsg, names="Transaction_type", values= "Transaction_amount",width = 400,
                        title=f"{States.upper()} TRANSACTION AMOUNT",hole=0.6)

        st.plotly_chart(fig_pie_1)
    
    
    with col2:
        fig_pie_2= px.pie(data_frame=tracsg, names="Transaction_type", values= "Transaction_count",width = 400,
                        title= f"{States.upper()} TRANSACTION COUNT",hole=0.6)

        st.plotly_chart(fig_pie_2)


    return tracs




#Aggregated user Analysis-1
def Agg_user_plot_1(df,year):
    agu_y= df[df["Year"]==2018]
    agu_y.reset_index(drop= True, inplace= True)

    agu_yg= pd.DataFrame(agu_y.groupby("Brands")["Transaction_count"].sum())
    agu_yg.reset_index(inplace=True)

    
    fig_bara_1 = px.bar(agu_yg, x= "Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSCATION COUNT", width= 500, height= 500)
    fig_bara_1.update_traces(marker_color='pink')  # Setting the color of bargraph
    st.plotly_chart(fig_bara_1)

    return agu_y



#Aggregated user Analysis-2
def Agg_user_plot_2(df,Quarter):
    agu_q= df[df["Quarter"]==Quarter]
    agu_q.reset_index(drop= True, inplace= True)

    agu_qg= pd.DataFrame(agu_q.groupby("Brands")["Transaction_count"].sum())
    agu_qg.reset_index(inplace=True)

    fig_bara_2 = px.bar(agu_qg, x= "Brands", y="Transaction_count", title= f"{Quarter} QUARTER BRANDS AND TRANSCATION COUNT", width= 500, height= 500)
    fig_bara_2.update_traces(marker_color='yellow')  # Setting the color of bargraph
    st.plotly_chart(fig_bara_2)

    return agu_q

#Aggregated user Analysis-3
def  Agg_user_plot_3(df,States):
    agu_s= df[df["States"]== States]
    agu_s.reset_index(drop= True, inplace= True)

    fig_line1=px.line(agu_s, x= "Brands", y= "Transaction_count", hover_data= "percentage",title= F"{States} BRANDS,TRANSACTION COUNT,PERCENTAGE",width=500, markers=True)
    st.plotly_chart(fig_line1)

    return agu_s

#Map insurance
def map_insur_districs(df, States):
    tracs = df[df["States"] == States]
    tracs.reset_index(drop = True, inplace= True)

    tracsg = tracs.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tracsg.reset_index(inplace= True)
    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tracsg, x= "Transaction_count", y= "Districts", orientation= "h", title= f"{States.upper()} DISTRICTS AND TRANSACTION COUNT")
        fig_bar_1.update_traces(marker_color='yellowgreen')  # Setting the color of bargraph
        st.plotly_chart(fig_bar_1)
    
    with col2:
        fig_bar_2= px.bar(tracsg, x= "Transaction_amount", y= "Districts", orientation= "h", title= f"{States.upper()} DISTRICTS AND TRANSACTION AMOUNT")
        st.plotly_chart(fig_bar_2)

        return tracs
    

#map_user Analysis-1
def map_user_plot1(df,Year):
    mapu_y= df[df["Year"] == Year]
    mapu_y.reset_index(drop= True, inplace= True)

    mapu_yg= mapu_y.groupby("States")[["registeredUsers","AppOpens"]].sum()
    mapu_yg.reset_index(inplace=True)

    fig_line1=px.line(mapu_y, x= "States", y= ["registeredUsers", "AppOpens"],title= f"{Year} REGISTEREDUSER AND APPOPENS",width=1000, height=800,markers=True)
    st.plotly_chart(fig_line1)

    return mapu_y



#map_user Analysis-2
def map_user_plot2(df,Quarter):
    mapu_q= df[df["Quarter"] == Quarter]
    mapu_q.reset_index(drop= True, inplace= True)

    mapu_qg= mapu_q.groupby("States")[["registeredUsers","AppOpens"]].sum()
    mapu_qg.reset_index(inplace=True)

    fig_line2=px.line(mapu_q, x= "States", y= ["registeredUsers", "AppOpens"],
                      title= f"{df["Year"].min()}  {Quarter} QUARTER REGISTEREDUSER AND APPOPENS",width=1000, height=800,markers=True)
    fig_line2.update_traces(marker_color='green')  

    st.plotly_chart(fig_line2)

    return mapu_q



#map_user_analysis-3
def map_user_plot3(df,States):
    mapu_s= df[df["States"]== States]
    mapu_s.reset_index(drop= True, inplace= True)
    print(mapu_s)

    fig_map_user_bar_1= px.bar(mapu_s, x= "registeredUsers", y= "Districts", orientation= "h",title=f"{States.upper()} REGISTERED USER",height= 500)
    fig_map_user_bar_1.update_traces(marker_color='turquoise')  
    st.plotly_chart(fig_map_user_bar_1)
    
    fig_map_user_bar_2= px.bar(mapu_s, x= "AppOpens", y= "Districts", orientation= "h",title=f"{States.upper()} APPOPENS",height= 500)
    fig_map_user_bar_2.update_traces(marker_color='violet')  
    st.plotly_chart(fig_map_user_bar_2)

    return mapu_s


#top insurance Analysis plot_1
def Top_insurance_plot_1(df,States):
    top_s= df[df["States"]==States]
    top_s.reset_index(drop= True, inplace= True)
    col1,col2 = st.columns(2)

    with col1:
        fig_top_user_bar_1= px.bar(top_s, x= "Quarter", y= "Transaction_amount", hover_data= "pincodes", title= "TRANSACTIONAMOUNT PINCODES",height= 800)
        fig_top_user_bar_1.update_traces(marker_color='turquoise')  # Setting the color of bargraph

        st.plotly_chart(fig_top_user_bar_1)

    with col2:
        fig_top_user_bar_2= px.bar(top_s, x= "Quarter", y= "Transaction_count", hover_data= "pincodes", title= "TRANSACTIONACOUNT PINCODES",height= 800)
        fig_top_user_bar_2.update_traces(marker_color='whitesmoke')  # Setting the color of bargraph

        st.plotly_chart(fig_top_user_bar_2)

#top_user Analysis-1
def top_user_plot_1(df,Year):
    topu_y= df[df["Year"]==2018]
    topu_y.reset_index(drop= True, inplace= True)

    topu_yg= pd.DataFrame(topu_y.groupby(["States","Quarter"])["registeredUsers"].sum())
    topu_yg.reset_index(inplace=True)

    fig_top_plot_1= px.bar(topu_yg, x= "States", y= "registeredUsers", title= f"{Year} REGISTERED USERS", width= 1000, height= 800)
    fig_top_plot_1.update_traces(marker_color= 'yellowgreen')
    st.plotly_chart(fig_top_plot_1)

    return topu_y

#top-user_analysis-2
def top_user_plot_2(df, States):
    tuys = df[df["States"]== States]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "registeredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER", width= 100, height= 100, 
                        color="registeredUsers", hover_data= "pincodes" )

    fig_top_plot_2.update_traces(marker_color= 'green')
    st.plotly_chart(fig_top_plot_2)

    return tuys

#sql connection
def top_chart_Transaction_mount(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CHARY@sri#",
        database="phonepe",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    query1= f'''select States, sum(Transaction_amount) as transaction_amount 
                from {table_name}
                group by States
                order by transaction_amount desc
                limit 10;'''

    mycursor.execute(query1)
    table= mycursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table, columns=("States","Transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 TRANSACTION AMOUNT OF DECENDING", height= 600, width= 600)
        fig_amount.update_traces(marker_color='yellow')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)


    #plot_2
    query2= f'''select States, sum(Transaction_amount) as transaction_amount 
                from {table_name}
                group by States
                order by transaction_amount 
                limit 10;'''

    mycursor.execute(query2)
    table= mycursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table, columns=("States","Transaction_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 TRANSACTION AMOUNT OF ACENDING", height= 600, width= 600)
        fig_amount_2.update_traces(marker_color='turquoise')  # Setting the color of bargraph
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select States, avg(Transaction_amount) as transaction_amount 
                from {table_name}
                group by States
                order by transaction_amount;
                '''

    mycursor.execute(query3)
    table= mycursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("States","Transaction_amount"))

    fig_amount_3 = px.bar(df_3, y="States", x="Transaction_amount", title="AVEARGE OF TRANSACTION AMOUNT", hover_name= "States", orientation= "h", height= 800, width= 700)
    fig_amount_3.update_traces(marker_color='green')  # Setting the color of bargraph
    st.plotly_chart(fig_amount_3)

    #sql connection
def top_chart_Transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CHARY@sri#",
        database="phonepe",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    query1= f'''select States, sum(Transaction_count) as transaction_amount 
                from {table_name}
                group by States
                order by transaction_amount desc
                limit 10;'''

    mycursor.execute(query1)
    table= mycursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table, columns=("States","Transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="States", y="Transaction_count", title="TOP 10 TRANSACTION COUNT OF DECENDIN", height= 600, width= 600)
        fig_amount.update_traces(marker_color='orange')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)


    #plot_2
    query2= f'''select States, sum(Transaction_count) as transaction_count 
                from {table_name}
                group by States
                order by transaction_count
                limit 10;'''

    mycursor.execute(query2)
    table= mycursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table, columns=("States","Transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States", y="Transaction_count", title="LAST 10 TRANSACTION COUNT OF ACENDING", height= 600, width= 600)
        fig_amount_2.update_traces(marker_color='violet')  # Setting the color of bargraph
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select States, avg(Transaction_count) as transaction_count 
                from {table_name}
                group by States
                order by transaction_count;
                '''

    mycursor.execute(query3)
    table= mycursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("States","Transaction_count"))

    fig_amount_2 = px.bar(df_3, y="States", x="Transaction_count", title="AVERAGE OF TRANSACTION COUNT ", hover_name= "States", orientation= "h", height= 800, width= 700)
    fig_amount_2.update_traces(marker_color='wheat')  # Setting the color of bargraph
    st.plotly_chart(fig_amount_2)


#sql connection
def top_chart_registeredUser(table_name,State):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CHARY@sri#",
        database="phonepe",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    query1= f'''select Districts, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                where States= '{State}'
                group by Districts
                order by RegisteredUsers desc
                limit 10;'''

    mycursor.execute(query1)
    table= mycursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table, columns=("Districts","RegisteredUsers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="Districts", y="RegisteredUsers", title="TOP CHART REGISTERED USER OF DESC", height= 600, width= 600)
        fig_amount.update_traces(marker_color='orange')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)


    #plot_2
    query2= f'''select Districts, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                where States= '{State}'
                group by Districts
                order by RegisteredUsers 
                limit 10;'''

    mycursor.execute(query2)
    table= mycursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table, columns=("Districts","RegisteredUsers"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="Districts", y="RegisteredUsers", title="LAST CHART OF REGISTEREDUSER ", height= 600, width= 600)
        fig_amount_2.update_traces(marker_color='violet')  # Setting the color of bargraph
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select Districts, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                where States= '{State}'
                group by Districts
                order by RegisteredUsers;'''

    mycursor.execute(query3)
    table= mycursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("Districts","RegisteredUsers"))

    fig_amount_2 = px.bar(df_3, y="Districts", x="RegisteredUsers", title="AVERAGE VALUE OF REGISTEREDUSER", hover_name= "Districts", orientation= "h", height= 800, width= 700)
    fig_amount_2.update_traces(marker_color='wheat')  # Setting the color of bargraph
    st.plotly_chart(fig_amount_2)

    #sql connection
def top_chart_AppOpens(table_name,State):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CHARY@sri#",
        database="phonepe",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    query1= f'''select Districts, sum(AppOpens)as AppOpens
                from {table_name}
                where States= '{State}'
                group by Districts
                order by AppOpens desc
                limit 10;'''

    mycursor.execute(query1)
    table= mycursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table, columns=("Districts","AppOpens"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="Districts", y="AppOpens", title="TOP CHART REGISTERED USER OF DESC", height= 600, width= 600)
        fig_amount.update_traces(marker_color='orange')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)


    #plot_2
    query2= f'''select Districts, sum(AppOpens)as AppOpens
                from {table_name}
                where States= '{State}'
                group by Districts
                order by AppOpens 
                limit 10;'''

    mycursor.execute(query2)
    table= mycursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table, columns=("Districts","AppOpens"))
    
    with col2:
        fig_amount_2 = px.bar(df_2, x="Districts", y="AppOpens", title="LAST CHART OF REGISTEREDUSER ", height= 500, width= 450)
        fig_amount_2.update_traces(marker_color='violet')  # Setting the color of bargraph
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select Districts, sum(AppOpens)as AppOpens
                from {table_name}
                where States= '{State}'
                group by Districts
                order by AppOpens;'''

    mycursor.execute(query3)
    table= mycursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("Districts","AppOpens"))

    fig_amount_2 = px.bar(df_3, y="Districts", x="AppOpens", title="AVERAGE VALUE OF REGISTEREDUSER", hover_name= "Districts", orientation= "h", height= 500, width= 450)
    fig_amount_2.update_traces(marker_color='wheat')  # Setting the color of bargraph
    st.plotly_chart(fig_amount_2)


#sql connection
def top_chart_registeredUsers(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CHARY@sri#",
        database="phonepe",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    #plot_1
    query1= f'''select States, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                group by States
                order by RegisteredUsers desc
                limit 10;'''

    mycursor.execute(query1)
    table= mycursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table, columns=("States","RegisteredUsers"))
    col1,col2=st.columns(2)
    with col1:

        fig_amount = px.bar(df_1, x="States", y="RegisteredUsers", title="TOP CHART REGISTERED USER OF DESC", height= 500, width= 450)
        fig_amount.update_traces(marker_color='orange')  # Setting the color of bargraph
        st.plotly_chart(fig_amount)


    #plot_2
    query2= f'''select States, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                group by States
                order by RegisteredUsers 
                limit 10;'''

    mycursor.execute(query2)
    table= mycursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table, columns=("States","RegisteredUsers"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States", y="RegisteredUsers", title="LAST CHART OF REGISTEREDUSER ", height= 500, width= 450)
        fig_amount_2.update_traces(marker_color='violet')  # Setting the color of bargraph
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select States, sum(RegisteredUsers)as RegisteredUsers
                from {table_name}
                group by States
                order by RegisteredUsers ;'''
    mycursor.execute(query3)
    table= mycursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("States","RegisteredUsers"))

    fig_amount_2 = px.bar(df_3, y="States", x="RegisteredUsers", title="AVERAGE VALUE OF REGISTEREDUSER", hover_name= "States", orientation= "h", height= 800, width= 700)
    fig_amount_2.update_traces(marker_color='wheat')  # Setting the color of bargraph
    st.plotly_chart(fig_amount_2)


#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

select = option_menu(menu_title = None,options = ["About","Home", "Dataexploration", "Top Charts"], default_index=0, orientation = "horizontal")

if select == "About":

    col1,col2=st.columns(2)
    
    with col1:
         st.header(":blue[PHONEPE]")
         st.subheader("INDIA'S BEST TRANSACTION APP")
         st.markdown("phonepe is an Indian digital payments and financial technology company")
         st.write(":red[****FEATURES****]")
         st.write("****Credit and Debit Card Linking****")
         st.write("****Bank Balance Check****")
         st.write("****Money Storage****")
         st.write("****Pin Authorization****")
         st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    with col2:
         st.image(Image.open(r"c:\Users\admin\Downloads\download.jfif"),width=400)

elif select == "Home":

    col3,col4=st.columns(2)

    with col3:
         st.image(r"c:\Users\admin\Downloads\download (1).jfif")  

    with col4:
         st.write("****Easy Transactions****") 
         st.write("****One App For All Your Payments****")
         st.write("****Your Bank Acount is All You Need****")
         st.write("****Multiple Payments Mode****")
         st.write("****Phonepe Merchants****")
         st.write("****Multiple Ways To Pay****")
         st.write("****Direct Transfor And More****")
         st.write("****QR Code****")     
         st.write("****Earn Great Rewards****")

    col5,col6=st.columns(2)

    with col5:
         st.write("****No Wallet Top-Up Required****")
         st.write("****Pay Directly From Any Bank To Any Bank A/C****")
         st.write("****Insatantly and Free****")

    with col6:
         st.image(Image.open(r"c:\Users\admin\Downloads\images.jfif"),width=380)

elif select == "Dataexploration":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2=st.columns(2)
            with col1:

                Year = st.slider("Select the Year", min_value=int(Agg_insurance["Year"].min()), max_value=int(Agg_insurance["Year"].max()), value=int(Agg_insurance["Year"].min()))
            agg_insu_tranac_Y= Transaction_amount_count_Y(Agg_insurance, Year)

            col1,col2 = st.columns(2)
            with col1:

                    Quarters = st.slider("Select the quarter", min_value=int(agg_insu_tranac_Y["Quarter"].min()), max_value=int(agg_insu_tranac_Y["Quarter"].max()), value=int(agg_insu_tranac_Y["Quarter"].min()))
            agg_insu_tranac_Y_Q=Transaction_amount_count_Y_Q(agg_insu_tranac_Y, Quarters)
        
        
        elif method == "Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                
                Year = st.selectbox("Slect the Year",Agg_transaction["Year"].unique())
            agg_tran_tranac_Y= Transaction_amount_count_Y(Agg_transaction, Year)


            
            col1,col2 = st.columns(2)
            with col1:

                    Quarter = st.selectbox("Slect the Quarter",agg_tran_tranac_Y["Quarter"].unique())
            agg_tran_tranac_Y_S_Q= Transaction_amount_count_Y_Q(agg_tran_tranac_Y, Quarter)


            col1,col2=st.columns(2)
            with col1:
                
                    States = st.selectbox("Slect the State",agg_tran_tranac_Y["States"].unique())
            agg_tran_tranac_Y_S= Aggre_tran_taransaction_type(agg_tran_tranac_Y, States)




        elif method == "User Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                Year = st.slider("Select the Year", min_value=int(Agg_user["Year"].min()), max_value=int(Agg_user["Year"].max()), value=int(Agg_user["Year"].min()))
            Agg_user_Y= Agg_user_plot_1(Agg_user, Year)


            with col2:
                Quarter = st.slider("Select the Quarter", min_value=int(Agg_user_Y["Quarter"].min()), max_value=int(Agg_user_Y["Quarter"].max()), value=int(Agg_user_Y["Quarter"].min()))
            Agg_user_q= Agg_user_plot_2(Agg_user_Y, Quarter)

            
            col1,col2=st.columns(2)
            with col1:
                States= st.selectbox("Select the States", Agg_user_q["States"].unique())
            Agg_user_q= Agg_user_plot_3(Agg_user_q, States)



    with tab2:

        method_2 = st.radio("Select The Method",["Map Insurance","Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            col1,col2=st.columns(2)
            with col1:
                
                Year = st.slider("Select the Year", min_value=int(Map_insur["Year"].min()), max_value=int(Map_insur["Year"].max()), value=int(Map_insur["Year"].min()))
            map_insur_tac_Y= Transaction_amount_count_Y(Map_insur, Year)



            col1,col2=st.columns(2)
            with col1:
                    
                States= st.selectbox("Select the States", map_insur_tac_Y["States"].unique())
            map_insur_districs(map_insur_tac_Y, States)

            col1,col2 = st.columns(2)
            with col1:

                    Quarter = st.selectbox("Slect the Quarter",map_insur_tac_Y["Quarter"].unique())
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, Quarter)

            col1,col2=st.columns(2)
            with col1:
                
                    States = st.selectbox("Slect the State",map_insur_tac_Y_Q["States"].unique())
            map_insur_districs(map_insur_tac_Y_Q, States)



        elif method_2 == "Map Transaction":

            col1,col2=st.columns(2)
            with col1:
                
                Year = st.slider("Select the Year", min_value=int(Map_Trans["Year"].min()), max_value=int(Map_Trans["Year"].max()), value=int(Map_Trans["Year"].min()))
            map_trans_tac_Y= Transaction_amount_count_Y(Map_Trans, Year)



            col1,col2=st.columns(2)
            with col1:
                    
                States= st.selectbox("Select the States", map_trans_tac_Y["States"].unique())
            map_insur_districs(map_trans_tac_Y, States)

            col1,col2 = st.columns(2)
            with col1:

                    Quarter = st.selectbox("Slect the Quarter",map_trans_tac_Y["Quarter"].unique())
            map_trans_tac_Y_Q= Transaction_amount_count_Y_Q(map_trans_tac_Y, Quarter)

            col1,col2=st.columns(2)
            with col1:
                
                    States = st.selectbox("Slect the State",map_trans_tac_Y_Q["States"].unique())
            map_insur_districs(map_trans_tac_Y_Q, States)

            
        elif method_2 == "Map User":
            
            col1,col2 = st.columns(2)
            with col1:
            
                    Year = st.slider("Select the Year", min_value=int(Map_users["Year"].min()), max_value=int(Map_users["Year"].max()), value=int(Map_users["Year"].min()))
            map_usr_Y= map_user_plot1(Map_users, Year)

            col1,col2 = st.columns(2)
            with col1:
            
                    Quarter = st.slider("Select the Quarter", min_value=int(map_usr_Y["Quarter"].min()), max_value=int(map_usr_Y["Quarter"].max()), value=int(map_usr_Y["Quarter"].min()))
            map_usr_Y_Q= map_user_plot2(map_usr_Y, Quarter)


            
            States = st.selectbox("Select the Stateru",map_usr_Y_Q["States"].unique())
            map_user_plot3(map_usr_Y_Q, States)

            
                
                    
            


    with tab3:
        
        method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction", "Top User"])
        
        if method_3 == "Top Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                
                Year = st.slider("Select the YearTi", min_value=int(Top_insur["Year"].min()), max_value=int(Top_insur["Year"].max()), value=int(Top_insur["Year"].min()))
            top_insur_tac_Y= Transaction_amount_count_Y(Top_insur, Year)


            col1,col2=st.columns(2)
            with col1:
                
                    States = st.selectbox("Select the StateTi",top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_Y, States)



            col1,col2 = st.columns(2)
            with col1:
            
                    Quarter = st.slider("Select the Quarter", min_value=int(top_insur_tac_Y["Quarter"].min()), max_value=int(top_insur_tac_Y["Quarter"].max()), value=int(top_insur_tac_Y["Quarter"].min()))
            Top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, Quarter)



        elif method_3 == "Top Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                
                Year = st.slider("Select the YearTi", min_value=int(Top_trans["Year"].min()), max_value=int(Top_trans["Year"].max()), value=int(Top_trans["Year"].min()))
            top_trans_tac_Y= Transaction_amount_count_Y(Top_trans, Year)


            col1,col2=st.columns(2)
            with col1:
                
                    States = st.selectbox("Select the State",top_trans_tac_Y["States"].unique())
            Top_insurance_plot_1(top_trans_tac_Y, States)



            col1,col2 = st.columns(2)
            with col1:
            
                    Quarter = st.slider("Select the Quarter", min_value=int(top_trans_tac_Y["Quarter"].min()), max_value=int(top_trans_tac_Y["Quarter"].max()), value=int(top_trans_tac_Y["Quarter"].min()))
            Top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_trans_tac_Y, Quarter)


        elif method_3 == "Top user":
            
            col1,col2=st.columns(2)
            with col1:
                
                Year = st.slider("Select the YearTu", min_value=int(Top_users["Year"].min()), max_value=int(Top_users["Year"].max()), value=int(Top_users["Year"].min()))
            top_user_y= top_user_plot_1(Top_users, Year)

            col1,col2=st.columns(2)
            with col1:
                States= st.selectbox("Select the States", top_user_y["States"].unique())
            top_user_s= top_user_plot_2(top_user_y, States)



elif select == "Top Charts":
    
    quation= st.selectbox("Select the Quation",["1. Transaction Amount and Count of Aggregated insurance",
                                                "2.Transaction Amount and Count of Map Agg_insurance",
                                                "3. Transaction Amount and Count of Top insurance",
                                                "4.Transaction Amount and Count of Aggragated Transaction", 
                                                "5.Transaction Amount and Count of Map Transaction",
                                                "6.Transaction Amount and count of Top Transaction",
                                                "7.Transaction Count of Aggregated User",
                                                "8. registered users of Map User",
                                                "9. App opens of Map User",
                                                "10. Registered users of Top User"])
   
   
    if quation == "1. Transaction Amount and Count of Aggregated insurance":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("aggregated_insurance")


    elif quation == "2.Transaction Amount and Count of Map Agg_insurance":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("map_insurance")


    
    elif quation == "3. Transaction Amount and Count of Top insurance":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("top_insurance")


        

    elif quation == "4.Transaction Amount and Count of Aggragated Transaction":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("aggregated_transaction")




    elif quation == "5.Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("map_transaction")



    elif quation == "6.Transaction Amount and count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT") 
        top_chart_Transaction_mount("top_transactions")

        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("top_transactions")


    elif quation == "7.Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_Transaction_count("aggregated_users")


    elif quation == "8. registered users of Map User":
        states= st.selectbox("select the states",Map_users["States"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registeredUser("map_users", states)


    elif quation == "9. App opens of Map User":
        states= st.selectbox("select the states",Map_users["States"].unique())
        st.subheader("APPOPENS")
        top_chart_registeredUser("map_users", states)


    elif quation == "10. Registered users of Top User":
        st.subheader("REGISTERED USERS")
        top_chart_registeredUsers("top_users")
