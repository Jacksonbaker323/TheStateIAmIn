from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point
import csv

def LoadStates():
    #load the state shapefiles
    states = GeoDataFrame.from_file('shapefiles/s_16de14.shp')
    states.set_index('NAME', inplace=True)
    return states


def StateFromPoint(latitude, longitude, states):
    #create a point
    point = Point([longitude, latitude])
    #create a pandas series that lists the states and if the point exists in it or nto
    state = states.contains(point)
    #return the name of the state that has the point in it
    return state[state == True].first_valid_index()

def LoadCSV(filename):
    #load the csv into a dataframe
    csv = pandas.read_csv(filename)
    #add a state column
    csv['State'] = pandas.Series()

if __name__ == '__main__':
    states = LoadStates()
    state_name = StateFromPoint(42, -120, states)
    print(state_name)
