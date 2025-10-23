import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
PLACEFILE_PATH = "mizzou_weather.txt"

def get_weather_data():
    response = requests.get(URL, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    temp = dew = wind = None

    # Find all tables and scan all cells for numeric data
    for row in soup.find_all("tr"):
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cells:
            continue
        line = " ".join(cells).lower()

        if "temp" in line and temp is None:
            # Grab first number-like value
            for c in cells:
                if c.replace('.', '', 1).isdigit():
                    temp = c
                    break

        elif "dew" in line and dew is None:
            for c in cells:
                if c.replace('.', '', 1).isdigit():
                    dew = c
                    break

        elif "wind" in line and wind is None:
            # Try to find mph or speed value
            for c in cells:
                if any(x in c.lower() for x in ["mph", "kt"]):
                    wind = c
                    break
                if c.replace('.', '', 1).isdigit():
                    wind = c
                    break

    if not temp or not dew or not wind:
        print("DEBUG: Could not find all weather data. Parsed rows:")
        for row in soup.find_all("tr"):
            print(row.get_text(" | ", strip=True))
        raise ValueError("Could not find all weather data on the page")

    return float(temp), float(dew), wind

def pick_icon(temp):
    """Choose icon color number based on temperature."""
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
  Text: 12,0,1,"Wind: {wind}",255,255,255
  Icon: 0,0,000,0,{icon},"Ste. Genevieve"
End:

; Last updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
"""
    with open(PLACEFILE_PATH, "w") as f:
        f.write(text)

if __name__ == "__main__":
    temp, dew, wind = get_weather_data()
    write_placefile(temp, dew, wind)
