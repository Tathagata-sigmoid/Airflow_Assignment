def get_data():
    import requests, json, csv

    cities = ['Kolkata', 'Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Patna', 'Chennai',
            'Goa', 'Hyderabad', 'Kota']
    states = ['West Bengal','Delhi','Maharashtra','Karnataka','Maharashtra','Bihar','Tamil Nadu',
            'Goa','Telangana','Rajasthan']
            
    newfile = open('/usr/local/airflow/store_files_airflow/result_many_city.csv', 'w')

    col_header = ['City', 'State', 'Description', 'Temperature', 'Feels Like Temperature', 'Min Temperature',
                    'Max Temperature', 'Humidity', "Clouds"]
    writer = csv.DictWriter(newfile, fieldnames=col_header)
    writer.writeheader()
    for city, state in zip(cities, states):
        q_str = city + ',in'
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        querystring = {"q": q_str, "lat": "0", "lon": "0", "callback": "test", "id": "2172797", "lang": "null",
                    "units": "imperial", "mode": "HTML"}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "305914f269msh0a74fe899214368p113526jsn1b82708a93ca"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        s = response.text
        res = ""
        for i in range(5, len(s) - 1):
            res += s[i]
        p = json.loads(res)
        d = dict()
        d['City'] = p['name']
        d['State'] = state
        d['Description'] = p['weather'][0]['description']
        d['Temperature'] = p['main']['temp']

        d['Feels Like Temperature'] = p['main']['feels_like']
        d['Min Temperature'] = p['main']['temp_min']

        d['Max Temperature'] = p['main']['temp_max']
        d['Humidity'] = p['main']['humidity']
        d["Clouds"] = p["clouds"]["all"]
        writer.writerow(d)

