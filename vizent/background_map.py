import cartopy.crs as ccrs
import cartopy.feature as cfeature 
import matplotlib.pyplot as plt

def get_basemap(gs, extent, show_axes, projection):

    if projection is None:
        projection = ccrs.PlateCarree()

    ax1 = plt.subplot(gs[0], projection=projection)
    ax1.coastlines('50m', zorder=0, color='0.85')
    try:
        ax1.set_extent(extent, crs=ccrs.PlateCarree())
    except ValueError:
        raise ValueError("The specified extent or values cannot be "
                            "plotted using Cartopy. Please ensure that you "
                            "are using valid latitude and longitude values. "
                            "Extent should be formatted as [minimum_x, "
                            "maximum_x, minimum_y, maximum_y].")

    ax1.add_feature(cfeature.NaturalEarthFeature('physical', 
                                                 'ocean', 
                                                 '50m', 
                                                 edgecolor='w', 
                                                 facecolor='#e6faff',
                                                 zorder=-1))
    ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                                    edgecolor='w', 
                                                    zorder=-1,
                                                    facecolor='#f0f8ec'))                                              
    gl = ax1.gridlines(draw_labels=show_axes)
    gl.top_labels=False
    gl.right_labels=False
    gl.xlines=False
    gl.ylines=False
    return ax1



def get_projected_aspects(extent, projection):
    lowerleft_projected_coords = projection.transform_point(
                                    x=extent[0], 
                                    y=extent[2],
                                    src_crs=ccrs.PlateCarree())

    upperright_projected_coords = projection.transform_point(
                                    x=extent[1], 
                                    y=extent[3], 
                                    src_crs=ccrs.PlateCarree())
    
    aspx = upperright_projected_coords[0] - lowerleft_projected_coords[0]
    aspy = upperright_projected_coords[1] - lowerleft_projected_coords[1]

    return aspx, aspy