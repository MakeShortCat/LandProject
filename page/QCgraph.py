import os
os.chdir(r'C:/Users/pgs66/Desktop/GoogleDrive/python/Project1')
import streamlit as st
from PageFunctions import GraphMaker

def app():
    
    st.title('QC전,후 그래프')
    
    vari = {'원본' : GraphMaker.original_graph,
            '이상값 삽입' : GraphMaker.Out_Range_Graph,
            '결측치 검사' : GraphMaker.nan_Graph,
            '한계값 검사' : GraphMaker.Limit_Graph,
            '단계 검사' : GraphMaker.Step_Graph,
            '지속성 검사' : GraphMaker.Continue_Graph,
            '전체비교' : GraphMaker.fig1}
    options = st.multiselect('그래프를 선택해주세요', vari)
    
    for i in vari.keys():
        if i in options:
            st.pyplot(vari[i])

# 파일별로 app을 만들어서 app.py에서 모은다
# multipage에 add_app 이라는 class를 만들어서