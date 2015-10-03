from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point
import pandas

'''
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
'''

def LoadCSV(filename):
    #load the csv into a dataframe
    csv = pandas.DataFrame.from_csv(filename, encoding="utf-8")
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

def AddStatesToFile(dataframe, shapefile, lat_col, lon_col):
    #load the states shapefiles
    states = GeoDataFrame.from_file(shapefile)
    states.set_index('NAME', inplace=True)

    for index, row in dataframe.iterrows():
        point = Point([row[lon_col], row[lat_col]])
        state = states.contains(point)
        state = state[state == True].first_valid_index()
        row[-1] = state

    print(dataframe)


if __name__ == '__main__':
    #load the file that has the points in it we want to find states for
    filename = input("Please enter the location of the file you want to load: ")
    user_file = LoadCSV(filename)
    #List the columns in that file and have the user select which ones they want to use for Latitude/Longitude
    PickColumns(user_file)
    lat_col = int(input("Please enter the column number you want to use for Latitude: "))
    lon_col = int(input("Please enter the column number you want to use for Longitude: "))

    user_file = AddColumn(user_file, "State")
    print("Adding states to file...")
    AddStatesToFile(user_file, 'shapefiles/s_16de14.shp', lat_col, lon_col)
    print("Done! Writing file to disk.")
