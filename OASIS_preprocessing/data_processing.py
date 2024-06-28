import torch
import os
import nibabel as nib

def read_data(func_file, anat_file, load_root, save_root, subj_name, scaling_method='z-norm', fill_zeroback=False, chunk_size=10):
    print(f"Processing: {func_file}", flush=True)
    func_path = os.path.join(load_root, 'func', func_file)
    anat_path = os.path.join(load_root, 'anat', anat_file)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    try:
        func_img = nib.load(func_path)
        func_data = func_img.get_fdata()

        anat_img = nib.load(anat_path)
        anat_data = torch.tensor(anat_img.get_fdata(), dtype=torch.float16, device=device)
    except Exception as e:
        print(f"Error loading files: {e}")
        return None
    
    save_dir = os.path.join(save_root, subj_name)
    os.makedirs(save_dir, exist_ok=True)
    
    for i in range(0, func_data.shape[-1], chunk_size):
        chunk = func_data[..., i:i+chunk_size]
        chunk_tensor = torch.tensor(chunk, dtype=torch.float16, device=device)
        
        background = chunk_tensor == 0
        
        if scaling_method == 'z-norm':
            global_mean = chunk_tensor[~background].mean()
            global_std = chunk_tensor[~background].std()
            data_temp = (chunk_tensor - global_mean) / global_std
        elif scaling_method == 'minmax':
            data_temp = (chunk_tensor - chunk_tensor[~background].min()) / (chunk_tensor[~background].max() - chunk_tensor[~background].min())

        data_global = torch.empty(chunk_tensor.shape, dtype=torch.float16, device=device)
        data_global[background] = data_temp[~background].min() if not fill_zeroback else 0 
        data_global[~background] = data_temp[~background]

        for j, TR in enumerate(data_global.split(1, 3)):
            torch.save(TR.cpu().clone(), os.path.join(save_dir, f"func_frame_{i+j:04d}.pt"))
        
        del chunk_tensor, data_temp, data_global
        torch.cuda.empty_cache()
    
    torch.save(anat_data.cpu(), os.path.join(save_dir, "anat.pt"))

    return subj_name