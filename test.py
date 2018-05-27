from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.request import urlopen
import urllib
from urllib import request
import os
import getpass
class FbScraper:
    def __init__(self, email, password, fb_name):
        option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(executable_path='C:/Users/ngoct/Downloads/chromedriver_win32/chromedriver', chrome_options=option)
        self.login(email, password)
    def __del__(self):
        self.driver.close()
    def login(self, email, password):
        self.driver.get('https://www.facebook.com/')
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('u_0_2').click()
    def getData(self,url):
        for urlT in url:
            data=self.colectData(urlT)
            # print(data["name"])
    def colectData(self, url):
        dataPersonal ={}
        link=url[:-10]+"/photos"
        name=url[25:-10]
        self.driver.get(link)
        # workPlace=self.driver.find_element_by_id("//*[@id='u_y_0']")
        #names
        images = self.driver.find_elements_by_tag_name("img")
        count=0
        if not os.path.exists(name):
            os.makedirs(name)
        for image in images:
            src = image.get_attribute("src")
            urllib.request.urlretrieve(src,".\\"+name+"\im"+str(count)+".png")
            count+=1
    def find_links(self, fb_name):
        self.driver.get("https://www.facebook.com/search/people/?q="+ fb_name)
        links_element = self.driver.find_elements_by_xpath("//a[@class='_32mo']")
        names_element = self.driver.find_elements_by_xpath("//a[@class='_32mo']/span")
        links = [x.get_attribute("href") for x in links_element]
        names = [x.text for x in names_element]
        nicknames = []
        for link in links:
            nickname = link.replace("https://www.facebook.com/", "")
            nickname = nickname[:(len(nickname) - 10)]
            if nickname[:(len(nickname) - 15)] == "profile.php?id=":
                # print(nickname[(len(nickname) - 15):])
                nickname = nickname[(len(nickname) - 15):]
            nicknames.append(nickname)
        return names, nicknames, links
#**********************************************************************************************************************************************
class LinkedInScraper:
    def __init__(self, email, password, fb_name):
        option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(executable_path='C:/Users/ngoct/Downloads/chromedriver_win32/chromedriver', chrome_options=option)
        self.login(email, password)
    def __del__(self):
        self.driver.close()
    def login(self, email, password):
        self.driver.get('https://www.linkedin.com/')
        self.driver.find_element_by_id('login-email').send_keys(email)
        self.driver.find_element_by_id('login-password').send_keys(password)
        self.driver.find_element_by_id('login-submit').click()
    def getData(self,url):
        totalPeople={}
        listName={}
        for urlT in url:
            data=self.colectData(urlT)
            # print(data["name"])
            if ( (data["name"].lower()+"1") in totalPeople ):
                # print(data["name"])
                newName=data["name"].lower()+str(listName[data["name"].lower()])
                listName[data["name"].lower()]+=1
                totalPeople[newName]=data
            else:
                totalPeople[data["name"].lower()+"1"]=data
                listName[data["name"].lower()]=2
        return totalPeople
    def colectData(self, url):
        dataPersonal ={}
        self.driver.get(url)
        for box in self.driver.find_elements_by_xpath('//*[@id="profile-content"]'):
            name=""
            loc=""
            pos=""
            try:
                name=box.find_element_by_xpath("//h1[@class='pv-top-card-section__name Sans-26px-black-85%']").text
                loc=box.find_element_by_xpath("//h3[@class='pv-top-card-section__location Sans-17px-black-55%-dense mt1 inline-block']").text
                pos=box.find_element_by_xpath("//h2[@class='pv-top-card-section__headline mt1 Sans-19px-black-85%']").text
            except Exception as e:
                if (name==""):
                    name="unknown"
                if(loc==""):
                    loc="unknown"
                if(pos==""):
                    pos="unknown"
            dataPersonal['name'] = name
            dataPersonal['location'] = loc
            dataPersonal['job'] = pos
        for box in self.driver.find_elements_by_xpath('//*[@id="education-section"]'):
            education=[]
            for name in box.find_elements_by_xpath("//h3[@class='pv-entity__school-name Sans-17px-black-85%-semibold']"):
                listTime=name.find_elements_by_xpath("//time")
                temp="From "
                time1=""
                time2=""
                try:
                    time1=listTime[0].text
                    time2=listTime[1].text
                    temp=temp+time1+" "+time2
                except Exception as e:
                    if(time1!=""):
                        time1="unknown"
                    if(time2!=""):
                        time2="unknown"
                education.append(name.text+" : "+temp)
            dataPersonal['education']=education
        exp=[]
        for box in self.driver.find_elements_by_xpath("//*[@id='experience-section']"):
            for name in box.find_elements_by_xpath("//div[@class='pv-entity__summary-info']"):
                valueName=name.text.split("\n")
                line1=name.find_element_by_xpath("//h3[@class='Sans-17px-black-85%-semibold']").text
                lines=name.find_element_by_xpath("//h4[@class='pv-entity__date-range inline-block Sans-15px-black-70%']")
                valueName=valueName+lines.text.split("\n")
                exp.append(valueName)
            dataPersonal['experience']=exp
        return dataPersonal
    def find_links(self, lk_name):
        self.driver.get("https://www.linkedin.com/search/results/people/?keywords="+ lk_name)
        links_element = self.driver.find_elements_by_xpath("//div[@class='search-result__info pt3 pb4 ph0']/a")
        names_element = self.driver.find_elements_by_xpath("//span[@class='name actor-name']")
        positions_element = self.driver.find_elements_by_xpath("//p[@class='subline-level-1 Sans-15px-black-85% search-result__truncate']")
        locations_element = self.driver.find_elements_by_xpath("//p[@class='subline-level-2 Sans-13px-black-55% search-result__truncate']")
        links = [x.get_attribute("href") for x in links_element]
        names = [x.text for x in names_element]
        positions = [x.text for x in positions_element]
        locations = [x.text for x in locations_element]
        nicknames = []
        for link in links:
            nickname = link.replace("https://www.linkedin.com/in/", "")
            nicknames.append(nickname[:(len(nickname) - 1)])
        return names, nicknames, positions, locations, links
#********************************************************************************************************************************************
def showResults(data):
    print(data.keys())
    name=input("enter the 1st name of who you want to see:\n")
    name=name.lower()
    count=0
    it=""
    for i in data.keys():
        if(len(name)<len(i)):
            if(name==i[: -(len(i)-len(name))]):
                count+=1
                it=i
                print("["+i+"]",end=" ")
    print()
    while (count>1):
        count=0
        partName=input("enter next part of the name:\n")
        name+=" "+partName
        for i in data.keys():
            if(name==i[: -(len(i)-len(name))]):
                count+=1
                it=i
                print("["+i+"]",end=" ")
    print()
    print(data[it].keys())
    command=""
    while (command!="exit"):
        print(data[it].keys())
        command=input("what do you want to know:?(type exit to get out)\n")
        if(command=="experience"):
                dem=0
                for query in data[it][command]:
                    for value in query:
                        dem+=1
                        if (dem==1):
                            print(value)
                        elif (dem%2==0):
                            print(value,end=": ")
                        else:
                            print(value)
                    print()
                    print("***************************")
        elif (command=="education"):
            dem=0
            for query in data[it][command]:
                dem+=1
                if (dem==1):
                    print(query)
                elif (dem%2==0):
                    print(query,end=": ")
                else:
                    print(query)
            print()
            print("***************************")
        else:
            print(data[it][command])
if __name__ == '__main__':
    # fb_user_email = str(input("Your Facebook email: "))
    # fb_user_password = getpass.getpass('Facebook password: ')
    # lk_user_email = str(input("Your LinkedIn email: "))
    # lk_user_password = getpass.getpass('Linked password: ')
    fb_user_email = "stalkerchan0211@gmail.com"
    fb_user_password = "ngoctien0211"
    lk_user_email = "stalkerchan0211@gmail.com"
    lk_user_password = "ngoctien0211"
    stalk_name = str(input("I'm stalker-chan, who do you to find: ")).replace(' ', '%20')
    # Facebook tracker
    fb_scraper = FbScraper(fb_user_email, fb_user_password, stalk_name)
    fb_names, fb_nicknames, fb_links = fb_scraper.find_links(stalk_name)
    for fb_name, fb_nickname, fb_link in zip(fb_names, fb_nicknames, fb_links):
        print("Fb: " + fb_name + ", " + fb_nickname + ", " + fb_link)
    fb_scraper.getData( fb_links)
    # LinkedIn Tracker
    # lk_scraper = LinkedInScraper(lk_user_email, lk_user_password, stalk_name)
    # lk_names, lk_nicknames, lk_positions, lk_locations, lk_links = lk_scraper.find_links(stalk_name)
    #
    # dataLinkedIn=lk_scraper.getData(lk_links)
    # showResults(dataLinkedIn)
    # for lk_name, lk_nickname, lk_position, lk_location, lk_link in zip(lk_names, lk_nicknames, lk_positions, lk_locations, lk_links):
    #     print("Lk: " + lk_name + ", " + lk_nickname + ", " + lk_position + ", " + lk_location + ", " + lk_link)
