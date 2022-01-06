import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar

df = pd.read_csv('Crop area 2021.csv').drop(columns=['Unnamed: 0'])
gdf =  geopandas.GeoDataFrame(df)

states_df = geopandas.read_file('data/usa-states-census-2014.shp')
mw = states_df[states_df['region'] == 'Midwest' ]
kent = states_df[states_df['NAME'] == 'Kentucky']
states = geopandas.GeoDataFrame(pd.concat([mw,kent])).to_crs(epsg=3857)

areas = states.merge(gdf,on='NAME')

fig = plt.figure(2) 
ax = fig.add_subplot(211)
areas.plot(ax=ax, column='Corn Area', alpha=0.5, edgecolor='k', cmap='YlGn', legend=True, vmax=55000)
ax.set_axis_off()
ax.set_title('Corn Area (Sq. Km)')
cx.add_basemap(ax, crs=states.crs.to_string(),  source=cx.providers.Stamen.TonerLite, attribution_size=1)

bx = fig.add_subplot(212)
areas.plot(ax=bx, column='Soybean Area', alpha=0.5, edgecolor='k', cmap='YlGn', legend=True, vmax=55000)
bx.set_axis_off()
bx.set_title('Soybean Area (Sq. Km)')
cx.add_basemap(bx, crs=states.crs.to_string(),  source=cx.providers.Stamen.TonerLite, attribution_size=1)

plt.savefig('heatmap.png', dpi=1200.0)
