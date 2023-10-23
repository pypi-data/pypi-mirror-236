import pandas as pd
pd.set_option('display.max_columns', None) 

type_data_analyse = {
    "path": "./data/",
    "df_analyze": "new_fraud_analyze.csv",
    "df_info": "new_tb_fraud_detect_info.csv",
    "threshold_police": 0.05
}


class Utils:
    def model_result_times(self, model_reason):
        normal = 0
        abnormal = 0
        for reason in model_reason:
            if "-normal" in reason:
                normal += 1
            else:
                abnormal += 1
        return normal, abnormal

    def model_typle(self, res):
        if res != "0":
            return 1
        else:
            return 0

    def count_rank_to_dict(dict_input_result, rank=4):
        top_keys = list(dict_input_result.keys())[0:rank]
        top_values = list(dict_input_result.values())[0:rank]
        
        dict_result = {}
        for k, v in zip(top_keys, top_values):
            dict_result[k] = v
        others_values = sum(list(dict_input_result.values())[rank:])
        dict_result["others"] = others_values
        return dict_result


class DataAnalyse(Utils):
    def __init__(self, type_data_analyse=type_data_analyse):
        self.type_data_analyse = type_data_analyse
        self.intersected_df = None
        self.intersected_df_normal = None
        self.df_all = None

    def read_fraud(self):
        df_ana = pd.read_csv(self.type_data_analyse['path'] + self.type_data_analyse['df_analyze'])
        df_info = pd.read_csv(self.type_data_analyse['path'] + self.type_data_analyse['df_info'])
        # print(df_ana.columns)

        abnormal_df = df_ana[df_ana["policy_score"] < self.type_data_analyse['threshold_police']]
        normal_df = df_ana[df_ana["policy_score"] >= self.type_data_analyse['threshold_police']]
        df_info = df_info.rename(columns={'pk_id': 'fd_info_id'})
        intersected_df = pd.merge(df_info, abnormal_df, on=['fd_info_id'], how='inner')
        intersected_df_normal = pd.merge(df_info, normal_df, on=['fd_info_id'], how='inner')
        self.intersected_df = intersected_df
        self.intersected_df_normal = intersected_df_normal

    def data_analyse(self):
        df_all = pd.DataFrame()
        for udid in self.intersected_df["udid"].value_counts().keys():
            df = self.intersected_df[self.intersected_df["udid"] == udid]

            fruit_dict = {
                "UDID": udid,
                "累積數量": len(df),
                "client_account": str(list(set(df.client_account))),
                "設備種類": str(list(set(df.hardware_device_type))),
                "IP": str(list(set(df.ip_request))),
                "是否為proxy": str(df.ip_is_proxy.value_counts().to_dict()),
                "是否為vpn": str(df.ip_is_vpn.value_counts().to_dict()),
                "是否為tor": str(df.ip_is_tor.value_counts().to_dict()),
                "瀏覽器種類": str(list(set(df.browser_name))),
                "異常模型數量": 0,
                "設備一致性正常次數": str(self.model_result_times(df.device_consistency_reason)[0]),
                "設備一致性異常次數": str(self.model_result_times(df.device_consistency_reason)[1]),
                "設備慣性正常次數": str(self.model_result_times(df.personal_device_reason)[0]),
                "設備慣性異常次數": str(self.model_result_times(df.personal_device_reason)[1]),
                "網路資訊正常次數": str(self.model_result_times(df.internet_info_reason)[0]),
                "網路資訊異常次數": str(self.model_result_times(df.internet_info_reason)[1]),
                "設備連線次數正常次數": str(self.model_result_times(df.device_connection_reason)[0]),
                "設備連線次數異常次數": str(self.model_result_times(df.device_connection_reason)[1]),
                "IP連線次數正常次數": str(self.model_result_times(df.ip_connection_reason)[0]),
                "IP連線次數異常次數": str(self.model_result_times(df.ip_connection_reason)[1]),
                "IP切換正常次數": str(self.model_result_times(df.ip_change_reason)[0]),
                "IP切換異常次數": str(self.model_result_times(df.ip_change_reason)[1]),
                "生物行為正常次數": str(self.model_result_times(df.bio_behavior_reason)[0]),
                "生物行為異常次數": str(self.model_result_times(df.bio_behavior_reason)[1]),
                "機器人特徵正常次數": str(self.model_result_times(df.robot_detection_reason)[0]),
                "機器人特徵異常次數": str(self.model_result_times(df.robot_detection_reason)[1]),
                "此UDID是否存在正常分佈中": str(udid in list(self.intersected_df_normal["udid"])),
            }

            dict_ab_model = self.model_typle(fruit_dict["設備一致性異常次數"]) + self.model_typle(fruit_dict["設備慣性異常次數"]) +\
                self.model_typle(fruit_dict["網路資訊異常次數"]) + self.model_typle(fruit_dict["設備連線次數異常次數"]) +\
                self.model_typle(fruit_dict["IP連線次數異常次數"]) + self.model_typle(fruit_dict["IP切換異常次數"]) +\
                self.model_typle(fruit_dict["生物行為異常次數"]) + \
                self.model_typle(fruit_dict["機器人特徵異常次數"])

            fruit_dict["異常模型數量"] = dict_ab_model

            df_all = df_all.append([fruit_dict])
        df_all.index = range(len(df_all))
        self.df_all = df_all


def main():
    da = DataAnalyse()
    da.read_fraud()
    da.data_analyse()
    da.df_all['UDID'] = da.df_all['UDID'].astype(str)
    with pd.ExcelWriter('Courses.xlsx') as writer:
        da.df_all.to_excel(writer, sheet_name='異常')
        da.intersected_df_normal.to_excel(writer, sheet_name='正常')


if __name__ == '__main__':
    main()
