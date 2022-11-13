import streamlit as st
import cufflinks as cf
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

st.write("Home Page")
st.sidebar.success("Select a page above")


if "Pick_stock" not in st.session_state:
    st.session_state["Pick_stock"] = ""

pick = st.text_input("Enter Stock Name", st.session_state["Pick_stock"])
submit_stk = st.button("Submit_stock")
if submit_stk:
    st.session_state["Pick_stock"] = pick
    st.write("You Selected: ", pick)

if "Pick_index" not in st.session_state:
    st.session_state["Pick_index"] = ""

index = st.text_input("Enter Index Name", st.session_state["Pick_index"])
submit = st.button("Submit_index")
if submit:
    st.session_state["Pick_index"] = index
    st.write("You Selected: ", index)


st.set_option("deprecation.showPyplotGlobalUse", False)

kdf = yf.download(pick+".NS", period='1d', interval='5m')
qf = cf.QuantFig(kdf, asFigure=True, legend="top", name="Intraday")
qfs = qf.iplot(asFigure=True)
st.write("---")

# st.plotly_chart(qfs)


akdf = yf.download(pick+".NS", period='1mo', interval='1d')
aqf = cf.QuantFig(akdf, asFigure=True, legend="top", name="Daily")
aqfs = aqf.iplot(asFigure=True)
st.write("---")
# st.plotly_chart(aqfs)


wkdf = yf.download(pick+".NS", period='1mo', interval='1wk')
wqf = cf.QuantFig(wkdf, asFigure=True, legend="top", name="Weekly")
wqfs = wqf.iplot(asFigure=True)
st.write("---")

a1, a2 = st.columns([1, 1])
a1.plotly_chart(wqfs, use_container_width=True)
a2.plotly_chart(aqfs, use_container_width=True)

st.plotly_chart(qfs, use_container_width=True)

count = st_autorefresh(interval=6000, limit=200,
                       key="fizzbuzzcounter")
if count == 200:
    st.write("Please Refresh Page")
else:
    st.write(count)
