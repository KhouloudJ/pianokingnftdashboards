from web3 import Web3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from etherscan import Etherscan
import streamlit as st
import numpy as np
import igraph
from igraph import Graph, EdgeSeq

from src.scripts.detect_pkn_data import detect_params

st.title('Piano King NFT Dashboard')
