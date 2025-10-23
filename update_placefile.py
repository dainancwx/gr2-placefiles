import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
PLACEFILE_PATH = "mizzou_weather.txt"

def get_weather_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    temp = dew = wind = None

    # Look through all table rows
    for row in soup.find_all("tr"):
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cells:
            continue
        # Match keywords in any cell
        if "Air Temperature" in cells[0]:
            temp = cells[1].split()[0]
        elif "Dew Point" in cells[0]:
            dew = cells[1].split()[0]
        elif "Wind Speed" in cells[0]:
            wind = cells[1].split()[0]

    if not all([temp, dew, wind]):
        raise ValueError("Could not find all weather data on the page")

    return float(temp), float(dew), float(wind)

def pick_icon(temp):
    """Pick icon color number based on temp."""
    if temp >= 85:
        return 1  # red
    elif temp >= 70:
        return 2  # yellow
    elif temp >= 50:
        return 3  # green
    else:
        return 4  # blue

def write_placefile(temp, dew, wind):
    icon = pick_icon(temp)

    text = f"""Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 255
Font: 1, 11, 1, "Arial"

IconFile: 1, https://raw.githubusercontent.com/dainancwx/gr2-placefiles/main/RedDot.png
IconFile: 2, https://raw.githubusercontent.com/dainancwx/gr2-placefiles/main/YellowDot.png
IconFile: 3, https://raw.githubusercontent.com/dainancwx/gr2-placefiles/main/GreenDot.png
IconFile: 4, https://raw.githubusercontent.com/dainancwx/gr2-placefiles/main/BlueDot.png

; Ste. Genevieve Weather Station
Object: 37.981,-90.043
  Threshold: 999
  Text: -12,-12,1,"Temp: {temp}°F",255,255,255
  Text: -12,12,1,"Dewpoint: {dew}°F",0,255,0
  Text: 12,0,1,"Wind: {wind} mph",255,255,255
  Icon: 0,0,000,0,{icon},"Ste. Genevieve"
End:

; Last updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
"""
    with open(PLACEFILE_PATH, "w") as f:
        f.write(text)

if __name__ == "__main__":
    temp, dew, wind = get_weather_data()
    write_placefile(temp, dew, wind)
