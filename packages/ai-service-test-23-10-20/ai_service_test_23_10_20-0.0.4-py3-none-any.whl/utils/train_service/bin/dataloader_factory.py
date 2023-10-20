from inceptionNetv3_dataset import InceptionNetv3Dataset
from vgg16_dataset import VGG16DataSet

class DataLoaderFactory:
    
    loaders = {
        "InceptionNetv3": InceptionNetv3Dataset,
        "VGG16": VGG16DataSet,
        # ... add other data loaders here
    }
    
    @staticmethod
    def get_data_loader(model_name, options: dict, train_mode):
        if model_name in DataLoaderFactory.loaders:
            return DataLoaderFactory.loaders[model_name](options, train_mode)
        else:
            raise ValueError(f"No data loader available for model: {model_name}")

if __name__=='__main__':
    # Usage:
    model_name = "InceptionNetv3"
    data_loader = DataLoaderFactory.get_data_loader(model_name)
    
