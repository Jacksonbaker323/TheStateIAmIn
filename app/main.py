from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point
import pandas
import pdb


def LoadCSV(filename):
    #load the csv into a dataframe
    csv = pandas.read_csv(filename, encoding="utf-8", nrows=100)
    #add a state column
    return csv

def PickColumns(dataframe):
    columns = dataframe.columns.tolist()
    col_count = len(columns)
    for i in range(col_count):
        print(str(i) + ": " + columns[i])

def AddColumn(dataframe, column_name):
    dataframe[column_name] = pandas.Series()
    return dataframe

def GetStateFromPoint(row, lat, lon):
    point = Point(row[lon], row[lat])
    state = states.contains(point)
    state = state[state == True].first_valid_index()
    return state

if __name__ == '__main__':
    #Load states from shapefile so they are universally available
    states = GeoDataFrame.from_file('shapefiles/s_16de14.shp')
    states.set_index('NAME', inplace=True)

    #load the file that has the points in it we want to find states for
    filename = input("Please enter the location of the file you want to load: ")
    user_file = LoadCSV(filename)
    #List the columns in that file and have the user select which ones they want to use for Latitude/Longitude
    PickColumns(user_file)
    lat_col = int(input("Please enter the column number you want to use for Latitude: "))
    lon_col = int(input("Please enter the column number you want to use for Longitude: "))

    user_file = AddColumn(user_file, "State")
    print("Adding states to file...")

    user_file['State'] = user_file.apply(lambda row: GetStateFromPoint(row, lat_col, lon_col), axis=1)

    user_file.to_csv('processed.csv')
    print("Done! Writing file to disk.")
