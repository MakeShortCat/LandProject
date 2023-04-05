import streamlit as st
import os
os.chdir(r'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1')
from multipage.MultiPage import MultiPage
from page import AverageGraph, GapFilling, QCgraph, House_Basic_Graph, HouseRegression


st.title('Project1')

app = MultiPage()

# 1번 페이지
app.add_page('QC그래프', QCgraph.app, 0)
app.add_page('시간별 평균 그래프', AverageGraph.app, 0)
app.add_page('결측치 예측 그래프', GapFilling.app, 0)

# 2번 페이지
app.add_page('부동산 자료 그래프', House_Basic_Graph.app, 1)
app.add_page('부동산 회귀 분석 그래프', HouseRegression.app, 1)

Category = ['기온', '부동산 가격 분석']


PageOption1 = st.sidebar.selectbox("보고싶은 자료를 선택하세요", Category)

if PageOption1 == '기온':
    PageOption2_1 = st.sidebar.radio("페이지를 선택하세요", MultiPage.PageName0.keys())
    MultiPage.PageName0[PageOption2_1]()
    
elif PageOption1 == '부동산 가격 분석':
    PageOption2_2 = st.sidebar.radio("페이지를 선택하세요", MultiPage.PageName1.keys())
    MultiPage.PageName1[PageOption2_2]()
    

