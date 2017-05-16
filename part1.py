import folium
import pandas as pd
from collections import Counter


#Used to make chicacoCrimeRates csv
def makeCrimeRateCSV():
    print("finding data")
    populations = pd.read_csv("chicagoPopulations.csv")
    fullData = pd.read_csv("Crimes_-_2013.csv")

    numCrimes = Counter([row["Community Area"] for index,row in fullData.iterrows()])
    crimeRate = []

    for index,row in populations.iterrows():
        area = row["Community Area"]
      
        crimes = numCrimes[area]
        rate = crimes / row["population"]
        name = row["name"]
        #area = '"'+ str(area) + '"'
        info = {"Community Area": area, "Name" : name, "Crime Rate" : rate}
        #crimeRate[name] = rate
        print(info)
        crimeRate.append(info)

    df = pd.DataFrame.from_dict(crimeRate)
    df.to_csv("chicagoCrimeRates.csv")
    print(df)
    
#############################################################
#makeCrimeRateCSV()

#reads the csv that was created above
rates = pd.read_csv("chicagoCrimeRates.csv")
print(rates)

map = folium.Map(location = [ 41.8781, -87.6298 ])
print("Creating Map")
map.choropleth(geo_path = "Boundaries - Community Areas (current).geojson",
                     fill_opacity = 0.5, line_opacity = 0.5  ,
                     data = rates,
                     fill_color = "OrRd",
                     key_on = "feature.properties.area_numbe",
                     
                     columns = ["Community Area", "Crime Rate"]
                      )

map.save(outfile = "mapCrime.html")
print("done")