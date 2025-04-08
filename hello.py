from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px

text("# Electric Vehicle Population Data")
text("This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently registered through Washington State Department of Licensing (DOL).")
text(f"Dataset source: [Data.gov](https://catalog.data.gov/dataset/electric-vehicle-population-data)")

connect() 

df = get_df('sample_csv')

# Do Data Cleaning
df = df.drop_duplicates()
df = df.dropna()

df['Electric Range'] = pd.to_numeric(df['Electric Range'], errors='coerce')

# See Electric car adoption trend
adoption_trend = df.groupby('Model Year').size().reset_index(name='Count')
fig = px.line(adoption_trend, x='Model Year', y='Count', markers=True,
              title='Electric Vehicle Adoption Trend Over Time')
fig.update_traces(textposition='top center', marker=dict(size=12, color='lightblue'))
fig.update_layout(template='plotly_white')
plotly(fig)
text("Electric vehicle adoption remained relatively low from the early 2000s until 2010. Since mid-2010s, adoption started to grow steadily; Around 2020–2023, adoption surged significantly. After reaching a peak in the early 2020s, the trend sharply decline. (possibly due to incomplete data for the later years).")

# See Brand's Popularity
make_counts = df['Make'].value_counts().reset_index()
make_counts.columns = ['Make', 'Count']
fig_popularity = px.bar(make_counts, x='Make', y='Count',
                        title='Vehicle Popularity by Brand',
                        labels={'Make': 'Brand', 'Count': 'Number of Vehicles'})
plotly(fig_popularity)
text("The chart makes it pretty clear that Tesla is leading the pack when it comes to the number of electric vehicles on the road. Brands like Chevrolet, Nissan, Ford, and Kia are following close behind, while most other manufacturers have only a small presence. It gives us a glimpse into how concentrated the electric vehicle space is right now.")


def extract_lat_long(point_str):
    try:
        coords_str = point_str.replace("POINT (", "").replace(")", "")
        coords = coords_str.split(' ')
        if len(coords) == 2:
            return float(coords[1]), float(coords[0])
    except Exception as e:
        return None, None
min_lat, max_lat = 45.5, 49.1
min_lon, max_lon = -124.8, -116.9
df[['Latitude', 'Longitude']] = df['Vehicle Location'].apply(lambda x: pd.Series(extract_lat_long(x)))

df = df[(df['Latitude'] >= min_lat) & (df['Latitude'] <= max_lat) &
                 (df['Longitude'] >= min_lon) & (df['Longitude'] <= max_lon)]

fig_map = px.scatter_mapbox(df,
                            lat='Latitude',
                            lon='Longitude',
                            hover_name='City',
                            hover_data=['County', 'Electric Range'],
                            color='Make',
                            zoom=6,
                            title='Washington State EV Registrations by Brand (You can zoom in the map with your touchpad 🔍)')
fig_map.update_layout(mapbox_style="open-street-map")
plotly(fig_map)




meaningful_df = df[['County', 'City', 'Model Year', 'Make', 'Electric Vehicle Type','Electric Range']]
text("Feel free to sort/filter data within the table below 👇")
table(meaningful_df)

text("#### Author: Lunya Cheng | " + f"[Resume](https://drive.google.com/file/d/1rAzqm3ChNEBJC04W0GOsq5ppqmAFp02Y/view?usp=sharing)" + " | " + f"[Linkedin](https://www.linkedin.com/in/lun-ya-cheng-90953598/)" + " | " + f"[Github](https://github.com/GraceChengLunya)")