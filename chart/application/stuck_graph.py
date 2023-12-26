from datetime import date,timedelta,datetime
import mplfinance as mpf
import pandas_datareader.data as web
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mplfinance._mplwraps import Mpf_Figure
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from oauth2client.service_account import ServiceAccountCredentials
import time
import sys
import cv2
import os
import shutil
import time

matplotlib.use('Agg')

def search():
    global Code
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    c = ServiceAccountCredentials.from_json_keyfile_name("/chart/application/my-project0805-e01f6f7ec73a.json", scope)

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)

    url = "https://jp.kabumap.com/servlets/kabumap/Action?SRC=easyScrn/base"
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='119.0.6045.105').install()),options=options)
    #driver = webdriver.Chrome(options=options)
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(executable_path=driver_path),options=options)
    driver.set_window_size(1400, 980)
    driver.get(url)

    Code = []
    

    price = driver.find_element(By.XPATH,"//*[@id='max_budget']")
    price.clear()
    price.send_keys("5")
    bs = driver.find_element(By.XPATH,"//*[@id='easyScrnQ']/fieldset[2]/div[2]/table/tbody/tr[9]/td[4]/input")
    bs.send_keys("15")
    btn = driver.find_element(By.XPATH,"//*[@id='button']")
    btn.click()
    mx = int(driver.find_element(By.XPATH,"//*[@id='KM_TABLERESULTNUM0']").text)
    print(mx)
    while len(Code) < mx:
        for i in range(2,32):
            try:
                search_code = driver.find_element(By.XPATH,"//*[@id='KM_TABLECONTENT0']/div[1]/table/tbody/tr[{}]/td[2]".format(i)).text
                Code.append(search_code)
            except:
                pass
        print(len(Code))
        arrow = driver.find_element(By.XPATH,"//*[@id='KM_TABLEINDEXBTM0']/div/table/tbody/tr/td[{}]".format((-((-mx)//30)*2)+3))
        arrow.click()
    return Code

def graph(num:str,j:int):
    global style,fname
    company_code = num + '.T'
    my_share = share.Share(company_code)
    symbol_data = None
    try:
        if j == 1:
            symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                          1,
                                          share.FREQUENCY_TYPE_DAY,
                                          1)
            print("day")
        elif j == 60:
            symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                          60,
                                          share.FREQUENCY_TYPE_MINUTE,
                                          60)
            print("hour")
        else:
            print("Error")
    except YahooFinanceError as e:
        print(e.message,num)
    
    try:
        df = pd.DataFrame(symbol_data)
        df.timestamp = pd.to_datetime(df.timestamp, unit='ms')
        df.index = pd.DatetimeIndex(df.timestamp, name='timestamp').tz_localize('UTC').tz_convert('Asia/Tokyo')
        df = df.reset_index(drop=True)
        df.set_index("timestamp",inplace=True)
        exp12 = df['close'].ewm(span=12, adjust=False).mean()
        exp26 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp12 - exp26
        # シグナル
        df['Signal'] = df['MACD'].rolling(window=9).mean()
                        
        # ヒストグラム(MACD - シグナル)
        df['Hist'] = df['MACD'] - df['Signal']

        df_up, df_down = df["close"].diff().copy(), df["close"].diff().copy()
        df_up[df_up < 0] = 0
        df_down[df_down > 0] = 0
        df_down = df_down * -1

        sim14_up = df_up.rolling(window=14).mean()
        sim14_down = df_down.rolling(window=14).mean()
        df['RSI'] = sim14_up / (sim14_up + sim14_down) * 100
        
        df["SMA5"] = df["close"].rolling(window=5).mean()
        df["SMA10"] = df["close"].rolling(window=10).mean()
        df["SMA20"] = df["close"].rolling(window=20).mean()
        df["SMA80"] = df["close"].rolling(window=80).mean()
        #df["SMA200"] = df["close"].rolling(window=200).mean()

        # MACDとシグナルのプロット作成
        add_plot = [mpf.make_addplot(df["SMA5"], panel=0, color="red", width=0.8),
                    mpf.make_addplot(df["SMA10"], panel=0, color="orange", width=0.8),
                    mpf.make_addplot(df["SMA20"], panel=0, color="yellow", width=0.8),
                    mpf.make_addplot(df["SMA80"], panel=0, color="green", width=0.8),
                    #mpf.make_addplot(df["SMA200"], panel=0, color="white", width=0.8),
                    mpf.make_addplot(df['MACD'], color='m', panel=1, secondary_y=False, ylabel='MACD'),
                    mpf.make_addplot(df['Signal'], color='c', panel=1, secondary_y=False),
                    mpf.make_addplot(df['Hist'], type='bar', color='g', panel=1, secondary_y=True),
                    mpf.make_addplot(df['RSI'], panel=2, ylabel='RSI')]

        hists = df['Hist']
        rsi = df["RSI"]
        macd = df["MACD"]
        dates = df.index
        print(df)
        if df["SMA80"].isnull().all():
            print(num)
            return num
        # 日数分ループ
        for i in range(1, hists.size):
            # 2日分取り出し
            h1 = hists.iloc[i-1]
            h2 = hists.iloc[i]
            m1 = macd.iloc[i]
                        
            # ゴールデンクロス・デッドクロスを判定
            if date.today().weekday() == 5 or date.today().weekday() == 6:
                fri = datetime.now().weekday() - 4
                start = datetime.now() - timedelta(days=fri)
                brank = timedelta(days=1)
            else:
                brank = timedelta(days=1)
                start = datetime.now()
            if h1 < 0 < h2 and start - dates[i] <= brank and j == 60:
                plt.clf()
                style = "Golden_cross"
                if m1 < 0:
                    fname = "転換"
                if m1 >= 0:
                    fname = "継続"
                # ゴールデンクロス
                print("Golden")
                mpf.plot(df, type='candle', volume=True, addplot=add_plot, volume_panel=3, title=num+"hour", style='nightclouds',savefig='/static/images/chart_graph/{}/{}/{}.png'.format(style,fname,num))
                img = cv2.cvtColor(cv2.imread("/static/images/chart_graph/{}/{}/{}.png".format(style,fname,num)), cv2.COLOR_BGR2RGB)
                plt.subplot(121),plt.imshow(img)
                plt.xticks([]), plt.yticks([])
                graph(num,1)
                

            elif h1 > 0 > h2 and start - dates[i] <= brank and j == 60:
                plt.clf()
                style = "Dead_cross"
                if m1 > 0:
                    fname = "転換"
                if m1 <= 0:
                    fname = "継続"
                # デッドクロス
                print("Dead")
                mpf.plot(df, type='candle', volume=True, addplot=add_plot, volume_panel=3, title=num+"hour", style='nightclouds',savefig='/static/images/chart_graph/{}/{}/{}.png'.format(style,fname,num))
                img = cv2.cvtColor(cv2.imread("/static/images/chart_graph/{}/{}/{}.png".format(style,fname,num)), cv2.COLOR_BGR2RGB)
                plt.subplot(121),plt.imshow(img)
                plt.xticks([]), plt.yticks([])
                graph(num,1)

        if j == 1:
            mpf.plot(df, type='candle', volume=True, addplot=add_plot, volume_panel=3, title=num+"day", style='nightclouds',savefig='/static/images/chart_graph/{}/{}/{}.png'.format(style,fname,num))
            img = cv2.cvtColor(cv2.imread("/static/images/chart_graph/{}/{}/{}.png".format(style,fname,num)), cv2.COLOR_BGR2RGB)
            plt.subplot(122),plt.imshow(img)
            plt.xticks([]), plt.yticks([])
            fig.savefig("/static/images/chart_graph/{}/{}/{}.png".format(style,fname,num),dpi=500, bbox_inches='tight', pad_inches=0)
            print("complete")
                
    except:
        print(num)

def do_graph():
    global fig
    fig = plt.figure()
    for i in ["Golden_cross","Dead_cross"]:
        for j in ["転換","継続"]:
            path = f"/static/images/chart_graph/{i}/{j}/"
            if os.path.exists(path):
                shutil.rmtree(path)
                os.mkdir(path)
    Code = search() 
    for num in Code:
        graph(num,60)
