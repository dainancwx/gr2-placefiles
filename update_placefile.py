import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_weather_data():
    url = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Clean text and split by '|'
    text = soup.get_text(separator="|", strip=True)
    parts = [p.strip() for p in text.split("|") if p.strip()]

    # Extract values
    temp = None
    dew = None
    wind_speed = None
    wind_dir = None

    for i, part in enumerate(parts):
        if "Temperature" in part and "°F" in parts[i + 1]:
            temp = float(parts[i + 1].replace("°F", "").strip())
        elif "Dewpoint" in part and "°F" in parts[i + 1]:
            dew = float(parts[i + 1].replace("°F", "").strip())
        elif "Wind Speed" in part and "mph" in parts[i + 1]:
            wind_speed = float(parts[i + 1].replace("mph", "").strip())
        elif "Wind Direction" in part:
            wind_dir = parts[i + 1].strip()

    if None in (temp, dew, wind_speed, wind_dir):
        raise ValueError("Could not find all weather data")

    return temp, dew, wind_speed, wind_dir


def get_icon_for_temp(temp):
    if temp < 32:
        return "BlueDot.png"
    elif temp < 60:
        return "GreenDot.png"
    elif temp < 80:
        return "YellowDot.png"
    else:
        return "RedDot.png"


def generate_placefile(temp, dew, wind_speed, wind_dir):
    icon_file = get_icon_for_temp(temp)
    placefile = f"""Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 255
Font: 1, 11, 1, "Arial"

; Ste. Genevieve Wx
Object: 37.981,-90.043
  Threshold: 999
  Text: -12,-12,1,"{temp:.1f}°F",255,0,0
  Text: -12,12,1,"{dew:.1f}°F",0,255,0
  Text: 12,0,1,"{wind_dir} {wind_speed:.0f} mph",255,255,255
  Icon: 0,0,000,0,1,"{icon_file}"
End:

; Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    with open("mizzou_weather.txt", "w") as f:
        f.write(placefile)


if __name__ == "__main__":
    temp, dew, wind_speed, wind_dir = get_weather_data()
    generate_placefile(temp, dew, wind_speed, wind_dir)
