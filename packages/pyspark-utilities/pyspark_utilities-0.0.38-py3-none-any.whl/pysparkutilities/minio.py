from .datastorage import DataStorage
from .utils import get_dataset_property


class Minio(DataStorage):

    # overriding abstract method
    def load_dataset(self, name, read_all=True, input_dest='', header=True):

        bucket = get_dataset_property(name, 'minio_bucket')

        if input_dest == '':
            input_dataset = get_dataset_property(name)
        else:
            input_dataset = input_dest
        
        delimiter = get_dataset_property(name, "delimiter") if get_dataset_property(name, "delimiter") is not None else ","
        
        input_file_format = get_dataset_property(name, "inputFileFormat") if get_dataset_property(name, "inputFileFormat") is not None else "csv"
        
        input_columns = get_dataset_property(name, "input_columns")
        if input_columns is not None:
            columns_list = input_columns.split(",")
        else:
            columns_list = ["*"]
        
        if read_all is True:
            return self.spark.read.load("s3a://" + bucket + "/" + input_dataset, format=input_file_format, sep=delimiter, inferSchema=True, header=header, error_bad_lines=False)
        else:
            return self.spark.read.load("s3a://" + bucket + "/" + input_dataset, format=input_file_format, sep=delimiter, inferSchema=True, header=header, error_bad_lines=False).select(*columns_list)

    # overriding abstract method
    def save_dataset(self, name, df, output_dest):

        bucket = get_dataset_property(name, 'minio_bucket')

        if output_dest == '':
            output_dataset = get_dataset_property(name)
        else:
            output_dataset = output_dest

        delimiter = get_dataset_property(name, "delimiter") if get_dataset_property(name, "delimiter") is not None else ","
        output_file_format = get_dataset_property(name, "outputFileFormat") if get_dataset_property(name, "outputFileFormat") is not None else "csv"

        df.write.options(delimiter=delimiter).\
            mode('overwrite').\
            option("header", True).\
            save("s3a://" + bucket + "/" + output_dataset, format = output_file_format)

