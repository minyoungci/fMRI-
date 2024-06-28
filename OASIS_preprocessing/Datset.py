import os
import torch
from torch.utils.data import Dataset
import json
import random

class BaseDataset(Dataset):
    def __init__(self, **kwargs):
        super().__init__()      
        self.register_args(**kwargs)
        self.sample_duration = self.sequence_length * self.stride_within_seq
        self.stride = max(round(self.stride_between_seq * self.sample_duration), 1)
        self.data = self._set_data(self.root, self.subject_dict)
    
    def register_args(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.kwargs = kwargs
    
    def load_sequence(self, subject_path, start_frame, sample_duration, num_frames=None):
        raise NotImplementedError("Required function")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        raise NotImplementedError("Required function")

    def _set_data(self, root, subject_dict):
        raise NotImplementedError("Required function")

class OASIS(BaseDataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _set_data(self, root, subject_dict):
        data = []
        img_root = os.path.join(root, 'img')

        for i, subject in enumerate(subject_dict):
                subject_info = subject_dict[subject]
                subject_sessions = [d for d in os.listdir(img_root) if d.startswith(f"sub-{subject}_ses-")]
                
                for session in subject_sessions:
                    subject_path = os.path.join(img_root, session)
                    num_frames = len([f for f in os.listdir(subject_path) if f.startswith('func_frame_')])
                    session_duration = num_frames - self.sample_duration + 1
                    for start_frame in range(0, session_duration, self.stride):
                        data_tuple = (i, subject, subject_path, start_frame, self.stride, num_frames, subject_info['target'], subject_info['sex'])
                        data.append(data_tuple)
        
        if self.train: 
            self.target_values = [tup[6] for tup in data]
        return data

    def load_sequence(self, subject_path, start_frame, sample_duration, num_frames=None):
        y = []
        load_fnames = [f'func_frame_{frame:04d}.pt' for frame in range(start_frame, start_frame+sample_duration, self.stride_within_seq)]
        
        for fname in load_fnames:
            img_path = os.path.join(subject_path, fname)
            y_loaded = torch.load(img_path).unsqueeze(0)
            y.append(y_loaded)
        y = torch.cat(y, dim=4)
        return y

    def __getitem__(self, index):
            _, subject, subject_path, start_frame, sequence_length, num_frames, target, sex = self.data[index]

            y = self.load_sequence(subject_path, start_frame, sequence_length, num_frames)

            background_value = y.flatten()[0]
            y = y.permute(0, 4, 1, 2, 3)
            y = torch.nn.functional.pad(y, (8, 7, 2, 1, 11, 10), value=background_value)  # 필요에 따라 패딩 조정
            y = y.permute(0, 2, 3, 4, 1)

            return {
                "fmri_sequence": y,
                "subject_name": subject,
                "target": target,
                "TR": start_frame,
                "sex": sex,
                "session": os.path.basename(subject_path)  
            }

root = '/home/minyoungxi/MINYOUNGXI/XFL/Data/OASIS_MNI_to_TRs_znorm'
metadata_file = os.path.join(root, 'metadata', 'subject_metadata.json')

with open(metadata_file, 'r') as f:
    subject_dict = json.load(f)

oasis_dataset = OASIS(
    root='/home/minyoungxi/MINYOUNGXI/XFL/Data/OASIS_MNI_to_TRs_znorm',
    subject_dict=subject_dict,
    sequence_length=10,
    stride_within_seq=1,
    stride_between_seq=1,
    train=True,
    contrastive=False,
    with_voxel_norm=False,
    shuffle_time_sequence=False
)

# 데이터셋 테스트
print(f"Dataset size: {len(oasis_dataset)}")
sample = oasis_dataset[0]
print(f"Sample keys: {sample.keys()}")
print(f"fMRI sequence shape: {sample['fmri_sequence'].shape}")
print(f"Subject name: {sample['subject_name']}")
print(f"Target: {sample['target']}")
print(f"TR: {sample['TR']}")
print(f"Sex: {sample['sex']}")
print(f"Session: {sample['session']}")