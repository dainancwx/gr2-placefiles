import requests
import re
from datetime import datetime

# URL of the Missouri weather station
URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"

# Output placefile name
PLACEFILE = "mizzou_weather.txt"

# Function to scrape and parse data
def get_weather_data():
    response = requests.get(URL)
    text = response.text

    # Clean up weird spacing and encoding
    clean_text = re.sub(r'\s+', ' ', text)
    clean_text = clean_text.replace("Â", "")

    # Extract key fields
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

# Pick icon color based on temperature
def choose_icon(temp):
    if temp >= 85:
        return "RedDot.png"
    elif temp >= 70:
        return "YellowDot.png"
    elif temp >= 50:
        return "GreenDot.png"
    else:
        return "BlueDot.png"

# Generate placefile content
def create_placefile(temp, dew, wind_speed, wind_dir):
    icon = choose_icon(temp)
    lat, lon = 37.935415, -90.132342

    content = f"""; Missouri Weather Station Placefile
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
    return content

# Main execution
if __name__ == "__main__":
    temp, dew, wind_speed, wind_dir = get_weather_data()
    placefile_text = create_placefile(temp, dew, wind_speed, wind_dir)

    with open(PLACEFILE, "w", encoding="utf-8") as f:
        f.write(placefile_text)

    print(f"✅ Wrote updated placefile: {PLACEFILE}")
    print(f"🌡 Temp: {temp}°F | Dew: {dew}°F | Wind: {wind_dir} {wind_speed} mph")
