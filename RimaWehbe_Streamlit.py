import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import chart_studio.plotly as py
from plotly.subplots import make_subplots
from PIL import Image 

# DATA AND PLOTS
df = pd.read_csv("https://raw.githubusercontent.com/rima-w/StreamlitAssignment/main/vgsales.csv", index_col =[0])
# print(df.head(3))

# Data Cleaning
df = df.dropna()
df['Year'] = df['Year'].astype(int)
df["Total_Sales"] = df["NA_Sales"] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales'] + df['Global_Sales']
df["Total_Sales"] = df["Total_Sales"].round(2)

# Graph 1
df_year_totalsales = df[["Year", "Total_Sales"]]
df_totalgrouped = df_year_totalsales.groupby('Year', as_index = False).sum()
# df_totalgrouped

fig1 = px.scatter(df_totalgrouped, x="Year", y="Total_Sales",  size='Total_Sales', hover_data=["Total_Sales"], title = "Total Video Game Sales Over the Years(1980-2016)", labels = {"Total_Sales":"Sales in Millions($)"})
# fig.show()


# Graph 2

df_activision = df[df["Publisher"]== "Activision"]
df_ea = df[df["Publisher"]== "Electronic Arts"]

df_year_sales = df_activision[["Year", "NA_Sales", "EU_Sales", "Global_Sales"]]
df_year_sales2 = df_ea[["Year", "NA_Sales", "EU_Sales", "Global_Sales"]]
df_grouped = df_year_sales.groupby('Year', as_index = False).sum()
df_grouped2 = df_year_sales2.groupby('Year', as_index = False).sum()

fig2 = make_subplots(rows=1, cols=3) #subplot_titles=()

fig2.add_trace(
    go.Scatter(x=df_grouped["Year"], y= df_grouped["NA_Sales"], marker=dict(color="purple", size=5), name = "Activision North America"),
    row=1, col=1)

fig2.add_trace(
    go.Scatter(x=df_grouped["Year"], y= df_grouped["EU_Sales"], marker=dict(color="blue", size=5), name = "Activision Europe"),
    row=1, col=2)

fig2.add_trace(
    go.Scatter(x=df_grouped["Year"], y= df_grouped["Global_Sales"], marker=dict(color="orange", size=5), name = "Activision Global"),
    row=1, col=3)

fig2.add_trace(
    go.Scatter(x=df_grouped2["Year"], y= df_grouped["NA_Sales"], marker=dict(color="pink", size=5), name = "EA North America"),
    row=1, col=1)

fig2.add_trace(
    go.Scatter(x=df_grouped2["Year"], y=df_grouped["EU_Sales"], marker=dict(color="green", size=5), name = "EA Europe"),
    row=1, col=2)

fig2.add_trace(
    go.Scatter(x=df_grouped2["Year"], y=df_grouped["Global_Sales"], marker=dict(color="yellow", size=5), name = "EA Global"),
    row=1, col=3)

fig2.update_layout(height=500, width=700, title_text="Activision vs. EA Sales in Millions ($) Over the Years in North America, Europe, and Globally")
#fig2.show()


# Graph 3
df_platform = df[["Total_Sales", "Platform"]]
df_grouped_platform = df_platform.groupby('Platform', as_index = False).sum()

for i, row in enumerate(df_grouped_platform["Total_Sales"]):
  if df_grouped_platform["Total_Sales"][i] < 1500:
    df_grouped_platform["Platform"][i] = "Other"

df_grouped_platform = df_grouped_platform.groupby('Platform', as_index = False).sum()

fig3 = px.pie(df_grouped_platform,values = "Total_Sales", names = "Platform")
fig3.update_layout(height=500, width=1500, title_text="Platforms Total Sales' Share of the Market")
fig3.update_layout(
    font=dict(
        size=20)
)
#fig3.show()

# GRAPH 4

df_sorted = df.sort_values(by=["Year"])

fig4 = px.histogram(df_sorted, x="Genre", y="Total_Sales", animation_frame="Year", animation_group= "Total_Sales", hover_name="Genre", color = "Genre", range_y=[0,150], range_x = [-1,12], labels = {"Genre": "Game Genre", "Total_Sales":"Sales in Millions($)"})
fig4.update_layout(title_text="Change in Total Sales for Every Game Genre Over the Years")
fig3.update_layout(
    font=dict(
        size=20))
#fig4.show()

# GRAPH 5

df_games = df[["Name", "Total_Sales"]]
df_games = df_games.groupby("Name", as_index = False).sum()
df_sorted_games = df_games.sort_values(by=["Total_Sales"])

fig5 = px.histogram(df_sorted_games.tail(10), x ="Name", y = "Total_Sales", color = "Name", labels = {"Name": "Game Name", "Total_Sales":"Sales in Millions($)"})
fig5.update_layout(title_text="Highest Selling Games (Measured in Total Sales) From 1980 till 2016")
fig3.update_layout(
    font=dict(
        size=20))
#fig5.show()

# WEBSITE BUILDING 

st.markdown("# *Analyzing Trends in Video Game Sales*")
st.markdown("#### Explore the Highest Selling Games and the Most Profitable Markets!")

img='https://github.com/rima-w/StreamlitAssignment/blob/main/games.png'
st.image(img,width=1000)


st.markdown("### Video Game Sales Peak in 2008 at an estimated $1.5 Billion, then Drop to Low Levels!")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### A Comparison between the Two Most Active Game Publishers: Activision and Electronic Arts")

img2='https://github.com/rima-w/StreamlitAssignment/blob/main/ea_acti.jpg'
st.image(img2,width=1000)

st.markdown("##### While Activision's Sales were dropping following the Recession in Game Sales observed above, Electronic Arts was gaining market share!" )
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### There are Many Platforms Used for Gaming, Yet, 5 Platforms Own Almost 55% of the Market!")
img3='https://github.com/rima-w/StreamlitAssignment/blob/main/platforms.jpg'
st.image(img3,width=700)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### The Most Popular Game Genre is Observable for Every Year:")
st.markdown("##### PRESS PLAY!")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("### The Highest Selling Game for the years 1980-2016 was Wii Sports!")
st.plotly_chart(fig5, use_container_width=True)

img4='https://github.com/rima-w/StreamlitAssignment/blob/main/wii.jpg'
st.markdown("#### Winner!")
st.image(img4,width=700)


