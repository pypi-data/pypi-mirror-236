import pandas as pd

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
except ModuleNotFoundError:
    matplotlib = None
    plt = None
    PatchCollection = None
    Polygon = None

try:
    from mpl_toolkits.basemap import Basemap
except ModuleNotFoundError:
    Basemap = None


idx = pd.IndexSlice


def plot_choropleth(
    df,
    shp_file,
    shp_attrcol,
    lat,
    lon,
    title=None,
    cmap="viridis",
    clabel=None,
    limits=None,
    ax=None,
    fig=None,
    cbar=True,
):
    if plt is None:
        msg = "To use the plot module, you need to install matplotlib."
        raise ModuleNotFoundError(msg)

    if ax is None:
        fig = plt.figure(figsize=[15, 10])
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    if title is not None:
        ax.set_title(title)

    if Basemap is None:
        msg = "To use the plot module, you need to install basemap."
        raise ModuleNotFoundError(msg)

    m = Basemap(
        llcrnrlon=lon[0],
        urcrnrlon=lon[1],
        llcrnrlat=lat[0],
        urcrnrlat=lat[1],
        rsphere=(6378137.00, 6356752.3142),
        resolution="l",
        projection="merc",
        lat_0=40.0,
        lon_0=-20.0,
        lat_ts=20.0,
        fix_aspect=True,
    )

    m.fillcontinents(color="#e0e0e0")

    m.readshapefile(shp_file, "map_layer", drawbounds=False)

    patches = {}
    for info, shape in zip(m.map_layer_info, m.map_layer):
        if info[shp_attrcol] not in patches.keys():
            patches[info[shp_attrcol]] = []
        patches[info[shp_attrcol]].append(Polygon(shape, True))

    cmap = matplotlib.cm.get_cmap(cmap)
    if limits is None:
        limits = [None, None]
    if limits[0] is None:
        limits[0] = float(df.min())
    if limits[1] is None:
        limits[1] = float(df.max())

    for ikey in df.index.values:
        if ikey in patches.keys():
            if not df.isna().loc[ikey].any():
                ax.add_collection(
                    PatchCollection(
                        patches[ikey],
                        facecolor=cmap(
                            float((df.loc[ikey] - limits[0]) / (limits[1] - limits[0]))
                        ),
                        edgecolor="k",
                        linewidths=0.5,
                        zorder=2,
                    )
                )
        else:
            print("Dataframe index {} has no corresponding shape".format(ikey))

    if cbar:
        cbar = plt.colorbar(
            matplotlib.cm.ScalarMappable(
                norm=matplotlib.colors.Normalize(vmin=limits[0], vmax=limits[1]),
                cmap=cmap,
            ),
            ax=ax,
        )

        if clabel is not None:
            cbar.set_label(clabel, rotation=90, labelpad=10)

    return fig, ax


def plot_network(
    df,
    shp_file,
    shp_attrcol,
    lat,
    lon,
    centroids,
    title=None,
    cmap="viridis",
    clabel=None,
    limits=None,
    ax=None,
    fig=None,
    cbar=True,
):
    if plt is None:
        msg = "To use the plot module, you need to install matplotlib."
        raise ModuleNotFoundError(msg)

    if ax is None:
        fig = plt.figure(figsize=[15, 10])
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    if Basemap is None:
        msg = "To use the plot module, you need to install basemap."
        raise ModuleNotFoundError(msg)

    m = Basemap(
        llcrnrlon=lon[0],
        urcrnrlon=lon[1],
        llcrnrlat=lat[0],
        urcrnrlat=lat[1],
        rsphere=(6378137.00, 6356752.3142),
        resolution="l",
        projection="merc",
        lat_0=40.0,
        lon_0=-20.0,
        lat_ts=20.0,
        fix_aspect=True,
    )

    m.fillcontinents(color="#e0e0e0")

    if title is not None:
        ax.set_title(title)

    # Plot model regions
    m.readshapefile(shp_file, "map_layer", drawbounds=False)

    patches = {}
    for info, shape in zip(m.map_layer_info, m.map_layer):
        if info[shp_attrcol] not in patches.keys():
            patches[info[shp_attrcol]] = []
        patches[info[shp_attrcol]].append(Polygon(shape, True))

    for ikey in patches.keys():
        ax.add_collection(
            PatchCollection(
                patches[ikey],
                facecolor="#fcfcfc",
                edgecolor="k",
                linewidths=0.5,
                zorder=2,
            )
        )

    # Plot network
    cmap = matplotlib.cm.get_cmap(cmap)
    if limits is None:
        limits = [None, None]
    if limits[0] is None:
        limits[0] = float(df.min())
    if limits[1] is None:
        limits[1] = float(df.max())

    df = df.sort_values(by=df.columns.values[-1])
    for ipos, ilink in enumerate(df.index.values):
        if len(ilink) == 1:
            start, end = ilink.split("__")
        elif len(ilink) == 2:
            start, end = ilink
        else:
            raise ("Error obtaining the link index")

        if not df.isna().loc[ilink].any():
            if start in centroids.keys() and end in centroids.keys():
                m.drawgreatcircle(
                    *centroids[start],
                    *centroids[end],
                    linewidth=7,
                    color="k",
                    solid_capstyle="round",
                )
                m.drawgreatcircle(
                    *centroids[start],
                    *centroids[end],
                    linewidth=5,
                    color=cmap(
                        float((df.iloc[ipos] - limits[0]) / (limits[1] - limits[0]))
                    ),
                    solid_capstyle="round",
                )
            else:
                if start not in centroids.keys():
                    print("No centroid defined for model node {}".format(start))
                else:
                    print("No centroid defined for model node {}".format(end))

    # for ilink in df.index.values:
    #     start, end = ilink.split("__")
    #     if not df.isna().loc[ilink]:
    #         if start in centroids.keys() and end in centroids.keys():
    #             m.drawgreatcircle(*centroids[start], *centroids[end],linewidth=5, color=cmap(((df.loc[ilink].data-limits[0])/(limits[1]-limits[0])), solid_capstyle="round")
    #         else:
    #             if start not in centroids.keys():
    #                 print("No centroid defined for model node {}".format(start))
    #             else:
    #                 print("No centroid defined for model node {}".format(end))

    if cbar:
        cbar = plt.colorbar(
            matplotlib.cm.ScalarMappable(
                norm=matplotlib.colors.Normalize(vmin=limits[0], vmax=limits[1]),
                cmap=cmap,
            ),
            ax=ax,
        )

        if clabel is not None:
            cbar.set_label(clabel, rotation=90, labelpad=10)

    return fig, ax
