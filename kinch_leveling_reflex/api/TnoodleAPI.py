import requests
import re

class TnoodleAPI:
  def __init__(self):
    self.base_url = "http://172.19.128.1:2014/frontend/puzzle/"
    self.body_cube = {
      "B": "#0000ff",
      "D": "#ffff00",
      "F": "#00ff00",
      "L": "#ff8000",
      "R": "#ff0000",
      "U": "#ffffff"
    }
    self.body_sq1 = {
      "B": "#ff8000",
      "D": "#ffffff",
      "F": "#ff0000",
      "L": "#0000ff",
      "R": "#00ff00",
      "U": "#ffff00"
    }
    self.body_minx = {
      "U": "#ffffff",
      "BL": "#ffcc00",
      "BR": "#0000b3",
      "R": "#dd0000",
      "F": "#006600",
      "L": "#8a1aff",
      "D": "#999999",
      "DR": "#ffffb3",
      "DBR": "#ff99ff",
      "B": "#71e600",
      "DBL": "#ff8433",
      "DL": "#88ddff",
    }
    self.body_pyram = {
      "F": "#00FF00",
      "D": "#FFFF00",
      "L": "#FF0000",
      "R": "#0000FF",
    }

  def _normalize_svg(self, svg: str) -> str:
    """Normaliza solo los atributos width y height del tag <svg>, sin tocar stroke-width.

    Se usan lookbehinds para asegurarnos de no coincidir con "stroke-width".
    Además se convierte a porcentaje para que escale dentro del contenedor.
    """
    # Solo reemplazar width/height que NO están precedidos por '-'
    svg = re.sub(r'(?<!-)width="[^"]+px"', 'width="100%"', svg)
    svg = re.sub(r'(?<!-)height="[^"]+px"', 'height="100%"', svg)
    return svg

  def get_scramble(self, category: str = '333') -> tuple[str, str]:
    if category == 'minx':
      body = self.body_minx
    elif category == 'sq1':
      body = self.body_sq1
    elif category == 'pyram':
      body = self.body_pyram
    else:
      body = self.body_cube

    response = requests.post(f"{self.base_url}{category}/scramble", json=body)
    if response.status_code == 200:
      data = response.json()
      scramble = data.get("scramble", "")
      svg_image = data.get("svgImage", "")
      if svg_image:
        svg_image = self._normalize_svg(svg_image)
      return scramble, svg_image
    return "Error", ""
