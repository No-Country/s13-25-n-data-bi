import streamlit as st
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
import os 
from view.Datos import yahooFinance
import matplotlib.pyplot as plt
import seaborn as sns


def visualizacion():
    icon = "📊"
    title = "Visualizacion de datos"

    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Graficas de la informacion obtenida")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()

    compras = pd.read_sql(sqlCommands[0], conn)
    lideres = pd.read_sql(sqlCommands[1], conn)
    materiales = pd.read_sql(sqlCommands[2], conn)
    tipos = pd.read_sql(sqlCommands[3], conn)
    proyectos = pd.read_sql(sqlCommands[4], conn)

    tabla_pt= pd.merge(proyectos, tipos, on='ID_Tipo', how='inner')
    tabla_ptl= pd.merge(tabla_pt, lideres, on='ID_Lider', how='inner')
    tabla_cm = pd.merge(compras, materiales, on='ID_MaterialConstruccion', how='inner')

    tabla_final = pd.merge(tabla_ptl, tabla_cm, on="ID_Proyecto", how="inner")
    
    columnas = ["ID_Proyecto","Acabados","Estrato","Ciudad","Constructora","Banco_Vinculado","Porcentaje_Cuota_Inicial","Financiable","Clasificacion_x","Nombre_Material","Cantidad","Precio_Unidad","Pagado","Proveedor"]
    st.subheader("Informacion de la BD de la constructora")
    st.write(tabla_final[columnas])


    # Graficas de proyectos terminados y no terminados
    conteo_proyectos = tabla_final.groupby('Acabados').size().reset_index(name='Cantidad')
    

    porcentajes = tabla_final.groupby('Acabados').size() / len(tabla_final) * 100

    fig, ax = plt.subplots()
    ax.pie(porcentajes, labels=porcentajes.index, autopct='%1.1f%%', startangle=90)
    st.title('Porcentaje de proyectos terminados')
    st.dataframe(conteo_proyectos)
    st.pyplot(fig)


    # Ciudades------------------------

    data = {
    'Ciudad': ['Manizales', 'Ibague', 'Pereira', 'Neiva', 'Barranquilla', 'Salento', 'Armenia', 'Monteria', 'Bogota', 'Bucaramanga', 'Santa Marta', 'Quibdo', 'Sta. Rosa de Cabal', 'Cartago', 'Cartagena'],
    'LAT': [5.0679, 4.4389, 4.8143, 2.9273, 10.9639, 4.6378, 4.5343, 8.7489, 4.6097, 7.1139, 11.2315, 5.6928, 4.868, 4.7466, 10.3997],
    'LON': [-75.5174, -75.2323, -75.6944, -75.2808, -74.7990, -75.6146, -75.6818, -75.8815, -74.0817, -73.1198, -74.2009, -76.6503, -75.6218, -75.5468, -75.5144]
    }

    porcentajes = tabla_final.groupby('Ciudad').size().reset_index(name='# Proyectos x Ciudad')
    

    st.title("Ciudades donde se realizaron proyectos")
    st.dataframe(porcentajes)
    st.map(data)

    # -------------------------------------

    pivot_table = pd.pivot_table(tabla_final, values='Clasificacion_x', index=['Estrato', 'Banco_Vinculado'], aggfunc='count').unstack()
    columnas_bancos = pivot_table.columns.get_level_values('Banco_Vinculado')
    pivot_table.columns = columnas_bancos
    st.table(pivot_table)

    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_table.plot(kind='bar', stacked=True, ax=ax)
    plt.legend(title='Clasificacion_x', bbox_to_anchor=(1, 1))
    plt.xlabel('Estrato y Bancos Vinculados', fontsize=14)
    plt.ylabel('Cantidad', fontsize=18)
    ax.set_xticklabels(ax.get_xticklabels())
    st.pyplot(fig)

    # -------- Grafica relacion vivienda y entidad bancaria --------------------
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='Clasificacion_x', hue='Banco_Vinculado', data=tabla_final)
    plt.title('Relación entre Tipo de Vivienda y Entidad Bancaria')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    fig3, ax3 = plt.subplots()
    tabla_final['Banco_Vinculado'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Distribución de Inversiones entre Entidades Bancarias')
    st.pyplot(fig3)


    # ------- Grafica relación tipo de vivienda y material utilizado ------------
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='Clasificacion_x', hue='Nombre_Material', data=tabla_final)
    plt.title('Relación entre Tipo de Vivienda y Material Utilizado')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    # Ejemplo de un gráfico de barras apiladas
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='Nombre_Material', data=tabla_final)
    plt.title('Patrones en Tipos de Materiales Seleccionados')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)



    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Banco_Vinculado', y='Porcentaje_Cuota_Inicial', data=tabla_final)
    plt.title('Diferencias en Términos de Financiamiento')
    st.pyplot(fig4)

    # Grafica de cantidad de proyectos de la constructora -----------------------
    agrupados = proyectos.groupby('Constructora').size().reset_index(name='cantidad_proyectos')
    st.dataframe(agrupados)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(agrupados['Constructora'], agrupados['cantidad_proyectos'])
    ax.set_ylabel('Cantidad de Proyectos')
    ax.set_xlabel('Constructora')
    ax.set_title('Cantidad de Proyectos por Constructora')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


    # Agrupar proyectos por Banco_Vinculado y contar la cantidad de proyectos por cada banco vinculado
    agrupados = proyectos.groupby('Banco_Vinculado').size().reset_index(name='cantidad_proyectos')
    st.title('Visualización de Proyectos por Banco Vinculado')
    st.dataframe(agrupados)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(agrupados['Banco_Vinculado'], agrupados['cantidad_proyectos'])
    ax.set_ylabel('Cantidad de Proyectos')
    ax.set_xlabel('Banco Vinculado')
    ax.set_title('Cantidad de Proyectos por Banco Vinculado')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)



    # ----------------- Graficas de las cryptomonedas -----------------------------
    st.subheader("Informacion de la BD de las CryptoMonedas")
    data = yahooFinance()
    cryptos = ['Cardano', 'Bitcoin Cash', 'Bitcoin', 'Ethereum', 'Litecoin', 'Ripple']

    st.write("Hallamos los rendimientos diarias")
    returns = data.pct_change().dropna() # Halla el cambio porcentual de datos consecutivos
    st.write(returns.head())


    st.write("Graficas de rendimientos diarios")
    fig, ax = plt.subplots(figsize=(12, 8))
    returns.hist(bins=50, figsize=(12, 8), alpha=0.5, ax=ax)
    ax.set_title('Histograma de Rendimientos de Criptomonedas')
    ax.set_xlabel('Rendimiento')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    returns = data.pct_change().dropna()
    for crypto in cryptos:
        returns[f'{crypto}_Target'] = (returns[crypto] > 0).astype(int)
    data_reset = returns.reset_index()
    data_reset['Date'] = pd.to_datetime(data_reset['Date']).dt.date
    cumulative_returns = (1 + returns).cumprod() - 1
    plt.figure(figsize=(10, 6))
    for crypto in cryptos:
        plt.bar(crypto, cumulative_returns[f'{crypto}'].iloc[-1], label=f'{crypto}')
    plt.title('Rendimiento acumulado de las 6 criptomonedas')
    plt.xlabel('Criptomoneda')
    plt.ylabel('Rendimiento Acumulado')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)
