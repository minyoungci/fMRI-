from monai.transforms import LoadImage
import torch
import os
import time
from multiprocessing import Process, Queue
import nibabel as nib
import multiprocessing
from data_processing import read_data

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
multiprocessing.set_start_method('spawn', force=True)

def main():
    dataset_name = 'OASIS'
    load_root = '/home/minyoungxi/MINYOUNGXI/XFL/Data/OASIS_615_fmriprep_output'
    save_root = f'/home/minyoungxi/MINYOUNGXI/XFL/Data/{dataset_name}_MNI_to_TRs_znorm'
    scaling_method = 'z-norm'

    os.makedirs(os.path.join(save_root, 'img'), exist_ok=True)
    os.makedirs(os.path.join(save_root, 'metadata'), exist_ok=True)
    save_root = os.path.join(save_root, 'img')
    
    finished_samples = os.listdir(save_root)
    
    tasks = []

    for item in sorted(os.listdir(load_root)):
        if not item.startswith('sub-') or not os.path.isdir(os.path.join(load_root, item)):
            continue
        subj_dir = item
        subj_path = os.path.join(load_root, subj_dir)
        
        for ses_dir in sorted(os.listdir(subj_path)):
            if not ses_dir.startswith('ses-'):
                continue
            func_path = os.path.join(subj_path, ses_dir, 'func')
            anat_path = os.path.join(subj_path, ses_dir, 'anat')
            if not os.path.isdir(func_path) or not os.path.isdir(anat_path):
                continue
            
            func_files = [f for f in os.listdir(func_path) if f.endswith('_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')]
            anat_files = [f for f in os.listdir(anat_path) if f.endswith('_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')]
            
            if not func_files or not anat_files:
                print(f"Missing func or anat file for {subj_dir}/{ses_dir}")
                continue
            
            func_file = func_files[0]
            anat_file = anat_files[0]
            
            subj_name = f"{subj_dir}_{ses_dir}"
            expected_seq_length = 200 

            if (subj_name not in finished_samples) or (len(os.listdir(os.path.join(save_root, subj_name))) < expected_seq_length + 1):  # +1 for anat.pt
                tasks.append((func_file, anat_file, os.path.join(subj_path, ses_dir), save_root, subj_name, scaling_method, False, 10))  

    
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(read_data, tasks)

    print(f"Processed subjects: {[r for r in results if r is not None]}")

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('\nTotal', round((end_time - start_time) / 60), 'minutes elapsed.')