import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'MXVIRAG6BRPCIN0O'
BASE_URL = 'https://www.alphavantage.co/query'

# Function to get real-time stock data
def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (1min)' in data:
        return data['Time Series (1min)']
    else:
        return None

# Class to manage the stock portfolio
class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol] += shares
        else:
            self.stocks[symbol] = shares

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol] -= shares
            if self.stocks[symbol] <= 0:
                del self.stocks[symbol]

    def get_portfolio_value(self):
        total_value = 0
        for symbol, shares in self.stocks.items():
            stock_data = get_stock_data(symbol)
            if stock_data:
                latest_price = float(list(stock_data.values())[0]['4. close'])
                total_value += latest_price * shares
        return total_value

    def display_portfolio(self):
        for symbol, shares in self.stocks.items():
            print(f'{symbol}: {shares} shares')

# Main function to interact with the user
def main():
    portfolio = Portfolio()
    while True:
        print("\n1. Add Stock\n2. Remove Stock\n3. View Portfolio\n4. View Portfolio Value\n5. Quit")
        choice = input("Enter your choice: ")
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            value = portfolio.get_portfolio_value()
            print(f'Total Portfolio Value: ${value:.2f}')
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()