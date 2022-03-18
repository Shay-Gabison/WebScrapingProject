from tldextract import extract
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os.path
import TxtManipulation
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def replaceFileName(name):
    name = name.replace("!", "_")
    name = name.replace("@", "_")
    name = name.replace("#", "_")
    name = name.replace("$", "_")
    name = name.replace("%", "_")
    name = name.replace("?", "_")
    name = name.replace("^", "_")
    name = name.replace("*", "_")
    name = name.replace("<", "_")
    name = name.replace(">", "_")
    name = name.replace("{", "_")
    name = name.replace("}", "_")
    name = name.replace("/", "_")
    name = name.replace("+", "_")
    name = name.replace("=", "_")
    name = name.replace("|", "_")
    name = name.replace(":", "_")

    return name




class WebSite:
    CHROMEDRIVER_PATH = 'C:/Users/OWNER/PycharmProjects/webScrapingProject/venv/Lib/chromedriver.exe'
    hrefs = []
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",

        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)

    def __init__(self, url):
        self.url = str(url)
        self.driver.get(self.url)


class ArticalWebsite(WebSite):
    def __init__(self, url):
        super(ArticalWebsite, self).__init__(url)
        self.listclass = ["Irrelevant",
                          "Insensitive",
                          "sensitive",
                          "Extremely sensitive"]

    def checkFileExist(self, td):
        if os.path.exists(r'C:\Users\OWNER\Downloads\%s.json' % td) is not True:
            with open(r'C:\Users\OWNER\Downloads\%s.json' % td, "a") as file:
                json.dump({"name": td}, file)
                file.close()

    def checkArticlExist(self, td, name):
        new_name = '%s.pdf' % name
        with open(r'C:\Users\OWNER\Downloads\%s.json' % td, "r") as file:
            json_object = json.load(file)

        if new_name in json_object:
            file.close()
            return True
        file.close()
        return False

    def saveArticl(self, td, name):
        #search init
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec, laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()


        self.driver.execute_script(f'''document.title="{'%s.pdf' % name}";''')
        time.sleep(1)
        self.driver.execute_script('window.print();')
        with open(r'C:\Users\OWNER\Downloads\%s.json' % td, "r") as file:
            json_object = json.load(file)
            name = replaceFileName(name)
            json_object['%s.pdf' % name] = {}
            json_object['%s.pdf' % name]["url"] = self.driver.current_url
            temp=TxtManipulation.TxtManipulation(r'C:\Users\OWNER\Downloads',r'C:\Users\OWNER\Downloads\%s.json' % td)
            temp.sumerisingArticls('%s.pdf' % name)
            json_object['%s.pdf' % name]["Classification"] = self.listclass[temp.classifaingArticals('%s.pdf' % replaceFileName(name))]

            file.close()
        with open(r'C:\Users\OWNER\Downloads\%s.json' % td, "w") as file:
            json.dump(json_object, file)
            file.close()

    def process(self):
        tsd, td, tsu = extract(self.url)  # prints abc, hostname, com
        self.checkFileExist(td)
        actions = ActionChains(self.driver)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.block-link__overlay-link")))
        time.sleep(1)
        media_list = self.driver.find_elements(By.CSS_SELECTOR, "a.block-link__overlay-link")
        for idx, val in enumerate(media_list):
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.block-link__overlay-link")))
            time.sleep(0.5)
            media_list = self.driver.find_elements(By.CSS_SELECTOR, "a.block-link__overlay-link")
            item = media_list[idx]
            name = item.text
            if self.checkArticlExist(td, item.text):
                continue
            actions.move_to_element(item).perform()

            actions.move_to_element(item).click(item).perform()
            time.sleep(0.5)

            if EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Sign in")):
                self.driver.refresh()

            time.sleep(1)

            self.saveArticl(td, name)
            time.sleep(0.5)
            self.driver.execute_script("window.history.go(-1)")
        self.driver.quit()


class FlightWebsite(WebSite):
    def __init__(self, url):
        super(FlightWebsite, self).__init__(url)

        temp = self.url.split("flightType=")
        self.typeOfSite = temp[1]

    def openResults(self):
        actions = ActionChains(self.driver)
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, "next")))
        item = self.driver.find_elements(By.ID, "next")
        while item[0].aria_role != 'none':
            item = self.driver.find_elements(By.ID, "next")
            actions.move_to_element(item[0]).perform()
            actions.move_to_element(item[0]).click(item[0]).perform()

    def getData(self):

        table = self.driver.find_elements(By.CLASS_NAME, "flight_row")
        list1 = ["Airline company", "Flight", "Coming from", "Terminal", "Schedule time", "Estimated time", "Status"]
        if self.typeOfSite == "departures":
            list1[2] = "Departing To"
        dict = {}
        for row in range(len(table)):
            dict1 = {}
            str = table[row].text
            list2 = str.split("\n")
            for i in range(len(list1)):
                dict1[list1[i]] = list2[i]
            dict[row] = dict1
        return dict

    def saveData(self, dict):
        name = str(datetime.datetime.now()).replace(":", ".")
        name = str(name).replace("-", ".")
        with open(r'C:\Users\OWNER\Downloads\%s.json' % name
                , "w") as file:
            json.dump(dict, file)
            file.close()

    def process(self):
        FlightWebsite.openResults(self)
        dict = FlightWebsite.getData(self)
        FlightWebsite.saveData(self, dict)

    def changeUrl(self, url2):
        time.sleep(5)
        self.driver.get(url2)
        time.sleep(5)

        pass
