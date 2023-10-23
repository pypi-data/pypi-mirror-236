from sqlalchemy import Column, Integer, Table, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP, VARCHAR, LONGTEXT
# from sqlalchemy.ext.declarative import declarative_base

Base_Model = declarative_base()


def create_model_performance(table_name):
    base_table = Table(
        table_name,
        Base_Model.metadata,
        Column("pk_id", Integer, primary_key=True,
               autoincrement=True, nullable=False),
        # Column("customer_id", VARCHAR(20)),
        # Column("training_id", VARCHAR(45)),
        Column("model_id", VARCHAR(20)),
        # Column("profile_id", VARCHAR(20)),
        # Column("tag", VARCHAR(20)),
        Column("model_name", VARCHAR(100)),
        Column("training_start_time", TIMESTAMP()),
        Column("training_end_time", TIMESTAMP()),
        Column("total_training_time", Integer),
        Column("training_data_start_date", TIMESTAMP()),
        Column("training_data_end_date", TIMESTAMP()),
        Column("number_of_dump_data", Integer),
        Column("number_of_training_data", Integer),
        Column("number_of_positive_samples_in_training_data", Integer),
        Column("number_of_negative_samples_in_training_data", Integer),
        Column("number_of_validation_data", Integer),
        Column("true_label_column", VARCHAR(45)),
        Column("number_of_positive_samples_in_validation_data", Integer),
        Column("number_of_negative_samples_in_validation_data", Integer),
        Column("threshold", LONGTEXT),
        Column("tp", LONGTEXT),
        Column("fp", LONGTEXT),
        Column("tn", LONGTEXT),
        Column("fn", LONGTEXT),
        Column("accuracy", LONGTEXT),
        Column("ppv", LONGTEXT),
        Column("recall", LONGTEXT),
        Column("f1_score", LONGTEXT),
        Column("fnr", LONGTEXT),
        Column("fpr", LONGTEXT),
        Column("npv", LONGTEXT),
        Column("fdr", LONGTEXT),
        Column("for_", LONGTEXT),
        Column("tnr", LONGTEXT),
        Column("auc", FLOAT),
        Column("reason", LONGTEXT),
        Column("return_code", LONGTEXT),
    )
    return base_table
