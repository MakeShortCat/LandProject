import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.font_manager as fm
from matplotlib import dates
import datetime as dt
from sklearn import linear_model
from PageFunctions import GraphMaker
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm

# 소득 관련하여 정리 2013 1월 ~ 2022 9월

house_path = 'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1/data/income/'

income1 = pd.read_csv(house_path + '소득10분위별__가구당_가계수지__전국_1인이상__20230210160458.csv',
                      encoding='euc-kr')

income1.drop(index=0, inplace=True)

income1.reset_index(inplace=True)

income2 = pd.read_csv(house_path + '소득10분위별_가구당_가계수지__전국_1인이상__20230210160348.csv',
                      encoding='euc-kr')

income2.drop(index=0, inplace=True)

income2.reset_index(inplace=True)

income1.iloc[:, -4:].astype(int)

income2.iloc[:, 3:7].astype(int)

((income1.iloc[:, -4:].astype(int) + income2.iloc[:, 3:7].astype(int)) / 2).astype(int)

income1.iloc[:, -4:] = ((income1.iloc[:, -4:].astype(int) + income2.iloc[:, 3:7].astype(int)) / 2).astype(int)

income = pd.concat([income1, income2.iloc[:, 7:]],axis=1)

income.iloc[:, 0:].head(10)

income.drop(columns='가계수지항목별', inplace = True)

income.drop(columns='index', inplace = True)

income.set_index('월소득10분위별', inplace=True)

income = income.transpose()

quater_date = pd.date_range(start = '2006-01-01', end = '2022-09-30', freq='Q')

income.set_index(quater_date, drop= True, inplace=True)

income_filled = income.resample('M').ffill()

income_drop_index = pd.date_range(start = '2006-3-01', end = '2012-12-31', freq='M')

income_filled.drop(index=income_drop_index, inplace = True)

income_filled = income_filled.astype(int)/1000000

# 아파트 매매 가격지수 정리 2013 1월 ~ 2022 9월

Apart_price = pd.read_excel('C:/Users/pgs66/Desktop/GoogleDrive/python/Project1/data/income/월간_매매가격지수_아파트.xlsx')

for i in range(3,464,2):
    Apart_price.drop(columns=f'Unnamed: {i}', inplace = True)

Apart_price.drop(columns='Unnamed: 1', inplace = True)
Apart_price.drop(columns='Unnamed: 2', inplace = True)
Apart_price.drop(index=0, inplace = True)

Apart_price.set_index(Apart_price['지 역'], drop= True, inplace=True)

Apart_price = Apart_price.transpose()

Apart_price.drop(index='지 역', inplace = True)

Apart_range = pd.date_range('2003-11-01', periods=230 , freq='M')

Apart_price.set_index(Apart_range, drop= True, inplace=True)

Apart_drop_index = pd.date_range(start = '2003-11-01', end = '2012-12-31', freq='M')

Apart_price.drop(index=Apart_drop_index, inplace = True)

Apart_drop_index = pd.date_range(start = '2022-10-01', end = '2022-12-31', freq='M')

Apart_price.drop(index=Apart_drop_index, inplace = True)


# 금리

path = 'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1/data/income/'

file_list = os.listdir(path)

file_list_py = [file for file in file_list if file.startswith('20')]

Rent = pd.DataFrame()

for i in file_list_py:
    data = pd.read_excel(path + i, header=0, usecols='A,C', skiprows=[1])
    data = data.assign(date=i.split('.')[0])
    Rent = pd.concat([Rent,data])

Rent['date']

miss_located = Rent.iloc[-36:, 3]

Rent.iloc[-36:, 1] = miss_located

Rent.drop(columns='신용점수별 금리(%)', inplace = True)

Rent.reset_index()

Rent_Bank = Rent['은행'].unique()

for i in Rent_Bank[18:]:
    Rent.replace(i ,i.strip() ,inplace=True)

Rent_Bank = Rent['은행'].unique()

Rent.set_index('date', inplace=True)

Arranged_Rent = pd.DataFrame()

for i in Rent_Bank:
    Arranged_Rent[f'{i}'] = Rent.groupby('은행').get_group(str(i))['신용등급별 금리(%)']
    
    
temp_Rent_period = pd.date_range(start = '2013-03-01', end = '2022-10-01', freq='M')

Arranged_Rent.set_index(temp_Rent_period, drop=True, inplace=True)

Arranged_Rent.replace('-', np.nan, inplace=True)

Arranged_Rent = Arranged_Rent.astype('float')

Arranged_Rent_min = Arranged_Rent.min(axis=1)
Arranged_Rent_mean = Arranged_Rent.mean(axis=1)

# 그래프 그리기

Arranged_Rent_mean_Graph = GraphMaker.DrawGraph(Arranged_Rent_mean.index, Arranged_Rent_mean.astype(float),
                                                (10, 5), '일시', '평균 이자율', '평균 이자율 그래프',
                                                xticks = ticker.IndexLocator(base= 180, offset=0),yLocator=ticker.MaxNLocator(nbins=6))

income_filled_Graph = GraphMaker.DrawGraph(income_filled.index, income_filled['전체'].astype(float),
                                                (10, 5), '일시', '평균 소득(백만원)', '평균 소득 그래프',
                                                xticks = ticker.IndexLocator(base= 180, offset=0), yLocator=ticker.MaxNLocator(nbins=6))

Apart_price_Graph = GraphMaker.DrawGraph(Apart_price.index, Apart_price['전국'].astype(float),
                                                (10, 5), '일시', '아파트 매매가 지수', '아파트 매매가 지수 그래프',
                                                xticks = ticker.IndexLocator(base= 180, offset=0))


merged = pd.concat([Arranged_Rent_mean, income_filled, Apart_price], axis=1).dropna()

merged = merged.rename(columns={0:'평균이자율'})

X = merged[['５분위','평균이자율']].astype(float)
Y = merged['수도권'].astype(float)

results = sm.OLS(Y.values.reshape(-1, 1), sm.add_constant(X)).fit()
print(results.summary())

reg = linear_model.LinearRegression().fit(X, Y)
print( "coefficient=",format(reg.coef_[0],'f') ,format(reg.coef_[1],'f'))
print( "intercept=", reg.intercept_ )
print( "R²=", reg.score(X, Y))

def HouseGraph_maker():
    X = merged[['５분위','평균이자율']].values.reshape(-1,2).astype(float)
    Y = merged['수도권'].astype(float)

    x = X[:, 0]
    y = X[:, 1]
    z = Y
    xx, yy = np.meshgrid(x, y)

    model_visual = np.array([xx.flatten(), yy.flatten()]).T

    ols = linear_model.LinearRegression()
    model = ols.fit(X, Y)

    predicted = model.predict(model_visual)

    r2 = model.score(X, Y)
    
    font_path = "C:/Windows/Fonts/gulim.ttc"
    fontprop = fm.FontProperties(fname=font_path, size=10).get_name()
    plt.rc('font', family=fontprop)

    fig = plt.figure(figsize=(25, 10))

    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')
    
    axes = [ax1, ax2, ax3]
    
    for ax in axes:
        ax.plot(x, y, z, color='k', zorder=100, linestyle='none', marker='o', alpha=0.5) #검은색 마커들
        ax.scatter(xx.flatten(), yy.flatten(), predicted, s=20, edgecolor='#70b3f0') #파란색 마커들
        ax.set_xlabel('소득(백만원)', fontsize=12) #해당 축을 설명하는 라벨
        ax.set_ylabel('이자', fontsize=12)
        ax.set_zlabel('매매가', fontsize=12)
        ax.locator_params(nbins=5, axis='x') #해당 축의 구간 개수 (쪼개진 구간도 포함)
        ax.locator_params(nbins=5, axis='y')
        ax.locator_params(nbins=5, axis='z')
    
    #높이와 방위각을 조절해서 보고 싶은 위치를 조정할 수 있음
    #elevation (높이), azimuth (방위각)
    ax1.view_init(elev=27, azim=112)
    ax2.view_init(elev=16, azim=20)
    ax3.view_init(elev=30, azim=160)
    
    fig.suptitle('$R^2 = %.2f$' % r2, fontsize=20)
    
    fig.tight_layout()

    return fig
