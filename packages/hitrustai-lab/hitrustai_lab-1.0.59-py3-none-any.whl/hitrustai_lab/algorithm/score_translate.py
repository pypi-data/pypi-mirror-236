import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


def total_score_to_policy_score(total_score):
    return round(total_score * -2 + 1, 6)


def policy_score_to_total_score(x):
    return round(1 - (x - 1) / (-2), 2)


def pca_column_rank(pca_model, list_need_features):
    n_pcs = pca_model.components_.shape[0]
    most_important = [np.abs(pca_model.components_[i]).argmax()
                      for i in range(n_pcs)]

    initial_feature_names = list_need_features
    most_important_names = [
        initial_feature_names[most_important[i]] for i in range(n_pcs)]
    dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}
    df = pd.DataFrame(dic.items())
    df["ratio"] = pca_model.explained_variance_ratio_
    return df


def pca_to_ahp(pca_df):
    list1 = []
    record = None
    idex = 1
    list_r = []
    for i in list(pca_df.ratio.values):
        try:
            r = str(i).split("0.")[1]
        except Exception:
            r = str(i).split(".")[0]
            r = r + "0"
        list_r.append(r)
    for i in list_r:
        if len(i) < 4 and int(i[0]) > 0:
            list1.append(idex)
            idex += 1
        else:
            for ii in i:
                if ii != "0":
                    if record == ii or record is None:
                        list1.append(idex)
                    else:
                        idex += 1
                        list1.append(idex)
                    record = ii
                    break
                else:
                    if record != "0" and record is not None:
                        idex += 1
                        record = ii
                    list1.append(idex)
    dict_from_list = dict(zip(list(pca_df[1]), list1))
    return dict_from_list


if __name__ == '__main__':
    df = pd.read_csv("model_predict.csv")
    features = ['device_consistency_score', 'internet_info_score',
                'personal_device_score', 'device_connection_score', 'ip_change_score',
                'ip_connection_score', 'bio_behavior_score', 'robot_detection_score']
    x = df.loc[:, features].values
    model = PCA(n_components=8)
    model.fit(x)
    df1 = pca_column_rank(model, features)
    dict_from_list = pca_to_ahp(df1)
    print(dict_from_list)