import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def grafPie(dfD, dfg, location=""):
    total_precio = dfD.groupby(dfg).count()
    colors = sns.color_palette('pastel')[0:6]
    co = total_precio.columns[0]
    fig, ax = plt.subplots()
    ax.pie(total_precio[co], labels=total_precio.index, colors=colors,
            autopct='%.0f%%')
    plt.title(f"Graph pie: {location}")
    # plt.show()
    
    st.pyplot(fig)


def grafBar(data, location=""):
    fig = plt.figure(figsize=(10, 5))
    # plt.title(f"Inscription by {data.name}: {location}")
    sns.countplot(data, order=data.value_counts().index)
    plt.xticks(rotation=90)
    plt.show()


def graf3Rel(df, xd, yd, zd):

    sns.relplot(x=xd, y=yd, hue=zd, data=df)
    # plt.title(f"Inscription by {df.university.unique()[0]}")
    plt.xticks(rotation=90)
    plt.show()


def grafBox(var1, var2, location=""):
    # plt.title(f"Inscription by {var1.name}:{var2.name}:{location}")
    sns.boxplot(x=var1, y=var2)
    plt.xticks(rotation=90)
    plt.show()


def grafViolin(df, x, y, location=""):
    # plt.title(f"Inscription by {var1.name}:{var2.name}:{location}")
    sns.violinplot(data=df, x=x, y=y)
    plt.xticks(rotation=90)
    plt.show()


def PieObj(df):
    df.info()
    dataObj = df.select_dtypes(object)
    dataNum = df.select_dtypes(include=[np.float64, np.int64])

    dataO = dataObj.columns[:]
    dataN = dataNum.columns[:]
    dfNum = df[dataN]
    for i in dataO:
        grafPie(dfD=df, dfg=i, location=i)
    #  To work with st , work with fig and ax 
    fig, ax = plt.subplots()
    dfNum.hist(bins=20,ax=ax)
    fig.tight_layout()  # Separate subplots 
    st.pyplot(fig)

def grupoB():
    icon = "🕮"
    title = "Analisis de datos exploratorios"
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Grupo B")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()
    
    df = pd.read_sql(sqlCommands[0], conn)

    # print(df)
    st.table(df)
    
    # Close connection
    conn.close()

def generalEDA():
    icon = "🕮"
    title = "Analisis de datos exploratorios"
    sns.set_theme()
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Analisis EDA")
    
    message = '''# EDA
Analisis de datos de caso propuesto base de datos de datos de Proyectos de construcción en Colombia.

- ¿Cuál es el comportamiento de la constructura por proyecto?
- ¿Cuál es el comportamiento del valor de los Proyectos?
- ¿Cuál es el comportamiento de la constructura por variables categoricas y numericas?'''
    
    st.markdown(message)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
    conn = connectionBD()

    dfCompra = pd.read_sql(sql=sqlCommands[0],con= conn)
    dfLider = pd.read_sql(sql=sqlCommands[1],con= conn)
    dfMaterial = pd.read_sql(sql=sqlCommands[2],con= conn)
    dfProyecto = pd.read_sql(sql=sqlCommands[3],con= conn)
    dfTipo = pd.read_sql(sql=sqlCommands[4],con= conn)
    dfPrecios = pd.read_sql(sql=sqlCommands[5],con= conn)
    dfCostoPro = pd.read_sql(sql=sqlCommands[6],con= conn)


    data = [dfCompra,dfLider,dfMaterial,dfPrecios,dfProyecto,dfTipo,dfPrecios,dfCostoPro]

    # print(df)
    # st.table(dfCostoPro)
    for dataob in data:
        PieObj(dataob)
    # Close connection
    conn.close()
