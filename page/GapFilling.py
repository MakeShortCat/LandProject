import os
os.chdir(r'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1')
import streamlit as st
from PageFunctions import GraphMaker

def app():
    st.title('NA값을 예측값으로 대체한 그래프')
    
    vari = {'예측값으로 대체 그래프' : GraphMaker.forecast_graph}
    
    options = st.multiselect('그래프를 선택해주세요', vari)
    
    for i in vari.keys():
        if i in options:
            st.pyplot(vari[i])