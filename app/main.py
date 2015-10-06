from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point
import pandas
from clint.textui import prompt, validators


def getFileNames():
    filename_dict = {}

    filename_dict['shapefile'] = prompt.query('Shapefile to process: ', 
            default='shapefiles/s_16de14.shp', 
            validators=[]
    )
    filename_dict['data']= prompt.query('Data to process: ',
            default='csv/meteorites.csv',
            validators=[]
    )

    filename_dict['output'] = prompt.query('Output file: ',
            default='output.csv',
            validators=[]
    )

    return filename_dict

def LoadCSV(filename):
    #load the csv into a dataframe
    csv = pandas.read_csv(filename, encoding="utf-8")
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

def GetStateFromPoint(row, lat, lon, states):
    point = Point(row[lon], row[lat])
    state = states.contains(point)
    state = state[state == True].first_valid_index()
    return state

def main():

    filenames = getFileNames()

    print('Loading Shapefiles from ' + filenames['shapefile'])
    #Open up the shapefile
    states = GeoDataFrame.from_file(filenames['shapefile'])
    #Set the 'Name' column as the index
    states.set_index('NAME', inplace=True)
    print('Done!')

    print('Loading data from ' + filenames['data'])
    #Load the file the user wants to process
    data = LoadCSV(filenames['data']) 
    print('Done!')

    #list out the columns in the data file
    PickColumns(data)
    #ask the user which columns they want to use for lat/lon
    lat_col = prompt.query('Please enter the column number for Latitude: ', 
            default = '7', 
            validators=[]
    )

    lon_col = prompt.query('Please enter the column number for Longitude: ',
            default='8',
            validators=[]
    )

    #Wrap them in ints because they need to be referenced as numbers later on
    lat_col = int(lat_col)
    lon_col = int(lon_col)


    #Add a State column to the data file
    data = AddColumn(data, 'State')

    #Process each row and add the state name to the new column
    data['State'] = data.apply(
        lambda row: GetStateFromPoint(row, lat_col, lon_col, states),
        axis=1
    )
    print("Writing file to " + filenames['output'])
    data.to_csv(filenames['output'])
    print("Done!")

if __name__ == '__main__':
    main()
