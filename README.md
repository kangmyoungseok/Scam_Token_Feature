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
- 각각의 Json파일을 이용하여 다음의 피처를 도출해 낸다.
1. 전체 Active Period중 Mint Transaction의 평균 발생 지점
2. 전체 Active Period중 Burn Transaction의 평균 발생 지점
3. 전체 Active Period중 Swap Transaction의 평균 발생 지점

- 전체 Active Period : ( Last Transaction TimeStamp - First Transaction TimeStamp )
- Last Transaction TimeStamp : Mint/Burn/Swap의 TimeStamp중 가장 마지막
- First Transaction TimeStamp : Mint의 첫번째 TimeStamp

\frac{\sum_{i=1}^{N} mint_{i} - FirstTimestamp }{N}
