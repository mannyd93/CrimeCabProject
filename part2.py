import folium
import pandas as pd
from collections import Counter





#this method is used to index the taxi trip csv to the year 2013 and make a new csv
def makeTaxiCSV():
    fullData = pd.read_csv("TaxiTripsSample.csv")
    columnNames = list(fullData.columns.values)
    print(columnNames)

    file = open("Taxi2013.csv", "w")
    for name in columnNames:
        file.write(name)
        file.write(",")
    file.write("\n")
    for index, row in fullData.iterrows():
        if("2013"in str(row["Trip End Timestamp"])):
           print(row["Trip End Timestamp"])
           for name in columnNames:
               if(name == ""):continue
               file.write(str(row[name]))
               file.write(",")
        
           file.write("\n")

    file.close()


#this method reads the csv made above and finds the rates of each neighborhood
def makeTaxiRateCSV():
    print("Loading Taxi Data and Populations....")
    populations = pd.read_csv("chicagoPopulations.csv")
    fullData = pd.read_csv("Taxi2013.csv")
    print(fullData)
   
    print("Counting Pickups...")
    numPick = Counter([row["Pickup Community Area"] for index,row in fullData.iterrows()])
    print("Counting Dropoffs...")
    numDrop = Counter([row["Dropoff Community Area"] for index,row in fullData.iterrows()])
 
    cabRate = []

    for index,row in populations.iterrows():
        area = row["Community Area"]
        picks = numPick[area]
        drops = numDrop[area]
        pickrate = picks/ row["population"]
        droprate = drops/row["population"]
        name = row["name"]
        info = {"Community Area": area, "Name" : name, "Pickup Rate" : pickrate, "Dropoff Rate":droprate}
        #crimeRate[name] = rate
        cabRate.append(info)

    df = pd.DataFrame.from_dict(cabRate)
    df.to_csv("chicagoTaxiRates.csv")
    print("Taxi Rate CSV Created")

#############################################################################
#makeTaxiCSV()
#makeTaxiRateCSV()

print("finding data")

#reads the csv that was created above
rates = pd.read_csv("chicagoTaxiRates.csv")
print(rates)

pickupmap = folium.Map(location = [ 41.8781, -87.6298 ])
pickupmap.choropleth(geo_path = "Boundaries - Community Areas (current).geojson",
                     fill_opacity = 0.5, line_opacity = 0.5  ,
                     data = rates,
                     fill_color = "PuRd",
                     key_on = "feature.properties.area_numbe",
                     columns = ["Community Area", "Pickup Rate"]
                        
                      )


pickupmap.save(outfile = "mapTaxiPickup.html")



dropoffmap = folium.Map(location = [ 41.8781, -87.6298 ])
dropoffmap.choropleth(geo_path = "Boundaries - Community Areas (current).geojson",
                     fill_opacity = 0.5, line_opacity = 0.5  ,
                     data = rates,
                     fill_color = "PuRd",
                     key_on = "feature.properties.area_numbe",
                     columns = ["Community Area", "Dropoff Rate"]
                        
                      )


dropoffmap.save(outfile = "mapTaxiDropoff.html")
print("done")


