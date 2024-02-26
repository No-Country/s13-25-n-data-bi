import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
from view.Datos import yahooFinance


def limpieza():
    icon = "🧹"
    title = "Limpieza de datos"

    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Revision de informacion faltante de los datasets")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()
    table1 = pd.read_sql(sqlCommands[0], conn)
    table2 = pd.read_sql(sqlCommands[1], conn)
    table3 = pd.read_sql(sqlCommands[2], conn)
    table4 = pd.read_sql(sqlCommands[3], conn)
    table5 = pd.read_sql(sqlCommands[4], conn)

    st.write("Tabla de Compras")
    st.table(table1.head())
    st.write("Observamos si hay datos nulos")
    st.write(table1.isnull().sum())
    st.write("Tabla de Lideres")
    st.table(table2.head())
    st.write("Observamos si hay datos nulos")
    st.write(table2.isnull().sum())
    st.write("Tabla de Materiales")
    st.table(table3.head())
    st.write("Observamos si hay datos nulos")
    st.write(table3.isnull().sum())
    st.write("Tabla de Tipos")
    st.table(table4.head())
    st.write("Observamos si hay datos nulos")
    st.write(table4.isnull().sum())
    st.write("Tabla de Proyectos")
    st.table(table5.head())
    st.write("Observamos si hay datos nulos")
    st.write(table5.isnull().sum())

    st.write("Muestras de las tabla de yahoo finance")
    data = yahooFinance()
    st.table(data.head())

    st.write("Observamos si hay datos nulos")
    st.write(data.isnull().sum())



