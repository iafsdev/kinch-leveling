import reflex as rx
import requests
import os
from dotenv import load_dotenv

class AuthState(rx.State):
  load_dotenv()
  WCA_ID: str = os.environ.get("WCA_ID")
  WCA_SECRET: str = os.environ.get("WCA_SECRET")
  REDIRECT_URI: str = "http://localhost:3000/auth/"
  TOKEN_URL: str = "https://www.worldcubeassociation.org/oauth/token"
  ME_URL: str = "https://www.worldcubeassociation.org/api/v0/me"
  isLogin: bool = False
  code: str
  token: str
  wca_id: str
  
  @rx.event
  def callback(self):
    url = self.router.url
    self.code = url.split("code=")[-1] if "code=" in url else ""
    data = {
      'grant_type': "authorization_code",
      'code': self.code,
      'client_id': self.WCA_ID,
      'client_secret': self.WCA_SECRET,
      'redirect_uri': self.REDIRECT_URI
    }
    token_response = requests.post(self.TOKEN_URL, data=data)
    if token_response.status_code == 200:
      self.isLogin = True
      self.token = token_response.json().get('access_token')
      
      headers = {'Authorization': f'Bearer {self.token}'}
      me_response = requests.get(self.ME_URL, headers=headers)
      if me_response.status_code == 200:
        self.wca_id = me_response.json().get('me')['wca_id']
        
    print(self.wca_id)
    return rx.redirect('/')
  
  @rx.event
  def logout(self):
    self.isLogin = False
    self.token = ""
    self.wca_id = ""
    return rx.redirect('/')