import cv2
from torch.utils.data import Dataset
import os
import numpy as np
from typing import Tuple, List, Dict
from typing import Dict

class InceptionNetv3Dataset(Dataset) :
    def __init__(self, options: dict, train_mode: str) :
        
        self.image_size = options['train_args']['image_size']
        
        if train_mode == 'train' :
            self.file_path = options['train_args']['train_data_directory']
        elif train_mode == 'valid' :
            self.file_path = options['train_args']['validation_data_directory']

        self.image_paths_and_label_dict = self._extract_image_paths_and_label(self.file_path)

        self.idx_to_class = {key: sub_key for key, sub_dicts in self.image_paths_and_label_dict.items() for sub_key in sub_dicts}
        #print(self.idx_to_class) # {0: 'softdot_1', 1: 'softline_2', 2: 'darkline_4', 3: 'darkspot_5', 4: 'curvedline_6'}
        print(self.idx_to_class)

        self.image_path_list = []
        self.label_list = []

        for key, sub_dict in self.image_paths_and_label_dict.items():
            for image_paths in sub_dict.values() :
                for image_path in image_paths:
                    self.image_path_list.append(image_path)
                    self.label_list.append(key)


    def __len__(self) -> int:
        return len(self.image_path_list)
    
    def __getitem__(self, idx) -> Tuple[np.ndarray, int]:
        image_path = self.image_path_list[idx]
        label = self.label_list[idx]

        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.image_size, self.image_size), interpolation=cv2.INTER_AREA)
        
        img = img.transpose(2, 0, 1).astype(np.float32) / 255.0

        return img, label, image_path
    

    def _extract_image_paths_and_label(self, file_path) -> Dict[str, Dict[int, List[str]]] :
        possible_image_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png']
        image_dict = {}
        
        # ['softdot_1', 'softline_2', 'darkline_4', 'darkspot_5', 'curvedline_6']
        sorted_labels = sorted(os.listdir(file_path), key=lambda x: int(x.split('_')[-1]))

        for i, label in enumerate(sorted_labels) :
            if os.path.isdir(os.path.join(file_path, label)) :
                image_lists = []
                for file in sorted(os.listdir(os.path.join(file_path, label))):
                    if os.path.splitext(file)[1] in possible_image_extension :
                        image_path = os.path.join(file_path, label, file)
                        image_lists.append(image_path)
                image_dict[i] = {label: image_lists}
        
        return image_dict
    