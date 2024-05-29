import requests

def get_temperature(city):
    api_key = "0ecec1d8c0639ec41ca8505c592184bb"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        return temperature
    else:
        return None
