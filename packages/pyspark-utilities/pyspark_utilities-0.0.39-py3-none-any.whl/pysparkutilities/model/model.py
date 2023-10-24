from abc import ABC
from ..utils import get_model_property


class ModelStorage(ABC):

    def __new__(cls, *args, **kw):
        
        storage_type = get_model_property(kw['name'], "storage_type")
        if storage_type == None:
            storage_type="filesystem"
        
        # Create a map of all subclasses based on storage type property (present on each subclass)
        subclass_map = {subclass.storage_type: subclass for subclass in cls.__subclasses__()}

        # Select the proper subclass based on
        subclass = subclass_map[storage_type.lower()]
        return super(cls, subclass).__new__(subclass)
    
    def __init__(self, spark, name):
        self.spark = spark
    
    # abstract method
    def load_model(self):
        pass

    # abstract method
    def save_model(self, model):
        pass
