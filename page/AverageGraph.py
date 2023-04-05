import os
os.chdir(r'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1')
import streamlit as st
from multipage import MultiPage
from PageFunctions import GraphMaker

def app():
    st.write('시간별 평균 그래프')

    vari = {'1시간별 기온 그래프' : GraphMaker.hour_average_graph,
            '3시간별 기온 그래프' : GraphMaker.hour_average3_graph,
            '일별 기온 그래프' : GraphMaker.day_average_graph}

    options = st.multiselect('그래프를 선택해주세요', vari)
    
    for i in vari.keys():
        if i in options:
            st.pyplot(vari[i])
    