import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import math
import statistics
import random
#from scipy.stats import norm
import Common

## EthnicState - Class for generation of Location Vs Ethnicity matrix
#
# Computes location vs Ethnicity matrix using input CSV file
#
class EthnicState:
    ## The constructor. Includes Helper object, Food Entry and FoodCount
    # @param self The object pointer
    def __init__(self):
        H = Common.Helper()
        self.ethnic_data = {0:"white", 1:"black", 2:"hispianic", 3:"asian"}        
        rows = len(H.GetZoneData())
        columns = len(self.ethnic_data)
        self.EthnicCount = np.zeros((rows,columns))
    
    ## GetEthnicData
    # @return self.ethnic_data
    def GetEthnicData(self):
        return self.ethnic_data

    ## CreateEthnicSet - Create the Location vs Ethnicity matrix,     
    # @param self The Object pointer
    #
    def CreateEthnicset(self):
        H = Common.Helper()
        df = pd.read_csv('ethnicity.csv')
        east_food = np.zeros(df.shape[1]-1)
        north_food = np.zeros(df.shape[1]-1)
        west_food = np.zeros(df.shape[1]-1)
        south_food = np.zeros(df.shape[1]-1)
        central_food = np.zeros(df.shape[1]-1)
        for column in range(1,df.shape[1]):
            for row in range(1,df.shape[0]):
                value = df.iloc[row][column]
                if df.iloc[row][0] in H.GetEastZone():
                    east_food[column-1] = east_food[column-1] + value
                elif df.iloc[row][0] in H.GetNorthZone():
                    north_food[column-1] = north_food[column-1] + value
                elif df.iloc[row][0] in H.GetWestZone():
                    west_food[column-1] = west_food[column-1] + value
                elif df.iloc[row][0] in H.GetSouthZone():
                    south_food[column-1] = south_food[column-1] + value
                else:
                    central_food[column-1] = central_food[column-1] + value
            east_food[column-1] = round(east_food[column-1]/len(east_food),2)
            north_food[column-1] = round(north_food[column-1]/len(north_food),2)
            west_food[column-1] = round(west_food[column-1]/len(west_food),2)
            south_food[column-1] = round(south_food[column-1]/len(south_food),2)
            central_food[column-1] = round(central_food[column-1]/len(central_food),2)

        zone_food = np.stack((east_food,north_food,west_food,south_food,central_food))
        #print(zone_food)

        num_rows = len(zone_food)
        num_columns = len(zone_food[0])

        total_zone = [0] * num_rows
        H.GetTotalForRows(zone_food,total_zone,num_rows)
        #print(total_zone)

        ## Scaled percentages
        #
        for value in range(0,num_rows):
            H.CalPercentage(zone_food[value],total_zone[value])

        num_entries = H.GetNumEntries()
        entries_per_zone = num_entries/num_rows
        for row in range(0,num_rows):
            for column in range(0,num_columns):
                zone_food[row][column] = math.floor(zone_food[row][column]/100 * entries_per_zone)

        ## Rounding correction
        #
        for row in range(0,num_rows):
            total = sum(zone_food[row,:])
            error = entries_per_zone - total
            assert (error >= 0),"Error should not be negative"
            while error > 0:
                zone_food[row][random.randint(0,num_columns-1)] += 1
                error -= 1

        ## @var TableEntry - Location vs Ethnicity matrix
        #  @var count - Count of each food entry in TableEntry for corresponding location
        zone_data = H.GetZoneData()
        count = np.zeros((num_rows,num_columns))
        TableEntry = list()
        TableEntry = [[]]*num_entries
        for entry in range(0,num_entries):
            row = random.randint(0,num_rows-1)
            column = random.randint(0, num_columns-1)
            while(count[row][column] >= zone_food[row][column]):
                row = random.randint(0,num_rows-1)
                column = random.randint(0, num_columns-1)
            ZoneValue = zone_data.get(row)
            ethnic = self.ethnic_data.get(column)
            TableEntry[entry] = [ZoneValue,ethnic]
            self.EthnicCount[row][column] += 1
            count[row][column] += 1

        return self.EthnicCount
        #print(TableEntry)
        #plt.title('PDF')
        #plt.xlabel('Food Type')
        #plt.ylabel('Probability')
        #plt.legend()
        #plt.show()
