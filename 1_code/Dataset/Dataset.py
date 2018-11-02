import Common
import Location
import CustomerDensity
import Dataethnic
import pandas as pd
import numpy as np

## @Package. docstring
#    Dataset creation module.

#    This module creates an artificial dataset based on a mathematical model.
#    It has four clases - Location, Ethnic State, DensityTime and Helper.
#    which collect data for different types of input data and generates a table of entries
#    based on the mathematical model.
#

H = Common.Helper()
L = Location.Location()
E = Dataethnic.EthnicState()
C = CustomerDensity.DensityTime()

# Module unit test OR Dataset creation
test = 0

if not test:
    FoodCount = L.CreateLocationDataset()
    EthnicCount = E.CreateEthnicset()
    C.CreateDensityTime(FoodCount,EthnicCount)
else:
    ##Zone Test case  - Location vs Food Entry module Unit testing.
    #                   This test verifies the pattern of table entry generation with the actual data in CSV file.
    #
    
    ##@var zone_entry - A test list used to verify the location vs Food
    #                   item table generation pattern.
    #
    zone_entry = np.array([[35,21,13,8,6,10,16],
                           [31,17,16,7,7,11,8],
                           [21,19,12,8,19,8,10],
                           [19,15,12,15,20,8,8],
                           [23,18,14,12,16,8,7]])
    FoodCount = L.CreateLocationDataset()

    ##@var FoodCount
    #     Table of Food Entry vs Location generated using mathematical modelling of input statisctics
    
    count = np.zeros((len(zone_entry),len(zone_entry[0])))
    for row in range(0,len(zone_entry)):
        for column in range(0,len(FoodCount[0])):
            Key_1 = H.GetKeyByValue(H.GetFoodEntry(),column,True)
            if H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Pizza":
                count[row][0] += FoodCount[row][column]
            elif H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Bakeries":
                count[row][1] += FoodCount[row][column]
            elif H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Sandwich shop":
                count[row][2] += FoodCount[row][column]
            elif H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Steak and BBQ":
                count[row][3] += FoodCount[row][column]
            elif H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Mexican":
                count[row][4] += FoodCount[row][column]
            elif H.GetKeyByValue(H.GetFoodType(),Key_1,False) == "Ice cream":
                count[row][5] += FoodCount[row][column]
            else:
                count[row][6] += FoodCount[row][column]

    ## Compare the expected output with the number of generated table entries
    #
    print("Zone vs Food Entry test case\n")
    print("Rows - Zones - East Zone, North Zone, West Zone, South Zone, Central Zone")
    print("Columns - Food Category - Pizza, Bakeries, Sandwich shop, Steak and BBQ, Mexican, Ice cream, Chinese")
    print(" Values - Number of entries for each Zone vs Food Entry ")
    print("\nActual output - (After running code)\n")
    print(count)
    print("\nExpected output - Using calculated data from csv file\n")
    print(zone_entry)
    print("\nMarginal error expected due to randomization of entries during generation")