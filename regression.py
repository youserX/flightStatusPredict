import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


def main():
    weatherCSV = readParisW()
    weatherCSV2 = readSHW()
    #_factors = getAllFactors(weatherCSV2)
    #_results = getResult(weatherCSV2)
    _factors = getAllFactors(weatherCSV)
    _results = getResult(weatherCSV)
    linearRegression(_factors, _results)
    ridgeRegression(_factors, _results)
    lassoRegression(_factors, _results)

def getWindDri():
    _windDri = {
        'North': 1, 'NNE': 2, 'NE': 3, 'ENE': 4,
        'East': 5, 'ESE': 6, 'SE': 7, 'SSE': 8,
        'South': 9, 'SSW': 10, 'SW': 11, 'WSW': 12,
        'West': 13,  'WNW': 14, 'NW': 15, 'NNW': 16
    }
    return _windDri


def readParisW():
    #print('readParisW called')
    _parisW = pd.read_csv('D:\PythonWorkStation\FPWeb\weather2.csv')
    return _parisW


def readSHW():
    _shanghaiW = pd.read_csv('D:\PythonWorkStation\FPWeb\weatherSH.csv')
    return _shanghaiW

def getHeader(weatherCSV):
    # put the original column names in a python list
    original_headers = list(weatherCSV.columns.values)
    #print(original_headers)
    return original_headers


def getAllFactors(weatherCSV):
    factor = pd.DataFrame(weatherCSV, columns=['Humidity', 'Pressure', 'Visibility', 'Wind Dir', 'Wind Speed', 'Conditions'])
    #print(factor)

    _newHumidity = []
    for i, _Humidity in enumerate(factor.Humidity):
        _newHumidity.append(int(_Humidity.split("%")[0]))

    _newPressure = []
    for i, _Pressure in enumerate(factor.Pressure):
        _newPressure.append(int(_Pressure))

    _newVisibility = []
    for i, _Visibility in enumerate(factor.Visibility):
        _newVisibility.append(int(_Visibility))

    _windDri = getWindDri()
    _newWindDri = []
    for i, _wind in enumerate(factor['Wind Dir']):
        _newWindDri.append(_windDri[_wind])

    newFactor = pd.DataFrame({"Humidity": _newHumidity, "Pressure": _newPressure, "Visibility": _newVisibility,
                              'Wind Dir': _newWindDri, 'Wind Speed': factor['Wind Speed']})
    #print(newFactor)
    return newFactor


def getResult(weatherCSV):
    _result = pd.DataFrame(weatherCSV, columns=['Status', 'Time'])

    _newStatus = []
    for i, _Status in enumerate(_result.Status):
        if _Status == 'Delay':
            _newStatus.append(int(-1))
        else:
            _newStatus.append(int(1))
    #print(_newStatus)

    newTime = []
    for i, _Etime in enumerate(_result.Time):
        hours = int(_Etime.split(':')[0])
        minutes = int(_Etime.split(':')[1]) + hours * 60
        newTime.append(minutes*_newStatus[i])

    _newResult = pd.DataFrame({'Status': newTime})
    #print(_newResult)
    return _newResult


def getFlightStatus(weatherCSV):
    _result = pd.DataFrame(weatherCSV, columns=['Status'])

    _newStatus = []
    for i, _Status in enumerate(_result.Status):
        if _Status == 'Delay':
            _newStatus.append(int(0))
        else:
            _newStatus.append(int(1))
    # print(_newStatus)

    _newResult = pd.DataFrame({'Status': _newStatus})
    return _result, _newResult


def linearRegression(factors, results):
    X_train, X_test, y_train, y_test = train_test_split(factors, results, random_state=1)
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    print(linreg.intercept_)
    print(linreg.coef_)

    y_pred = linreg.predict(X_test)
    print('predict result')
    print(y_pred)
    print('actual result')
    print(y_test)
    print('---------------linear---------------')
    print("MSE:",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


def ridgeRegression(factors, results):
    X_train, X_test, Y_train, Y_test = train_test_split(factors, results, random_state=1)
    print(X_train.shape)
    print(Y_train.shape)
    print(X_test.shape)
    print(Y_test.shape)
    from sklearn import linear_model
    from sklearn.linear_model import RidgeCV
    ridgeReg = linear_model.Ridge(alpha=100)
    ridgeReg2 = RidgeCV(alphas=[0.01, 0.1, 0.5, 1, 3, 5, 7, 10, 20, 50, 100])
    ridgeReg.fit(X_train, Y_train)
    ridgeReg2.fit(X_train, Y_train)
    print(ridgeReg2.alpha_)
    Y_predict = ridgeReg.predict(X_test)
    new_y_pre = []
    for y in Y_predict:
        y1 = round(y[0])
        new_y_pre.append(y1)
    print('predict result')
    print(new_y_pre)
    print('actual result')
    print(Y_test)
    print('------------------ridge-----------------')
    print("MSE:",metrics.mean_squared_error(Y_test, Y_predict))
    print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(Y_test, Y_predict)))


def ridgeReg(factors, results):
    X_train, X_test, Y_train, Y_test = train_test_split(factors, results, random_state=1)
    #print(X_train.shape)
    #print(Y_train.shape)
    #print(X_test.shape)
    #print(Y_test.shape)
    from sklearn import linear_model
    ridgeReg = linear_model.Ridge(alpha=100)
    ridgeReg.fit(X_train, Y_train)
    return ridgeReg
    #Y_predict = ridgeReg.predict(X_test)
    #print('predict result')
    #print(Y_predict)
    #print('actual result')
    #print(Y_test)
    #print("MSE:",metrics.mean_squared_error(Y_test, Y_predict))
    #print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(Y_test, Y_predict)))



def lassoRegression(factors, results):
    X_train, X_test, Y_train, Y_test = train_test_split(factors, results, random_state=1)
    #print(X_train.shape)
    #print(Y_train.shape)
    #print(X_test.shape)
    #print(Y_test.shape)
    from sklearn.linear_model import Lasso
    lassoReg = Lasso(max_iter=10000, alpha=5)
    lassoReg.fit(X_train, Y_train)
    Y_predict = lassoReg.predict(X_test)
    print('predict result')
    print(Y_predict)
    print('actual result')
    print(Y_test)
    print('----------------lasso-------------')
    print("MSE:", metrics.mean_squared_error(Y_test, Y_predict))
    print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(Y_test, Y_predict)))


def getRidgeResult(loc, factor):
    #print('Ridge called')
    if loc =='Paris':
        #print('loc is Paris')
        #print(type(factor))
        weatherCSV = readParisW()
        #print(weatherCSV)
        Paris_factors = getAllFactors(weatherCSV)
        #print(Paris_factors)
        Paris_results = getResult(weatherCSV)
        #print(Paris_results)
        Paris_model = ridgeReg(Paris_factors, Paris_results)
        print(type(Paris_model))
        print(factor)
        Y_predict = Paris_model.predict(factor)
        new_y_pre = []
        for y in Y_predict:
            y1 = round(y[0])
            new_y_pre.append(y1)
        return new_y_pre
    else:
        if loc =='Shanghai':
            weatherCSV2 = readSHW()
            SH_factors = getAllFactors(weatherCSV2)
            SH_results = getResult(weatherCSV2)
            SH_model = ridgeReg(SH_factors, SH_results)
            Y_predict = SH_model.predict(factor)
            new_y_pre = []
            for y in Y_predict:
                y1 = round(y[0])
                new_y_pre.append(y1)
            return new_y_pre

if __name__ == "__main__":
    main()