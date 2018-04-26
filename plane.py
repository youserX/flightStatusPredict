#coding=utf-8
import urllib.request
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup
from pytesseract import image_to_string
import datetime
import os
import time
filename="cookies.txt"
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
plane_code=""
all_info=[]
date=""
cookies = http.cookiejar.MozillaCookieJar(filename)

#遍历两个时间段内的每一天
def getEveryDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

#设置cookie
def openner_cookie():
    # cookies=http.cookiejar.MozillaCookieJar(filename)
    handle=urllib.request.HTTPCookieProcessor(cookies)
    openner=urllib.request.build_opener(handle)
    return openner

#获取html中包含需要信息的航班
def get_simpleplane(url_link):
    html=openner_cookie().open(url_link)
    obj=BeautifulSoup(html.read(),"html.parser")
    plane_info=obj.find_all("",{"class":"fly_list"})
    return plane_info
#获取详细的航班信息，包括起终点，到达时间，以及是否准点
def get_detailplane(url_link):
    simplane_info=get_simpleplane(url_link)
    result_0=simplane_info[-1].find_all("",{"class":"li_com"})
    result_1=result_0[-1].get_text().splitlines()
    # result_2=result_1.readlines()
    url_list=image_url(url_link)

    down_image(url_list)
    number_info=distinguish()
    begin_area=result_1[13]
    begin_time=result_1[9]
    end_area=result_1[19]
    end_time=result_1[15]
    v_stime=number_info[0]
    v_etime=number_info[1]
    v_percent=number_info[2]
    detailinfo=[plane_code,begin_area,begin_time,end_area,end_time,v_stime,v_etime,v_percent]
    all_info.append(detailinfo)
    return all_info
#解析并生产图片地址，此图片地址有三个，分别为起飞和到达的实际时间以及准点率
def image_url(url_link):
    plane_info=get_simpleplane(url_link)
    content=plane_info[-1].find_all(name="img")
    url_list=[]
    x=0
    for con in content:
        con2=con.get("src")
        if "http" not in con2:
            url_end="http://www.variflight.com"+con2
            url_list.append(url_end)
            x=x+1
    return url_list
#识别图像中的数字
def distinguish():
    number_info = []
    for m in range(3):
        number_info.append(image_to_string(Image.open("D:\\plane_test\\%s\\%s\\%s.jpg"% (plane_code,date, m)),config=tessdata_dir_config))
    return number_info
# def save_path():
#     return ("D:\\plane_test\\%s")
#将图片下载到本地
def down_image(urllist):
    x=0
    for image_url in urllist:
        fp="D:\\plane_test\\%s\\%s\\%s.jpg"% (plane_code,date,x)
        with open(fp, "wb") as f:
            response = openner_cookie().open(image_url)
            f.write(response.read())
        x+=1
def generate_url(plane_code,date):
    url_link="http://www.variflight.com/flight/fnum/%s.html?AE71649A58c77&fdate=%s"% (plane_code,date)
    return url_link
#创建保存目录
def mk_planedirs(plane_code,date):
    os.makedirs("D:\\plane_test\\%s\\%s"% (plane_code,date))

#保存文件内容
def save_txt(txt_content):
    with open("D:\\plane_test\\%s\\%s.txt"% (plane_code,plane_code),"w") as f:
        f.write(txt_content)

if __name__ == '__main__':
    start=time.clock()
    plane_code="AF116"
    date_list=getEveryDay('2018-03-11', '2018-03-13')
    # plane_code=input("Please input the code of plane:\n")
    # start_date=input("please input the start date:\n")
    # end_date=input("please input the end date:\n")
    for dateday in date_list:
        date=dateday
        mk_planedirs(plane_code,date)
        url_link=generate_url(plane_code,date)
        detal_info=get_detailplane(url_link)
    print(all_info)
    save_txt(str(all_info))
    end=time.clock()
    print("Total time is %s" %(end-start))