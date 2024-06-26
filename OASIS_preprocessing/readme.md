`ValueError: The length of the input vector x must be greater than padlen, which is 33.`

본 오류 메시지는 입력 벡터의 길이가 패딩 길이보다 작아서 발생하는 문제

> fMRI 데이터가 아니라 T1w 해부학적 데이터를 사용하기 


---

# Preprocessing 

main.py 실행하면 비뇌영역 제거 , z-norm 적용, float16으로 torch tensor 저장