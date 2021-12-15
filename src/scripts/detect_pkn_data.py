from web3 import Web3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from etherscan import Etherscan
import numpy as np
import datetime
import matplotlib.pyplot as plt
from itertools import groupby
from operator import itemgetter
import os

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
    df_pkg = pd.DataFrame(columns=['address', 'nbtoken', 'FirstTimeOwner', 'FirstTokenName', 'FirstTokenSymbol', 'NumTxn','TotalPianoKingNFT', 'TotalPKMint', 'TotalPKBurn' ])
    with open('resources/output/raw_data.csv', 'w') as f:
        f.write(',blockNumber,timeStamp,hash,nonce,blockHash,from,contractAddress,to,tokenID,tokenName,tokenSymbol,tokenDecimal,transactionIndex,gas,gasPrice,gasUsed,cumulativeGasUsed,input,confirmations,date,address,status') 
        f.write('\n') 
    for _, wl in enumerate(wls):
        # print(wl)
        n=0
        k=0
        j=0
        c = 0
        nb = wrapper.contract.functions.getWhitelistAllowance(wl).call()
        
        nftOwners = eth.get_erc721_token_transfer_events_by_address(address = wl, startblock = 0, endblock= enumerate(wl), sort = "yes")
        lst=[]
        for item in enumerate(nftOwners):
            
            date = datetime.datetime.fromtimestamp(int(item[1]['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
            item[1]['date'] = date
        
        nftOwners.sort(key = lambda x:x['date'])
        FirstTokenName = nftOwners[0]['tokenName']
        FirstTokenSymbol = nftOwners[0]['tokenSymbol']
   
        if FirstTokenSymbol == 'PK':
            FirstTimeOwner = True
        else:
            FirstTimeOwner = False
        for i in range(len(nftOwners)):
            nftOwners[i]['address'] = wl
            if nftOwners[i]['tokenSymbol'] == 'PK':
                n+=1
                # if nftOwners[i]["to"].startswith('0x000000000000000000000000000000000'):
                #     nftOwners[i]["status"] = "burn"
                #     k+=1
                
                if nftOwners[i]["to"].strip() is wl :
                    print(wl)
                    if nftOwners[i]['tokenSymbol'] == 'PK':
                        c+=1
            if nftOwners[i]["from"].startswith('0x000000000000000000000000000000000'):
                nftOwners[i]["status"] = "mint"
                if nftOwners[i]['tokenSymbol'] == 'PK':
                    j+=1
            # if nftOwners[i]["to"].startswith('0x000000000000000000000000000000000'):
            #     nftOwners[i]["status"] = "burn"
            #     if nftOwners[i]['tokenSymbol'] == 'PK':
            #         k+=1

                    

            
            

        df_raw = pd.DataFrame(nftOwners, columns = ['blockNumber','timeStamp','hash','nonce','blockHash','from','contractAddress','to','tokenID','tokenName','tokenSymbol','tokenDecimal','transactionIndex','gas','gasPrice','gasUsed','cumulativeGasUsed','input','confirmations','date','address', 'status'])


        df_pkg = df_pkg.append([{'address': (wl), 'nb_token': nb, 'FirstTimeOwner' : FirstTimeOwner, 'FirstTokenName': FirstTokenName, 'FirstTokenSymbol': FirstTokenSymbol, 'NumTxn': len(nftOwners) , 'TotalPianoKingNFT': n , 'TotalPKMint': k, 'TotalPKBurn': c }])
        df_pkg.to_csv('resources/output/pianoking_data.csv')
        df_raw = df_raw.to_csv('resources/output/raw_data.csv',  mode='a', header=False)


if __name__ == '__main__':
    detect_params()