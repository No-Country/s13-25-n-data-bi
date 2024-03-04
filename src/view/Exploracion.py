import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
from view.Datos import yahooFinance


def exploracion():
    icon = "🔍"
    title = "Exploracion de los datos"

    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Resumen estadistico de las tablas de la base de datos")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()

    compras = pd.read_sql(sqlCommands[0], conn)
    lideres = pd.read_sql(sqlCommands[1], conn)
    materiales = pd.read_sql(sqlCommands[2], conn)
    tipos = pd.read_sql(sqlCommands[3], conn)
    proyectos = pd.read_sql(sqlCommands[4], conn)

    st.write("Resumen estadistico de tabla de Compras")
    st.write(compras.describe().round(2))
    st.write("Resumen estadistico de tabla de Lideres")
    st.write(lideres.describe().round(2))
    st.write("Resumen estadistico de tabla de Materiales")
    st.write(materiales.describe().round(2))
    st.write("Resumen estadistico de tabla de Tipos")
    st.write(tipos.describe().round(2))
    st.write("Resumen estadistico de tabla de Proyectos")
    st.write(proyectos.describe().round(2))

    # Unir la tabla de proyectos con la de tipos
    tabla_pt = pd.merge(proyectos, tipos, on='ID_Tipo', how='inner')
    # ahora unimos la de lideres a la anterior
    tabla_ptl = pd.merge(tabla_pt, lideres, on='ID_Lider', how='inner')

    # unimos la tabla compras con la de materiales
    tabla_cm = pd.merge(compras, materiales, on='ID_MaterialConstruccion', how='inner')

    # unimos la de compras y materiales a la de proyectos anterior
    tabla_final = pd.merge(tabla_ptl, tabla_cm, on="ID_Proyecto", how="inner")
    st.write("Join de las tablas")
    st.write(tabla_final.head())
    st.write("Resumen estadistico del Join de las tablas")
    st.write(tabla_final.describe())

    data = yahooFinance()

    st.write("Resumen estadistico de los datos de YahooFinance")
    st.write(data.describe().round(2))
