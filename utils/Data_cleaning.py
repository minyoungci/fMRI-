import os
import shutil

# 탐색할 루트 디렉토리 경로
root_dir = '/home/minyoungxi/MINYOUNGXI/XFL/Suji-20240428_200129_76-80_mr_bold_freesurfers'

# 루트 디렉토리의 하위 디렉토리를 탐색
for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    # 루트 디렉토리와 직접적인 하위 디렉토리에 대해서만 작업을 수행
    if dirpath == root_dir:
        for dirname in dirnames:
            subdir_path = os.path.join(dirpath, dirname)
            # 하위 디렉토리 내에 'func' 폴더가 있는지 확인
            if not any(subdirname.startswith('func') for subdirname in os.listdir(subdir_path) if os.path.isdir(os.path.join(subdir_path, subdirname))):
                # 'func' 폴더가 없는 경우 디렉토리 삭제
                shutil.rmtree(subdir_path)
                print(f"Deleted: {subdir_path}")

print("Cleanup complete.")
