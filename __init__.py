import requests 
import json
from bs4 import BeautifulSoup


class gutefrage:

  def __init__(self, user, pwd):
      self.gutefrageusername = user
      self.gutefragepasswort = pwd
      self.subrefferer = ""
      self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}
      myobj = {"query":"\n        \n    mutation LoginWithUsernameOrEmail($emailOrUsername: String!, $password: String!) {\n      loginWithUsernameOrEmail(emailOrUsername: $emailOrUsername, password: $password) {\n        accessToken\n        refreshToken\n      }\n    }\n  \n\n        \n      ","variables":{"emailOrUsername":self.gutefrageusername,"password": self.gutefragepasswort}}
      req = requests.post("https://www.gutefrage.net/graphql", headers=self.headers, json=myobj)
      try:
          tokens = json.loads(req.text)
          self.accessToken = tokens["data"]["loginWithUsernameOrEmail"]["accessToken"]
          self.refreshToken = tokens["data"]["loginWithUsernameOrEmail"]["refreshToken"]
          self.user = self.gutefrageusername
          del self.gutefragepasswort
          del self.gutefrageusername
      except:
          tokens = req.text
          print("\033[31m\033[1mError: "+tokens)
      super(gutefrage, self).__init__()
  # def post(self):
  #     self.subrefferer = "frage_hinzufuegen"
  #     req = requests.post("https://www.gutefrage.net/graphql", headers=self.headers, cookies = {"gfAccessToken":self.accessToken,"gfRefreshToken":self.refreshToken})
  #     print(req.text)
  #May come back later. Post via the API

  def convert_to_id(self, url):
      self.subrefferer = "mitteilungen"
      req = requests.get("https://www.gutefrage.net/frage/"+url, headers = self.headers)
      if req.status_code == 200:
        content = req.content
        bsdoc = BeautifulSoup(content, 'html.parser')
        return bsdoc.find("article")['id'].replace("Question-","")
      else:
        print("Error: "+str(req.status_code))

  def convert_to_url(self, id):
    self.id = id
    self.subrefferer = "nmms-api/questions/"
    req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+self.id, headers = self.headers)
    jsontext = json.loads(req.text)
    self.id = self.id
    self.url = jsontext["stripped_title"]
    return self.url


  def question(self, id):
    return self._question(id, self.accessToken, self.refreshToken)
  
  class _question:
      def __init__(self, id, accessToken, refreshToken):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.id = id
        self.subrefferer = ""
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}


      def info(self):
          self.subrefferer = "nmms-api/questions/"
          req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+self.id, headers = self.headers)
          jsontext = json.loads(req.text)
          return jsontext
    

      def like(self): #Sadly for some reason doesn't work
        self.id = int(self.id)
        self.subrefferer = "mitteilungen"
        myobj = {"query":"\n        \n    mutation UpvoteQuestion($questionId: Int!) {\n      question {\n        upvotes: upvote(questionId: $questionId)\n      }\n    }\n  \n\n        \n      ","variables":{"questionId":self.id}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return "success"
        else:
          print(req2.status_code)
          print(req2.text)