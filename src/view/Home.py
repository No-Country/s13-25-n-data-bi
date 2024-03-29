import streamlit as st
import sys
from view.Datos import datos
from view.Objetivo import objetivo
from view.Limpieza import limpieza
from view.Exploracion import exploracion
from view.Visualizacion import visualizacion
from view.ML import ml
from view.Conclusiones import conclusiones


def main():
    #  Conexion a la base de datos

    # Tabs
    page_names_to_funcs = {
        "Objetivo": objetivo,
        "Datos": datos,
        "Limpieza": limpieza,
        "Exploracion": exploracion,
        "Visualizacion": visualizacion,
        "ML": ml,
        "Conclusiones": conclusiones,
    }

    v = sys.version.split(" ")

    st.sidebar.header(f"🐍 {v[0]}")

    selected_page = st.sidebar.selectbox(
        "Selecciona una página", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()


if __name__ == "__main__":
    print("HOME")


