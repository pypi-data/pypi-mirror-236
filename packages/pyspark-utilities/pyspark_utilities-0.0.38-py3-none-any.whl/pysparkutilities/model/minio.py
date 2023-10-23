from ..utils import get_model_property
from .model import ModelStorage
import os

class Minio(ModelStorage):
    storage_type = os.path.basename(__file__).split('.py')[0]

    def __init__(self, spark, name):
        self.spark = spark
        self.name = name

    def load_model(self):
        return "s3a://" + get_model_property(name=self.name, property='minio_bucket')+ "/" + get_model_property(name=self.name)

    def save_model(self, model):
        model_path = "s3a://" + get_model_property(name=self.name, property='minio_bucket')+ "/" + get_model_property(name=self.name)
        model.write().overwrite().save(model_path)

