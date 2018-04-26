from flask import Flask, render_template, request, json, redirect
import getWeatherAndTitle as GWAT
import pandas as pd
import regression as rg
import weather_api
import NNpredict as np
app = Flask(__name__)
month = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

_windDri = {
            'North': 1, 'NNE': 2, 'NE': 3, 'ENE': 4,
            'East': 5, 'ESE': 6, 'SE': 7, 'SSE': 8,
            'South': 9, 'SSW': 10, 'SW': 11, 'WSW': 12,
            'West': 13, 'WNW': 14, 'NW': 15, 'NNW': 16
        }

no_to_wind = {
            1: 'North', 2: 'NNE', 3: 'NE', 4: 'ENE',
            5: 'East', 6: 'ESE', 7: 'SE', 8: 'SSE',
            9: 'South', 10: 'SSW', 11: 'SW', 12: 'WSW',
            13: 'West', 14: 'WNW', 15: 'NW', 16: 'NNW'
        }


@app.route('/')
def main():
    return render_template('ShowPage.html')


@app.route('/calculate', methods=['post'])
def calculate():
    try:
        _location = request.form['inputLocation']
        _destination = request.form['inputDestination']
        _date = request.form['pickedDate']

        if _location != 'Paris':
            return render_template('error.html', error=str(_location + 'is not access for prediction!'))
        else:
            if _destination != 'Shanghai':
                return render_template('error.html', error=str(_destination + 'is not access for prediction!'))
            else:
                if _date:
                    _dateSplited = _date.split()
                    print(_dateSplited)
                    _day = _dateSplited[0]
                    _DMonth = month[_dateSplited[1]]
                    _year = _dateSplited[2]
                    _tomorrow = int(_day) + 1
                    _tag = GWAT.getTag(_year, _DMonth, _tomorrow)
                    print(_tag)
                    _wea = GWAT.getWeather(_year, _DMonth, _tomorrow)
                    print(_wea)

                else:
                    _new_date = weather_api.get_date()
                    _paris_factors = weather_api.paris_weather()
                    _shanghai_factors = weather_api.shanghai_weather()
                    print('-------------shang hai--------------')
                    print(_shanghai_factors)
                    print('------------new dates --------------')
                    print(_new_date)
                    pr_result_of_Paris = rg.getRidgeResult(_location, _paris_factors)
                    land_corp_of_p = np.MLPLandStatus(_location, _paris_factors)
                    print(land_corp_of_p)
                    land_c_a_p = get_corp_ave(land_corp_of_p)
                    pr_result_of_SH = rg.getRidgeResult(_destination, _shanghai_factors)
                    land_corp_of_s = np.MLPLandStatus(_destination, _shanghai_factors)
                    land_c_a_s = get_corp_ave(land_corp_of_s)
                    print('-----------------------------------------')
                    return render_template('result3.html', dt=_new_date, corp_p=land_c_a_p, corp_s=land_c_a_s,
                                           p_SH=pr_result_of_SH, p_Paris=pr_result_of_Paris,
                                           factors_SH=_shanghai_factors, factors_Paris=_paris_factors, wind=no_to_wind)
    except Exception as e:
        return render_template('error.html', error=str(e))


def get_corp_ave(land_corp_of_p):
    status_av = [0, 0]
    for y in land_corp_of_p:
        status_av[0] = status_av[0] + round(y[0], 6) / 3
        status_av[1] = status_av[1] + round(y[1], 6) / 3
    print(status_av)
    return status_av


@app.route('/calculate2', methods=['post'])
def calculate2():
    _Humidity = []
    _Pressure = []
    _Visibility = []
    _Wind_DirN = []
    _Wind_Speed = []
    try:
        _location = request.form['inputLocation']
        _destination = request.form['inputDestination']
        _Humidity.append(int(request.form['Humidity']))
        print(_Humidity)
        _Pressure.append(int(request.form['Pressure']))
        print(_Pressure)
        _Visibility.append(int(request.form['Visibility']))
        print(_Visibility)
        _Wind_Dir = request.form['Wind_Dir']
        print(_Wind_Dir)
        _Wind_DirN.append(_windDri[_Wind_Dir])
        print(_Wind_DirN)
        _Wind_Speed.append(int(request.form['Wind_Speed']))
        print(_Wind_Speed)
        _factor = pd.DataFrame({"Humidity": _Humidity, "Pressure": _Pressure, "Visibility": _Visibility,
                                'Wind Dir': _Wind_DirN, 'Wind Speed': _Wind_Speed})
        print(_factor)
        print('-------2333--------2333---------')
        if _location != 'Paris':
            return render_template('error.html', error=str(_location + 'is not access for prediction!'))
        else:
            if _destination != 'Shanghai':
                return render_template('error.html', error=str(_destination + 'is not access for prediction!'))
            else:
                pr_result_of_Paris = rg.getRidgeResult(_location, _factor)
                print(pr_result_of_Paris)
                pr_result_of_SH = rg.getRidgeResult(_destination, _factor)
                print('-----------------------------------------')
                return render_template('result2.html', SH=pr_result_of_SH, Paris=pr_result_of_Paris, fa=_factor, wind=no_to_wind)
    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run()
