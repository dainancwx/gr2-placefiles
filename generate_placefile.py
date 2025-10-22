import requests, re, datetime

stations = {
    "Ste. Genevieve": {
        "url": "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp",
        "lat": 37.981,
        "lon": -90.043
    },
    "Columbia": {
        "url": "http://agebb.missouri.edu/weather/realtime/columbia.asp",
        "lat": 38.942,
        "lon": -92.326
    },
    "Novelty": {
        "url": "http://agebb.missouri.edu/weather/realtime/novelty.asp",
        "lat": 40.017,
        "lon": -92.225
    },
    "Mt. Vernon": {
        "url": "http://agebb.missouri.edu/weather/realtime/mt_vernon.asp",
        "lat": 37.104,
        "lon": -93.879
    }
}

output = """Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 0
Font: 1, 11, 1, "Arial"
"""

for name, s in stations.items():
    try:
        html = requests.get(s["url"], timeout=10).text
        temp = re.search(r"Air Temp\s*</td><td[^>]*>([\d.]+)", html).group(1)
        wind = re.search(r"Wind Speed\s*</td><td[^>]*>([\d.]+)", html).group(1)
        direction = re.search(r"Wind Direction\s*</td><td[^>]*>([A-Z]+)", html).group(1)
        rain = re.search(r"Rainfall Today\s*</td><td[^>]*>([\d.]+)", html).group(1)
    except Exception as e:
        print(f"Error parsing {name}: {e}")
        continue

    output += f"""
Object: {s['lat']},{s['lon']}
  Threshold: 999
  Icon: 0,0,000,2,1,"{name} Wx"
  Text: 0,0,1,"Temp: {temp} °F"
  Text: 0,15,1,"Wind: {wind} mph {direction}"
  Text: 0,30,1,"Rain: {rain} in"
End:
"""

output += f"\n; Last updated: {datetime.datetime.now()}\n"

with open("mizzou_weather.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ Generated mizzou_weather.txt")
