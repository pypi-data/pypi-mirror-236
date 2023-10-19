import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class DataLoaderForChatGLM(Dataset):
    def __init__(self, args, config, dataset_size=None):
        self.vocab_size = args.vocab_size
        self.sentence_length = args.seq_length
        self.dataset_size = 2560 * 16 if dataset_size is None else dataset_size
        self.data_length = np.random.randint(self.sentence_length//8,self.sentence_length,(self.dataset_size,))

        self.input_ids, self.labels = [], []
        for i in range(self.dataset_size):
            sentence = np.random.randint(0,self.vocab_size,(self.sentence_length,))
            label = sentence.copy()

            mask_position = np.random.randint(1, self.data_length[i])
            sentence[self.data_length[i]] = config.bos_token_id
            sentence[mask_position] = config.mask_token_id
            label[mask_position] = -100
            self.input_ids.append(sentence)
            self.labels.append(label)
        
        self.input_ids = np.array(self.input_ids)
        self.labels = np.array(self.labels)

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        input_ids = torch.LongTensor(self.input_ids[idx])
        labels = torch.LongTensor(self.labels[idx])
        return input_ids, labels