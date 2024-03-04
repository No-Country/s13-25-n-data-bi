import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
import yfinance as yf
from datetime import datetime, timedelta


def yahooFinance():
    cryptos = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'ADA-USD']
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=4*365)).strftime("%Y-%m-%d")
    data = yf.download(cryptos, start=start_date, end=end_date)["Adj Close"]

    nombres_cryptos = {
        'BTC-USD': 'Bitcoin',
        'ETH-USD': 'Ethereum',
        'XRP-USD': 'Ripple',
        'LTC-USD': 'Litecoin',
        'BCH-USD': 'Bitcoin Cash',
        'ADA-USD': 'Cardano'
    }
    data.columns = [nombres_cryptos[c] for c in data.columns]
    return data


def datos():
    icon = "📂"
    title = "Datos"

    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Muestras de las tablas de la base de datos")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()

    compras = pd.read_sql(sqlCommands[0], conn)
    lideres = pd.read_sql(sqlCommands[1], conn)
    materiales = pd.read_sql(sqlCommands[2], conn)
    tipos = pd.read_sql(sqlCommands[3], conn)
    proyectos = pd.read_sql(sqlCommands[4], conn)

    st.subheader("Muestra de la BD de la constructora")
    st.write("Tabla de Compras")
    st.table(compras.head())
    st.write("Tabla de Lideres")
    st.table(lideres.head())
    st.write("Tabla de Materiales")
    st.table(materiales.head())
    st.write("Tabla de Tipos")
    st.table(tipos.head())
    st.write("Tabla de Proyectos")
    st.table(proyectos.head())

    # Unir la tabla de proyectos con la de tipos
    tabla_pt = pd.merge(proyectos, tipos, on='ID_Tipo', how='inner')
    # ahora unimos la de lideres a la anterior
    tabla_ptl = pd.merge(tabla_pt, lideres, on='ID_Lider', how='inner')
    # unimos la tabla compras con la de materiales
    tabla_cm = pd.merge(compras, materiales, on='ID_MaterialConstruccion', how='inner')
    # unimos la de compras y materiales a la de proyectos anterior
    tabla_final = pd.merge(tabla_ptl, tabla_cm, on="ID_Proyecto", how="inner")

    st.write("Join de las tablas de la constructora")
    st.write(tabla_final.head())

    st.subheader("Muestras de las tablas de la base de datos de yahoo Finance")
    st.write("Tabla de Criptomonedas")
    data = yahooFinance()
    st.table(data.head())

    conn.close()
