import streamlit as st
from PageFunctions import HouseGraph

def app():
    st.title('부동산 회귀 분석 그래프')
    
    vari = {'부동산 회귀 분석 그래프' : HouseGraph.HouseGraph_maker()}
    
    options = st.multiselect('그래프를 선택해주세요', vari)
    
    for i in vari.keys():
        if i in options:
            st.pyplot(vari[i])