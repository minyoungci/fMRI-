import os
import shutil

# 원본 데이터 디렉토리
source_dir = '/home/minyoungxi/MINYOUNGXI/XFL/dbssus123-20240602_045938'

# BIDS 데이터를 저장할 디렉토리
bids_dir = '/home/minyoungxi/MINYOUNGXI/XFL/BIDS'

# 각 세션의 데이터를 올바른 BIDS 형식으로 이동
for item in os.listdir(source_dir):
    if os.path.isdir(os.path.join(source_dir, item)) and item.startswith('OAS30002'):
        participant_id = item.split('_')[0]  # 예: OAS30004
        session_id = item.split('_')[2]      # 예: d3457

        session_path = os.path.join(source_dir, item)
        participant_folder = f'sub-{participant_id}'
        session_folder = f'ses-{session_id}'
        session_bids_path = os.path.join(bids_dir, participant_folder, session_folder)

        # 각 폴더(anat, func)에 대한 경로를 생성하고 파일 이동
        for modality_dir in os.listdir(session_path):
            modality_path = os.path.join(session_path, modality_dir)
            if 'anat' in modality_dir or 'func' in modality_dir:
                target_folder = 'anat' if 'anat' in modality_dir else 'func'
                target_path = os.path.join(session_bids_path, target_folder)
                os.makedirs(target_path, exist_ok=True)

                # BIDS, NIFTI 폴더 내 파일을 적절한 폴더로 이동
                for subfolder in os.listdir(modality_path):
                    subfolder_path = os.path.join(modality_path, subfolder)
                    for file_name in os.listdir(subfolder_path):
                        # BIDS JSON 파일이면 같이 이동
                        if file_name.endswith('.json') or file_name.endswith('.nii.gz'):
                            shutil.move(os.path.join(subfolder_path, file_name), os.path.join(target_path, file_name))

print("Data has been reorganized into the BIDS format.")
