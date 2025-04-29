# Importar bibliotecas necessárias
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


class DadosAcoes:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
    
    def obter_dados_acoes(ticker, start, end):
            ticker = 'AAPL'  # Ticker da ação da Apple
            data = yf.download(ticker, start='2018-01-01', end='2023-01-01')  # Dados de 5 anos

            print("Dados obtidos:")
            print(data.head())

            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

            data['Target'] = data['Close'].shift(-1)

            data = data[:-1]

            X = data[['Open', 'High', 'Low', 'Volume']]  # Features
            y = data['Target']  # Alvo

            # Passo 4: Dividir os dados em treinamento e teste
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)                
            model = LinearRegression()
            model.fit(X_train, y_train)

                
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            if mse:
                return f'Erro quadrático médio (MSE): {mse}'    
                
            for actual, predicted in zip(y_test[:5], y_pred[:5]):
                return f"Atual: {actual:.2f}, Previsto: {predicted:.2f}" 

        
            
            


