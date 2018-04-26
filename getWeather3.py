from bs4 import BeautifulSoup
import requests

class Weather(object):
    def __init__(self, time):
        self.time = time
        self.humidity = self.getHumidity()
        self.pressure = self.getPressure()
        self.visibility = self.getVisibility()
        self.windDir = self.getWind_Dir()
        self.windSpeed = self.getWind_Speed()
        self.conditions = self.getConditions()

    def getHumidity(self):
        t1 = self.time.contents[9]
        return t1.text

    def getPressure(self):
        t1 = self.time.contents[11]
        t2 = t1.contents[1]
        t3 = t2.contents[0]
        return t3.text

    def getVisibility(self):
        t1 = self.time.contents[13]
        t2 = t1.contents[1]
        t3 = t2.contents[0]
        return t3.text

    def getWind_Dir(self):
        t1 = self.time.contents[15]
        return t1.text

    def getWind_Speed(self):
        t1 = self.time.contents[17]
        t2 = t1.contents[1]
        t3 = t2.contents[0]
        return t3.text

    def getConditions(self):
        t1 = self.time.contents[25]
        return t1.text


def spiderShanghai(year, month, day):
    url = 'https://www.wunderground.com/history/airport/ZSSS/{0}/{1}/{2}/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='.format(
        str(year), str(month), str(day+1))
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')
    #timeTag = soup.find(text='Time ')
    #timeTagParent = timeTag.parent
    #tagTr = timeTagParent.parent

    if soup.find(text="4:30 PM") is not None:
        pm11_00 = soup.find(text="4:30 PM").parent.parent
        w_info = Weather(pm11_00)
        print(day)
        print(Weather(pm11_00))
        data = [(day, '4:30 PM', w_info.humidity, w_info.pressure, w_info.visibility,
                 w_info.windDir, w_info.windSpeed, w_info.conditions)]
        print(data)

    else:
        print(day)
        print('none')
        data = [(day, '4:30 PM', 'none', 'none', 'none', 'none', 'none', 'none')]
        print(data)


def spiderParis(year, month, day):
    url = 'https://www.wunderground.com/history/airport/LFPG/{0}/{1}/{2}/DailyHistory.html?&reqdb.zip=&reqdb.magic=&reqdb.wmo='.format(
        str(year), str(month), str(day))
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')
    #timeTag = soup.find(text='Time ')
    #timeTagParent = timeTag.parent
    #tagTr = timeTagParent.parent

    if soup.find(text="11:30 PM") is not None:
        pm11_00 = soup.find(text="11:30 PM").parent.parent
        w_info = Weather(pm11_00)
        print(day)
        print(Weather(pm11_00))
        data = [(day, '11:30 PM', w_info.humidity, w_info.pressure, w_info.visibility,
                 w_info.windDir, w_info.windSpeed, w_info.conditions)]
        print(data)

    else:
        print(day)
        print('none')
        data = [(day, '11:30 PM', 'none', 'none', 'none', 'none', 'none', 'none')]
        print(data)


def main():
    spiderParis(2018, 4, 5)
    spiderShanghai(2018, 4, 6)

if __name__ == "__main__":
    main()
