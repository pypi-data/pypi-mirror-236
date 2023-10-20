from abc import ABC, abstractmethod

# TODO: lr scheduler의 경우 각자 구현해서 쓰게 할지, init을 만들어 인터페이스로부터 관리할지 논의가 필요.
class BaseTrainer(ABC):
        
    @abstractmethod
    def start_train(self) -> str:
        """
        Start training the model. Implementations of this method in 
        subclasses should handle the entire training process.
        Train should be start like this: 
        _, save_directory = self.train_model() 
        """
        pass
    
    @abstractmethod
    def validate_epoch(self):
        pass
    
    @ abstractmethod
    def train_epoch(self):
        pass
    
    @abstractmethod
    def train_model(self):
        pass
    