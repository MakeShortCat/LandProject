import os
os.chdir(r'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1')
import streamlit as st
from PageFunctions import HouseGraph

def app():
    st.title('부동산 분석 전 정리가 완료된 자료들의 그래프')
    
    vari = {'아파트 매매가 그래프' : HouseGraph.Apart_price_Graph,
            '평균 이자율 그래프' : HouseGraph.Arranged_Rent_mean_Graph,
            '평균 소득 그래프' : HouseGraph.income_filled_Graph}
    
    options = st.multiselect('그래프를 선택해주세요', vari)
    
    for i in vari.keys():
        if i in options:
            st.pyplot(vari[i])