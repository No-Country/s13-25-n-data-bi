import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD

import nbformat
import numpy as np

# def grupoJ():
#     icon = "🐴"
#     title = "Analisis de datos exploratorios Pegasso"
    
#     st.markdown(f"# {title} {icon}")
#     st.sidebar.markdown(f"# {title} {icon}")
#     st.write("Grupo J")

#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     sqlCommands = sqlCommand(path=BASE_DIR+"/data/sql/")
#     conn = connectionBD()
    
#     table1 = pd.read_sql(sqlCommands[0], conn)
#     table2 = pd.read_sql(sqlCommands[1], conn)

#     st.table(table1)
#     st.table(table2)
    
#     conn.close()

def grupoJ():
    st.title("Colab Notebook en Streamlit")

    st.write("Here's our first attempt at using data to create a table:")
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    }))

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construye la ruta completa al archivo .ipynb
    notebook_path = os.path.join(BASE_DIR, "..", "cripto.ipynb")

    # Imprime la ruta para verificar
    print(f'Ruta del archivo .ipynb: {notebook_path}')

    # Verifica la existencia del archivo
    if os.path.exists(notebook_path):
        
        # Carga el contenido del archivo .ipynb
        with open(notebook_path, "r", encoding="utf-8") as notebook_file:
            notebook_content = nbformat.read(notebook_file, as_version=4)

        # Muestra cada celda en Streamlit
        for cell in notebook_content['cells']:
            if cell['cell_type'] == 'code':
                st.code(cell['source'])
            elif cell['cell_type'] == 'markdown':
                st.markdown(cell['source'])
    else:
        st.error(f"El archivo {notebook_path} no existe.")