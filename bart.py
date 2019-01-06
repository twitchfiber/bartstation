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

# 
# Your previous Plain Text content is preserved below:
# 
# ===== Preface =====
# 
# This question is very difficult in C and C++, where there is
# insufficient library support to answer it in an hour. If you
# prefer to program in one of those languages, please ask us to
# provide you with a question designed for those languages instead!
# 
# 
# ===== Intro =====
# 
# The Delphix San Francisco office is located in San Francisco’s
# financial district.  BART (Bay Area Rapid Transit) is a public
# transportation system serving the San Francisco Bay Area. Many
# engineers in the SF office use the Montgomery Street BART station
# to get to/from the office.
# 
# As engineers in the office will tell you, the BART system is
# infamously off schedule. Luckily, the BART public API
# (http://api.bart.gov/docs/overview/index.aspx) has a real-time
# information feed containing information about real-time estimated
# departures for specific stations. Your goal is to write a small
# program that utilizes the BART API that will quickly tell us the
# current time, the next 10 trains leaving Montgomery Street station,
# where they are going, and in how many minutes they leave the
# station.
# 
# Rules/constraints:
# * Print the trains in the order that they are leaving the station
# * Limit the output to the next 10 trains leaving the station
# * Print the number of minutes that the train will leave the station
# * Print the destination of the train
# 
# Example output:
# 
#     --------------------------------------------------
#     Montgomery St.  04:36:04 PM PDT
#     --------------------------------------------------
#     2 min  Dublin/Pleasanton
#     4 min  Daly City
#     5 min  Millbrae
#     5 min  Pittsburg/Bay Point
#     7 min  Fremont
#     9 min  Pleasant Hill
#     10 min  SF Airport
#     12 min  Daly City
#     12 min  Richmond
#     14 min  Millbrae
# 
# Your output does not need to match this, this is just an example.
# If you have better ideas of how to display the data, please do!
# 
# You should implement this in whatever language you're most
# comfortable with -- just make sure your code is production
# quality, well designed, and easy to read.
# 
# Finally, please help us by keeping this question and your
# answer secret so that every candidate has a fair chance in
# future Delphix interviews.
# 
# 
# ===== Steps =====
# 
# 1.  Choose the language you want to code in from the menu
#     labeled "Plain Text" in the top right corner of the
#     screen. You will see a "Run" button appear on the top
#     left -- clicking this will send your code to a Linux
#     server and compile / run it. Output will appear on the
#     right side of the screen.
#     
#     For information about what libraries are available for
#     your chosen language, see:
# 
#         https://coderpad.io/languages
# 
# 2.  Pull up the documentation for the API you'll be using:
# 
#       http://api.bart.gov/docs/etd/etd.aspx
# 
# 3.  You'll need an API key in order to query the data from
#     BART. You can create your own key
#     (http://www.bart.gov/schedules/developers/api) or use the demo
#     key:
# 
#         MW9S-E7SL-26DU-VV8V
# 
# 4.  Implement the functionality described above, using data
#     fetched dynamically from the BART API described here:
# 
#       http://api.bart.gov/docs/etd/etd.aspx
# 
# 5.  Add any tests for your code to the main() method of
#     your program so that we can easily run them.
# 
# 
# 
# ====== FAQs =====
# 
# Q:  How do I know if my solution is correct?
# A:  Make sure you've read the prompt carefully and you're
#     convinced your program does what you think it should
#     in the common case. If your program does what the prompt 
#     dictates, you will get full credit. We do not use an
#     auto-grader, so we do not have any values for you to
#     check correctness against.
#     
# Q:  What is Delphix looking for in a solution?
# A:  After submitting your code, we'll have a pair of engineers
#     evaluate it and determine next steps in the interview process.
#     We are looking for correct, easy-to-read, robust code.
#     Specifically, ensure your code is idiomatic and laid out
#     logically. Ensure it is correct. Ensure it handles all edge
#     cases and error cases elegantly.
#     
# Q:  If I need a clarification, who should I ask?
# A:  Send all questions to the email address that sent you
#     this document, and an engineer at Delphix will get
#     back to you ASAP (we're pretty quick during normal
#     business hours).
# 
# Q:  How long should this question take me?
# A:  Approximately 1 hour, but it could take more or less
#     depending on your experience with web APIs and the
#     language you choose.
# 
# Q:  When is this due?
# A:  We will begin grading your answer 24 hours after it is
#     sent to you, so that is the deadline.
#     
# Q:  What if something comes up and I cannot complete the
#     problem during the 24 hours?
# A:  Reach out to us and let us know! We will work with you
#     to figure out an extension if necessary.
# 
# Q:  How do I turn in my solution?
# A:  Anything you've typed into this document will be saved.
#     Email us when you are done with your solution. We will
#     respond confirming we've received the solution within
#     24 hours.
# 
# Q:  Can I use any external resources to help me?
# A:  Absolutely! Feel free to use any online resources you
#     like, but please don't collaborate with anyone else.
# 
# Q:  Can I use my favorite library in my program?
# A:  Unfortunately, there is no way to load external
#     libraries into CoderPad, so you must stick to what
#     they provide out of the box for your language:
# 
#         https://coderpad.io/languages
# 
#     If you really want to use something that's not
#     available, email the address that sent you this link
#     and we will work with you to find a solution.
# 
# Q:  Can I code this up in a different IDE?
# A:  Of course! However, we do not have your environment
#     to run your code in. We ask that you submit your final
#     code via CoderPad (and make sure it can run). This gives
#     our graders the ability to run your code rather than guessing.
# 
# Q:  Why does my program terminate unexpectedly in
#     CoderPad, and why can't I read from stdin or pass
#     arguments on the command line?
# A:  CoderPad places a limit on the runtime and amount of
#     output your code can use, but you should be able to
#     make your code fit within those limits. You can hard
#     code any arguments or inputs to the program in your
#     main() method or in your tests.
# 
# Q:  I'm a Vim/Emacs fan -- is there any way to use those
#     keybindings? What about changing the tab width? Font
#     size?
# A:  Yes! Hit the button at the bottom of the screen that
#     looks like a keyboard.

