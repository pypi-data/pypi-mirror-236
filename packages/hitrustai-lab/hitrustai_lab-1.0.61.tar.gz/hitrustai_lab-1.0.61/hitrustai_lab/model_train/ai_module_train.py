import os
import re
import json
import time
import datetime
import pandas as pd
import numpy as np
from decouple import AutoConfig
from sqlalchemy import Column, text, Integer
from sqlalchemy.dialects.mysql import TIMESTAMP

from hitrustai_lab.model_train.core.utils import decrypt_passwd, sugg_batch_size
from hitrustai_lab.apollo.apollo_client import ApolloClient
from hitrustai_lab.apollo.util import check_apollo_change, get_apollo_value

from hitrustai_lab.matrix.model_performance import ModelPerfornance
from hitrustai_lab.orm import Orm, get_orm_profile
from hitrustai_lab.orm.Tables.ModelPerformance import create_model_performance, Base_Model


dict_init_arg = {
    "list_y_test": list,
    "list_y_score": np.array,
    # "customer_id_lst": str,
    # "training_id_lst": str,
    "model_id_lst": str,
    # "profile_id_lst": str,
    # "tag_lst": str,
    "train_start_time": str,
    "total_training_time_lst": int,
    "training_start_time_lst": datetime,
    "training_end_time_lst": datetime,
    "number_of_dump_data": int,
    "number_of_training_data": int,
    "number_of_positive_samples_in_training_data": int,
    "number_of_negative_samples_in_training_data": int,
    "number_of_validation_data": int,
    "true_label_column_lst": str,
    "number_of_positive_samples_in_validation_data": int,
    "number_of_negative_samples_in_validation_data": int,
    "return_code": str,
    "reason": str
}


class TrainModelToSQl:
    def __init__(self, host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test", table_name="int") -> None:
        self.table_name = table_name
        self.orm_profile = get_orm_profile(host=host, port=port, db=db, user=user, pwd=passwd)
        self.orm = Orm(profile=self.orm_profile)

    def performance(self, dict_init_arg: dict):
        mp = ModelPerfornance(score_type='policy_score')
        try:
            result = mp.performance_output(dict_init_arg["list_y_test"], dict_init_arg["list_y_score"])
            result = {
                # 'customer_id': dict_init_arg["customer_id_lst"],
                # 'training_id': dict_init_arg["training_id_lst"],
                'model_id': dict_init_arg["model_id_lst"],
                # 'profile_id': dict_init_arg["profile_id_lst"],
                # 'tag': dict_init_arg["tag_lst"],
                # 'model_name': dict_init_arg["model_id_lst"] + "-" + "".join(re.findall(r'\d+', str(datetime.datetime.now()))),
                'model_name': dict_init_arg["model_id_lst"] + "-" + dict_init_arg["train_start_time"],
                'training_start_time': dict_init_arg["training_start_time_lst"],
                'training_end_time': dict_init_arg["training_end_time_lst"],
                'total_training_time': dict_init_arg["total_training_time_lst"],
                'training_data_start_date': dict_init_arg["training_data_start_date"],
                'training_data_end_date': dict_init_arg["training_data_end_date"],
                'number_of_dump_data': dict_init_arg["number_of_dump_data"],
                'number_of_training_data': dict_init_arg["number_of_training_data"],
                'number_of_positive_samples_in_training_data': dict_init_arg["number_of_positive_samples_in_training_data"],
                'number_of_negative_samples_in_training_data': dict_init_arg["number_of_negative_samples_in_training_data"],
                'number_of_validation_data': dict_init_arg["number_of_validation_data"],
                'true_label_column': dict_init_arg["true_label_column_lst"],
                'number_of_positive_samples_in_validation_data': dict_init_arg["number_of_positive_samples_in_validation_data"],
                'number_of_negative_samples_in_validation_data': dict_init_arg["number_of_negative_samples_in_validation_data"],
                'threshold': [result['threshold_lst']],
                'tp': [result['tp_lst']],
                'fp': [result['fp_lst']],
                'tn': [result['tn_lst']],
                'fn': [result['fn_lst']],
                'accuracy': [result['accuracy_lst']],
                'ppv': [result['precision_lst']],
                'recall': [result['recall_lst']],
                'f1_score': [result['f1_score_lst']],
                'fnr': [result['fnr_lst']],
                'fpr': [result['fpr_lst']],
                'npv': [result['npv_lst']],
                'fdr': [result['fdr_lst']],
                'for_': [result['for_lst']],
                'tnr': [result['tnr_lst']],
                'auc': result['auc_lst'],
                "return_code": dict_init_arg['return_code'],
                "reason": dict_init_arg['reason']
            }
        except Exception:
            result = {
                # 'customer_id': dict_init_arg["customer_id_lst"],
                # 'training_id': dict_init_arg["training_id_lst"],
                'model_id': dict_init_arg["model_id_lst"],
                # 'profile_id': dict_init_arg["profile_id_lst"],
                # 'tag': dict_init_arg["tag_lst"],
                'model_name': dict_init_arg["model_id_lst"] + "-" + dict_init_arg["train_start_time"],
                'training_start_time': "2000-01-01 00:00:00",
                'training_end_time': "2000-01-01 00:00:00",
                'total_training_time': -1,
                'training_data_start_date': "2000-01-01 00:00:00",
                'training_data_end_date': "2000-01-01 00:00:00",
                'number_of_dump_data': -1,
                'number_of_training_data': -1,
                'number_of_positive_samples_in_training_data': -1,
                'number_of_negative_samples_in_training_data': -1,
                'number_of_validation_data': -1,
                'true_label_column': dict_init_arg["true_label_column_lst"],
                'number_of_positive_samples_in_validation_data': -1,
                'number_of_negative_samples_in_validation_data': -1,
                'threshold': [[]],
                'tp': [[]],
                'fp': [[]],
                'tn': [[]],
                'fn': [[]],
                'accuracy': [[]],
                'ppv': [[]],
                'recall': [[]],
                'f1_score': [[]],
                'fnr': [[]],
                'fpr': [[]],
                'npv': [[]],
                'fdr': [[]],
                'for_': [[]],
                'tnr': [[]],
                'auc': [[]],
                "return_code": dict_init_arg['return_code'],
                "reason": dict_init_arg['reason']
            }   
        return result

    def dict_to_dataframe(self, dict_init_arg: dict, dict_add_column=None):
        self.need_column = self.performance(dict_init_arg)
        if dict_add_column is not None:
            for key in dict_add_column:
                self.need_column[key] = dict_init_arg[key]
        
        df = pd.DataFrame(data=self.need_column)
        df['total_training_time'] = df.total_training_time
        df['training_data_start_date'] = df.training_data_start_date
        df['training_data_end_date'] = df.training_data_end_date

        for col in [
            'threshold', 'tp', 'fp', 'tn', 'fn', 'accuracy', 'ppv', 'recall', 'f1_score',
            'fnr', 'fpr', 'npv', 'fdr', 'for_', 'tnr'
        ]:
            df[col] = df[col].apply(lambda x: json.dumps(x))

        return df

    def insert_db(self, data: dict, dict_add_column=None):
        # if not data:
        #     return
        base_table = create_model_performance(self.table_name)
        if dict_add_column is not None:
            for key in dict_add_column:
                base_table.append_column(dict_add_column[key])
        base_table.append_column(Column("create_time", TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6)")))
        
        class User(Base_Model):
            __table__ = base_table
        # self.orm.create_table(Base_Model, User)
        
        data = self.dict_to_dataframe(data, dict_add_column)
        
        self.orm.data_to_DB(data, User)


class GetConfArg:
    def tryerr(self, cnf, key):
        try:
            cnf_read = cnf(key)
            return cnf_read
        except Exception:
            self.err_return_code = "0105"
            self.err_reason = f"{self.model_name}-failed(lack {key} env variables)"
            return ""
    
    def read_train_conf_env(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        db_pass = config('DB_PASS', default='')
        password = decrypt_passwd(self.passwd_so_name, db_pass)

        self.SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            config('DB_ENGINE', default=''),
            config('DB_USERNAME', default=''),
            password,
            config('DB_HOST', default=''),
            config('DB_PORT', default=''),
            config('DB_NAME', default='')
        )
        self.tryerr(config, 'TRUE_LABEL_COLUMN')
        self.appollo_info = {
            # "customer_id": config('CUSTOMER_ID', default=''),
            # "PROFILE_ID": config('PROFILE_ID', default=''),
            # "tag": config('tag', default=''),
            # "training_id": config('TRAINING_ID', default=''),

            "model_id": config('MODEL_ID', default=''),
            "TRAIN_START_TIME": config('TRAIN_START_TIME', default=''),
            "BATCH_SIZE": int(config('BATCH_SIZE', default=6000)),
            "TRUE_LABEL_COLUMN": self.tryerr(config, 'TRUE_LABEL_COLUMN'),
            "kg_path": config('SOURCE_PATH_KNOWLEDGE', default='./data/kg'),
            "lib_path": config('SOURCE_PATH_LIB', default='./data/lib'),
            "DB_ENGINE": self.tryerr(config, 'DB_ENGINE'),
            "DB_USERNAME": self.tryerr(config, 'DB_USERNAME'),
            "DB_PASS": password,
            "DB_HOST": self.tryerr(config, 'DB_HOST'),
            "DB_PORT": self.tryerr(config, 'DB_PORT'),
            "DB_NAME": self.tryerr(config, 'DB_NAME')
        }

    def read_train_conf_apollo(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        try:
            APOLLO_URL = config('APOLLO_URL')
            APOLLO_APPID = config('APOLLO_APPID')
            APOLLO_CLUSTER = config('APOLLO_CLUSTER')
            APOLLO_SECRET = config('APOLLO_SECRET')
            APOLLO_NAMESPACE_INF = config('APOLLO_NAMESPACE_INF')
            APOLLO_NAMESPACE_MODAL = config('APOLLO_NAMESPACE_MODAL')
        except Exception:
            os.kill(0, 4)
        apollo_client = ApolloClient(
            app_id=APOLLO_APPID,
            cluster=APOLLO_CLUSTER,
            config_url=APOLLO_URL,
            secret=APOLLO_SECRET,
            change_listener=check_apollo_change)

        db_pass = get_apollo_value(apollo_client, "DB_PASS", APOLLO_NAMESPACE_INF)

        password = decrypt_passwd(self.passwd_so_name, db_pass)
        self.SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            get_apollo_value(apollo_client, "DB_ENGINE", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_USERNAME", APOLLO_NAMESPACE_INF),
            password,
            get_apollo_value(apollo_client, "DB_HOST", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_PORT", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_NAME", APOLLO_NAMESPACE_INF)
        )
        self.appollo_info = {
            # "customer_id": get_apollo_value(apollo_client, "CUSTOMER_ID", APOLLO_NAMESPACE_MODAL),
            # "tag": get_apollo_value(apollo_client, "tag", APOLLO_NAMESPACE_MODAL),
            # "PROFILE_ID": get_apollo_value(apollo_client, "PROFILE_ID", APOLLO_NAMESPACE_MODAL),
            # "training_id": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),
            # "topic": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),

            "model_id": get_apollo_value(apollo_client, "MODEL_ID", APOLLO_NAMESPACE_MODAL),
            "BATCH_SIZE": int(get_apollo_value(apollo_client, "BATCH_SIZE", APOLLO_NAMESPACE_MODAL)),
            "TRUE_LABEL_COLUMN": get_apollo_value(apollo_client, "TRUE_LABEL_COLUMN", APOLLO_NAMESPACE_MODAL),
            "kg_path": config('SOURCE_PATH_KNOWLEDGE'),
            "lib_path": config('SOURCE_PATH_LIB'),
            "DB_ENGINE": get_apollo_value(apollo_client, "DB_ENGINE", APOLLO_NAMESPACE_INF),
            "DB_USERNAME": get_apollo_value(apollo_client, "DB_USERNAME", APOLLO_NAMESPACE_INF),
            "DB_PASS": password,
            "DB_HOST": get_apollo_value(apollo_client, "DB_HOST", APOLLO_NAMESPACE_INF),
            "DB_PORT": get_apollo_value(apollo_client, "DB_PORT", APOLLO_NAMESPACE_INF),
            "DB_NAME": get_apollo_value(apollo_client, "DB_NAME", APOLLO_NAMESPACE_INF)
        }


class HitrustaiTrainTemple(GetConfArg):
    def __init__(self, dict_model, init_logger, passwd_so_name="./data/passwd.so", model_name="fraud detect"):
        self.err_reason = ""
        self.err_return_code = "9909"
        self.dict_model = dict_model
        self.init_logger = init_logger
        self.passwd_so_name = passwd_so_name
        self.model_name = model_name
        self.dict_init_arg = None
        self.template_output_txt = '''
INFO_MODEL_NAME="%s"
INFO_MODEL_ID="%s"
DATA_START_DATE="%s"
DATA_END_DATE="%s"
DATA_TOTAL_ROW="%s"
TRAINING_DATE="%s"
TRAINING_TIME="%s"
TRAINING_RETURN_CODE="%s"
TRAINING_REASON="%s"
        '''

    def err_template(self):
        self.training_start_time_lst = "2000-01-01 00:00:00"
        self.total_training_time_lst = -1
        self.training_end_time_lst = "2000-01-01 00:00:00"
        self.DATA_START_DATE = "2000-01-01 00:00:00"
        self.DATA_END_DARE = "2000-01-01 00:00:00"
        self.DATA_TOTAL_ROW = -1
        self.dict_init_arg = self.error_arg_dict()
        self.dict_init_arg["reason"] = self.err_reason

    def error_arg_dict(self):
        try:
            true_lable_name = self.dict_model.true_lable_name
        except Exception:
            true_lable_name = None
        try:
            model_id = self.appollo_info.get("model_id")
            train_start_time = self.appollo_info.get("TRAIN_START_TIME")
        except Exception:
            model_id = None
            train_start_time = None
        
        dict_init_arg = {
            "list_y_test": [],
            # "list_y_score": np.array(self.df["total_score_fd7"]),
            "list_y_score": [],
            # "customer_id_lst": self.appollo_info["customer_id"],
            # "training_id_lst": self.appollo_info["training_id"],
            "model_id_lst": model_id,
            "train_start_time": train_start_time,
            # "profile_id_lst": self.appollo_info["PROFILE_ID"],
            # "tag_lst": self.appollo_info["tag"],
            "training_start_time_lst": self.training_start_time_lst,
            "total_training_time_lst": self.total_training_time_lst,

            "training_data_start_date": self.DATA_START_DATE,
            "training_data_end_date": self.DATA_END_DARE,
            "training_end_time_lst": self.training_end_time_lst,
            "number_of_dump_data": -1,
            "number_of_training_data": -1,
            "number_of_positive_samples_in_training_data": -1,
            "number_of_negative_samples_in_training_data": -1,
            "number_of_validation_data": -1,
            "true_label_column_lst": true_lable_name,
            "number_of_positive_samples_in_validation_data": -1,
            "number_of_negative_samples_in_validation_data": -1,
            "return_code": self.err_return_code,
        }
        return dict_init_arg

    def input_arg_dict(self):
        """
        dict_init_arg = {
            "list_y_test": list,
            "list_y_score": np.array,
            # "customer_id_lst": str,
            # "training_id_lst": str,
            "model_id_lst": str,
            # "profile_id_lst": str,
            # "tag_lst": str,
            "training_start_time_lst": str,
            "total_training_time_lst": int,
            "training_start_time_lst": datetime,
            "training_end_time_lst": datetime,
            "number_of_dump_data": int,
            "number_of_training_data": int,
            "number_of_positive_samples_in_training_data": int,
            "number_of_negative_samples_in_training_data": int,
            "number_of_validation_data": int,
            "true_label_column_lst": str,
            "number_of_positive_samples_in_validation_data": int,
            "number_of_negative_samples_in_validation_data": int,
            "return_code": str,
            "reason": str
        }
        """
        
        dict_init_arg = {
            "list_y_test": list(self.dict_model.df[self.dict_model.true_lable_name]),
            # "list_y_score": np.array(self.df["total_score_fd7"]),
            "list_y_score": np.array,
            # "customer_id_lst": self.appollo_info["customer_id"],
            # "training_id_lst": self.appollo_info["training_id"],
            "model_id_lst": self.appollo_info["model_id"],
            "train_start_time": self.appollo_info["TRAIN_START_TIME"],
            # "profile_id_lst": self.appollo_info["PROFILE_ID"],
            # "tag_lst": self.appollo_info["tag"],
            "training_start_time_lst": self.training_start_time_lst,
            "total_training_time_lst": self.total_training_time_lst,

            "training_data_start_date": self.DATA_START_DATE,
            "training_data_end_date": self.DATA_END_DARE,
            "training_end_time_lst": self.training_end_time_lst,
            "number_of_dump_data": self.dict_model.DATA_TOTAL_ROW,
            "number_of_training_data": self.dict_model.DATA_TOTAL_ROW_TRAIN,
            "number_of_positive_samples_in_training_data": self.dict_model.VAL_POSITION_NUMBER,
            "number_of_negative_samples_in_training_data": self.dict_model.VAL_POSITION_NEGATIVE,
            "number_of_validation_data": self.dict_model.DATA_TOTAL_ROW_VAL,
            "true_label_column_lst": self.dict_model.true_lable_name,
            "number_of_positive_samples_in_validation_data": self.dict_model.VAL_POSITION_NUMBER_VAL,
            "number_of_negative_samples_in_validation_data": self.dict_model.VAL_POSITION_NEGATIVE_VAL,
            "return_code": self.dict_report["return_code"],
            "reason": self.dict_report["reason"]
        }
        return dict_init_arg

    def train(self):
        try:
            self.read_train_conf_env()
            # config = AutoConfig(search_path=os.getcwd() + "/env")
            # if config('ENV_METHOD') == "env":
            #     self.read_train_conf_env()
            # else:
            #     self.read_train_conf_apollo()
            # ===========================================================================================
            file_path = self.dict_model.file_path
            batch_size = self.appollo_info["BATCH_SIZE"]
            count = self.dict_model.check_data_row(file_path, batch_size)
            ideal_batch = sugg_batch_size(count, max_batch_size=100000)
            print("ideal batch:", ideal_batch)
            ideal_batch_bool = False
            if batch_size > count:
                self.err_return_code = "9933"
                self.err_reason = f"{self.model_name}-failed(Suggested value for batch size is: {ideal_batch})"
                self.err_template()
                return
            elif batch_size > ideal_batch:
                batch_size = ideal_batch
                ideal_batch_bool = True
            # ===========================================================================================

            t1 = time.time()
            self.training_start_time_lst = datetime.datetime.now()
            self.dict_report = self.dict_model.train(chunksize=batch_size, true_lable_name=self.appollo_info["TRUE_LABEL_COLUMN"])
            self.total_training_time_lst = time.time() - t1
            self.training_end_time_lst = datetime.datetime.now()
            self.DATA_START_DATE = self.dict_model.DATA_START_DATE
            self.DATA_END_DARE = self.dict_model.DATA_END_DARE
            self.DATA_TOTAL_ROW = self.dict_model.DATA_TOTAL_ROW
            if self.dict_report["return_code"] != "4008":
                self.err_reason = self.dict_report["reason"]
                self.err_template()
            else:
                if ideal_batch_bool:
                    self.dict_report["reason"] = self.dict_report["reason"] + "(%s %s .The batch size is too large.)" % ("The value has been changed to", ideal_batch)
                self.dict_init_arg = self.input_arg_dict()

        except Exception as e:
            if self.err_reason != "":
                self.err_reason = self.err_reason
            else:
                err = e.args[0]
                self.err_reason = f"{self.model_name}-failed({err})"
            self.err_template()

    def insert_db(self, table_name, dict_add_column=None):
        try:
            tmts = TrainModelToSQl(
                host=self.appollo_info["DB_HOST"],
                port=self.appollo_info["DB_PORT"],
                user=self.appollo_info["DB_USERNAME"],
                passwd=self.appollo_info["DB_PASS"],
                db=self.appollo_info["DB_NAME"],
                table_name=table_name
            )
            tmts.insert_db(data=self.dict_init_arg, dict_add_column=dict_add_column)
        except Exception as e:
            self.dict_init_arg["return_code"] = "0105"
            if self.err_reason != "":
                self.dict_init_arg["reason"] = self.err_reason
            else:
                self.dict_init_arg["reason"] = self.model_name + "-" + e.args[0]

    def output_txt(self, model_name="Fraud Detect"):
        output_txt = self.template_output_txt % (
            model_name,
            # self.dict_init_arg["training_id_lst"],
            # self.dict_init_arg["customer_id_lst"],
            self.dict_init_arg["model_id_lst"],
            self.dict_init_arg["training_data_start_date"],
            self.dict_init_arg["training_data_end_date"],
            self.dict_init_arg["number_of_dump_data"],
            self.dict_init_arg["training_start_time_lst"],
            self.dict_init_arg["total_training_time_lst"],
            self.dict_init_arg["return_code"],
            self.dict_init_arg["reason"],
        )
        with open(self.appollo_info["lib_path"] + "/output.txt", 'w') as f:
            f.write(output_txt + "\n")


if __name__ == '__main__':
    dict_add_column = {
        "add_column1": Column("add_column1", Integer, primary_key=True),
        "add_column2": Column("add_column2", Integer, primary_key=True)
    }

    tmts = TrainModelToSQl(
        host="192.168.10.203",
        port="3305",
        user="diia",
        passwd="diia16313302",
        db="service_report",
        table_name="test111111"
    )

    tmts.insert_db(data=dict_init_arg, dict_add_column=dict_add_column)
