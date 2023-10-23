from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc
import numpy as np
import pandas as pd


class ModelPerfornance:
    def __init__(self, score_type="total_score"):
        self.score_type = score_type

    def calculate_prc_auc(self, recall_lst, precision_lst):
        try:
            pr_list = list(zip(precision_lst, recall_lst))
            pr_list = [item for item in pr_list if -1 not in item]
            precision_lst, recall_lst = list(zip(*pr_list))
            auc_precision_recall = round(auc(recall_lst, precision_lst), 3)
        except Exception:
            precision_lst[-1] = -0.99999
            precision_lst[-2] = -0.99999
            pr_list = list(zip(precision_lst, recall_lst))
            pr_list = [item for item in pr_list if -1 not in item]
            precision_lst, recall_lst = list(zip(*pr_list))
            auc_precision_recall = round(auc(recall_lst, precision_lst), 3)
        return [auc_precision_recall]

    # def calculate_prc_auc(self, recall_lst, precision_lst):
    #     pr_list = list(zip(precision_lst, recall_lst))
    #     pr_list = [item for item in pr_list if -1 not in item]
    #     if len(pr_list):
    #         precision_lst, recall_lst = list(zip(*pr_list))
    #         auc_precision_recall = round(auc(recall_lst, precision_lst), 3)
    #         return [auc_precision_recall]
    #     return [-1]

    def division(self, a, b):
        if sum(b):
            x = (a/b).round(3)
            return np.nan_to_num(x, nan=-1).tolist()
        return [-1]*a.shape[0]

    def filter_by_score_type(self, data):
        if self.score_type == 'policy_score':
            return data[::-1]
        return data

    def performance_output(self, y_test, y_score):
        threshold_lst = []
        tp_lst = fp_lst = tn_lst = fn_lst = np.array([])

        if len(y_score) and len(y_test):
            for i in range(0, 11, 1):
                threshold = i / 10
                y_pre = np.where(y_score >= threshold, 1, 0)

                if self.score_type == 'policy_score':
                    threshold_lst.append(round(-2*threshold+1, 3))
                elif self.score_type == 'total_score':
                    threshold_lst.append(threshold)

                tb = pd.DataFrame({'predict_label': y_pre, 'true_label': y_test})
                tp = sum(((tb.true_label == 1) & (tb.predict_label == 1)))
                fp = sum(((tb.true_label == 0) & (tb.predict_label == 1)))
                tn = sum(((tb.true_label == 0) & (tb.predict_label == 0)))
                fn = sum(((tb.true_label == 1) & (tb.predict_label == 0)))

                tp_lst = np.append(tp_lst, tp)
                fp_lst = np.append(fp_lst, fp)
                tn_lst = np.append(tn_lst, tn)
                fn_lst = np.append(fn_lst, fn)

            accuracy_lst = self.division(tp_lst+tn_lst, tp_lst+tn_lst+fp_lst+fn_lst)
            precision_lst = self.division(tp_lst, tp_lst+fp_lst)
            recall_lst = self.division(tp_lst, tp_lst+fn_lst)
            f1_score_lst = self.division(
                2*np.array(precision_lst)*np.array(recall_lst),
                np.array(precision_lst)+np.array(recall_lst)
            )
            fnr_lst = self.division(fn_lst, tp_lst+fn_lst)
            fpr_lst = self.division(fp_lst, fp_lst+tn_lst)
            npv_lst = self.division(tn_lst, fn_lst+tn_lst)
            fdr_lst = self.division(fp_lst, tp_lst+fp_lst)
            for_lst = self.division(fn_lst, fn_lst+tn_lst)
            tnr_lst = self.division(tn_lst, fp_lst+tn_lst)

            auc_precision_recall = self.calculate_prc_auc(fpr_lst, recall_lst)
        else:
            accuracy_lst = precision_lst = recall_lst = f1_score_lst = []
            fnr_lst = fpr_lst = npv_lst = fdr_lst = for_lst = tnr_lst = []
            auc_precision_recall = [-1]

        result = {
            "threshold_lst": self.filter_by_score_type(threshold_lst),
            "tp_lst": self.filter_by_score_type(tp_lst.tolist()),
            "fp_lst": self.filter_by_score_type(fp_lst.tolist()),
            "tn_lst": self.filter_by_score_type(tn_lst.tolist()),
            "fn_lst": self.filter_by_score_type(fn_lst.tolist()),
            "accuracy_lst": self.filter_by_score_type(accuracy_lst),
            "precision_lst": self.filter_by_score_type(precision_lst),
            "recall_lst": self.filter_by_score_type(recall_lst),
            "f1_score_lst": self.filter_by_score_type(f1_score_lst),
            "fnr_lst": self.filter_by_score_type(fnr_lst),
            "fpr_lst": self.filter_by_score_type(fpr_lst),
            "npv_lst": self.filter_by_score_type(npv_lst),
            "fdr_lst": self.filter_by_score_type(fdr_lst),
            "for_lst": self.filter_by_score_type(for_lst),
            "tnr_lst": self.filter_by_score_type(tnr_lst),
            "auc_lst": self.filter_by_score_type(auc_precision_recall)
        }
        return result

    
    def model_train(self):
        random_state = 1
        # Create dataset for binary classification with 5 predictors
        X, y = datasets.make_classification(n_samples=1000,
                                            n_features=5,
                                            n_informative=3,
                                            n_redundant=2)
        # n_redundant=2, random_state=random_state)

        # Split into training and test
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.5)
        # test_size=0.5 ,random_state=random_state)

        # Create classifier using logistic regression
        classifier = LogisticRegression(random_state=random_state)
        classifier.fit(X_train, y_train)
        y_score = classifier.predict_proba(X_test)[:, 1]
        # result = self.performance_output(y_test, y_score)
        # return result
        return y_test, y_score


def main():
    mp = ModelPerfornance(score_type='policy_score')
    list_y_test, list_y_score = mp.model_train()
    result = mp.performance_output(list_y_test, list_y_score)
    print(result)


if __name__ == "__main__":
    main()
