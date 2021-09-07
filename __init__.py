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
        return int(bsdoc.find("article")['id'].replace("Question-",""))
      else:
        print("Error: "+str(req.status_code))

  def convert_to_stripped(self, id):
    self.id = id
    self.subrefferer = "nmms-api/questions/"
    req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
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
        self.like = self._like()
      
      def reply(self,msg):
        self.subrefferer = "frage"
        myobj = {"query":"\n        \n    mutation CreateAnswer($answer: NewAnswer!) {\n      answer {\n        createAnswer: createAnswer(answer: $answer) {\n          id\n        }\n      }\n    }\n  \n\n        \n      ","variables":{"answer":{"questionId":self.id,"body":"<p>"+msg+"</p>","images":[]}}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return req2.text
        else:
          print(req2.status_code)
          print(req2.text)



      def info(self, *args):
          self.subrefferer = "nmms-api/questions/"
          req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
          jsontext = json.loads(req.text)
          if len(args) == 0:
            return jsontext
          else:
            for arg in args:
              return jsontext[arg]
          # elif data == "title":
          #   return jsontext["title"]
          # elif data == "id":
          #   return jsontext["id"]
          # elif data == "userid":
          #   return jsontext["userid"]
          # elif data == "stripped_title":
          #   return jsontext["stripped_title"]
          # elif data == "tag_ids":
          #   return jsontext["tag_ids"]



      def _like(self): 
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
    



  def new(self, amount: int):
    cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
    myobj = {"query":"\n        \n    query LatestQuestions(\n      $limit: Int!\n      $onlyUnanswered: Boolean!\n      $onlyResubmitted: Boolean!\n      $downCursor: StreamCursor\n      $ownUserId: Int!\n      $fromDateTime: OffsetDateTime\n    ) {\n      questions {\n        stream {\n          byLatestSubmission(\n            limit: $limit\n            onlyUnanswered: $onlyUnanswered\n            onlyResubmitted: $onlyResubmitted\n            downCursor: $downCursor\n            fromDateTime: $fromDateTime\n          ) {\n            questions {\n              ...Question\n            }\n            boundaries {\n              down {\n                cursor\n              }\n            }\n          }\n        }\n      }\n      userById(userId: $ownUserId) {\n        userInterests {\n          tag {\n            name\n            slug\n            questionFrequency\n          }\n        }\n      }\n    }\n  \n\n        \n    fragment Question on Question {\n      __typename\n      id\n      slug\n      title\n      htmlBody\n      upvotes\n      self {\n        hasUpvotedQuestion\n        hasBookmarkedQuestion\n      }\n      clarifications {\n        id\n        body\n        createdAt\n        isDeleted\n      }\n      questionTags {\n        tag {\n          id\n          name\n          normalizedTag\n          slug\n          questionFrequency\n        }\n        hidden\n        hiddenByUser {\n          slug\n          displayedName\n        }\n        creator {\n          slug\n          displayedName\n        }\n      }\n      questionStatus: status\n      isDeleted\n      isApprovedByAdmin\n      deletionInfo {\n        ...QuestionDeletionInfo\n      }\n      createdAt\n      answerCount\n      resubmissionCount\n      latestSubmission {\n        isResubmission\n        datetime\n        user {\n          id\n          nickname\n          displayedName\n          ...AuthorAvatar\n        }\n      }\n      poll {\n        choices {\n          id\n          text\n          voteCount\n        }\n      }\n      images {\n        id\n        urls {\n          big\n          thumbnail\n        }\n        webpUrls {\n          big\n          thumbnail\n        }\n      }\n      author {\n        ...Author\n        ...AuthorMods\n      }\n      mostHelpfulAnswerStatus\n      complaints {\n        ...Complaint\n      }\n      category {\n        ...Category\n      }\n      moderationAnnotations {\n        ...ModerationAnnotation\n      }\n    }\n  ,\n    fragment Author on User {\n      id\n      nickname\n      displayedName\n      createdAt\n      ...AuthorAvatar\n      roles\n      onlineStatus\n    }\n  ,\n    fragment AuthorMods on User {\n      complaints {\n        type\n      }\n    }\n  ,\n    fragment AuthorAvatar on User {\n      avatar {\n        urls {\n          default\n          nmmslarge\n        }\n        webpUrls {\n          default\n          nmmslarge\n        }\n      }\n    }\n  ,\n    fragment Complaint on Complaint {\n      createdAt\n      message\n      type\n      user {\n        displayedName\n        nickname\n      }\n    }\n  ,\n    fragment Category on HierarchicalCategory {\n      category {\n        name\n      }\n      parentCategories {\n        name\n      }\n    }\n  ,\n    fragment QuestionDeletionInfo on QuestionDeletion {\n      moderator {\n        nickname\n        displayedName\n      }\n      reason {\n        __typename\n        ... on QuestionDeletionCustomReason {\n          freetext\n        }\n        ... on QuestionDeletionPredefinedReason {\n          value\n        }\n      }\n    }\n  ,\n    fragment ModerationAnnotation on ModerationAnnotation {\n      id\n      user {\n        id\n        slug\n        displayedName\n      }\n      content\n      createdAt\n      leastRequiredRole\n      entityId\n      entity {\n        __typename\n        ... on User {\n          id\n          displayedName\n          slug\n        }\n        ... on Question {\n          id\n        }\n      }\n    }\n  \n      ","variables":{"onlyUnanswered":False,"onlyResubmitted":False,"limit":amount,"ownUserId":1}}

    subrefferer = "home/neue/alle"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}

    req_new = requests.post("https://www.gutefrage.net/graphql", headers=headers, json=myobj, cookies = cookies)
    parsed = json.loads(req_new.text)
    questions = parsed["data"]["questions"]["stream"]["byLatestSubmission"]["questions"]
    quests = []
    # print(json.dumps(questions, indent=4, sort_keys=True))
    for question in questions:
      quests.append(question)
    return quests
    # print(req_new.text)
    
