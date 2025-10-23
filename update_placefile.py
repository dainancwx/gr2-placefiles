import requests
import re
from datetime import datetime

def get_weather_data():
    url = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
    r = requests.get(url)
    r.raise_for_status()
    text = r.text

    # Use regex to extract values
    temp_match = re.search(r"Temperature:\s*\|?\s*([0-9.]+)°F", text)
    dew_match = re.search(r"Dewpoint:\s*\|?\s*([0-9.]+)°F", text)
    wind_speed_match = re.search(r"Wind Speed:\s*\|?\s*([0-9.]+)\s*mph", text)
    wind_dir_match = re.search(r"Wind Direction:\s*\|?\s*([A-Z]+)", text)

    if not all([temp_match, dew_match, wind_speed_match, wind_dir_match]):
        raise ValueError("Could not find all weather data on the page")

    temp = float(temp_match.group(1))
    dew = float(dew_match.group(1))
    wind_speed = float(wind_speed_match.group(1))
    wind_dir = wind_dir_match.group(1)

    print(f"DEBUG: Parsed values -> Temp={temp} Dew={dew} Wind={wind_dir} {wind_speed}mph")
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
