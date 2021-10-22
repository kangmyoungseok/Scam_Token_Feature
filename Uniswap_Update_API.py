from pprint import pprint
from pandas.core.frame import DataFrame
import pandas as pd
import json
import requests
import time
from tqdm import tqdm
from multiprocessing import Pool
from multiprocessing import Process
# function to use requests.post to make an API call to the subgraph url

global datas
global datas_len
datas = pd.read_csv('./Pairs_v1.2.csv').to_dict('records')
datas_len = len(datas)
global count
count= 0

#global exist_mint_datas 
#with open('./mint.json','r') as f:
#    exist_mint_datas = json.load(f)
#exist_mint_datas.clear()


#global exist_burn_datas 
#with open('./burn.json','r') as f:
#    exist_burn_datas = json.load(f)

#global exist_swap_datas 
#with open('./swap.json','r') as f:
#    exist_swap_datas = json.load(f)


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
def get_mint_subProcess(data):
    mint_list = []
    pair_address = data['id']
    try:
        mint_list = exist_mint_datas[pair_address]
        return {pair_address : mint_list}
    except:
        try:
            query = mint_query_template.replace('pair_address',pair_address)
            result = run_query(query)
            return {pair_address : result['data']['mints']}
        except:
            return {pair_address : ['Error Occur']}
        
def get_mint():
    file_path = "./mint_update.json"
    mint_json = {}
    try:
      p = Pool(24)
      global count
      for ret in p.imap(get_mint_subProcess,datas):
        count = count+1
        mint_json.update(ret) 
        if(count % 1000 == 0):
          print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))

      print('finish ' + str(count))
      with open(file_path,'w') as outfile:
            json.dump(mint_json, outfile, indent=4)
      p.close()
      p.join()
      mint_json.clear()        
    except Exception as e:
        print(e)


#############모든 pair 쌍에 대해서 Mint Query 후 결과 저장##############
def get_swap_subProcess(data):
    swap_list = []
    pair_address = data['id']
    try:
        swap_list = exist_swap_datas[pair_address]
        return {pair_address : swap_list}
    except:
        try:
            query = swap_query_template.replace('pair_address',pair_address)
            result = run_query(query)
            return {pair_address : result['data']['swaps']}
        except:
            return {pair_address : ['Error Occur']}
        
def get_swap():
    file_path = "./swap_update.json"
    swap_json = {}
    try:
      p = Pool(4)
      global count
      for ret in p.imap(get_swap_subProcess,datas):
        count = count+1
        swap_json.update(ret) 
        if(count % 1000 == 0):
          print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))

      print('finish ' + str(count))
      with open(file_path,'w') as outfile:
            json.dump(swap_json, outfile, indent=4)
      p.close()
      p.join()
      swap_json.clear()        
    except Exception as e:
        print(e)

#############모든 pair 쌍에 대해서 Burn Query 후 결과 저장##############
def get_burn_subProcess(data):
    burn_list = []
    pair_address = data['id']
    try:
        burn_list = exist_burn_datas[pair_address]
        return {pair_address : burn_list}
    except:
        try:
            query = burn_query_template.replace('pair_address',pair_address)
            result = run_query(query)
            return {pair_address : result['data']['burns']}
        except:
            return {pair_address : ['Error Occur']}
        
def get_burn():
    file_path = "./burn_update.json"
    burn_json = {}
    try:
      p = Pool(24)
      global count
      for ret in p.imap(get_burn_subProcess,datas):
        count = count+1
        burn_json.update(ret) 
        if(count % 1000 == 0):
          print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))

      print('finish ' + str(count))
      with open(file_path,'w') as outfile:
            json.dump(burn_json, outfile, indent=4)
      p.close()
      p.join()
      burn_json.clear()        
    except Exception as e:
        print(e)


if __name__=='__main__': 
    get_mint()
#    get_burn()
#    get_swap()