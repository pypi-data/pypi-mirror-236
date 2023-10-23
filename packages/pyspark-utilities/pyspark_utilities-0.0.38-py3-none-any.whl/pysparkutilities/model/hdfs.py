from ..utils import get_model_property
from .model import ModelStorage
import os
from bdaserviceutils import get_cmd_arg

class Hdfs(ModelStorage):
    storage_type = os.path.basename(__file__).split('.py')[0]

    def __init__(self, spark, name):
        self.spark = spark
        self.name = name

    def load_model(self):
        return get_cmd_arg('hdfsUrl') + get_model_property(name=self.name)

    def save_model(self, model):
        model_path = get_cmd_arg('hdfsUrl') + get_model_property(name=self.name)
        model.write().overwrite().save(model_path)

