import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import ticker
from prophet import Prophet
import matplotlib.font_manager as fm
from matplotlib import dates

path = 'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1/data/'

file_list = os.listdir(path)

file_list_py = [file for file in file_list if file.endswith('.csv')]

air_Temp = pd.DataFrame()

for i in file_list_py:
    data = pd.read_csv(path + i, encoding='euc-kr')
    air_Temp = pd.concat([air_Temp, data], ignore_index=True)

air_Temp_origin = air_Temp.copy()

air_Temp.loc[1000 , '기온(°C)'] = 4000
air_Temp.loc[3000 , '기온(°C)'] = 9999
air_Temp.loc[5000 , '기온(°C)'] = 10
air_Temp.loc[7000:7179 , '기온(°C)'] = 0.5

original_air_temp = air_Temp[['일시','기온(°C)']].copy()

original_air_temp['일시'] = pd.to_datetime(original_air_temp['일시']).apply(lambda x : x.strftime('%m-%d %H:%M'))

#그래프 그리는 함수
def DrawGraph(x, y, size, xlabelname, ylabelname, title, xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(1)):
    font_path = "C:/Windows/Fonts/gulim.ttc"
    fontprop = fm.FontProperties(fname=font_path, size=10).get_name()
    plt.rc('font', family=fontprop)
    fig, ax = plt.subplots(figsize=size)
    ax.plot(x, y)
    ax.yaxis.set_major_locator(yLocator)
    ax.xaxis.set_major_locator(xticks)
    plt.xticks(rotation=45, fontsize= 10)
    ax.set_xlabel(f"{xlabelname}")
    ax.set_ylabel(f"{ylabelname}")
    ax.set_title(f'{title}')
    return fig

original_graph = DrawGraph(original_air_temp['일시'], original_air_temp['기온(°C)'], (10, 5), "일시", "기온(°C)",'기온 원본 자료',
                           xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(2000))


class QCfunc:
    ErrorName = []
    ErrorLoc = []
    ErrorValue = []

    def QC_1(temp):
        for i in range(len(temp)):
            if temp.iloc[i] == 9999 or temp.iloc[i] ==99999:
                QCfunc.ErrorName.append('결측치')
                QCfunc.ErrorLoc.append(f'{i}')
                QCfunc.ErrorValue.append(temp.iloc[i])
                temp.iloc[i] = np.NaN
                return temp

    def QC_2(temp):
        for i in range(len(temp)):
            if temp.iloc[i]>40 or temp.iloc[i]<-33:
                QCfunc.ErrorName.append('물리한계 초과')
                QCfunc.ErrorLoc.append(f'{i}')
                QCfunc.ErrorValue.append(temp.iloc[i])
                temp.iloc[i] = np.NaN
                return temp

    def QC_3(temp):
        for i in range(len(temp)):
            if i < 10079 and abs(temp.iloc[i+1] - temp.iloc[i]) > 3 and abs(temp.iloc[i] - temp.iloc[i-1]) > 3 and temp.iloc[i+1] != 9999 and temp.iloc[i+1] !=99999 and temp.iloc[i+1]<40 and temp.iloc[i+1]>-33:
                QCfunc.ErrorName.append('단계검사 기준 초과')
                QCfunc.ErrorLoc.append(f'{i}')
                QCfunc.ErrorValue.append(temp.iloc[i])
                temp.iloc[i] = np.NaN
                return temp
                
    def QC_4(temp):         
        for i in range(len(temp)):
            if 180 + i < len(temp):
                if len(temp.iloc[i:i+180].unique()) == 1:
                    for j in range(180):
                        QCfunc.ErrorName.append('지속성 검사 기준 초과')
                        QCfunc.ErrorLoc.append(f'{i+j}')
                        QCfunc.ErrorValue.append(temp.iloc[i+j])
                        temp.iloc[i+j] = np.NaN
                    return temp

air_Temp_data = air_Temp[['일시','기온(°C)']].copy()

air_Temp_data['일시'] = pd.to_datetime(air_Temp['일시']).apply(lambda x : x.strftime('%m-%d %H:%M'))

# 이상값 포함된 그래프

Out_Range_Graph = DrawGraph(air_Temp_data['일시'], air_Temp_data['기온(°C)'], (10, 5), "일시", "기온(°C)",'이상값이 포함된 기온',
                             xticks = ticker.IndexLocator(base= 1440, offset=0),yLocator=ticker.MultipleLocator(2500))

#QC1 후 그래프 결측치
QC1 = QCfunc.QC_1(air_Temp['기온(°C)'].copy())

nan_Graph = DrawGraph(air_Temp_data['일시'], QC1, (10, 5), "일시", "기온(°C)", '결측치 제거 후 기온',
                      xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(1000))

#QC2 후 그래프 한계값
QC2 = QCfunc.QC_2(QC1.copy())

Limit_Graph = DrawGraph(air_Temp_data['일시'], QC2, (10, 5), "일시", "기온(°C)",'물리한계 검사 후 기온',
                        xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(1))

#QC3 후 그래프 단계검사
QC3 = QCfunc.QC_3(QC2.copy())

Step_Graph = DrawGraph(air_Temp_data['일시'], QC3, (10, 5), "일시", "기온(°C)", '단계검사 후 기온',
                       xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(1))

#QC4 후 그래프 지속성
QC4 = QCfunc.QC_4(QC3.copy())

Continue_Graph = DrawGraph(air_Temp_data['일시'], QC4, (10, 5), "일시", "기온(°C)", '지속성 검사 후 기온',
                           xticks = ticker.IndexLocator(base= 1440, offset=0), yLocator=ticker.MultipleLocator(1))

error_dataframe = pd.DataFrame(zip(QCfunc.ErrorName, QCfunc.ErrorLoc, QCfunc.ErrorValue), columns=['ErrorName', 'ErrorLoc', 'ErrorValue'])

fig1, [ax1,ax2,ax3,ax4,ax5] = plt.subplots(
    nrows=5, ncols=1, 
    sharex=True,
    sharey=False,
    figsize=(20, 20))

xticks = ticker.IndexLocator(base=1440, offset=0)

ax1.xaxis.set_major_locator(xticks)
ax2.xaxis.set_major_locator(xticks)
ax3.xaxis.set_major_locator(xticks)
ax4.xaxis.set_major_locator(xticks)
ax5.xaxis.set_major_locator(xticks)

ax1.set_title('이상값이 포함된 기온')
ax2.set_title('결측치 제거 후 기온')
ax3.set_title('물리한계 검사 후 기온')
ax4.set_title('단계검사 후 기온')
ax5.set_title('지속성 검사 후 기온')

ax1.plot(air_Temp_data['일시'], air_Temp_data['기온(°C)'])
ax2.plot(QC1)
ax3.plot(QC2)
ax4.plot(QC3)
ax5.plot(QC4)
plt.xticks(rotation=45)

QC5 = pd.DataFrame(QC4.copy())

df = pd.concat([air_Temp['일시'],QC4],axis=1)

df = df.rename(columns = {'일시':'ds', '기온(°C)':'y'})

m = Prophet(changepoint_prior_scale=0.08, daily_seasonality=15)
m.fit(df)

future = m.make_future_dataframe(periods=0)
forecast = m.predict(future)

forecasted_error_list = []

for i in error_dataframe['ErrorLoc'].astype(int):
    forecasted_error_list.append(forecast['yhat'].iloc[i])

forecasted_error_list = pd.Series(forecasted_error_list)

air_Temp_origin_list = []

for i in error_dataframe['ErrorLoc'].astype(int):
    air_Temp_origin_list.append(air_Temp_origin['기온(°C)'].iloc[i])

air_Temp_origin_list = pd.Series(air_Temp_origin_list)

error_size = abs(forecasted_error_list - air_Temp_origin_list)

error_size.var()

fig2 = m.plot(forecast)

QC_nan_exist = pd.concat([air_Temp['일시'],QC5],axis=1)

QC_nan_exist['일시'] = pd.to_datetime(QC_nan_exist['일시'])

QC_nan_exist.set_index('일시', inplace=True)

#1시간 80퍼센트 없을경우 결과

QC_nan_exist_60min = QC_nan_exist.rolling(60, min_periods=int(60 * 8/10),closed='left').mean()

DF_QC_nan_exist = QC_nan_exist.copy()
DF_QC_nan_exist['기온(°C)'] = np.nan
DF_QC_nan_exist = DF_QC_nan_exist.resample('H').mean()

for i in range(len(DF_QC_nan_exist)-1):
    if QC_nan_exist['기온(°C)'].iloc[i*60:i*60+60].isnull().sum() <= 12:
        DF_QC_nan_exist.iloc[i] = QC_nan_exist.resample('H').mean().iloc[i]
        
    else: DF_QC_nan_exist.iloc[i] = np.nan

#예측값 채워넣은 값
for i in error_dataframe['ErrorLoc'].astype(int):
    QC5.iloc[i] = forecast['yhat'].iloc[i]

QC5_1 = pd.concat([air_Temp['일시'],QC5],axis=1)
QC5_1 = QC5_1.rename(columns = {'일시':'ds', '기온(°C)':'y'})

QC5_1.ds = pd.to_datetime(QC5_1.ds)

QC5_1.set_index(QC5_1.ds, inplace=True)

forecast_graph = DrawGraph(QC5_1['ds'], 
                                QC5_1['y'], (10, 5), "일시", "기온(°C)", '결측치 예측 기온',
                                xticks=dates.DayLocator(interval=1), yLocator=ticker.MultipleLocator(1))

hour_average3 = QC5_1.resample('3H').mean()
hour_average3.iloc[-1] = np.nan

day_average = QC5_1.resample('D').mean()
day_average.iloc[-1] = np.nan

hour_average_graph = DrawGraph(DF_QC_nan_exist.index, 
                                DF_QC_nan_exist['기온(°C)'], (10, 5), "일시", "기온(°C)", '시간별 평균 기온',
                                xticks=dates.HourLocator(byhour=range(0,24,6)),yLocator=ticker.MultipleLocator(1))

hour_average3_graph = DrawGraph(hour_average3.index, 
                                hour_average3['y'], (10, 5), "일시", "기온(°C)", '3시간별 평균 기온',
                                xticks=dates.HourLocator(byhour=range(0,24,6)),yLocator=ticker.MultipleLocator(1))

day_average_graph = DrawGraph(day_average.index, 
                                day_average['y'], (10, 5), "일시", "기온(°C)", '일별 평균 기온',
                                xticks=dates.DayLocator(interval=1),yLocator=ticker.MultipleLocator(1))

