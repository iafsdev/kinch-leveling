import reflex as rx
import requests
import os
from dotenv import load_dotenv
from kinch_leveling_reflex.api.api import create_new_profile, check_profile

class AuthState(rx.State):
  load_dotenv()
  WCA_ID: str = os.environ.get("WCA_ID")
  WCA_SECRET: str = os.environ.get("WCA_SECRET")
  REDIRECT_URI: str = "http://localhost:3000/auth/"
  TOKEN_URL: str = "https://www.worldcubeassociation.org/oauth/token"
  ME_URL: str = "https://www.worldcubeassociation.org/api/v0/me"
  code: str
  token: str = rx.Cookie(max_age=172800)  
  wca_id: str = rx.Cookie(max_age=172800)
  
  @rx.var
  def isLogin(self) -> bool:
    return True if self.wca_id else False
  
  @rx.event
  def login(self):
    return self.logout() if self.isLogin else rx.redirect('https://www.worldcubeassociation.org/oauth/authorize?client_id=VBetj_Bft05DLM40sQTY3EGpjv0N1IUYFMUL7TvGGIo&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth%2F&response_type=code&scope=public')
  
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

        if not check_profile(self.wca_id):
          create_new_profile(self.wca_id)
        
    return rx.redirect('/')
  
  @rx.event
  def logout(self):
    self.isLogin = False
    self.wca_id = ''
    return rx.redirect('/')