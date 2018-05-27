from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedInScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def getData(self, username, password,url):
        self.driver.get('https://www.linkedin.com/')
        self.driver.find_element_by_id('login-email').send_keys(username)
        self.driver.find_element_by_id('login-password').send_keys(password)
        self.driver.find_element_by_id('login-submit').click()
        totalPeople={}
        listName=[]
        for urlT in url:
            data=self.colectData(username, password,urlT)
            totalPeople[data["name"].lower()]=data
            listName.append(data["name"].lower())
        return totalPeople

    def __del__(self):
        self.driver.close()

    def colectData(self, username, password,url):
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

def showResults(data):
    print(data.keys())
    name=input("enter the 1st name of who you want to see:\n")
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


if __name__ == '__main__':
    scraper = LinkedInScraper()
    data=scraper.getData(username='ttestnum@gmail.com',
                              password='thisisapassword' ,
                              url=["https://www.linkedin.com/in/hungryzi/","https://www.linkedin.com/in/phanngoctien/","https://www.linkedin.com/in/soundslikeknock/"])


    # data: Name=>data
    #data: [['name', 'location', 'job',  'education', 'experience']]
    #       string    string      string  list         list
    showResults(data)
