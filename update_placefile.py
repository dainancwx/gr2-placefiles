import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://agebb.missouri.edu/weather/realtime/ste_genevieve.asp"
OUTPUT_FILE = "mizzou_weather.txt"

r = requests.get(URL, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

def get_val(label):
    el = soup.find("td", string=lambda s: s and label in s)
    if el and el.find_next("td"):
        return el.find_next("td").get_text(strip=True)
    return "N/A"

temp = get_val("Air Temperature").split()[0]
dew = get_val("Dew Point").split()[0]
wind_dir = get_val("Wind Direction").split()[0]
wind_spd = get_val("Wind Speed").split()[0]

try:
    t = float(temp)
except:
    t = None

# --- choose GR2 color ---
if t is None:
    color = (200, 200, 200)      # gray
elif t <= 32:
    color = (0, 0, 255)          # blue
elif t <= 59:
    color = (0, 255, 0)          # green
elif t <= 84:
    color = (255, 255, 0)        # yellow
else:
    color = (255, 0, 0)          # red

r, g, b = color

placefile = f"""Title: Mizzou Weather Network
RefreshSeconds: 300
Color: 255 255 255
Font: 1, 11, 1, "Arial"

; Ste. Genevieve WX
Object: 37.981,-90.043
  Threshold: 999
  Icon: 0,0,2,1,1,""      ; built-in GR2 dot
  Color: {r} {g} {b}
  Text: -12,-12,1,"{temp}",255,0,0
  Text: -12,12,1,"{dew}",0,255,0
  Text: 12,0,1,"{wind_dir}{wind_spd}",255,255,255
End:

; Last updated: {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}
"""

with open(OUTPUT_FILE, "w") as f:
    f.write(placefile)

print("✅ Placefile updated.")
