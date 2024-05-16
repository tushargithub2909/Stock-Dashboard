import streamlit as st,pandas as pd,numpy as np,yfinance as yf
import plotly.express as px

st.title('Stock Dashboard')

ticker=st.sidebar.text_input('Ticker',value='MSFT')
start_date=st.sidebar.text_input('Start Date',value='2021-12-24')
end_date=st.sidebar.text_input('End Date',value='2022-12-24')

data=yf.download(ticker,start=start_date,end=end_date)
fig=px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)

pricing_data,fundameantal_data,news=st.tabs(['Pricing Data','Fundameantal Data','Top 10 news'])

with pricing_data :
    st.header('Pricing Movement')
    data2=data
    data2['% Change']=data['Adj Close']/data['Adj Close'].shift(1)-1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return=data2['% Change'].mean()*252*100
    st.write('Annual Return is ',annual_return,'%')
    stdev=np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard deviation is ',stdev*100,'%')
    st.write('Risk Adj. Return is',annual_return/(stdev*100))

from alpha_vantage.fundamentaldata import FundamentalData
with fundameantal_data :
    key='83504ea78e14483586ea72db936e236e'
    fd=FundamentalData(key,output_format='pandas')
    st.subheader('Balanced Sheet')
    balanced_sheet=fd.get_balance_sheet_annual(ticker)[0]
    bs=balanced_sheet.T[2:]
    bs.columns=list(balanced_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement=fd.get_income_statement_annual(ticker)[0]
    is1=income_statement.T[2:]
    is1.columns=list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow=fd.get_cash_flow_annual(ticker)[0]
    cf=cash_flow.T[2:]
    cf.columns=list(cash_flow.T.iloc[0])
    st.write(cf)

from stocknews import StockNews

with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]  # Corrected column name
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')
