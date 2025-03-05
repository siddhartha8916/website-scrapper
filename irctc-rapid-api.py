import requests

url = "https://irctc1.p.rapidapi.com/api/v2/getFare"

querystring = {"trainNo":"12368","fromStationCode":"ANVT","toStationCode":"PNBE"}

headers = {
	"x-rapidapi-key": "99ea3c0b83msha6c700b3dc3559cp13457bjsn230aa7666c65",
	"x-rapidapi-host": "irctc1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())