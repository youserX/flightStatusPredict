from bs4 import BeautifulSoup
import requests
import csv


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


def main():
    day = 3
    csvfile = open('weatherSH.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'time', 'Humidity', 'Pressure', 'Visibility', 'Wind Dir', 'Wind Speed', 'Conditions'])
    while day < 6:
        spider(day, writer)
        day = day + 1
    spider(7, writer)
    csvfile.close()

def spider(day, writer):
    url2 = 'https://www.wunderground.com/history/airport/ZSSS/2018/1/' + str(
        day) + '/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
    url = 'https://www.wunderground.com/history/airport/LFPG/2018/1/' + str(
        day) + '/DailyHistory.html?&reqdb.zip=&reqdb.magic=&reqdb.wmo='
    re = requests.get(url2)
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')

    # get the table colum name
    timeTag = soup.find(text='Time ')
    timeTagParent = timeTag.parent
    tagTr = timeTagParent.parent

    # get the weather between 11 to12
    if soup.find(text="5:30 PM") is not None:
        pm11_00 = soup.find(text="11:00 PM").parent.parent
        w_info = Weather(pm11_00)
        print(day)
        print(Weather(pm11_00))
        data = [(day, '5:30 PM', w_info.humidity, w_info.pressure, w_info.visibility,
                 w_info.windDir, w_info.windSpeed, w_info.conditions)]
        writer.writerows(data)

    else:
        print(day)
        print('none')
        data = [(day, '5:30 PM', 'none', 'none', 'none', 'none', 'none', 'none')]
        writer.writerows(data)

    # return Pm11_00,Pm11_30


if __name__ == "__main__":
    main()
