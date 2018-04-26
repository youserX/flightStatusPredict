from bs4 import BeautifulSoup
import requests

def main():
    day = 1
    while day < 2:
        spider(day)
        day = day + 1

def getTemp(time):
    t1=time.contents[3]
    t2 = t1.contents[1]
    t3 = t2.contents[0]
    return  t3.text

def getWindchill(time):
    t1=time.contents[5]
    return t1.text


def getDew_Point(time):
    t1=time.contents[7]
    #t2 = t1.contents[1]
    #t3 = t2.contents[0]
    return len(t1)

def getHumidity(time):
    t1=time.contents[9]
    return  t1.text

def getPressure(time):
    t1 = time.contents[11]
    t2 = t1.contents[1]
    t3 = t2.contents[0]
    return t3.text

def getVisibility(time):
    t1 = time.contents[13]
    #t2 = t1.contents[1]
    #t3 = t2.contents[0]
    return t1

def getWind_Dir(time):
    t1 = time.contents[15]
    return t1.text

def getWind_Speed(time):
    t1 = time.contents[11]
    #t2 = t1.contents[0]
    #t3 = t2.contents[0]
    return t1

def getGust_Speed(time):
    t1 = time.contents[19]
    if t1.text == ' -':
        return t1.text



def spider(day):
    re = requests.get(
        'https://www.wunderground.com/history/airport/LFPG/2018/1/1/DailyHistory.html?&reqdb.zip=&reqdb.magic=&reqdb.wmo=')
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')

    # get the table colum name
    timeTag = soup.find(text='Time ')
    timeTagParent = timeTag.parent
    tagTr = timeTagParent.parent

    # get the weather between 11 to12
    Pm11_00 = soup.find(text="11:00 PM").parent.parent
    Temp00 = getTemp(Pm11_00)
    Windchill00 = getWindchill(Pm11_00)
    Dew_Point00 = getDew_Point(Pm11_00)
    Humidity00 = getHumidity(Pm11_00)

    Pressure00 = getPressure(Pm11_00)
    Visibility00 = getVisibility(Pm11_00)
    Wind_Dir00 = getWind_Dir(Pm11_00)
    Wind_Speed00 = getWind_Speed(Pm11_00)
    Gust_Speed00 = getGust_Speed(Pm11_00)
    Events00 = getWind_Speed(Pm11_00)
    Conditions00 = getWind_Speed(Pm11_00)

    Pm11_30 = soup.find(text="11:30 PM").parent.parent

    print(Wind_Speed00)
    # return Pm11_00,Pm11_30

if __name__ == "__main__":
    main()

