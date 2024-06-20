import os

def rename_files_and_folders(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname.startswith('ses-sub-'):
                new_dirname = dirname.replace('ses-', '')
                new_dirpath = os.path.join(dirpath, new_dirname)
                os.rename(os.path.join(dirpath, dirname), new_dirpath)
                
                sub_folder = new_dirpath
                sub_dirnames = os.listdir(sub_folder)
                
                for sub_dirname in sub_dirnames:
                    new_sub_dirname = f"ses-d{sub_dirname}"
                    new_sub_dirpath = os.path.join(sub_folder, new_sub_dirname)
                    os.rename(os.path.join(sub_folder, sub_dirname), new_sub_dirpath)

        for filename in filenames:
            if filename.endswith('.json') or filename.endswith('.nii.gz'):
                parts = filename.split('_')
                if len(parts) == 5:
                    sub, ses, task, run, bold = parts
                    if not ses.startswith('ses-d'):
                        ses = f"ses-d{ses.split('-')[1]}"
                    new_filename = f"{sub}_{ses}_task-{task}_{run}_{bold}"
                    os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))

# 사용 예시
root_directory = '/home/minyoungxi/MINYOUNGXI/XFL/BIDS'
rename_files_and_folders(root_directory)