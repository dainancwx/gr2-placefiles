import requests
import re
from datetime import datetime

URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
PLACEFILE = "mizzou_weather.txt"

def get_weather_data():
    response = requests.get(URL)
    text = response.text

    # Normalize spaces and remove garbage characters
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("Â", "").replace("", "")

    # Broaden regex: allow |, :, or whitespace between label/value
    temp_match = re.search(r'Temperature[^0-9]*([\d.]+)\s*°F', text, re.IGNORECASE)
    dew_match = re.search(r'Dewpoint[^0-9]*([\d.]+)\s*°F', text, re.IGNORECASE)
    wind_speed_match = re.search(r'Wind Speed[^0-9]*([\d.]+)\s*mph', text, re.IGNORECASE)
    wind_dir_match = re.search(r'Wind Direction[^A-Z]*([A-Z]+)', text, re.IGNORECASE)

    if not all([temp_match, dew_match, wind_speed_match, wind_dir_match]):
        print("DEBUG: Could not find all weather data.")
        print(f"temp={temp_match}, dew={dew_match}, wind_speed={wind_speed_match}, wind_dir={wind_dir_match}")
        snippet_start = text.find("Current Conditions:")
        print("Parsed snippet:", text[snippet_start:snippet_start + 400])
        raise ValueError("Could not find all weather data on the page")

    temp = float(temp_match.group(1))
    dew = float(dew_match.group(1))
    wind_speed = float(wind_speed_match.group(1))
    wind_dir = wind_dir_match.group(1).upper()

    return temp, dew, wind_speed, wind_dir


def choose_icon(temp):
    if temp >= 85:
        return "RedDot.png"
    elif temp >= 70:
        return "YellowDot.png"
    elif temp >= 50:
        return "GreenDot.png"
    else:
        return "BlueDot.png"


def create_placefile(temp, dew, wind_speed, wind_dir):
    icon = choose_icon(temp)
    lat, lon = 37.935415, -90.132342

    return f"""; Missouri Weather Station Placefile
Title: Mizzou Weather - Ste. Genevieve
Refresh: 1
Color: 255 255 255
Font: 1, 11, 1, "Courier New"
IconFile: 1, 25, 25, 12, 12, "{icon}"
Threshold: 999

; Data updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Object: {lat}, {lon}
  Threshold: 999
  Icon: 0,0,{icon}
  Text: 10, 10, 1, "Temp: {temp}°F  Dew: {dew}°F  Wind: {wind_dir} {wind_speed} mph"
End:
"""


if __name__ == "__main__":
    temp, dew, wind_speed, wind_dir = get_weather_data()
    placefile_text = create_placefile(temp, dew, wind_speed, wind_dir)

    with open(PLACEFILE, "w", encoding="utf-8") as f:
        f.write(placefile_text)

    print(f"✅ Wrote updated placefile: {PLACEFILE}")
    print(f"🌡 Temp: {temp}°F | Dew: {dew}°F | Wind: {wind_dir} {wind_speed} mph")
