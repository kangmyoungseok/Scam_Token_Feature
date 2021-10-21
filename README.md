# Scam_Token_listing
Listing scam tokens in Uniswap

# Uniswap 에서 스캠토큰 리스트 찾아오기
- TheGraph API를 통해서 Uniswap 전체 Pool을 가져온다.
- 가져온 풀에서 토큰쌍을 구별해 내고, 그 중 규모가 작은 토큰에서 Liquidity pool 찾는다.
