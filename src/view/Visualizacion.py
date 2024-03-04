import streamlit as st
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
import os 
from view.Datos import yahooFinance
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 



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
    proyectosC = pd.read_sql(sqlCommands[5], conn)

    tabla_pt= pd.merge(proyectos, tipos, on='ID_Tipo', how='inner')
    tabla_ptl= pd.merge(tabla_pt, lideres, on='ID_Lider', how='inner')
    tabla_cm = pd.merge(compras, materiales, on='ID_MaterialConstruccion', how='inner')

    tabla_final = pd.merge(tabla_ptl, tabla_cm, on="ID_Proyecto", how="inner")
    
    columnas = ["ID_Proyecto","Acabados","Estrato","Ciudad","Constructora","Banco_Vinculado","Porcentaje_Cuota_Inicial","Financiable","Clasificacion_x","Nombre_Material","Cantidad","Precio_Unidad","Pagado","Proveedor"]
    st.subheader("Informacion de la BD de la constructora")
    st.write(tabla_final[columnas])


    # Gráfico de barras para mostrar proyectos terminados y no terminados por banco
    st.title("Informacion de proyectos terminados y no terminados por banco")
    tabla_frecuencia = pd.crosstab(tabla_final['Banco_Vinculado'], tabla_final['Acabados'])
    st.dataframe(tabla_frecuencia)

    proyectos_terminados = tabla_frecuencia['Si']
    proyectos_no_terminados = tabla_frecuencia['No']
    promedio_terminados_no_terminados_por_banco = (proyectos_terminados / proyectos_no_terminados)
    df_promedio_terminados_no_terminados = pd.DataFrame({'Banco': promedio_terminados_no_terminados_por_banco.index, 'Promedio_Terminados/NoTerminados': promedio_terminados_no_terminados_por_banco.values})
    df_promedio_terminados_no_terminados = df_promedio_terminados_no_terminados.sort_values(by='Promedio_Terminados/NoTerminados', ascending=False)
    st.dataframe(df_promedio_terminados_no_terminados)

    st.dataframe(tabla_frecuencia.describe())
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Banco_Vinculado', hue='Acabados', data=tabla_final)
    plt.title('Proyectos Terminados y No Terminados por Banco')
    plt.xlabel('Banco')
    plt.ylabel('Cantidad de Proyectos')
    plt.legend(title='Estado')
    st.pyplot(plt)

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
    st.title("Informacion de proyectos por estratos y su relacion con las entidades bancarias")

    pivot_table = pd.pivot_table(tabla_final, values='Clasificacion_x', index=['Estrato', 'Banco_Vinculado'], aggfunc='count').unstack()
    columnas_bancos = pivot_table.columns.get_level_values('Banco_Vinculado')
    pivot_table.columns = columnas_bancos
    st.table(pivot_table)

    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_table.plot(kind='bar', stacked=False, ax=ax)
    plt.legend(title='Clasificacion_x', bbox_to_anchor=(1, 1))
    plt.xlabel('Estrato y Bancos Vinculados', fontsize=14)
    plt.ylabel('Cantidad', fontsize=18)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

    # -------- Grafica relacion vivienda y entidad bancaria --------------------
    st.title("Informacion de proyectos por tipo de vivienda y su relacion con las entidades bancarias")

    tabla_contingencia = pd.crosstab(tabla_final['Clasificacion_x'], tabla_final['Banco_Vinculado'], margins=True, margins_name="Total")
    st.dataframe(tabla_contingencia)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='Clasificacion_x', hue='Banco_Vinculado', data=tabla_final)
    plt.title('Relación entre Tipo de Vivienda y Entidad Bancaria')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)



    st.title("Informacion de entidades bancarias")
    fig3, ax3 = plt.subplots()
    tabla_final['Banco_Vinculado'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Distribución de Inversiones entre Entidades Bancarias')
    st.pyplot(fig3)

    st.title("Informacion de financimiento segun banco y tipo de vivienda")
    # Crear la figura y los ejes
    g = sns.catplot(
        x='Clasificacion_x',
        hue='Banco_Vinculado',
        col='Financiable',
        data=tabla_final,
        kind='count',
        height=18,  # Ajusta este valor según tus necesidades
        aspect=1.2,
        palette='viridis',
    )

    # Ajustar las etiquetas y la leyenda
    g.set_axis_labels('Clasificacion_x', 'Cantidad')
    g.set_titles(col_template="{col_name} Financiable")
    g.add_legend(title='Entidad Bancaria', bbox_to_anchor=(1.05, 0.8), loc='upper left')

    # Ajustar las propiedades del texto y los ejes
    g.set_xticklabels(rotation=45, ha='right', fontsize=12)
    g.set_yticklabels(fontsize=12)
    g.set_titles(fontsize=14)
    g.set_xlabels(fontsize=14)
    g.set_ylabels(fontsize=14)

    # Mostrar la gráfica en Streamlit
    st.pyplot(g)


    # ------- Grafica relación tipo de vivienda y material utilizado ------------
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='Clasificacion_x', hue='Nombre_Material', data=tabla_final)
    plt.title('Relación entre Tipo de Vivienda y Material Utilizado')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)


    st.title("Grafica de porcentaje de cuota inicial segun el banco")

    tabla_promedios = tabla_final.groupby('Banco_Vinculado')['Porcentaje_Cuota_Inicial'].mean().reset_index()
    tabla_promedios = tabla_promedios.sort_values(by='Porcentaje_Cuota_Inicial', ascending=True)
    st.dataframe(tabla_promedios)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Banco_Vinculado', y='Porcentaje_Cuota_Inicial', data=tabla_final) 
    plt.title('Diferencias en Términos de Financiamiento')
    plt.xlabel('Banco Vinculado')
    plt.ylabel('Promedio de Porcentaje de Cuota Inicial')
    st.pyplot(fig)

    # Grafica de cantidad de proyectos de la constructora -----------------------
    st.title("Grafica de cantidad de proyectos segun constructora")
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

    st.markdown(f"# Costo por proyecto :dollar:")
    # Costo por proyecto -----------------------
    st.write("Valor de los proyectos")
    df = st.dataframe(proyectosC)
    

    dtprecioD = proyectosC.describe().Costo_Proyecto
    dtprecio = dtprecioD.to_list()
    mean = dtprecio[1]
    std = dtprecio[2]
    dtprecio = dtprecio[4:7]
    st.write(dtprecioD)

    #  Grafica  histograma por precio de proyecto
    fig, ax = plt.subplots()
    colors = sns.color_palette('pastel')[0:len(dtprecio)]

    plt.title(rf'Histogram of IQ: $\mu={np.round(mean,2)}$, $\sigma={np.round(std,2)}$')
    sns.histplot(x="Costo_Proyecto", kde=True, data=proyectosC)
    #  Grafica cuartiles 25,50,75
    for i,j in enumerate(dtprecio):
        plt.axvline(j,color=colors[i],linestyle='--')
    datlegend = ["kde"]  # estimación de densidad de Kernel (KDE)
    datlegend = datlegend+dtprecio
    plt.legend(datlegend)
    st.pyplot(fig)



    # ----------------- Graficas de las cryptomonedas -----------------------------
    st.subheader("Informacion de la BD de las CryptoMonedas")
    data = yahooFinance()
    cryptos = ['Cardano', 'Bitcoin Cash', 'Bitcoin', 'Ethereum', 'Litecoin', 'Ripple']

    st.write("Hallamos los rendimientos diarias")
    returns = data.pct_change().dropna() # Halla el cambio porcentual de datos consecutivos
    st.write(returns.head())

    fig, ax = plt.subplots(figsize=(12, 6))
    for crypto in cryptos:
        plt.plot(data.index, data[crypto], label=crypto)
    # Ajustar el diseño y las etiquetas
    plt.title('Precios Históricos de Criptomonedas')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre Ajustado')
    plt.legend()
    st.pyplot(fig)


    st.write("Graficas de rendimientos diarios")
    fig, ax = plt.subplots(figsize=(12, 8))
    returns.hist(bins=50, figsize=(12, 8), alpha=0.5, ax=ax)
    ax.set_title('Histograma de Rendimientos de Criptomonedas')
    ax.set_xlabel('Rendimiento')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    returns = data.pct_change().dropna()

    
    