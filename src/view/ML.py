# import streamlit as st
# import pandas as pd
# from statsmodels.tsa.api import VAR
# from matplotlib.dates import DateFormatter
# import matplotlib.pyplot as plt
# from view.Datos import yahooFinance
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

# def ml():
#     # ------------------------- Titulo -------------------------------
#     icon = "🧠"
#     title = "Modelo de Machine Learning"
#     st.markdown(f"# {title} {icon}")
#     st.sidebar.markdown(f"# {title} {icon}")

#     # ------------- Obtenemos los datos de yahoo finance -------------
#     data = yahooFinance()

#     cryptos = ['Cardano', 'Bitcoin Cash', 'Bitcoin', 'Ethereum', 'Litecoin', 'Ripple']

#     # Creamos una columna target para cada criptomoneda ya que haremos una clasificación binaria
#     # Hallamos los rendimientos diarios
#     returns = data.pct_change().dropna()

#     for crypto in cryptos:
#         returns[f'{crypto}_Target'] = (returns[crypto] > 0).astype(int)

#     # -------------- Reseteamos los indices --------------------------
#     data_reset = returns.reset_index()
#     data_reset['Date'] = pd.to_datetime(data_reset['Date']).dt.date

#     # Calcular el rendimiento acumulado para cada criptomoneda
#     cumulative_returns = (1 + returns).cumprod() - 1

#     # Visualizar el rendimiento acumulado de las 6 criptomonedas
#     st.write("Rendimiento acumulado de las 6 criptomonedas")
#     plt.figure(figsize=(10, 6))

#     for crypto in cryptos:
#         plt.bar(crypto, cumulative_returns[f'{crypto}'].iloc[-1], label=f'{crypto}')

#     plt.title('Rendimiento acumulado de las 6 criptomonedas')
#     plt.xlabel('Criptomoneda')
#     plt.ylabel('Rendimiento Acumulado')
#     plt.xticks(rotation=45)
#     plt.legend()
#     st.pyplot(plt)

