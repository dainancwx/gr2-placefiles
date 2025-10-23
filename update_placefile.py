import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
ICON_BASE = "https://dainancwx.github.io/gr2-placefiles"

def get_weather_data():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    # Example: find the temp and dewpoint cells from the table
    temp = float(soup.find(string="Air Temperature").find_next("td").text.strip())
    dew = float(soup.find(string="Dew Point").find_next("td").text.strip())
    wind = soup.find(string="Wind Speed").find_next("td").text.strip()

    return temp, dew, wind

def get_icon(temp):
    if temp < 40:
        return f"{ICON_BASE}/BlueDot.png"
    elif temp < 65:
        return f"{ICON_BASE}/GreenDot.png"
    elif temp < 85:
        return f"{ICON_BASE}/YellowDot.png"
    else:
        return f"{ICON_BASE}/RedDot.png"

def write_placefile(temp, dew, wind):
    icon_url = get_icon(temp)
    content = f"""Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 255
Font: 1, 11, 1, "Arial"
IconFile: 1, {icon_url}

; Ste. Genevieve Wx
Object: 37.981,-90.043
  Threshold: 999
  Text: -12,-12,1,"{int(temp)}°",255,0,0
  Text: -12,12,1,"{int(dew)}°",0,255,0
  Text: 12,0,1,"{wind}",255,255,255
  Icon: 0,0,000,0,1,""
End:

; Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
    with open("mizzou_weather.txt", "w") as f:
        f.write(content)

if __name__ == "__main__":
    temp, dew, wind = get_weather_data()
    write_placefile(temp, dew, wind)
