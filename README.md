# Scam_Token_listing
Listing scam tokens in Uniswap

# Uniswap 에서 스캠토큰 리스트 찾아오기
- TheGraph API를 통해서 Uniswap 전체 Pool을 가져온다.
- 가져온 풀에서 토큰쌍을 구별해 내고, 그 중 규모가 작은 토큰에서 Liquidity pool 찾는다.

# 10.18 Pair.py 업로드
- TheGraph API를 통해서 Uniswap에 저장된 모든 Pair를 불러오기.
- Switch_token 함수를 구현해 놨는데, 해당 함수를 이용하면 기존 Pair(Token0/Token1)에서 Token1로 큰 토큰(USDT,ETH 등..)이 오도록 정렬시킴
- + 추가로 Pairs_v1.1 파일을 보면 Token0/Token1  |  Token00/Token11 이렇게 두가지 쌍이 있는데 Token00/11쪽이 정렬된 열임

# 10.20 Uniswap_API.py 업로드
- TheGraph API를 통해서 하나의 Pair에 대해서 Mint/Burn/Swap 기록을 JSON 파일로 저장
- API를 불러오는 경우 통상 로컬에서 돌리는 것보다, Colab을 통해서 하는게 훨씬 빠름.
- Json 파일을 크기가 커서 Github에 안올라 가기 때문에 로컬에 저장해 둔다.

# 10.21 MBS_Active.py 업로드
###  각각의 Json파일을 이용하여 다음의 피처를 도출해 낸다.
- __전체 Active Period중 Mint Transaction의 평균 발생 지점(Burn Swap도 동일)__
  + <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{Mint\,&space;Average\,&space;\,&space;TimeStamp&space;}&space;{Active&space;Period}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{Mint\,&space;Average\,&space;\,&space;TimeStamp&space;}&space;{Active&space;Period}" title="\frac{Mint\, Average\, \, TimeStamp } {Active Period}" /></a>  
  + <a href="https://www.codecogs.com/eqnedit.php?latex=Mint\,&space;Average\,&space;\,&space;TimeStamp&space;=&space;\frac{\sum_{i=1}^{N}&space;mint_{i}&space;-&space;FirstTimestamp&space;}{N}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Mint\,&space;Average\,&space;\,&space;TimeStamp&space;=&space;\frac{\sum_{i=1}^{N}&space;mint_{i}&space;-&space;FirstTimestamp&space;}{N}" title="Mint\, Average\, \, TimeStamp = \frac{\sum_{i=1}^{N} mint_{i} - FirstTimestamp }{N}" /></a>

  + 전체 Active Period : ( Last Transaction TimeStamp - First Transaction TimeStamp )
  + Last Transaction TimeStamp : Mint/Burn/Swap의 TimeStamp중 가장 마지막
  + First Transaction TimeStamp : Mint의 첫번째 TimeStamp

- __Mint/Burn/Swap의 수__
- __Swap-In / Swap-Out의 비율__

# 10.22 전체 파일 업데이트
- Pair.py 새로 실행해서 Pairs_v1.3으로 업데이트 / 교환 쌍이 WETH인 경우에 대해서만 불러오도록 수정 / 현재 토큰 개수 : 
- Uniswap_API.py : Pairs_v1.3에 맞춰서 Mint/Burn/Swap Json 파일 업데이트. 기존 desc로 데이터가 정렬된걸 asc로 바꿨음
- Uniswap_Update_API.py :  Uniswap_API.py는 한번 돌리는데 시간이 오래 걸리기 때문에, 추후에 Pair.py에서 업데이트 후에 기존 mint/burn/swap.json파일에서 추가된 토큰들에 대해서만 정보를 구해올 수 있다.
- initial_Liquidity_Eth.py : __'initial_Liquidity_Eth'__ / __'initial_Liquidity_token'__ 값을 구해오는 파일. mint.json파일에서 각각의 Contract의 첫번째 값이 처음의 Add Liquidity 이므로 이를 이용해서 구함. / 네트워크단을 거치지 않고 json파일에서 결과를 구하기 때문에 결과가 빨리 나옴
- Creator.py : 현재 에러발생
 로직 : Etherplorer API에서 1차로 불러오고, 불러지지 않는 값에 대해서 Etherscan에서 Crawling 하는 방식
 문제 1. 
