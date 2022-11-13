import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import datetime
import streamlit as st

pick = st.session_state["Pick_stock"]

df = yf.download(pick+'.NS', period='2d', interval='5m')
# df=yf.download('awl.ns',period='1mo',interval='1d')

newdata = df.resample('D').agg(
    {'High': max, 'Low': min, 'Open': 'first'}).dropna()
newdata['P_D_High'] = newdata['High'].shift(1)
newdata['P_D_Low'] = newdata['Low'].shift(1)
newdata['UP_H-L*0.55+O'] = round((newdata['P_D_High'] -
                                  newdata['P_D_Low'])*0.55+newdata['Open'], 2)
newdata['LB_H-L*0.55-O'] = round((newdata['P_D_High'] -
                                  newdata['P_D_Low'])*0.55-newdata['Open'], 2)


df = yf.download(pick+'.NS', period='1d', interval='5m')
# df=yf.download('^NSEI',start='2022-08-22',end='2022-08-24',interval='5M')
mthly_lvls = df.copy(deep=True)
sessions_break = [i for i in list(
    mthly_lvls.resample('D').mean().dropna().index)]
# for i in list(df.resample('D').mean().dropna().index):
#     sessions_break.append(str(i))
vlines = tuple(sessions_break)
# impt_levels=tuple([df['High'].max(),df['Low'].min(),df['Close'].max(),df['Close'].min(),df.describe().loc['50%']['Close']])
impt_levels = tuple(abs(newdata.iloc[-1:, 3:].values[0]))
# impt_levels=(39603.949219,38489.351562,39419.73,38193.67)
mystyle = mpf.make_mpf_style(base_mpf_style='yahoo', gridstyle="")
st.set_option('deprecation.showPyplotGlobalUse', False)
fig1 = mpf.plot(df,
                style=mystyle,
                type='candlestick',
                figsize=(16, 16),
                vlines=dict(vlines=vlines[1:], linestyle="-.",
                            linewidths=0.5, alpha=0.5, colors=['darkgray']),
                hlines=dict(hlines=(impt_levels), colors=[
                    'green', 'red', 'lightgreen', 'pink'], linewidths=[1], alpha=0.5,),
                volume=True)
st.pyplot(fig1)
