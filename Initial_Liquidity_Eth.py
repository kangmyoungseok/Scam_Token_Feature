#Etherplorer API / Etherscan Crawling으로 Creator Address를 구한다.
from pandas.core.frame import DataFrame
from requests import Request, Session
import pandas as pd
import json
from bs4 import BeautifulSoup
import re # 추가
from urllib.request import urlopen
import requests
import time
from multiprocessing import Pool
import json


with open('./mint.json', 'r') as f:
    mint_json = json.load(f)

len(mint_json)
datas = pd.read_csv('Pairs_v1.2.csv',encoding='utf-8-sig').to_dict('records')


for data in datas:
    pair_id = data['id']

    if(len(mint_json[pair_id]) == 0 ):     #Mint 정보가 없는 pair는 초기 Liquidity를 0으로 한다.
        data['initial_Liquidity_ETH'] = 0
        data['initial_Liquidity_token'] = 0
        continue


    if(data['token0.symbol'] == 'WETH'):
        initial_Liquidity_ETH = mint_json[pair_id][0]['amount0']
        initial_Liquidity_token = mint_json[pair_id][0]['amount1']
    else:
        initial_Liquidity_ETH = mint_json[pair_id][0]['amount1']
        initial_Liquidity_token = mint_json[pair_id][0]['amount0']

    data['initial_Liquidity_ETH'] = initial_Liquidity_ETH  
    data['initial_Liquidity_token'] = initial_Liquidity_token


for i in range(20):
    print(datas[i]['initial_Liquidity_token'])

DataFrame(datas).to_csv('Pairs_v1.2.csv',encoding='utf-8-sig')