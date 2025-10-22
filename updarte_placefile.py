import requests, re, datetime

# --- CONFIG ---
station_name = "Ste. Genevieve Wx"
lat, lon = 37.981, -90.043
icon_url = "https://raw.githubusercontent.com/dainancwx/gr2-placefiles/main/RedDotX.svg.png"
output_file = "mizzou_weather.txt"

# --- SCRAPE TEMP ---
url = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
html = requests.get(url).text
match = re.search(r"Temperature</TD><TD[^>]*>([\d.]+)", html)
temp = float(match.group(1)) if match else 70.0  # fallback

# --- CHOOSE DOT COLOR ---
if temp <= 32:
    color = "0,0,255"       # blue
elif temp < 60:
    color = "0,255,255"     # cyan
elif temp < 80:
    color = "255,255,0"     # yellow
else:
    color = "255,0,0"       # red

# --- BUILD PLACEFILE ---
placefile = f"""Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 255
Font: 1, 11, 1, "Arial"

; dynamic icon based on temperature
File: 1, "{icon_url}"

Object: {lat},{lon}
  Threshold: 999
  Text: -12,-12,1,"{int(temp)}",255,0,0
  Icon: 0,0,1,1,1,"", {color}
End:

; Last updated: {datetime.datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC
"""

with open(output_file, "w") as f:
    f.write(placefile)
print(f"Updated {output_file} with temp {temp}°F and color {color}")
