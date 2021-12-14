import pandas as pd
from etherscan import Etherscan
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

def fmt(x):
    print(x)
    return '{:.4f}%\n({:.0f})'.format(x, total*x/100)

st.title('Piano King NFT Dashboard')

df = pd.read_csv('resources/output/pianoking_data.csv', sep=',')



values = pd.Series(df['FirstTimeOwner'])
v_counts = values.value_counts()
total = len(values)
fig = plt.figure()
plt.pie(v_counts, labels=v_counts.index, autopct=fmt, shadow=False)
plt.show()
st.subheader('Piano King Primo Wallet Holders')
st.pyplot(fig)

st.subheader('Pa')
