# importing requests and json
import requests, json
import random


# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# API key
API_KEY = "857a04bf402d432f6d13307cee57d8e7"
# upadting the URL
URL = BASE_URL + "q=" + "&appid=" + API_KEY +"&lat=35.245919&lon=33.033941"


def get_random_numbers(temperature,humidity):
  num1 = random.randint(int(temperature*0.8), int(temperature*1.3))  # generates a random integer between 0 and 100
  num2 = random.randint(int(humidity*0.7), int(humidity*1.2))  # generates a random integer between 0 and 100
  return num1, num2



def isAboveThreshold(tempList,humidityList):
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
       # getting data in the json format
       data = response.json()
       # getting the main dict block
       main = data['main']
       # getting temperature
       temperature = main['temp']
       # getting the humidity
       humidity = main['humidity']
       # getting the pressure
       #pressure = main['pressure']
       # weather report
       #report = data['weather']
       temperature_in_celsius = temperature - 273.15

       index = 0
       for value in tempList:
          #Above threshhold
          if (tempList[index]>temperature_in_celsius*1.1) or (humidityList[index]>humidity*0.9):
             return True
          index+=1

    else:
      # showing the error message
      print("Error in the HTTP request")
      
    return False 




if __name__ == "__main__":

    isAboveThreshold= isAboveThreshold([20.22,124.0],[45,30])
    print(isAboveThreshold)
    #print("list 2 is {}".format(list2))