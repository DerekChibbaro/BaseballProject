##pip install streamlit
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.title("Mini Project: MLB Shift Rule Analysis")

st.write("Type the range of dates for analysis")

##pip install pybaseball


from pybaseball import statcast
start_date = st.text_input("Start Date (YYYY-MM-DD):", value="2024-09-21")
end_date = st.text_input("End Date (YYYY-MM-DD):", value="2024-09-22")


data = statcast(start_dt=start_date, end_dt=end_date)

# Specify desired columns and remove events that did not result in balls put in play
new_data = data[["game_date", "home_team", "hit_location", "events"]][(data["events"]!="strikeout") & (data["hit_location"]!="<NA>")]
new_data["game_date"] = new_data["game_date"].dt.date
# Convert the date column to strings
new_data["game_date"] = new_data["game_date"].astype(str)
st.write("Snapshot of data frame")
st.write(new_data.head(100))

# Add a dropdown for selecting the home field
home_team_selected = st.selectbox("Select Home Team:", new_data["home_team"].unique())

# Filter data based on the selected home team
filtered_data = new_data[new_data["home_team"] == home_team_selected]

# Add a dropdown for selecting the hit location
hit_location_selected = st.selectbox("Select Hit Location:", sorted(filtered_data["hit_location"].unique(),key=int))

# Filter data based on the selected hit location
final_data = filtered_data[filtered_data["hit_location"] == hit_location_selected]


################################################################################
# Add a slider for selecting the date
#selected_date = st.slider("Select Date", min_value=new_data["game_date"].min().strftime("%Y-%m-%d"), max_value=new_data["game_date"].max().strftime("%Y-%m-%d"))

# Filter data based on the selected date
#filtered_data = new_data[new_data["game_date"].dt.strftime("%Y-%m-%d") == selected_date]
################################################################################


# Set the title
st.title("Number of Hits at home field by Game Date("+home_team_selected+")")
# Create a bar chart for counts of hits at certain positions over time
st.bar_chart(final_data["game_date"].value_counts())



total_hits_second_base = new_data[new_data["hit_location"] == 4]["hit_location"].count()

total_hits_first_base = new_data[new_data["hit_location"] == 3]["hit_location"].count()

total_hits_third_base = new_data[new_data["hit_location"] == 5]["hit_location"].count()

total_hits_shortstop = new_data[new_data["hit_location"] == 6]["hit_location"].count()

allhitscounts = pd.DataFrame({
    "hit_location": [3, 4, 5, 6],
    "hit_count": [total_hits_first_base, total_hits_second_base, total_hits_third_base, total_hits_shortstop]
})
st.write("Counts for Infield Positions")
allhitscounts

count_hits = new_data[new_data["hit_location"].isin([3, 4, 5, 6])].value_counts()

total_infield_hits = count_hits.sum()

# Calculate percentages
percentage_to_second_base = (total_hits_second_base / total_infield_hits) * 100
percentage_to_first_base = (total_hits_first_base / total_infield_hits) * 100
percentage_to_third_base = (total_hits_third_base / total_infield_hits) * 100
percentage_to_shortstop = (total_hits_shortstop / total_infield_hits) * 100

totalLeftside = total_hits_third_base + total_hits_shortstop
percentage_Leftside = (totalLeftside / total_infield_hits) * 100

totalRightside = total_hits_second_base + total_hits_first_base
percentage_Rightside = (totalRightside / total_infield_hits) * 100







# IMAGE of Baseball field
# Load the baseball field image
#image_url = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTTWrLmP_Aadig6XdnRHmNAE3xq07nbVy1w3yOuNSRwL1nQzEux"
#st.image(image_url, use_column_width=True)


# HEAT MAP
# Create a colormap
cmap = plt.cm.YlOrRd  # You can choose a different colormap (e.g., 'coolwarm')

# Create a heatmap
# Create a heatmap
#fig = plt.figure()

# Create Plotly figure
fig = go.Figure(data=[go.Bar(x=allhitscounts["hit_location"], y=allhitscounts["hit_count"],
                             marker_color='rgb(158,202,243)',
                             text=allhitscounts["hit_count"])])

# Customize the figure
fig.update_layout(
    title='Hit Counts by Position('+start_date+" through "+end_date+")",
    xaxis=dict(title='Hit Location', tickmode='array', tickvals=[3, 4, 5, 6], ticktext=["First Base (3)", "Second Base (4)", "Third Base (5)", "Shortstop (6)"]),
    yaxis=dict(title='Hit Count')
)



# Display the figure in Streamlit
st.plotly_chart(fig)

st.header("Total hits breakdown")
st.write("Total hits for given range of dates:", total_infield_hits)
st.write("Total hits to the Left side of field:", totalLeftside)
st.write("Total hits to the Right side of field:", totalRightside)

st.header("Percentages")
st.write("Percentage of batted balls to second base:", round(percentage_to_second_base,2))
st.write("Percentage of batted balls to first base:", round(percentage_to_first_base,2))
st.write("Percentage of batted balls to third base:", round(percentage_to_third_base,2))
st.write("Percentage of batted balls to shortstop:", round(percentage_to_shortstop,2))
st.write("Percentage of batted balls to Right side of field:", round(percentage_Rightside,2))
st.write("Percentage of batted balls to Left side of field:", round(percentage_Leftside,2))



st.write("Based on numerous analyses with different years before and after the new rule change, there is no preliminary difference in the location of where a batted ball was hit in the infield. The approximate percentages for balls hit to second base, first base, third base, and shortstop are 27%, 17%, 25%, and 29% respectively.")


#ax = fig.gca()
#ax.pcolor(count_hits, vmin=0, vmax=count_hits.max(), cmap=cmap)

# Set labels and title for the heatmap
#ax.set_xticks(range(len(count_hits)))
#ax.set_yticks([0])
#ax.set_xticklabels(count_hits.index, rotation=0, ha="center")
#ax.set_yticklabels([])
#ax.set_title("Heatmap of Hit Locations")




### This is a more complicated way I think!
#def interactive_plot(df):
    #x_values = st.selectbox("Select home team", options = df["home_team"].unique())
    #y_values = st.selectbox("Select hit location", options = df["hit_location"].unique())
    #sns.catplot(df, x = df[["home_team"]["x_values"]], y = df[["home_team"]["y_values"]])
#interactive_plot(new_data)
# st.bar_chart(data,x="home_team",y="hit_location")
