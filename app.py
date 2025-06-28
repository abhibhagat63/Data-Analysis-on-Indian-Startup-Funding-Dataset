import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide",page_title="Startup Analysis")
# streamlit run app.py
df = pd.read_csv("D:\DS\Data Science\CampusX\python\Data Analysis on Indian Startup Funding Dataset\startup_clean.csv")
# df["date"].dt.month_name()


def load_overall_analysis():
    st.title("Overall Analysis")
    #total invested
    total_inv = round(df["amount"].sum())
    # Max amount infused in startup
    max_inv = df.groupby("startup")["amount"].sum().sort_values(ascending=False).head(1)
    #average ticket size
    avg_inv = round(df.groupby("startup")["amount"].sum().mean())
    #total Funded Startups
    total_sart = df["startup"].nunique()

    col1, col2,col3, col4= st.columns(4)
     
    with col2:
        st.metric("Maximum investment", str(max_inv.values[0]) + " Cr")
    with col1:
        st.metric("Total",str(total_inv) +" Cr")
    with col3 :
        st.metric("Average",avg_inv)
    with col4:
        st.metric("Funded Startups",total_sart)

    col1 , col2 = st.columns(2)
    #MOM investment analysis
    with col1:
        st.subheader("MOM invetment analysis")
        mom = df.groupby(["year_inv"])["amount"].sum()
        fig2 = px.line(mom, x = mom.index,y = mom.values,hover_name=mom.index)
        minor = fig2.update_yaxes(minor=dict(ticks="outside", ticklen=4, tickcolor="white"))
        st.plotly_chart(fig2,use_container_width = True)

    #sector analysis Pie 
    with col2:
        st.subheader("City wise Analysis")
        sec_anal = df.groupby("city")["amount"].sum().sort_values(ascending = False).head(12)
        fig1 = px.bar(sec_anal, x = sec_anal.index,y = sec_anal.values,hover_name=sec_anal.index)
        minor = fig1.update_yaxes(minor=dict(ticks="outside", ticklen=4, tickcolor="white"))
        st.plotly_chart(fig1,use_container_width = True)
        
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Equity Based Analysis")
        sec_anal = df.groupby("subvertical")["amount"].sum().sort_values(ascending = False).head(10)
        sec = plt.pie(sec_anal,labels = sec_anal.index,autopct = "%0.1f%%")
        fig2 , ax2 = plt.subplots()
        ax2.pie(sec_anal.values,autopct="%0.1f%%",labels=sec_anal.index)
        st.pyplot(fig2)
    
    with col4 :
        st.subheader("Sector Analysis")
        sec_anal = df.groupby("vertical")["amount"].sum().sort_values(ascending = False).head(10)
        sec = plt.pie(sec_anal,labels = sec_anal.index,autopct = "%0.1f%%")
        fig2 , ax2 = plt.subplots()
        ax2.pie(sec_anal.values,autopct="%0.1f%%",labels=sec_anal.index)
        st.pyplot(fig2)
    
    top_inv = df.groupby("investors")["amount"].sum().sort_values(ascending=False).head(10)
    st.subheader("Top investors")
    top_inv = st.dataframe(top_inv)
    
st.title("Startups")
def load_startups(startup):

    col1, col2,col3, col4= st.columns(4)

    total = df[df["startup"].str.contains(startup,case=True)]["amount"].sum().item()

    with col1:
        st.metric("Total Investment", str(total) + " Cr")

    inv = df[df["startup"].str.contains(startup,case=True)][["investors","vertical","subvertical","city"]]
    # inv_1 = inv.loc["Ola"/
    st.dataframe(inv)

    

#Fronted 
st.sidebar.title("Startup Funding Analysis")
option =st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

def load_investor_details(investor):
    st.title("Investors")
    # load the recent 5 investment of investor
    last_5df = df[df["investors"].str.contains(investor,case = True)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Most recent Investment")
    st.dataframe(last_5df)


    #Biggest investment
    try :
        col1,col2 = st.columns(2)
        with col1:
            big_5 = df[df["investors"].str.contains(investor,case=False)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
            st.subheader("Biggest Investment")
            # st.dataframe(big_5)
            fig1 = px.bar(big_5, x = big_5.index,y = big_5.values,hover_name=big_5.index)
            minor = fig1.update_yaxes(minor=dict(ticks="outside", ticklen=4, tickcolor="white"))
            st.plotly_chart(fig1,use_container_width = True)

        with col2:
            st.subheader("Year over year investment")
            yoy = df[df["investors"].str.contains(investor)].groupby("year_inv")["amount"].sum()
            # st.dataframe(yoy)
            fig2 = px.line(yoy, x=yoy.index, y=yoy.values)
            minor = fig2.update_yaxes(minor=dict(ticks="outside", ticklen=4, tickcolor="white"))
            st.plotly_chart(fig2,use_container_width = True)
            

        col3,col4 = st.columns(2)
        with col3 :
            st.subheader("Round")
            big_5stage = df[df["investors"].str.contains(investor, case=False)].groupby("round")["amount"].sum().sort_values(ascending=False).head(10)
            fig3 , ax3 = plt.subplots()
            ax3.pie(big_5stage.values,autopct="%0.1f%%",labels=big_5stage.index)
            st.pyplot(fig3)

        with col4 :
            st.subheader("Invested in Cities")
            big_5city = df[df["investors"].str.contains(investor, case=False)].groupby("city")["amount"].sum().sort_values(ascending=False).head(10)
            fig4 , ax4 = plt.subplots()
            ax4.pie(big_5city.values,autopct="%0.1f%%",labels=big_5city.index)
            st.pyplot(fig4)

        col5, col6 = st.columns(2)

        with col5:
            st.subheader("Sector invested in")
            big_5ser = df[df["investors"].str.contains(investor, case=False)].groupby("vertical")["amount"].sum().sort_values(ascending=False).head(10)
            fig2 , ax2 = plt.subplots()
            ax2.pie(big_5ser.values,autopct="%0.1f%%",labels=big_5ser.index)
            st.pyplot(fig2)
    except Exception as e:
        st.write(e)
        


if option == "Overall Analysis":
    btn0 = st.sidebar.button("Show Overall Analysis")
    if btn0:
        load_overall_analysis()
elif option == "Startup":
    selected_startups=st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar .button("Find Startup Details")
    if btn1:
        load_startups(selected_startups)
else:
    selected_investor = st.sidebar.selectbox("Select Investor",sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor  Details")
    if btn2:
        load_investor_details(selected_investor)
