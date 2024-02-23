import streamlit as st
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
import os 

import yfinance as yf
from view.Datos import yahooFinance
import matplotlib.pyplot as plt


def visualizacion():
    icon = "📊"
    title = "Visualizacion de datos"
    
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()
    
    compras = pd.read_sql(sqlCommands[0], conn)
    lideres = pd.read_sql(sqlCommands[1], conn)
    materiales = pd.read_sql(sqlCommands[2], conn)
    tipos = pd.read_sql(sqlCommands[3], conn)
    proyectos = pd.read_sql(sqlCommands[4], conn)


    # Unir la tabla de proyectos con la de tipos
    tabla_pt= pd.merge(proyectos,tipos,on='ID_Tipo', how='inner')
    # ahora unimos la de lideres a la anterior
    tabla_ptl= pd.merge(tabla_pt,lideres,on='ID_Lider', how='inner')

    #unimos la tabla compras con la de materiales 
    tabla_cm = pd.merge(compras, materiales, on='ID_MaterialConstruccion', how='inner')
    # unimos la de compras y materiales a la de proyectos anterior
    tabla_final = pd.merge(tabla_ptl,tabla_cm,on="ID_Proyecto",how="inner")

    st.write("Graficas de la tabla de datos de la constructora")
    st.write(tabla_final)

    agrupados = proyectos.groupby('Constructora').size().reset_index(name='cantidad_proyectos')
    st.dataframe(agrupados)
    # Graficar la cantidad de proyectos por constructora
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(agrupados['Constructora'], agrupados['cantidad_proyectos'])
    ax.set_ylabel('Cantidad de Proyectos')
    ax.set_xlabel('Constructora')
    ax.set_title('Cantidad de Proyectos por Constructora')
    plt.xticks(rotation=45, ha='right')
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)


    # Agrupar proyectos por Banco_Vinculado y contar la cantidad de proyectos por cada banco vinculado
    agrupados = proyectos.groupby('Banco_Vinculado').size().reset_index(name='cantidad_proyectos')

    # Configurar la aplicación Streamlit
    st.title('Visualización de Proyectos por Banco Vinculado')

    # Mostrar los datos agrupados
    st.dataframe(agrupados)

    # Ajustar el tamaño de la figura
    fig, ax = plt.subplots(figsize=(10, 6))  # Puedes ajustar los valores (ancho, alto) según tus necesidades

    # Graficar la cantidad de proyectos por Banco_Vinculado
    ax.bar(agrupados['Banco_Vinculado'], agrupados['cantidad_proyectos'])
    ax.set_ylabel('Cantidad de Proyectos')
    ax.set_xlabel('Banco Vinculado')
    ax.set_title('Cantidad de Proyectos por Banco Vinculado')

    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    st.write("Grafica de precios historicos")
    data = yahooFinance()

    cryptos = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'ADA-USD']
        #  Bitcoinb  , Ethereum,   XRP    , Litecoin , Bitcoins cash, Cardano
    
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plotear los datos
    for crypto in cryptos:
        ax.plot(data.index, data[crypto], label=crypto)

    # Personalizar el gráfico
    ax.set_title('Precios Históricos de Criptomonedas')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio de Cierre Ajustado')
    ax.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



    st.write("Hallamos los rendimientos diarias")
    returns = data.pct_change().dropna()
    st.write(returns.head())


    st.write("Graficas de rendimientos diarios")
    # Crear la figura
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotear el histograma
    returns.hist(bins=50, figsize=(12, 8), alpha=0.5, ax=ax)

    # Personalizar el gráfico
    ax.set_title('Histograma de Rendimientos de Criptomonedas')
    ax.set_xlabel('Rendimiento')
    ax.set_ylabel('Frecuencia')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)