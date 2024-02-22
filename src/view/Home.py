


import streamlit as st
import pandas as pd
import sys
import os
from view.GrupoB import grupoB,generalEDA,edaArque
def main():
    #  Conexion a la base de datos

    # Tabs
    page_names_to_funcs = {
        "Home Page": grupoB,
        "EDA": generalEDA,
        "Arquitectura S.A.": edaArque,
        # "Update": update,
        # "Delete": delete,
    }
    v = sys.version.split(" ")

    st.sidebar.header(f"🐍 {v[0]}")
 

    selected_page = st.sidebar.selectbox(
        "Selecciona una página", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()


if __name__ == "__main__":

    
    print("HOME")

