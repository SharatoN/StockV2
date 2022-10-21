from queue import Empty
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from sp500 import get_SP500_name
import streamlit as st


def get_investment_data(stock_data,difference_data):
    buy_data = []
    buy_data_index=[]
    sell_data = []
    sell_data_index = []
    first=None

    if difference_data[0]>=0:
        sign_prev = 1
    else:
        sign_prev = -1

    for i in range(len(difference_data)-1):
        if difference_data[i+1]>=0:
            sign = 1
        else:
            sign = -1
        
        if sign_prev!=sign:
            if sign_prev==1:
                sell_data.append(f"{stock_data.keys()[i+1]} sell - price: {stock_data[i+1]}")
                sell_data_index.append(i+1)
                if first == None:
                    first = -1
            else:
                buy_data.append(f"{stock_data.keys()[i+1]} buy - price: {stock_data[i+1]}")
                buy_data_index.append(i+1)
                if first == None:
                    first = 1
        sign_prev = sign
    return buy_data,buy_data_index,sell_data,sell_data_index,first

def check_financial_result(data,buy_data, sell_data):
    capitalization = 1

    if first ==1:
        for i in range(len(sell_data_index)):
            capitalization = data[sell_data_index[i]]/data[buy_data_index[i]]*capitalization #long position
            capitalization = data[sell_data_index[i]]/data[buy_data_index[i+1]]*capitalization   #short position

    else:
        for i in range(len(buy_data_index)-1):
            capitalization = data[sell_data_index[i]]/data[buy_data_index[i]]*capitalization   #short position
            capitalization = data[sell_data_index[i+1]]/data[buy_data_index[i]]*capitalization #long position

    return capitalization


st.title("Moving Average as a Open/Close position")

st.sidebar.header('Chose your company/index/currency pair')
data_start = st.sidebar.text_input('Start of investing (yyyy-mm-dd)', '2020-8-20')
data_end= st.sidebar.text_input('End of investing (yyyy-mm-dd)', '2021-8-20')
average_level = st.sidebar.selectbox('Average_level',list(reversed(range(2,101)))) #range 1-100
money = st.sidebar.number_input('Invested money [$]')

name =st.sidebar.selectbox('Chose your company',get_SP500_name()) 

stock_title = name

stock = yf.Ticker(stock_title)

# get stock info
st.header(f'Stock info ({stock_title})')
data = stock.history(start=str(data_start), end=str(data_end))

data

average_data = []

data = data.Close
for i in range(average_level, len(data)):
    start = i - average_level
    end = i
    average_data.append((data[start:end].mean()))


data = data[average_level:]

difference_data = [(data[i]-average_data[i]) for i in range(len(data))]

dict_average_data = {'Average': average_data}

data_clear=[]
data_date=[]
row_data={}

for i in range(len(data)):
    data_clear.append(data[i])
    data_date.append(data.keys()[i])

merge_data = {'Close':data_clear, 'Average':average_data}

difference =  {'Difference':difference_data}

df = pd.DataFrame(merge_data, index = data_date)

dfd = pd.DataFrame(difference, index = data_date)

st.line_chart(df)

st.line_chart(dfd)


buy_data,buy_data_index,sell_data,sell_data_index,first = get_investment_data(data,difference_data)

capitalization = check_financial_result(data,buy_data, sell_data)

st.title(f"Final Result: {round(capitalization*money,2)} $")
buy_data
sell_data
