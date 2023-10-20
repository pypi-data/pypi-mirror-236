import torch
from typing import Dict
from inceptionNetv3_train import InceptionNetv3Trainer
from vgg16_train import VGG16Trainer

class TrainFactory:
    loaders = {
        "InceptionNetv3": InceptionNetv3Trainer,
        "VGG16": VGG16Trainer,
        # ... add other data Trainer here
    }
    
    @staticmethod
    def get_data_trainer(model_name, 
                         dataloader: Dict[str, torch.utils.data.DataLoader], 
                         options: dict, 
                         log
    ):
        if model_name in TrainFactory.loaders:
            return TrainFactory.loaders[model_name](dataloader, options, log)
        else:
            raise ValueError(f"No data loader available for model: {model_name}")

if __name__=='__main__' :
    # Usage:
    model_name = "InceptionNetv3"
    data_loader = TrainFactory.get_data_loader(model_name)
    
