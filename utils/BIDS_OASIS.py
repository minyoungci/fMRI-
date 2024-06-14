import os
import shutil

# Define the paths
base_dir = "/home/minyoungxi/MINYOUNGXI/XFL/dbssus123-20240614_075307"
output_dir = "/home/minyoungxi/MINYOUNGXI/XFL/OASIS_614"

# Function to create BIDS structure
def create_bids_structure(base_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each subject and session directory
    for subject in os.listdir(base_dir):
        subject_path = os.path.join(base_dir, subject)
        if os.path.isdir(subject_path):
            subject_id = subject.split('_')[0]
            session_id = subject.split('_')[-1]

            for dir_name in os.listdir(subject_path):
                dir_path = os.path.join(subject_path, dir_name)

                if os.path.isdir(dir_path) and dir_name.startswith("anat"):
                    bids_anat_dir = os.path.join(output_dir, f"sub-{subject_id}", f"ses-{session_id}", "anat")
                    os.makedirs(bids_anat_dir, exist_ok=True)
                    
                    if os.path.exists(os.path.join(dir_path, "NIFTI")):
                        for file in os.listdir(os.path.join(dir_path, "NIFTI")):
                            if file.endswith(".nii.gz"):
                                shutil.copy2(os.path.join(dir_path, "NIFTI", file), os.path.join(bids_anat_dir, f"sub-{subject_id}_ses-{session_id}_T1w.nii.gz"))

                    if os.path.exists(os.path.join(dir_path, "BIDS")):
                        for file in os.listdir(os.path.join(dir_path, "BIDS")):
                            if file.endswith(".json"):
                                shutil.copy2(os.path.join(dir_path, "BIDS", file), os.path.join(bids_anat_dir, f"sub-{subject_id}_ses-{session_id}_T1w.json"))

                elif os.path.isdir(dir_path) and dir_name.startswith("func"):
                    bids_func_dir = os.path.join(output_dir, f"sub-{subject_id}", f"ses-{session_id}", "func")
                    os.makedirs(bids_func_dir, exist_ok=True)
                    
                    if os.path.exists(os.path.join(dir_path, "NIFTI")):
                        for file in os.listdir(os.path.join(dir_path, "NIFTI")):
                            if file.endswith(".nii.gz"):
                                shutil.copy2(os.path.join(dir_path, "NIFTI", file), os.path.join(bids_func_dir, f"sub-{subject_id}_ses-{session_id}_task-rest_bold.nii.gz"))

                    if os.path.exists(os.path.join(dir_path, "BIDS")):
                        for file in os.listdir(os.path.join(dir_path, "BIDS")):
                            if file.endswith(".json"):
                                shutil.copy2(os.path.join(dir_path, "BIDS", file), os.path.join(bids_func_dir, f"sub-{subject_id}_ses-{session_id}_task-rest_bold.json"))

# Run the function
create_bids_structure(base_dir, output_dir)
