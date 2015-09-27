from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point

states = GeoDataFrame.from_file('shapefiles/s_16de14.shp')
states.set_index('NAME', inplace=True)

point = Point([47.53, -120.62])

state = states.contains(point).first_valid_index()

print(state)
