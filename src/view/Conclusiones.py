import streamlit as st


def conclusiones():
    icon = "🚀"
    title = "Conclusiones "

    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
    st.write("Conclusiones del analisis")

    st.write("6. ***¿Que banco tiene mayor presencia en el tema de construcciones?***")
    st.write("La precensia de los bancos en los bancos va relacionada con el estado de las construcciones")
    conclusion6 = """Se puede observar que los bancos que tienen mayor indice de construcciones terminadas son los bancos 
    Colmena = 172, 
    Conavi = 142, 
    Colpatria = 136  
    Concluyendo el banco que tiene mayor indice de proyectos terminados es el Banco Conavi ya que cuenta con 1.51% de proyectos terminados.
    """
    st.write(conclusion6)


    st.write("9. ***¿Cuál es el comportamiento del valor de los proyectos?***")
    st.write("El valor de los proyectos puede ser analizado a través del histograma, concluyendo su comportamiento según los atributos siguientes.")
    conclusion9 = """-Variabilidad de costos: El amplio rango de valores, desde el mínimo de 2,386 hasta el máximo de 183,195, junto con una desviación estándar de 35,874.002, indica una gran variabilidad en los costos de los proyectos de construcción.
    -Distribución de costos: La mediana (50%) de 58,804 es significativamente menor que la media de 64,042.1816, sugiriendo que puede haber algunos proyectos con costos muy altos que están sesgando la media hacia arriba. Esto indica una distribución sesgada a la derecha en los costos de los proyectos.
    -Tendencia central: La mayoría de los proyectos de construcción (75%) tienen costos inferiores a 87,121.5, lo que sugiere que la mayoría de los proyectos se sitúan en el rango medio a bajo en términos de costo."""
    st.write(conclusion9)
