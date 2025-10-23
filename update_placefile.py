import requests
import re
from datetime import datetime

PLACEFILE_PATH = "mizzou_weather.txt"
URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"

def get_weather_data():
    response = requests.get(URL)
    text = response.text

    # Clean up HTML text
    clean_text = re.sub(r'\s+', ' ', text)
    clean_text = clean_text.replace("Â", "")  # handle odd encoding characters

    # Regex patterns for each field
    temp_match = re.search(r'Temperature:\s*\|?\s*([\d.]+)\s*°F', clean_text)
    dew_match = re.search(r'Dewpoint:\s*\|?\s*([\d.]+)\s*°F', clean_text)
    wind_match = re.search(r'Wind Speed:\s*\|?\s*([\d.]+)\s*mph', clean_text)
    wind_dir_match = re.search(r'Wind Direction:\s*\|?\s*([A-Z]+)', clean_text)

    if not all([temp_match, dew_match, wind_match, wind_dir_match]):
        print("DEBUG: Could not find all weather data.")
        print("Parsed snippet:", clean_text[:500])
        print(f"temp_match={temp_match}, dew_match={dew_match}, wind_match={wind_match}, wind_dir_match={wind_dir_match}")
        raise ValueError("Could not find all weather data on the page")

    temp = float(temp_match.group(1))
    dew = float(dew_match.group(1))
    wind_speed = float(wind_match.group(1))
    wind_dir = wind_dir_match.group(1)

    return temp, dew, wind_speed, wind_dir


def write_placefile(temp, dew, wind_speed, wind_dir):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    content = f"""Title: Mizzou Weather
Refresh: 5
Color: 255 255 255
Font: 1, 11, 1, "Arial"

Object: 37.935415, -90.132342
  Threshold: 999
  Icon: 0,0,000,0,0,"Ste. Genevieve Weather"
  Text: 0,15,1,"Temp: {temp:.1f}°F"
  Text: 0,30,1,"Dewpoint: {dew:.1f}°F"
  Text: 0,45,1,"Wind: {wind_dir} @ {wind_speed:.1f} mph"
  Text: 0,60,1,"Updated: {now}"
End:
"""
    with open(PLACEFILE_PATH, "w") as f:
        f.write(content)

    print(f"✅ Wrote updated placefile: {PLACEFILE_PATH}")


if __name__ == "__main__":
    try:
        # ✅ FIXED unpacking: get all four return values
        temp, dew, wind_speed, wind_dir = get_weather_data()
        write_placefile(temp, dew, wind_speed, wind_dir)
    except Exception as e:
        print(f"Error: {e}")
