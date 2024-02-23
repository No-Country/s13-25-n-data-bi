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
    return data


def datos():
    icon = "📂"
    title = "Datos"
    
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Muestras de las tablas de la base de datos de la constructora")
    

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
    st.write("Tabla de Lideres")
    st.table(table2.head())
    st.write("Tabla de Materiales")
    st.table(table3.head())
    st.write("Tabla de Tipos")
    st.table(table4.head())
    st.write("Tabla de Proyectos")
    st.table(table5.head())


    st.write("Muestras de las tablas de la base de datos de yahoo Finance")
    
    st.write("Tabla de Criptomonedas")
    data = yahooFinance()
    st.table(data.head())
    
    conn.close()
