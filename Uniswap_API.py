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

global df
global df_len
df = pd.read_csv('./Pairs_v1.3.csv').to_dict()
df_len = len(df['id'])
global count
count= 0

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
  mints(orderBy: timestamp, orderDirection: asc, where:{ pair: "pair_address" }) {
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
  swaps(orderBy: timestamp, orderDirection: asc, where:{ pair: "pair_address" }) {
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
  burns(orderBy: timestamp, orderDirection: asc, where:{ pair: "pair_address" }) {
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
        return {pair_address : result['data']['mints']}
    except:
        return {pair_address : ['Error Occur']}
        
def get_mint():
    file_path = "./mint.json"
    mint_json = {}
    try:
      p = Pool(8)
      start = time.time()
      global count
      for ret in p.imap(get_mint_subProcess,df['id'].values()):
        count = count+1
#        print("Got value",ret,"Time :",time.time()-start)
        mint_json.update(ret) 
        if(count % 1000 == 0):
          print("Process Rate : {}/{} {}%".format(count,df_len,int((count/df_len)*100)))
#          print("write file count : " + str(count))
#          with open(file_path,'w') as outfile:
#            json.dump(mint_json, outfile, indent=4)    
  
      print('finish ' + str(count))
      with open(file_path,'w') as outfile:
            json.dump(mint_json, outfile, indent=4)
      delta_t = time.time() - start
      print("Total Time :",delta_t)
      p.close()
      p.join()
      mint_json.clear()        

    except Exception as e:
        print(e)


#############모든 pair 쌍에 대해서 Mint Query 후 결과 저장##############
def get_swap_subProcess(pair_address):
    try:
        query = swap_query_template.replace('pair_address',pair_address)
        result = run_query(query)
        return {pair_address : result['data']['swaps']}
    except:
        return {pair_address : ['Error Occur']}
        
def get_swap():
    file_path = "./swap.json"
    swap_json = {}
    try:
        p = Pool(8)
        start = time.time()
        global count
        for ret in p.imap(get_swap_subProcess,df['id'].values()):
            count = count+1
            swap_json.update(ret)
            if(count % 1000 == 0):
                print("Process Rate : {}/{} {}%".format(count,df_len,int((count/df_len)*100)))
 #               print("write file count : " + str(count))
 #               with open(file_path,'w') as outfile:
 #                   json.dump(swap_json, outfile, indent=4)    
  
        p.close()
        p.join()
        print('finish ' + str(count))
        with open(file_path,'w') as outfile:
            json.dump(swap_json, outfile, indent=4)
        delta_t = time.time() - start
        print("Total Time :",delta_t)
        swap_json.clear()        

    except Exception as e:
        print(e)

#############모든 pair 쌍에 대해서 Burn Query 후 결과 저장##############
def get_burn_subProcess(pair_address):
    try:
        query = burn_query_template.replace('pair_address',pair_address)
        result = run_query(query)
        return {pair_address : result['data']['burns']}
    except:
        return {pair_address : ['Error Occur']}
        
def get_burn():
    file_path = "./burn.json"
    burn_json = {}
    try:
        p = Pool(8)
        start = time.time()
        global count
        for ret in p.imap(get_burn_subProcess,df['id'].values()):
            count = count+1
            burn_json.update(ret)
            if(count % 1000 == 0):
                print("Process Rate : {}/{} {}%".format(count,df_len,int((count/df_len)*100)))
#                print("write file count : " + str(count))
#                with open(file_path,'w') as outfile:
#                    json.dump(burn_json, outfile, indent=4)    
  
        p.close()
        p.join()
        print('finish ' + str(count))
        with open(file_path,'w') as outfile:
            json.dump(burn_json, outfile, indent=4)
        delta_t = time.time() - start
        print("Total Time :",delta_t)
        burn_json.clear()        

    except Exception as e:
        print(e)


if __name__=='__main__': 
    get_mint()
#    get_burn()
#    get_swap()