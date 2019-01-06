import json
import requests

# Objective: This script prints to the console real-time estimates for trains leaving the Montgomery
# bart station. Limited to 10 of the soonest results for the purposes of this demonstration.

# API request and Json conversion
def getBartJsonObject(station, command):
    # Get the response from the API for Montgomery Station
    response = requests.get("http://api.bart.gov/api/etd.aspx?cmd="
            + command +"&orig="+ station +"&key=QQBH-5GHH-9HTT-DWE9&json=y")
    data = response.json()
    return data

# printing out the table header
def printHeader(data):
    # display header info for the result chart
    current_date = data["root"]["date"]
    current_time = data["root"]["time"]
    current_station = data["root"]["station"][0]["name"]
    print("-----------------------------------------------")
    print(current_station, "-", current_time, "-",current_date)
    print("-----------------------------------------------")

# parses json object for the 10 soonest trains leaving from station
def storeAndSortResults(res, data):
    # number of stations Montgomery is going to
    num_etds = len(data["root"]["station"][0]["etd"])

    # store all departures into our result array
    for dest in range(num_etds):
        destination_name = data["root"]["station"][0]["etd"][dest]["destination"]
        #print(destination_name)
        
        for est in range(len(data["root"]["station"][0]["etd"][dest]["estimate"])):
            estimated_time = data["root"]["station"][0]["etd"][dest]["estimate"][est]["minutes"]
            
            # edge case for "Leaving", essentially translates to 0 minutes
            if estimated_time == "Leaving":
                estimated_time = "0"

            res.append([estimated_time, destination_name])

    # sort based on estimated time - Python's Timsort is O(n lg n)
    if len(res) > 0:
        res = sorted(res, key = lambda x: int(x[0]))
    return res

# will take in result array and 'num' of results to display and print num of results out
def printResult(res, num_results):
    # print res to console
    
    # Edge Case: if there are no results, it means bart isn't running anymore
    if len(res) == 0:
        print("No trains running at this time!")
        
    # Edge Case: if there are less than 10 entires, we should just print what's available at least
    elif 0 < len(res) < num_results:
        print("We don't have enough data for " + num_results + " but here's what we do have:")
        i = 0
        while i < len(res):
            print(res[i][0].rjust(2) + " min" + "\t" +res[i][1])
            i += 1
    else:
        i = 0
        while i < num_results:
            print(res[i][0].rjust(2) + " min" + "\t" +res[i][1])
            i += 1

def main():
    # data provided by Bay Area Rapid Transit's API
    data = getBartJsonObject("MONT", "etd")

    # display header info for the result chart
    printHeader(data)

    # store final results
    res = storeAndSortResults([], data)

    # print results to console
    printResult(res, 10)

if __name__ == '__main__':
    main()

