from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import operator
import requests
import json
import twitter
import getpass
import os
from urllib.request import urlopen
import urllib
from urllib import request

class FbScraper:
    def __init__(self, email, password, fb_name):
        # option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()
        self.login(email, password)

    def __del__(self):
        self.driver.close()

    def login(self, email, password):
        self.driver.get('https://www.facebook.com/')
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('u_0_2').click()

    def find_links(self, fb_name):
        self.driver.get("https://www.facebook.com/search/people/?q="+ fb_name)
        links_element = self.driver.find_elements_by_xpath("//a[@class='_32mo']")
        names_element = self.driver.find_elements_by_xpath("//a[@class='_32mo']/span")
        links = [x.get_attribute("href") for x in links_element]
        names = [x.text for x in names_element]
        nicknames = []
        for link in links:
            nick_temp = link.replace("https://www.facebook.com/", "")
            nickname = ""
            print(nick_temp[:15])
            if nick_temp[:15] == "profile.php?id=":
                print(nick_temp[15:])
                nick_temp= nick_temp[15:]
                for i in nick_temp:
                    if i == '&':
                        break
                    else:
                        nickname += i
            else:
                for i in nick_temp:
                    if i == '?':
                        break
                    else:
                        nickname += i
            nicknames.append(nickname)
        return names, nicknames, links

    def getData(self,name, urls):
        for url in urls:
            data=self.downloadImage(url)

            # print(data["name"])

    def downloadImage(self,name, url):
        dataPersonal ={}
        link=url[:-10]+"/photos"
        self.driver.get(link)
        # workPlace=self.driver.find_element_by_id("//*[@id='u_y_0']")
        #names
        images = self.driver.find_elements_by_tag_name("img")
        count=0
        if not os.path.exists(name):
            os.makedirs(name)
        for image in images:
            try:
                src = image.get_attribute("src")
                urllib.request.urlretrieve(src,".\\"+name+"\im"+str(count)+".png")
                count+=1
            except Exception:
                pass

class LinkedInScraper:
    def __init__(self, email, password, lk_name):
        # option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()
        self.login(email, password)

    def __del__(self):
        self.driver.close()

    def login(self, email, password):
        self.driver.get('https://www.linkedin.com/')
        self.driver.find_element_by_id('login-email').send_keys(email)
        self.driver.find_element_by_id('login-password').send_keys(password)
        self.driver.find_element_by_id('login-submit').click()

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



class GithubScraper:
    def __init__(self, email, password, gh_name):
        # option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()
        self.login(email, password)

    def __del__(self):
        self.driver.close()

    def login(self, email, password):
        self.driver.get('https://github.com/login')
        self.driver.find_element_by_id('login_field').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_xpath("//*[@id='login']/form/div[3]/input[3]").click()

    def find_links(self, gh_name):
        self.driver.get("https://github.com/search?q="+ gh_name + "&type=Users")
        links_element = self.driver.find_elements_by_xpath("//div[@class='user-list-info ml-2']/a")
        links = [x.get_attribute("href") for x in links_element]
        nicknames = []
        for link in links:
            nickname = link.replace("https://github.com/", "")
            nicknames.append(nickname)
        return nicknames, links

    def find_projects(self, gh_name):
        # github_id = str(input("Your github id: "))
        self.driver.get("https://github.com/"+ gh_name)

        titles_element = self.driver.find_elements_by_xpath("//a[@class='text-bold']")
        titles = [x.text for x in titles_element]
        language_element = self.driver.find_elements_by_xpath("//p[@class='mb-0 f6 text-gray']")
        languages = [x.text for x in language_element]

        print('titles:')
        print(titles, '\n')
        print("languages:")
        print(languages, '\n')

        for title, language in zip(titles, languages):
            print("Repositories name : Language")
            print(title + ": " + language, '\n')


class TwitterScraper:
    def __init__(self, email, password, tt_name):
        # option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()
        self.login(email, password)

    def __del__(self):
        self.driver.close()

    def login(self, email, password):
        self.driver.get('https://twitter.com/login')
        self.driver.find_element_by_xpath("//*[@id='page-container']/div/div[1]/form/fieldset/div[1]/input").send_keys(email)
        self.driver.find_element_by_xpath("//*[@id='page-container']/div/div[1]/form/fieldset/div[2]/input").send_keys(password)
        self.driver.find_element_by_xpath("//*[@id='page-container']/div/div[1]/form/div[2]/button").click()

    def find_links(self, tt_name):
        self.driver.get("https://twitter.com/search?f=users&vertical=default&q="+ tt_name)
        links_element = self.driver.find_elements_by_xpath("//a[@class='fullname ProfileNameTruncated-link u-textInheritColor js-nav']")
        nicknames_element = self.driver.find_elements_by_xpath("//b[@class='u-linkComplex-target']")
        links = [x.get_attribute("href") for x in links_element]
        names = [x.text for x in links_element]
        nicknames = [x.text for x in nicknames_element]
        return names, nicknames, links

    def analyze(handle):
        twitter_consumer_key = ''
        twitter_consumer_secret = ''
        twitter_access_token = ''
        twitter_access_secret = ''

        twitter_api = twitter.Api(consumer_key = twitter_consumer_key,
                        consumer_secret = twitter_consumer_secret,
                        access_token_key = twitter_access_token,
                        access_token_secret = twitter_access_secret)

        statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
        text = ""
        for s in statuses:
            if (s.lang == 'en'):
                text += str(s.text.encode('utf-8'))

        # pi_result = PersonalityInsights(username="51436b66-0914-4989-9609-10b378b5ff3b", password="mC3iaLrPhYZ1").profile(text)
        # return pi_result
        return text
def showData(data):
    print(data.keys())
    command=input("what do you want to know:?(type exit to get out)\n")
    if(command=="experience"):
            dem=0
            for query in data[command]:
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
    if (command=="education"):
        dem=0
        for query in data[command]:
            dem+=1
            if (dem==1):
                print(query)
            elif (dem%2==0):
                print(query,end=": ")
            else:
                print(query)
        print()
        print("***************************")

def showResults(data):
    print(data.keys())
    name=input("Enter the 1st name of who you want to see:\n")
    name=name.lower()
    count=0
    it=""
    for i in data.keys():
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
        if (command=="education"):
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
def stalkFacebook(fb_user_email,fb_user_password,stalk_name):
    fb_scraper = FbScraper(fb_user_email, fb_user_password, stalk_name)
    fb_names, fb_nicknames, fb_links = fb_scraper.find_links(stalk_name)
    for fb_name, fb_nickname, fb_link in zip(fb_names, fb_nicknames, fb_links):
        print("Fb: " + fb_name + ", " + fb_nickname + ", " + fb_link)
        downI=input("download Image of this person(y/n)?")
        if (downI=="y"):
            fb_scraper.downloadImage(fb_nickname, fb_link)

def stalkLinkedIn(lk_user_email, lk_user_password, stalk_name):
    lk_scraper = LinkedInScraper(lk_user_email, lk_user_password, stalk_name)
    lk_names, lk_nicknames, lk_positions, lk_locations, lk_links = lk_scraper.find_links(stalk_name)

    for lk_name, lk_nickname, lk_position, lk_location, lk_link in zip(lk_names, lk_nicknames, lk_positions, lk_locations, lk_links):
        print("Lk: " + lk_name + ", " + lk_nickname + ", " + lk_position + ", " + lk_location + ", " + lk_link + "\n")
        choice = input("Do you want to retrieve data of this person: (yes (y)/no (n)/break (b))?")
        if choice == 'y':
            showData(lk_scraper.colectData(lk_link))

        elif choice == 'b':
            break
    dataLinkedIn=lk_scraper.getData(lk_links)
    return dataLinkedIn

def stalkTwitter(tt_user_email,tt_user_password,stalk_name):
    # Twitter tracker
    tt_scraper = TwitterScraper(tt_user_email, tt_user_password, tt_stalk_name)
    tt_names, tt_nicknames, tt_links = tt_scraper.find_links(tt_stalk_name)
    for tt_name, tt_nickname, tt_link in zip(tt_names, tt_nicknames, tt_links):
        print("Tt: " + tt_name + ", " + tt_nickname + ": " + tt_link)
        choice = input("Do you want to retrieve all tweets of this person: (yes (y)/no (n)/break (b))?")
        if choice == 'y':
            tt_scraper.analyze(tt_nickname)
        elif choice == 'b':
            break


def stalkGithub(gh_user_email,gh_user_password,stalk_name):
    # Github tracker
    gh_scraper = GithubScraper(gh_user_email, gh_user_password, gh_stalk_name)
    gh_nicknames, gh_links = gh_scraper.find_links(gh_stalk_name)
    for gh_nickname, gh_link in zip(gh_nicknames, gh_links):
        print("Gh: " + gh_nickname + ": " + gh_link)
        choice = input("Do you want to retrieve all projects of this person: (yes (y)/no (n)/break (b))?")
        if choice == 'y':
            gh_scraper.find_projects(gh_nickname)
        elif choice == 'b':
            break

if __name__ == '__main__':
    # Input user email and password
    # fb_user_email = str(input("Your Facebook email: "))
    # fb_user_password = getpass.getpass('Facebook password: ')
    # lk_user_email = str(input("Your LinkedIn email: "))
    # lk_user_password = getpass.getpass('Linked password: ')
    # gh_user_email = str(input("Your Github email: "))
    # gh_user_password = getpass.getpass('Github password: ')
    # tt_user_email = str(input("Your Twitter email: "))
    # tt_user_password = getpass.getpass('Twitter password: ')

    # Specifying accounts to stalk (default)

    fb_user_email = "stalkerchan0211@gmail.com"
    fb_user_password = "ngoctien0211"
    lk_user_email = "stalkerchan0211@gmail.com"
    lk_user_password = "ngoctien0211"
    gh_user_email = "stalkerchan0211@gmail.com"
    gh_user_password = "ngoctien0211"
    tt_user_email = "stalkerchan0211@gmail.com"
    tt_user_password = "ngoctien0211"
    stalk_name = str(input("I'm stalker-chan, who do you to find: "))
    fb_stalk_name = stalk_name.replace(' ', '%20')
    lk_stalk_name = stalk_name.replace(' ', '%20')
    gh_stalk_name = stalk_name.replace(' ', '+')
    tt_stalk_name = stalk_name.replace(' ', '%20')

    choice = str(input("Choose your platform to stalk Linked/Facebook/Github/Twitter (l/f/g/t): "))

    while choice != "exit":
        if choice == 'f':
            stalkFacebook(fb_user_email,fb_user_password,stalk_name)
            choice = str(input("Choose your platform to stalk Linked/Facebook/Github/Twitter (l/f/g/t): "))
        elif choice == 'l':
            dataLinkedIn=stalkLinkedIn(lk_user_email, lk_user_password, stalk_name)
            choice = str(input("Choose your platform to stalk Linked/Facebook/Github/Twitter (l/f/g/t): "))
        elif choice == 'g':
            stalkGithub(gh_user_email, gh_user_password, stalk_name)
            choice = str(input("Choose your platform to stalk Linked/Facebook/Github/Twitter (l/f/g/t): "))
        elif choice == 't':
            stalkTwitter(tt_user_email, tt_user_password, stalk_name)
            choice = str(input("Choose your platform to stalk Linked/Facebook/Github/Twitter (l/f/g/t): "))
        else:
            pass
    # Facebook tracker

    # LinkedIn Tracker



    # fb_scraper.getData(fb_links)
    showResults(dataLinkedIn)
