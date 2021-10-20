from pprint import pprint
from pandas.core.frame import DataFrame
import pandas as pd
import json
import requests
import time
from tqdm import tqdm
from multiprocessing import Pool
# function to use requests.post to make an API call to the subgraph url

global df
global df_len
global count
df = pd.read_csv('./Pairs_v1.1.csv').to_dict()
df_len = len(df['id'])
count = 0


def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


mint_query_template = '''
{
  mints(orderBy: timestamp, orderDirection: desc, where:{ pair: "pair_address" }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 

swap_query_template = '''
{
  swaps(orderBy: timestamp, orderDirection: desc, where:{ pair: "pair_address" }) {
      amount0In
      amount0Out
      amount1In
      amount1Out
      to
      sender
      timestamp
 }
}
''' 

burn_query_template = '''
{
  burns(orderBy: timestamp, orderDirection: desc, where:{ pair: "pair_address" }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 

#############모든 pair 쌍에 대해서 Mint Query 후 결과 저장##############
def get_mint_subProcess(pair_address):
    try:
        query = mint_query_template.replace('pair_address',pair_address)
        result = run_query(query)
        return {pair_address,result['data']['mints']}
    except:
        return {pair_address,['Error Occur']}
    finally:
        count = count+1
        if(count %100 == 0):
            print(str(count) + "/" + str(df_len))
    

def get_mint():
    try:
        pool = Pool(processes=4)
        mint_json = pool.map(get_mint_subProcess,df['id'])
    except Exception as e:
        print(e)
    finally:
        file_path = "./mint.json"
        with open(file_path,'w') as outfile:
            json.dump(mint_json, outfile, indent=4)

    



if __name__=='__main__': 
    get_mint()
#    get_burn()
#    get_swap()