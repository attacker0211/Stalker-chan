from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

    # LinkedIn Tracker
    lk_scraper = LinkedInScraper(lk_user_email, lk_user_password, stalk_name)
    lk_names, lk_nicknames, lk_positions, lk_locations, lk_links = lk_scraper.find_links(stalk_name)

    for lk_name, lk_nickname, lk_position, lk_location, lk_link in zip(lk_names, lk_nicknames, lk_positions, lk_locations, lk_links):
        print("Lk: " + lk_name + ", " + lk_nickname + ", " + lk_position + ", " + lk_location + ", " + lk_link)
