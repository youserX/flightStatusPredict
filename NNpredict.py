from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import pandas as pd
import regression

def MLPReg():
    paris_w = regression.readParisW()
    paris_factors = regression.getAllFactors(paris_w)
    paris_result = regression.getResult(paris_w)
    sc1 = StandardScaler()
    sc2 = StandardScaler()
    sc1.fit(paris_factors)
    sc2.fit(paris_result)
    X = sc1.transform(paris_factors)
    Y = sc2.transform(paris_result)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
    print(X_train)
    mlp = MLPRegressor(hidden_layer_sizes=(5, 5, 5), max_iter=200)
    mlp.fit(X_train, Y_train)
    Y_pre = mlp.predict(X_test)

    print("MSE:", metrics.mean_squared_error(Y_test, Y_pre))
    print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(Y_test, Y_pre)))

def MLPClaClassic():
    paris_w = regression.readParisW()
    paris_factors = regression.getAllFactors(paris_w)
    paris_land_status =regression.getFlightStatus(paris_w)
    sc = StandardScaler()
    sc.fit(paris_factors)
    X = sc.transform(paris_factors)
    Y = paris_land_status[1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
    mlp = MLPClassifier(hidden_layer_sizes=(5, 5, 5), max_iter=200)
    mlp.fit(X_train, Y_train)
    
    Y_pre = mlp.predict_proba(X_test)
    print(Y_pre)
    delay = 0
    early = 0
    for y in Y_pre:
        delay = delay + y[0]
        early = early + y[1]
    delay = delay/6
    early = early/6
    print(delay)
    print(early)
    #print("MSE:", metrics.mean_squared_error(Y_test, Y_pre))
    #print("RMSE:", pd.np.sqrt(metrics.mean_squared_error(Y_test, Y_pre)))

def MLPCla(factor, result):
    mlp = MLPClassifier(hidden_layer_sizes=(5, 5, 5), max_iter=200)
    mlp.fit(factor, result)
    return mlp


def MLPLandStatus(loc, factor):
    if loc =='Paris':
        #print('loc is Paris')
        #print(type(factor))
        weatherCSV = regression.readParisW()
        #print(weatherCSV)
        Paris_factors = regression.getAllFactors(weatherCSV)
        print(Paris_factors)
        paris_land_status = regression.getFlightStatus(weatherCSV)
        print(paris_land_status)
        print('...........................')
        Paris_model = MLPCla(Paris_factors, paris_land_status[1])
        print(type(Paris_model))
        print(factor)
        Y_predict = Paris_model.predict_proba(factor)
        return Y_predict
    else:
        if loc =='Shanghai':
            print(loc)
            weatherCSV2 = regression.readSHW()
            SH_factors = regression.getAllFactors(weatherCSV2)
            SH_land_status = regression.getFlightStatus(weatherCSV2)
            SH_model = MLPCla(SH_factors, SH_land_status[1])
            Y_predict = SH_model.predict_proba(factor)
            return Y_predict


