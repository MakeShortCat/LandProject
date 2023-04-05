import streamlit as st

# 페이지 추가하는 메서드 정의

class MultiPage:
    
    PageName0 = {}
    PageName1 = {}
    PageList = [PageName0, PageName1]
    
    def add_page(self, PageNameWeb, PageContent, Listnum):
        MultiPage.PageList[Listnum][PageNameWeb] = PageContent
        
    
        

        
        
