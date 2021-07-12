import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import pandas as pd

# Borders of the image
BBox = [20.7693, 20.9526, 39.6013, 39.7278]

# Data Load
df = pd.read_csv('TripAdvisor.csv')
df = df[['store', 'latitude', 'longitude']]
# Data Prep
df = df[(df.latitude < BBox[3]) & (df.latitude > BBox[2]) &
        (df.longitude < BBox[1]) & (df.longitude > BBox[0])]
# GEO DATA FRAME CREATION
print(df[df.store < 'a'].sample(10))
geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
    df.longitude, df.latitude, crs="EPSG:4326"))
print(geo_df[geo_df.store < 'a'].sample(10))
print(geo_df[['store', 'geometry']].sample(10))
# REGIONS LOAD
regions = gpd.read_file('geo.geojson')

print(regions)
# JOIN GEO_DATA WITH REGIONS
geo_df = gpd.sjoin(geo_df, regions, how='inner', op='within')
print(geo_df)
for_plot = regions.merge(
    geo_df.groupby('index_right').store.count(), how='left', left_on=regions.index, right_on='index_right').fillna(0)
print(for_plot)
# PLOT
f, ax = plt.subplots(1, figsize=(11, 9))
# IMAGE
ioa_im = plt.imread('map.png')
ax.imshow(ioa_im, zorder=0, extent=BBox)
# BINS
bins = mapclassify.Quantiles(for_plot['store'], k=8).bins
for i in range(len(bins)):
    bins[i] = bins[i]
# PLOT SETTINGS AND LABELS
for_plot.plot(column='store', ax=ax, legend=True, alpha=0.7, edgecolor='black',
              scheme="User_Defined", classification_kwds=dict(bins=bins), cmap='RdYlGn')
#for_plot.plot(column = 'store', ax =ax, legend = True, alpha = 0.7, edgecolor = 'black', legend_kwds={'label': "Total number of reviews by shape"})
plt.title("TripAdvisor's Reviews")
# plt.xlabel('From: ' + str(geo_df.date.min()) +
#           ' to: ' + str(geo_df.date.max()))
plt.ylabel("Total number of reviews: " + str(int(for_plot.store.sum())))
plt.show()
