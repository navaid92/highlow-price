from flask import Flask,request,redirect
from flask import render_template
from sklearn.externals import joblib
from xauusd import predictXauUsd
from eurusd import Eurusdpredict
from gbpusd import PredictGbpusd
from usdcad import predictusdcad
from usdjpy import predictUsdJpy
from datetime import datetime
import pandas as pd 
import numpy as np
import requests
app = Flask(__name__)
print(app)

@app.route('/') #home
def Auth():
    return render_template('form.html')
@app.route('/login')
def Login():
    return render_template('login.html')
@app.route('/login/check',methods = ['POST'])
def checkuser():
    if request.form.get('uname') == 'admin' and request.form.get('psw') == 'admin1234':
        return redirect('/getdata')
    else:
        return redirect('/')
@app.route('/getdata')
def GetData():
    
    opens = []
    close = []
    high = []
    low = []
    currency = []
    data_to_get = ['GBPUSD','EURUSD','USDJPY','XAUUSD','USDCAD']
    x = datetime.now()
    dtes = f"{x.year}-{x.month}-{x.day - 1}"
    get = {}
    d = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date={dtes}&currency=USDCAD').json()['date']
    for i in data_to_get:
        data = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date={dtes}&currency={i}').json()
        get[i] = data['quotes'][0] 
    prerictions = {}
    for cur in data_to_get:
        opens.append(get[cur]['open'])
        close.append(get[cur]['close'])
        high.append(get[cur]['high'])
        low.append(get[cur]['low'])
        currency.append(cur)
    inputs = {}
    inputs['cur'] = currency
    inputs['open'] = opens
    inputs['close'] = close
    inputs['high'] = high
    inputs['low'] = low
 
    prerictions['xdate'] = str(f"{x.year}-{x.month}-{x.day}")
    clf = joblib.load('gbpusd.pkl')
    x =clf.predict(np.array([[opens[0],low[0],high[0],close[0]]]))
    prerictions[currency[0]] = [x[0][0],x[0][1]]

    clf = joblib.load('eurusd.pkl')
    x = clf.predict(np.array([[opens[1],low[1],high[1],close[1]]]))
    prerictions[currency[1]] = [x[0][0],x[0][1]]

    clf = joblib.load('usdjpy.pkl')
    x = clf.predict(np.array([[opens[2],low[2],high[2],close[2]]]))
    prerictions[currency[2]] = [x[0][0],x[0][1]]

    clf = joblib.load('xauusd.pkl')
    x = clf.predict(np.array([[opens[3],low[3],high[3],close[3]]]))
    prerictions[currency[3]] = [x[0][0],x[0][1]]

    clf = joblib.load('usdcad.pkl')
    x = clf.predict(np.array([[opens[4],low[4],high[4],close[4]]]))
    prerictions[currency[4]] = [x[0][0],x[0][1]]

    pd.DataFrame(prerictions).to_csv('predictions.csv',index = False)
    data = pd.read_csv('predictions.csv')
    #converting float into specific decimal places
    data['XAUUSD'] = data['XAUUSD'].apply('{:,.2f}'.format)
    data['USDJPY'] = data['USDJPY'].apply('{:,.3f}'.format)
    data.update(data.select_dtypes(include=np.number).applymap('{:,.5f}'.format))
    x = data['XAUUSD']
    x[0] = x[0].replace(',',"")
    x[1] = x[1].replace(',',"")
    data['XAUUSD'] = x
    return render_template('table.html',data = data)

@app.route('/upload_files',methods = ['GET','POST'])
def UploadData():
    
    if request.method == "POST":
        files = request.files['fileToupload']
        file_name = request.form.get('filenamax')
        if files:
            files.save(f"{file_name}.csv")
            return render_template('upload_files.html')
    else:
        return render_template('admin_login.html')

@app.route('/adminlogin',methods = ['POST'])
def admin_login():
    
    admin_data = pd.read_csv('admin.csv')
    us = request.form.get('uname')
    psw = request.form.get('psw')
    if admin_data.iloc[:,1].values == us and admin_data.iloc[:,2].values == psw:
        return render_template('upload_files.html')
    else:
        return render_template('admin_login.html')
    
@app.route('/change_pass')
def chage():
    return render_template('change_pass.html')
@app.route("/forget",methods = ['POST'])
def chage_password():
    
    
    username = request.form.get('uname')
    passw = request.form.get('psw')
    admin_data = pd.read_csv('admin.csv')
    admin_data['username'] = username
    admin_data['pass'] = passw
    admin_data.to_csv('admin.csv',index = False)
    return render_template('admin_login.html')

@app.route("/train")
def Trian():
    
    opens = []
    close = []
    high = []
    low = []
    currency = []
    data_to_get = ['GBPUSD','EURUSD','USDJPY','XAUUSD','USDCAD']
    x = datetime.now()
    dtes = f"{x.year}-{x.month}-{x.day - 1}"
    get = {}
    d = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date={dtes}&currency=USDCAD').json()['date']
    for i in data_to_get:
        data = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date={dtes}&currency={i}').json()
        get[i] = data['quotes'][0] 
    prerictions = {}
    for cur in data_to_get:
        opens.append(get[cur]['open'])
        close.append(get[cur]['close'])
        high.append(get[cur]['high'])
        low.append(get[cur]['low'])
        currency.append(cur)
    inputs = {}
    inputs['cur'] = currency
    inputs['open'] = opens
    inputs['close'] = close
    inputs['high'] = high
    inputs['low'] = low
 
    prerictions['xdate'] = str(f"{x.year}-{x.month}-{x.day}")
   
    x =PredictGbpusd(opens[0],low[0],high[0],close[0])
    prerictions[currency[0]] = [x[0][0],x[0][1]]

    x = Eurusdpredict(opens[1],low[1],high[1],close[1])
    prerictions[currency[1]] = [x[0][0],x[0][1]]

    x = predictUsdJpy(opens[2],low[2],high[2],close[2])
    prerictions[currency[2]] = [x[0][0],x[0][1]]

    x = predictXauUsd(opens[3],low[3],high[3],close[3])
    prerictions[currency[3]] = [x[0][0],x[0][1]]

    x = predictusdcad(opens[4],low[4],high[4],close[4])
    prerictions[currency[4]] = [x[0][0],x[0][1]]

    pd.DataFrame(prerictions).to_csv('predictions.csv',index = False)
    data = pd.read_csv('predictions.csv')
    #converting float into specific decimal places
    data['XAUUSD'] = data['XAUUSD'].apply('{:,.2f}'.format)
    data['USDJPY'] = data['USDJPY'].apply('{:,.3f}'.format)
    data.update(data.select_dtypes(include=np.number).applymap('{:,.5f}'.format))
    x = data['XAUUSD']
    x[0] = x[0].replace(',',"")
    x[1] = x[1].replace(',',"")
    data['XAUUSD'] = x
    return render_template('table.html',data = data)


if __name__ == '__main__':
    app.run(debug = True)













'''
def solvemefirst(a,b):
    return a + b
res = solvemefirst(2,3)
print()
'''
