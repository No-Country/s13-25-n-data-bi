import streamlit as st
import sys
<<<<<<< HEAD
import os
from view.GrupoB import grupoB,generalEDA,edaArque
=======
from view.Datos import datos
from view.Objetivo import objetivo
from view.Limpieza import limpieza
from view.Exploracion import exploracion
from view.Visualizacion import visualizacion
from view.ML import ml
from view.Conclusiones import conclusiones


>>>>>>> jorgehn
def main():
    #  Conexion a la base de datos

    # Tabs
    page_names_to_funcs = {
<<<<<<< HEAD
        "Home Page": grupoB,
        "EDA": generalEDA,
        "Arquitectura S.A.": edaArque,
        # "Update": update,
        # "Delete": delete,
=======
        "Objetivo": objetivo,
        "Datos": datos,
        "Limpieza": limpieza,
        "Exploracion": exploracion,
        "Visualizacion": visualizacion,
        "ML": ml,
        "Conclusiones": conclusiones,
>>>>>>> jorgehn
    }

    v = sys.version.split(" ")

    st.sidebar.header(f"🐍 {v[0]}")

    selected_page = st.sidebar.selectbox(
        "Selecciona una página", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()


if __name__ == "__main__":
    print("HOME")


