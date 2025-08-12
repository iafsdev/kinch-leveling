import requests

class TnoodleAPI:
  def __init__(self):
    self.base_url = "http://172.19.128.1:2014/frontend/puzzle/"
    
  def get_scramble(self, category: str = '333') -> list[str]:
    body = {
      "B": "#0000ff",
      "D": "#ffff00",
      "F": "#00ff00",
      "L": "#ff8000",
      "R": "#ff0000",
      "U": "#ffffff"
    }
    response = requests.post(f"{self.base_url}{category}/scramble", json=body)
    if response.status_code == 200:
      return response.json().get('scramble', "Error")
    return "Error"
