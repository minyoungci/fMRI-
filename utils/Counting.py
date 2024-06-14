import os

# 탐색할 루트 디렉토리 경로
root_dir = '/home/minyoungxi/MINYOUNGXI/XFL/dbssus123-20240614_075307'

# 'ses'로 시작하는 폴더를 가진 디렉토리를 저장할 리스트
ses_directories = []

# 루트 디렉토리부터 하위 디렉토리 탐색
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 각 디렉토리 내에서 'ses'으로 시작하는 폴더가 있는지 확인
    for dirname in dirnames:
        if dirname.startswith('ses'):
            ses_directories.append(os.path.join(dirpath, dirname))

# 결과 출력
print(f"Total 'ses' directories: {len(ses_directories)}")
for directory in ses_directories:
    print(directory)
