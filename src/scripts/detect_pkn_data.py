from web3 import Web3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from etherscan import Etherscan
import numpy as np
import datetime
import matplotlib.pyplot as plt


class ContractWrapper:
    MIN_TOKEN_ID: int = 1

    def __init__(self, addr: str):
        self.addr = addr


class ContractWrapper:
    MIN_TOKEN_ID: int = 1

    def __init__(self, addr: str):
        self.addr = addr
        self.abi = abi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"addr","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountOfToken","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fundsDeposited","type":"uint256"}],"name":"AddressWhitelisted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"getSupplyLeft","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"adr","type":"address"}],"name":"getWhitelistAllowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getWhitelistedAddresses","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"retrieveFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"addr","type":"address"}],"name":"setPianoKingWallet","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"open","type":"bool"}],"name":"setSaleStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"whiteListSender","outputs":[],"stateMutability":"payable","type":"function"}]'
        self._addr = Web3.toChecksumAddress(self.addr)
        self._w3 = Web3(Web3.HTTPProvider(
            "https://mainnet.infura.io/v3/cfa87b8468ee4780a779f6553b70c6c0"))
        self.test = [False, False]
        self.contract = self._w3.eth.contract(self._addr, abi=abi)
        self.eth = self._w3.eth
        self._lock_base_uri = False
        self._locked_base_uri = False
        self._base_uri = None


def detect_params():
    wrapper = ContractWrapper("0xB2E31C3D51bbfefB4653789CF0965f9dfa7C902a")
    eth = Etherscan("TMEEV5AC6X3HY2MJRRWHURBEBA5VSYJ6FI") 
    wls = wrapper.contract.functions.getWhitelistedAddresses().call()
    FirstTimeOwner = True
    n=0
    df_pkg = pd.DataFrame(columns=['address', 'nbtoken', 'NumNFT', 'FirstTimeOwner'])
    for _, wl in enumerate(wls):
        nb = wrapper.contract.functions.getWhitelistAllowance(wl).call()
        
        nftOwners = eth.get_erc721_token_transfer_events_by_address(address = wl, startblock = 0, endblock= enumerate(wl), sort = "yes")
        lst=[]
        for item in enumerate(nftOwners):
            
            date = datetime.datetime.fromtimestamp(int(item[1]['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
            item[1]['date'] = date
        nftOwners.sort(key = lambda x:x['date'])

        for item in enumerate(nftOwners):
            print(item)
            if item[1]['tokenSymbol'] == 'PK':
                FirstTimeOwner = True
            else: 
                FirstTimeOwner = False
        df_pkg = df_pkg.append([{'address': (wl), 'nb_token': nb, 'NumNFT': len(nftOwners), 'FirstTimeOwner' : FirstTimeOwner}])
        df_pkg.to_csv('resources/output/pianoking_data.csv')