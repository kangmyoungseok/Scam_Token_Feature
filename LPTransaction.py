from pprint import pprint
from pandas.core.frame import DataFrame
import pandas as pd
import json
import requests
import time
from tqdm import tqdm

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

##### 파일 불러오기 #####
df = pd.read_csv('Pairs_v1.1.csv').to_dict()
mint_json = {}
swap_json = {}
burn_json = {}
error_mint_list = []
error_swap_list = []
error_burn_list = []

#================== 테스트 라인 =======================#
'''
  with open(file_path,'w') as outfile:
    json.dump(result_json,outfile,indent=4)

  with open(file_path,"r") as json_file:
    json_data = json.load(json_file)
  json_data.keys()
'''
#===================== 테스트 끝 ==========================#


#############모든 pair 쌍에 대해서 Mint Query 후 결과 저장##############
for i in tqdm(range(len(df['id']))):
  pair_address = df['id'][i]
  try:
    query = mint_query_template.replace('pair_address',pair_address)
    result = run_query(query)
    mint_json[pair_address] = result['data']['mints']
  except:
    error_mint_list.append(pair_address)

# json 파일로 저장
file_path = "./mint.json"
with open(file_path,'w') as outfile:
  json.dump(mint_json, outfile, indent=4)

# error가 있는 contract는 따로 저장
DataFrame(error_mint_list).to_csv('./error_mint.csv',index=False)
error_mint_list.clear()


#############모든 pair 쌍에 대해서 Burn Query 후 결과 저장##############
for i in range(len(df['id'])):
  pair_address = df['id'][i]
  try:
    query = burn_query_template.replace('pair_address',pair_address)
    result = run_query(query)
    burn_json[pair_address] = result['data']['burns']
  except:
    error_burn_list.append(pair_address)

# json 파일로 저장
file_path = "./burn.json"
with open(file_path,'w') as outfile:
  json.dump(burn_json, outfile, indent=4)

# error가 있는 contract는 따로 저장
DataFrame(error_burn_list).to_csv('./error_burn.csv',index=False)
error_burn_list.clear()



#############모든 pair 쌍에 대해서 Swap Query 후 결과 저장##############
for i in range(len(df['id'])):
  pair_address = df['id'][i]
  try:
    query = swap_query_template.replace('pair_address',pair_address)
    result = run_query(query)
    swap_json[pair_address] = result['data']['swaps']
  except:
    error_swap_list.append(pair_address)

# json 파일로 저장
file_path = "./swap.json"
with open(file_path,'w') as outfile:
  json.dump(swap_json, outfile, indent=4)

# error가 있는 contract는 따로 저장
DataFrame(error_swap_list).to_csv('./error_swap.csv',index=False)
error_swap_list.clear()

