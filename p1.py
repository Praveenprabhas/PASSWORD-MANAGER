class password_manager():
     """ This was developloped by vamshi krishna"""
     create_webdata={}
     create_appdata={}
     #webappdata=[]
     webappdata = [{"website_url":"https://www.google.com/","website_name":"google","username":"abc@gmail.com","password":"123"},{"website_url":"https://www.facebook.com/","website_name":"facebook","username":"xyz@gmail.com","password":"456"}]
     appdata=[]
     def home(self):
            print("welcome to password manager")
            print("1. create password")
            print("2. view password")
            print("3. change password")
            print("4. delete password")
            print("5. exit")
            #self.choose=int(input("enter your choice : "))
            self.choose=input("enter your choice : ")
            if self.choose=="1":
                  self.create_password()
            elif self.choose=="2":
                  self.view_password()
            elif self.choose=="3":
                  self.change_password()
            elif self.choose=="4":
                  self.delete_password()
            elif self.choose=="5":
                  print("exiting the password manager....")
                  exit()
            elif self.choose=="":
                  self.home()
            else:
                  print("invalid choice")
                  self.home()
    
     def create_password(self):
           print("this it the create password page")
           print("1. website")
           print("2. app")
           print("3. back")
           #self.choose=int(input("enter your choice : "))
           self.choose=input("enter your choice : ")
           if self.choose=="1":
                  self.create_web_password()
           elif self.choose=="2":
                  self.create_app_password()
           elif self.choose=="3":
                  self.home()
           elif self.choose=="":
                  self.create_password()
           else:
                  print("invalid choice")
                  self.create_password()
     # def create_web_password(self):
     #        weburl=input("enter website url : ")
     #        if len(weburl)==0:
     #               print("please enter a valid url")
     #               self.create_web_password()
     #        else:
     #           webname=input("enter website name : ")
     #           if len(webname)==0:
     #                print("please enter a valid name")
     #                self.create_web_password()
     #           else:
     #               username=input("enter username : ")
     #               if len(username)==0:
     #                    print("please enter a valid username")
     #                    self.create_web_password()
     #               else:
     #                   password=input("enter password : ")
     #                   if len(password)==0:
     #                        print("please enter a valid password")
     #                        self.create_web_password()
     #                   else:
     #                      self.create_webdata={"website_url":weburl,"website_name":webname,"username":username,"password":password}

     #        self.webappdata.append(self.create_webdata)
     #        # print(self.create_webdata)
     #        print("\n\nwebsite url : ",self.create_webdata["website_url"],"\nwebsite Name : ",self.create_webdata["website_name"],"\nUsername : ",self.create_webdata["username"],"\nPassword : ",self.create_webdata["password"])
     #        print("\nThis data was updated....\n\n")
     #        self.home()

     def create_web_password(self):
      while True:
        weburl = input("Enter website URL: ")
        if not weburl:
            print("Please enter a valid URL")
            continue
        webname = input("Enter website name: ")
        if not webname:
            print("Please enter a valid name")
            continue
        username = input("Enter username: ")
        if not username:
            print("Please enter a valid username")
            continue
        password = input("Enter password: ")
        if not password:
            print("Please enter a valid password")
            continue

        # If all inputs are valid, save the data
        self.create_webdata = {
            "website_url": weburl,
            "website_name": webname,
            "username": username,
            "password": password,
        }
        self.webappdata.append(self.create_webdata)
        print("\nWebsite details saved successfully!")
        break
      self.home()
      def get_input(self, prompt, error_message="Invalid input! Please try again."):
        while True:
            value = input(prompt).strip()
            if value:
               return value
            print(error_message)


     # def create_app_password(self):
     #        appname=input("enter App name : ")
     #        if len(appname)==0:
     #               print("please enter a valid app name")
     #               self.create_app_password()
     #        else:
     #         username=input("enter username : ")
     #         if len(username)==0:
     #              print("please enter a valid username")
     #              self.create_app_password()
     #         else:
     #          password=input("enter password : ")
     #          if len(password)==0:
     #               print("please enter a valid password")
     #               self.create_app_password()
     #          else:
     #           self.create_appdata={"app_name":appname,"username":username,"password":password}
     #        self.appdata.append(self.create_appdata)
     #        print("\n\nApp Name : ",self.create_appdata["app_name"],"\nUsername : ",self.create_appdata["username"],"\nPassword : ",self.create_appdata["password"])
     #        print("\nThis data was updated....\n\n")
     #        # print(self.appdata)
     #        # print(self.create_appdata.values())
     #        self.home()
     def create_app_password(self):
        while True:
            appname=input("enter App name : ")
            if not appname:
                   print("please enter a valid app name")
                   continue
            username=input("enter username : ")
            if not username:
                  print("please enter a valid username")
                  continue
            password=input("enter password : ")
            if not password:
                   print("please enter a valid password")
                   continue
            self.create_appdata={"app_name":appname,"username":username,"password":password}
            self.appdata.append(self.create_appdata)
            print("\n\nApp Name : ",self.create_appdata["app_name"],"\nUsername : ",self.create_appdata["username"],"\nPassword : ",self.create_appdata["password"])
            print("\nThis data was updated....\n\n")
            # print(self.appdata)
            # print(self.create_appdata.values())
            self.home()

     def view_password(self):
           print("this it the view password page")
           print("1. website")
           print("2. app")
           print("3. back")
           #self.choose=int(input("enter your choice : "))
           self.choose=input("enter your choice : ")
           if self.choose=="1":
                  self.vew_web_password()
           elif self.choose=="2":
                  self.view_app_password()
           elif self.choose=="3":
                  self.home()
           elif self.choose=="":
                  self.view_password()
           else:
                  print("invalid choice")
                  self.view_password()
     def vew_web_password(self):
           print("this is the view web password")
           websearch=input("enter website name : ")
           if len(websearch)==0:
               print("please enter a valid website name")
               self.vew_web_password()
           for i in range(len(self.webappdata)):
                if self.webappdata[i]["website_name"]==websearch:
                      print(self.webappdata[i])
           self.home()


     def view_app_password(self):
           if len(self.appdata)==0:
                  print("no data found")
                  self.home()
           else:
                  self.appname = input("enter the app name : ")
                  for i in range(len(self.appdata)):
                       if(self.appname==self.appdata[i]["app_name"]):
            #      print(self.appdata[i]["app_name"])
              #      self.op=self.appdata[i]  self.op=self.appdata[i].values()
                  #      self.op=self.appdata[i]
                  #      print(self.op)
                         print(self.appdata[i])
                       break
                  else:
                       print("no such app found")
                  self.home()
           self.home()
     def change_password(self):
           print("this it the change password page")
           print("1. website")
           print("2. app")
           print("3. back")
           #self.choose=int(input("enter your choice : "))
           self.choose=input("enter your choice : ")
           if self.choose=="1":
                  self.change_web()
           elif self.choose=="2":
                  self.change_app()
           elif self.choose=="3":
                  self.home()
           elif self.choose=="":
                  self.change_password()
           else:
                  print("invalid choice")
                  self.change_password()

     def change_web(self):
           print("this is the change web page")
           webname=input("enter website name : ")
           tempweb=[]
           for i in range(len(self.webappdata)):
                if(webname==self.webappdata[i]["website_name"]):
                    tempweb.append(self.webappdata[i])
           print("names matching with your search are : ")         
           for i in range(len(tempweb)):
                print(i+1,")",tempweb[i])
           print("choose one of them and press enter")
           choose=int(input())
           select_web=tempweb[choose-1]
           print(select_web)

           for i in range(len(self.webappdata)):
                if(select_web == self.webappdata[i] ):
                    print("1.website url")
                    print("2.website name")
                    print("3.website username")
                    print("4.website password")
                    self.choose_web_change=input("enter your choice : ")
                    if self.choose_web_change=="1":
                         weburl=input("enter new url : ")
                         if len(weburl)==0:
                              print("please enter a valid url")
                              self.change_web()
                         else:
                              self.webappdata[i]["website_url"]=weburl
                    elif self.choose_web_change=="2":
                         webname=input("enter new name : ")
                         if len(webname)==0:
                              print("please enter a valid name")
                              self.change_web()
                         else:
                             self.webappdata[i]["website_name"]=webname
                    elif self.choose_web_change=="3":
                         webusername=input("enter new username : ")
                         if len(webusername)==0:
                              print("please enter a valid username")
                              self.change_web()
                         else:
                            self.webappdata[i]["username"]=webusername
                    elif self.choose_web_change=="4": 
                         webpassword=input("enter new password : ")
                         if len(webpassword)==0:
                              print("please enter a valid password")
                              self.change_web()
                         else:
                           self.webappdata[i]["password"]=webpassword
                    elif self.choose_web_change=="":
                         print("entered value should be atleast 1 value")   

                    else:
                         print("invalid choice")
                         self.change_web()
                    print(self.webappdata[i])
                    break
                else:
                    continue

           else:
                print("no such website found")
           tempweb=[]
           self.home()
     def change_app(self):
           print("this is the change app page")
           appname=input("enter app name : ")
           tempapp=[]
           for i in range(len(self.appdata)):
                if(appname==self.appdata[i]["website_name"]):
                    tempapp.append(self.appdata[i])
           print("names matching with your search are : ")         
           for i in range(len(tempapp)):
                print(i+1,")",tempapp[i])
           print("choose one of them and press enter")
           choose=int(input())
           select_app=tempapp[choose-1]
           print(select_app)

           for i in range(len(self.webappdata)):
                if(select_app==self.webappdata[i]["app_name"]):
                    print("1.App name")
                    print("2.App username")
                    print("3.App password")
                    self.choose_web_change=input("enter your choice : ")
                    if self.choose_web_change=="1":
                         appname=input("enter new App name  : ")
                         if len(appname)==0:
                              print("please enter a valid App name")
                              self.change_app()
                         else:
                             self.appdata[i]["app_name"]=appname
                    elif self.choose_web_change=="2":
                         appusername=input("enter new App username : ")
                         if len(appusername)==0:
                              print("please enter a valid App username")
                              self.change_app()
                         else:
                             self.appdata[i]["username"]=appusername
                    elif self.choose_web_change=="3":
                         apppassword=input("enter new App password : ")
                         if len(apppassword)==0:
                              print("please enter a valid App password")
                              self.change_app()
                         else:
                             self.appdata[i]["password"]=apppassword
                    elif self.choose_web_change=="":
                         print("entered value should be atleast 1 value")   

                    else:
                         print("invalid choice")
                         self.change_web()
                    print(self.appdata[i])
                    break
           else:
                print("no such app found")
           tempapp=[]
           self.home()

     def delete_password(self):
           print("this it the delete password page")
           print("1. website")
           print("2. app")
           print("3. back")
           #self.choose=int(input("enter your choice : "))
           self.choose=input("enter your choice : ")
           if self.choose=="1":
                  self.delete_web()
           elif self.choose=="2":
                  self.delete_app()
           elif self.choose=="3":
                  self.home()
           elif self.choose=="":
                  self.delete_password()
           else:
                  print("invalid choice")
                  self.delete_password()

     def delete_web(self):
           print("this is the delete web page")
           delname=input("enter website name : ")
           tempweb=[]
           for i in range(len(self.webappdata)):
                if(delname==self.webappdata[i]["website_name"]):
                    tempweb.append(self.webappdata[i])
           print("names matching with your search are : ")         
           for i in range(len(tempweb)):
                print(i+1,")",tempweb[i])
           #print("choose one of them and press enter")
           choose=int(input("choose one of them and press enter : "))
           select_web=tempweb[choose-1]
           print(select_web)

           for i in range(len(self.webappdata)):
                if(select_web==self.webappdata[i]):
                        del self.webappdata[i]
                        print("deleted successfully")
                        break
           else:
                print("no such website found")

           tempweb=[]
           self.home()

     def delete_app(self):
           print("this is the delete app page")
           delname=input("enter app name : ")
           tempapp=[]
           for i in range(len(self.appdata)):
                if(delname==self.appdata[i]["website_name"]):
                    tempapp.append(self.appdata[i])
           print("names matching with your search are : ")         
           for i in range(len(tempapp)):
                print(i+1,")",tempapp[i])
           #print("choose one of them and press enter")
           choose=int(input("choose one of them and press enter : "))
           select_app=tempapp[choose-1]
           print(select_app)

           for i in range(len(self.appdata)):
                if(select_app==self.appdata[i]):
                        del self.appdata[i]
                        print("deleted successfully")
                        break
           else:
                print("no such app found")
           tempapp=[]
           self.home()

     def error():
          print("please enter a valid app name")
     def __init__(self):
           self.home()
           #print(self.choose)

def login():
   admin="admin"
   password="password"
   user_name=input("enter user name : ")
   if admin==user_name:
           pass_word=input("enter password : ")
           if password==pass_word:
                 mypass=password_manager()
           else:
                 print("wrong password")

print(password_manager.__doc__)
login()
#mypass=password_manager()