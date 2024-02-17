import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD


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
