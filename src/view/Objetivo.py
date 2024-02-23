import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD



def objetivo():
    icon = "🎯"
    title = "Objetivos "
    
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Objetivos del analisis")


    st.write("¿Que lider o lideres tienen mayor porcentaje de finalizacion de proyectos?")
    st.write("¿Cuanto se gasta en materiales cada lider por proyecto?")
    st.write("¿Que banco tiene mayor presencia en el tema de construcciones?")
    st.write("¿Cual es el estrato donde hay un mayor indice de construcciones?")

    st.write("¿Como podemos escoger cual es la criptomoneda mas rentable para invertir?")

    
