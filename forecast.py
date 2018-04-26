import json
content = {"HeWeather6":[{"basic":{"cid":"FR2988507","location":"Paris","admin_area":"","cnty":"France","lat":"48.85340881","lon":"2.34879994","tz":"+1.00"},"update":{"loc":"2018-04-10 22:46","utc":"2018-04-10 21:46"},"status":"ok","daily_forecast":[{"cond_code_d":"103","cond_code_n":"103","cond_txt_d":"Partly Cloudy","cond_txt_n":"Partly Cloudy","date":"2018-04-10","hum":"76","mr":"04:52","ms":"14:23","pcpn":"0.0","pop":"0","pres":"998","sr":"07:10","ss":"20:34","tmp_max":"16","tmp_min":"11","uv_index":"3","vis":"20","wind_deg":"150","wind_dir":"SE","wind_sc":"3-4","wind_spd":"13"},{"cond_code_d":"103","cond_code_n":"103","cond_txt_d":"Partly Cloudy","cond_txt_n":"Partly Cloudy","date":"2018-04-11","hum":"70","mr":"05:25","ms":"15:26","pcpn":"0.0","pop":"0","pres":"1005","sr":"07:08","ss":"20:36","tmp_max":"19","tmp_min":"12","uv_index":"4","vis":"20","wind_deg":"120","wind_dir":"SE","wind_sc":"3-4","wind_spd":"13"},{"cond_code_d":"104","cond_code_n":"101","cond_txt_d":"Overcast","cond_txt_n":"Cloudy","date":"2018-04-12","hum":"84","mr":"05:53","ms":"16:31","pcpn":"0.0","pop":"0","pres":"1000","sr":"07:06","ss":"20:37","tmp_max":"15","tmp_min":"11","uv_index":"4","vis":"19","wind_deg":"15","wind_dir":"NE","wind_sc":"3-4","wind_spd":"13"}]}]}
json_content = json.dumps(content)
json_content2 = json.loads(json_content)
print(json_content)
print (type(json_content2))
forecast = json_content2['HeWeather6'][0]['daily_forecast']
i=0
while i<3:
    print(forecast[i]['date'])
    print(forecast[i]['hum'])
    print(forecast[i]['pres'])
    print(forecast[i]['wind_dir'])
    print(forecast[i]['wind_spd'])
    print(forecast[i]['vis'])
    i=i+1


