import rasterio
import rasterio.features
import rasterio.warp
from rasterio.plot import show, show_hist
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import contextily as cx
from rasterio.mask import mask
import time

t0 = time.time()
fp = r'aug_2021.tif'

with rasterio.open(fp) as dataset:

    # Read the dataset's valid data mask as a ndarray.
    # mask = dataset.dataset_mask()
    img = dataset
    # shape = dataset[dataset.read(1) > 0]
    
    CRS = img.crs
    print(CRS)
    # plt.figure()
    # world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # print(world["name"].value_counts)
    # us = world[world['name'] == 'United States of America']
    # us.boundary.plot()

    states_df = geopandas.read_file('data/usa-states-census-2014.shp')
    mw = states_df[states_df['region'] == 'Midwest' ]
    kent = states_df[states_df['NAME'] == 'Kentucky']
    states = geopandas.GeoDataFrame(pd.concat([mw,kent])).to_crs(CRS)
    # print(states.info())
    # states.boundary.plot(color='black', linewidth=0.5)
    fig = plt.figure(1) 
    ax = fig.add_subplot()
    # states.apply(lambda x: ax.annotate(text=x.NAME, xy=x.geometry.centroid.coords[0], ha='center', fontsize=5),axis=1);
    ax = states.boundary.plot(ax=ax, color='Black', linewidth=.4)
    # states.plot(ax=ax, cmap='Pastel2', figsize=(12, 12))
    # ax.text(-0.05, 0.5, '', transform=ax.transAxes,
    #         fontsize=12, color='gray', alpha=0.5,
    #         ha='center', va='center', rotation='90')

    cx.add_basemap(ax, crs=CRS.to_string(), source=cx.providers.Stamen.TonerLite, attribution_size=1)

    cmaplist = ['white', 'green']  # ['white', 'green'] for soybean, ['red', 'white'] for corn, ['red', 'green'] for both  
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'Custom cmap', cmaplist, 2)
    

    ax = show(img, cmap=cmap)
    ax.set_xlim([-104.2,-80.3])
    ax.set_ylim([36.3,49.7])
    ax.set_xlabel("Logitude")
    ax.set_ylabel("Latitude")
    ax.set_axis_off()
    # bx = fig.add_subplot(212)
    # show_hist(img, bins=3, ax=bx, label=['corn', 'soybean'])
    # ax.add_artist(ScaleBar(30))
    # print(img.height, img.width)
    # us.boundary.plot()
    # cx.add_basemap(ax, crs=img.crs, source=cx.providers.OpenStreetMap.Mapnik)
    plt.savefig('abc.png', dpi=1800.0)
    # ax.savefig('test2.png', dpi=1200.0)
    # plt.show()

print("Time taken: {} minutes".format((time.time()-t0)/60))