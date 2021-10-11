from pprint import pprint
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json
from bs4 import BeautifulSoup
import re # 추가
from urllib.request import urlopen
import requests
import time

# swap function makes scam token to token0
def switch_token(result):
    for pair in result['data']['pairs']:
        if (int(pair['token0']['txCount']) > int(pair['token1']['txCount'] )):
            pair['reserve0'],pair['reserve1'] = pair['reserve1'],pair['reserve0']
            pair['token0'],pair['token1'] = pair['token1'],pair['token0']
    
# function to use requests.post to make an API call to the subgraph url
def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


query_init = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
   liquidityProviderCount
 }
}
''' 


query_iter = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where: {createdAtBlockNumber_lt:initial}) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
   liquidityProviderCount
 }
}
''' 



pair_frame = [] # 쿼리의 결과를 여기에 List 형태로 담을 것. 50000개

##### 맨 처음 쿼리. 반복문 불가####
query = query_init
result = run_query(query)
switch_token(result)
for pair in result['data']['pairs']:
    year = time.gmtime(int(pair['createdAtTimestamp'])).tm_year
    month = time.gmtime(int(pair['createdAtTimestamp'])).tm_mon
    day = time.gmtime(int(pair['createdAtTimestamp'])).tm_mday
    pair['createdAtTimestamp'] = str(year) + '-' + str(month) + '-' + str(day)
    pair_frame.append(pair)

last_block = result['data']['pairs'][999]['createdAtBlockNumber']
query_iter = query_iter.replace('initial',last_block)
query = query_iter

try:
    while(1):
        result = run_query(query_iter)
        switch_token(result)
        print(result.keys())
        for pair in result['data']['pairs']:
            year = time.gmtime(int(pair['createdAtTimestamp'])).tm_year
            month = time.gmtime(int(pair['createdAtTimestamp'])).tm_mon
            day = time.gmtime(int(pair['createdAtTimestamp'])).tm_mday
            pair['createdAtTimestamp'] = str(year) + '-' + str(month) + '-' + str(day)
            pair_frame.append(pair)
        query_iter = query_iter.replace(last_block,result['data']['pairs'][999]['createdAtBlockNumber'])
        last_block = result['data']['pairs'][999]['createdAtBlockNumber']
        time.sleep(3)
        print(last_block)

except Exception as e:
#    print(result['errors'])
    df = pd.json_normalize(pair_frame)
    df.to_csv('Pairs.csv',encoding='utf-8-sig')



