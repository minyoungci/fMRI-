import os
import shutil

# 원본 데이터 디렉토리
source_dir = 'Suji-20240428_200129_76-80_mr_bold_freesurfers'

# BIDS 데이터를 저장할 디렉토리
bids_dir = '/home/minyoungxi/MINYOUNGXI/XFL/BIDS'

# 각 세션의 데이터를 올바른 BIDS 형식으로 이동
for patient_folder in os.listdir(source_dir):
    if os.path.isdir(os.path.join(source_dir, patient_folder)) and patient_folder.startswith('OAS'):
        participant_id = patient_folder.split('_')[0]  # 예: OAS30004
        session_id = '1'  # 세션 정보가 따로 없으므로 모든 세션을 '1'로 처리

        patient_path = os.path.join(source_dir, patient_folder)
        participant_folder = f'sub-{participant_id[3:]}'  # 'OAS30004'에서 '30004' 추출
        session_folder = f'ses-{session_id}'
        session_bids_path = os.path.join(bids_dir, participant_folder, session_folder)

        # func 폴더들을 찾아서 해당 데이터를 이동
        for func_dir in ['func1', 'func2', 'func3']:
            func_path = os.path.join(patient_path, func_dir)
            if os.path.exists(func_path):
                bids_func_path = os.path.join(session_bids_path, 'func')
                os.makedirs(bids_func_path, exist_ok=True)

                # BIDS와 NIFTI 폴더 내 파일을 적절한 폴더로 이동
                for subfolder in ['BIDS', 'NIFTI']:
                    subfolder_path = os.path.join(func_path, subfolder)
                    if os.path.exists(subfolder_path):
                        for file_name in os.listdir(subfolder_path):
                            # .json과 .nii.gz 파일 이동
                            if file_name.endswith('.json') or file_name.endswith('.nii.gz'):
                                shutil.move(os.path.join(subfolder_path, file_name), os.path.join(bids_func_path, file_name))

print("Data has been reorganized into the BIDS format.")
