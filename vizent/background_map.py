import cartopy.crs as ccrs
import cartopy.feature as cfeature 
import matplotlib.pyplot as plt

def get_basemap(gs, extent, show_axes):

    ax1 = plt.subplot(gs[0], projection=ccrs.PlateCarree())
    ax1.coastlines('50m', zorder=0)
    try:
        ax1.set_extent(extent)
    except ValueError:
        raise ValueError("The specified extent or values cannot be "
                            "plotted using Cartopy. Please ensure that you "
                            "are using valid latitude and longitude values. "
                            "Extent should be formatted as [minimum_x, "
                            "maximum_x, minimum_y, maximum_y].")

    ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', 
                                                    '50m', edgecolor='face', 
                                                    facecolor='#B3CFDD',
                                                    zorder=-1))
    ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                                    edgecolor='face', 
                                                    zorder=-1,
                                                    facecolor='#EFEFDB'))                                              
    gl = ax1.gridlines(draw_labels=show_axes)
    gl.top_labels=False
    gl.right_labels=False
    return ax1
