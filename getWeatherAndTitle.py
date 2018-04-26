import requests
from bs4 import BeautifulSoup


def getTag(year, month, day):
    url = 'https://www.wunderground.com/history/airport/ZSSS/{0}/{1}/{2}/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='.format(
        str(year), str(month), str(day + 1))
    print(url)
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')
    timeTag = soup.find(text='Time ')
    timeTagParent = timeTag.parent
    tagTr = timeTagParent.parent
    return tagTr



def getWeather(year, month, day):
    url = 'https://www.wunderground.com/history/airport/ZSSS/{0}/{1}/{2}/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='.format(
        str(year), str(month), str(day + 1))
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.find(text='11:30 PM'))
    print(soup.find(text='<td >4:30 PM</td>'))
    if soup.find(text='4:30 PM') is not None:
        child = soup.find(text='4:30 PM')
        print(child)
        print(child.parent)
        pm11_00 = soup.find(text='4:30 PM').parent.parent
        print(pm11_00)
        return pm11_00
    else:
        return ''

