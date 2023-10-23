from .datastorage import DataStorage
from .utils import get_dataset_property

class Presto(DataStorage):

    # Initialize Presto Python Driver

    # overriding abstract method
    def load_dataset(self, name, read_all=True, input_dest='', header=True):

        input_columns = get_dataset_property("input_columns") if get_dataset_property("input_columns") is not None else "*"

        if input_dest == '':
            input_dataset = get_dataset_property(name)
        else:
            input_dataset = input_dest

        password = get_dataset_property(name, "prestoPassword")
        user = get_dataset_property(name, "prestoUser")
        host = get_dataset_property(name, "prestoHost")
        port = get_dataset_property(name, "prestoPort")
        db = get_dataset_property(name, "prestoDb")

        if password is not None and password not in ['', "", "''"]:
            if read_all:
                df = self.spark.read.format("jdbc").option("driver", "com.facebook.presto.jdbc.PrestoDriver"). \
                    option("url", "jdbc:presto://" + host+":"+port+"/" + db).option("dbtable", "(SELECT * FROM " + input_dataset + ")"). \
                    option("user", user). \
                    option('password', password).load()
            else:
                df = self.spark.read.format("jdbc").option("driver", "com.facebook.presto.jdbc.PrestoDriver"). \
                    option("url", "jdbc:presto://"+host+":"+port+"/"+db).option("dbtable", "(SELECT " + input_columns + " FROM " + input_dataset + ")"). \
                    option("user", user). \
                    option('password', password).load()
        else:
            if read_all:
                df = self.spark.read.format("jdbc").option("driver", "com.facebook.presto.jdbc.PrestoDriver"). \
                    option("url", "jdbc:presto://"+host+":"+port+"/"+db).option("dbtable", "(SELECT * FROM " + input_dataset + ")"). \
                    option("user", get_dataset_property("prestoUser-input-dataset")).load()
            else:
                df = self.spark.read.format("jdbc").option("driver", "com.facebook.presto.jdbc.PrestoDriver"). \
                    option("url", "jdbc:presto://"+host+":"+port+"/"+db).option("dbtable", "(SELECT " + input_columns + " FROM " + input_dataset + ")"). \
                    option("user", user).load()

        # rename column
        for column in input_columns.split(","):
            df = df.withColumnRenamed(column.lower(), column)
        return df

    # overriding abstract method
    def save_dataset(self, name, df, output_dest):
        pass
