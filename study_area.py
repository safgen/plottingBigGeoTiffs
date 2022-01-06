import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import contextily as cx
import time
from matplotlib_scalebar.scalebar import ScaleBar


t0 = time.time()

states_df = geopandas.read_file('data/usa-states-census-2014.shp')#.to_crs(epsg=3857)
mw = states_df[states_df['region'] == 'Midwest' ]
kent = states_df[states_df['NAME'] == 'Kentucky']
states = geopandas.GeoDataFrame(pd.concat([mw,kent])).to_crs(epsg=3857)

fig = plt.figure(1) 
ax = fig.add_subplot()
# states.apply(lambda x: ax.annotate(text=x.NAME, xy=x.geometry.centroid.coords[0], ha='center', fontsize=5),axis=1);
ax = states.boundary.plot(ax=ax, color='Black', linewidth=.4)
ax = states.plot(alpha=0.25, edgecolor='k')

ax.set_xlim([-1.40e7,-0.75e7])
ax.set_ylim([3e6,6.5e6])

ax.set_axis_off()
ax.add_artist(ScaleBar(1))

cx.add_basemap(ax, crs=states.crs.to_string(),  source=cx.providers.OpenStreetMap.Mapnik, attribution_size=1)
plt.savefig('xyz.png', dpi=1800.0)

print("Time taken: {} minutes".format((time.time()-t0)/60))
