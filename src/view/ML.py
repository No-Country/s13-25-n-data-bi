import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from view.Datos import yahooFinance
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def ml():
    # ------------------------- Titulo -------------------------------
    icon = "🧠"
    title = "Modelo de Machine Learning"
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")

    # ------------- Obtenemos los datos de yahoo finance -------------
    data = yahooFinance()

    cryptos = ['Cardano', 'Bitcoin Cash', 'Bitcoin', 'Ethereum', 'Litecoin', 'Ripple']

    # Creamos una columna target para cada criptomoneda ya que haremos una clasificación binaria
    # Hallamos los rendimientos diarios
    returns = data.pct_change().dropna()

    for crypto in cryptos:
        returns[f'{crypto}_Target'] = (returns[crypto] > 0).astype(int)

    # -------------- Reseteamos los indices --------------------------
    data_reset = returns.reset_index()
    data_reset['Date'] = pd.to_datetime(data_reset['Date']).dt.date

    st.dataframe(data_reset)
    st.write("Revisamos si hay datos nulos")
    st.dataframe(data_reset.isnull().sum())

    # Dividimos los datos para tomar los de entrenamiento y los de prueba
    X_train, X_test, y_train, y_test = train_test_split(returns.drop(columns=[f'{crypto}_Target' for crypto in cryptos]),
                                                        returns[[f'{crypto}_Target' for crypto in cryptos]],
                                                        test_size=0.2, random_state=42)

    # Creamos el modelo de clasificacion (Random Forest) y lo entremos con los datos
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Realizamos las predicciones en el conjunto de prueba
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    st.write(f'Accuracy: {accuracy:.2f}')

    st.write('Classification Report:')
    st.write(classification_report(y_test, predictions))

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Confusion Matrices for Cryptocurrencies')

    # Iterar a través de las criptomonedas y dibujar las matrices de confusión
    for i, crypto in enumerate(cryptos):
        conf_matrix = pd.crosstab(index=y_test[f'{crypto}_Target'], columns=predictions[:, i],
                                rownames=['Actual'], colnames=['Predicted'])

        # Obtener el índice correcto para el subgráfico
        row_index = i // 3
        col_index = i % 3

        # Dibujar la matriz de confusión en el subgráfico correspondiente
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=axes[row_index, col_index])
        axes[row_index, col_index].set_title(f'{crypto}')

    # Ajustar el diseño y mostrar la figura
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    recommended_crypto = cryptos[model.feature_importances_.argmax()]
    print(f'Recommended Cryptocurrency: {recommended_crypto}')


    # Prediccion del valor de las crypto
    from sklearn.linear_model import LinearRegression
    predictions_df = pd.DataFrame(data)

    for crypto in cryptos:
        X = np.arange(len(data[data.index.year == 2024])).reshape(-1, 1)
        y = data[data.index.year == 2024][crypto].values
        

        model = LinearRegression()
        model.fit(X, y)
        
        predicted_prices = model.predict(np.arange(len(predictions_df)).reshape(-1, 1))
        
        predictions_df[crypto] = predicted_prices
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Graficar las predicciones para el año 2024
    fig,ax =plt.subplots(figsize=(12, 6))
    for crypto in cryptos:
        ax.plot(data[data.index.year == 2024].index, data[data.index.year == 2024][crypto], label=f'{crypto} Valor Real')
        ax.plot(predictions_df.index, predictions_df[crypto], linestyle='--', label=f'{crypto} Predicción')
    ax.set_title('Predicciones de Criptomonedas para el Año 2024')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio de Cierre Ajustado')
    ax.legend()
    st.pyplot()
