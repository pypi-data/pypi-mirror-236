import torch
from torch.utils.data import Dataset
import numpy as np

class DataLoaderForCLIP(Dataset):
    def __init__(self,config):
        self.seq_len = config.text_config.max_position_embeddings
        self.image_size = config.vision_config.image_size
        self.vocab_size = config.text_config.vocab_size
        self.dataset_size = 2560*2
        self.input_ids = np.random.randint(0,self.vocab_size,(self.dataset_size, self.seq_len))
        self.attention_mask = np.random.randint(0,2,(self.dataset_size, self.seq_len))
        self.pixel_values = np.random.randint(0,256,(self.dataset_size, 3, self.image_size, self.image_size))

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        input_ids = torch.LongTensor(self.input_ids[idx])
        attention_mask = torch.Tensor(self.attention_mask[idx])
        pixel_values = torch.FloatTensor(self.pixel_values[idx])
        return input_ids, attention_mask, pixel_values