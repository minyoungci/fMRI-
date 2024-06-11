import os

# 탐색할 루트 디렉토리 경로
root_dir = '/home/minyoungxi/MINYOUNGXI/XFL/Suji_20240428_160844_over80_mr_bold_freesurfers'

# 'func'으로 시작하는 폴더를 가진 디렉토리를 저장할 리스트
directories_with_func = []

# 루트 디렉토리부터 하위 디렉토리 탐색
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 각 디렉토리 내에서 'func'으로 시작하는 폴더가 있는지 확인
    for dirname in dirnames:
        if dirname.startswith('func'):
            directories_with_func.append(dirpath)
            break  # 한번 찾으면 해당 디렉토리 내에서는 더 이상 찾을 필요 없음

# 결과 출력
print(f"Total directories containing 'func' folder: {len(directories_with_func)}")
for directory in directories_with_func:
    print(directory)
