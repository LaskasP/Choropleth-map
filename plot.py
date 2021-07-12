import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import pandas as pd


BBox = [20.7693, 20.9526, 39.6013, 39.7278]
df = pd.read_csv('Reviews.csv')
df = df[['store', 'latitude', 'longitude']]
df = df[(df.latitude < BBox[3]) & (df.latitude > BBox[2]) &
        (df.longitude < BBox[1]) & (df.longitude > BBox[0])]
geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
    df.longitude, df.latitude, crs="EPSG:4326"))
regions = gpd.read_file('geo.geojson')
geo_df = gpd.sjoin(geo_df, regions, how='inner', op='within')
for_plot = regions.merge(
    geo_df.groupby('index_right').store.count(), how='left', left_on=regions.index, right_on='index_right').fillna(0)
f, ax = plt.subplots(1, figsize=(11, 9))
ioa_im = plt.imread('map.png')
ax.imshow(ioa_im, zorder=0, extent=BBox)
bins = mapclassify.Quantiles(for_plot['store'], k=8).bins
for i in range(len(bins)):
    bins[i] = bins[i]
for_plot.plot(column='store', ax=ax, legend=True, alpha=0.7, edgecolor='black',
              scheme="User_Defined", classification_kwds=dict(bins=bins), cmap='RdYlGn')
plt.title("Reviews")
plt.ylabel("Total number of reviews: " + str(int(for_plot.store.sum())))
plt.show()
