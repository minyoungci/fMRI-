import os
import shutil

source_dir = '/home/minyoungxi/MINYOUNGXI/XFL/UKB_Over_75_resting_functional_MRI'
bids_dir = '/home/minyoungxi/MINYOUNGXI/XFL/BIDS_UKB'

if not os.path.exists(bids_dir):
    os.makedirs(bids_dir)

# 필수 dataset_description.json 파일이 없다면 생성
dataset_description_path = os.path.join(bids_dir, 'dataset_description.json')
if not os.path.exists(dataset_description_path):
    with open(dataset_description_path, 'w') as f:
        f.write('''
{
    "Name": "OASIS fMRI",
    "BIDSVersion": "1.4.0",
    "DatasetDOI": "http://dx.doi.org/10.0000/example"
}
''')

for folder in os.listdir(source_dir):
    sub_id = folder.split('_')[0]  # 예: '1002051'
    session_id = '1'  # UKB 데이터는 세션 정보가 명확하지 않으므로 '1'로 가정

    participant_bids_dir = os.path.join(bids_dir, f'sub-{sub_id}', f'ses-{session_id}')
    
    # func 디렉토리 처리
    func_dir = os.path.join(participant_bids_dir, 'func')
    os.makedirs(func_dir, exist_ok=True)

    # anat 디렉토리 처리
    anat_dir = os.path.join(participant_bids_dir, 'anat')
    os.makedirs(anat_dir, exist_ok=True)

    # 각 fMRI 데이터와 메타데이터 파일을 BIDS 구조로 이동
    fmri_path = os.path.join(source_dir, folder, 'fMRI', 'rfMRI.nii.gz')
    fmri_json_path = os.path.join(source_dir, folder, 'fMRI', 'rfMRI.json')

    new_fmri_path = os.path.join(func_dir, f'sub-{sub_id}_ses-{session_id}_task-rest_bold.nii.gz')
    new_fmri_json_path = os.path.join(func_dir, f'sub-{sub_id}_ses-{session_id}_task-rest_bold.json')

    # 해부학적 MRI 데이터와 메타데이터 파일 이동
    anat_path = os.path.join(source_dir, folder, 'anat', 'T1.nii.gz')
    anat_json_path = os.path.join(source_dir, folder, 'anat', 'T1.json')

    new_anat_path = os.path.join(anat_dir, f'sub-{sub_id}_ses-{session_id}_T1w.nii.gz')
    new_anat_json_path = os.path.join(anat_dir, f'sub-{sub_id}_ses-{session_id}_T1w.json')

    # 파일 이동
    if os.path.exists(fmri_path) and os.path.exists(fmri_json_path):
        shutil.move(fmri_path, new_fmri_path)
        shutil.move(fmri_json_path, new_fmri_json_path)
    else:
        print(f'Missing fMRI files for {folder}')
    
    if os.path.exists(anat_path) and os.path.exists(anat_json path):
        shutil.move(anat_path, new_anat_path)
        shutil.move(anat_json_path, new_anat_json_path)
    else:
        print(f'Missing anat files for {folder}')

print("Conversion to BIDS format completed successfully.")
