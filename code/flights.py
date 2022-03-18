import Website
import time

url1 = "https://www.iaa.gov.il/en/airports/ben-gurion/flight-board/?flightType=departures"
url2 = "https://www.iaa.gov.il/en/airports/ben-gurion/flight-board/?flightType=arrivals"
dep = Website.FlightWebsite(url1)
while True:
    dep.process()
    dep.changeUrl(url2)
    dep.process()
    time.sleep(60)
    dep.changeUrl(url1)
