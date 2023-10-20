## 前置作業
```sh
git clone https://gitlab-cloud.hitrustai.com/bruce60108010204/hitrustai-lab.git -b v1.1.0
cd hitrustai_lab
chmod u+x *.sh
git config --global credential.helper store
```

## 安裝
- 安裝完可以只留./gitlab_update.sh，其餘可以刪除
```sh
pip install git+https://gitlab-cloud.hitrustai.com/bruce60108010204/hitrustai-lab@v1.1.0
```
## 更新到 PyPi
1. 更新 [setup.py](./setup.py) line 32 的版本號
2. 更新 [PyPi最新版本](##PyPi最新版本)的版本號
3. Run: 
```
./gitlab_update.sh
```

## PyPi最新版本
```sh
pip install hitrustai-lab==1.0.58
```

## 文件記錄
`路徑: hitrustai-lab/hitrustai_lab/readme`
- 會議記錄
- 部屬環境連結(版本)

## API使用範例
### 1.algorithm
<details>
<summary>1.1 AHP</summary>
<pre><code>
from hitrustai_lab.algorithm.ahp import AHPWeight
ahp_weight = {
    "robot_detection_score": 1,
    "ip_connection_score": 2,
    "internet_info_score": 2,
    "ip_change_score": 3,
    "device_consistency_score": 4,
    "device_connection_score": 5,
    "personal_device_score": 6,
    "bio_behavior_score": 7
}
ahpw = AHPWeight(ahp_weight)
dict_weight = ahpw.output_weight()
dict_weight
</code></pre>
</details>

<details>
<summary>1.2 PCA轉AHP</summary>
<pre><code>
from hitrustai_lab.algorithm.score_translate import pca_to_ahp
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
</code></pre>
</details>

<details>
<summary>1.3 PCA欄位重要度排名</summary>
<pre><code>
from hitrustai_lab.algorithm.score_translate import pca_column_rank
df = pd.read_csv("model_predict.csv")
features = ['device_consistency_score', 'internet_info_score',
            'personal_device_score', 'device_connection_score', 'ip_change_score',
            'ip_connection_score', 'bio_behavior_score', 'robot_detection_score']
x = df.loc[:, features].values
model = PCA(n_components=8)
model.fit(x)
df1 = pca_column_rank(model, features)
</code></pre>
</details>

<details>
<summary>1.4 Total Score 轉 Policy Score</summary>
<pre><code>
from hitrustai_lab.algorithm.score_translate import total_score_to_policy_score
total_score_to_policy_score(0.1)
</code></pre>
</details>

<details>
<summary>1.5 Policy Score轉 Total Score </summary>
<pre><code>
from hitrustai_lab.algorithm.score_translate import policy_score_to_total_score
policy_score_to_total_score(0.1)
</code></pre>
</details>


### 2.Matrix
<!-- <details>
<summary>2.1 透過回歸找尋最佳policy_score以下為1</summary>
<pre><code>
import numpy as np
from hitrustai_lab.matrix.model_matrix import get_best_score
policy_score = np.random.rand(100)
label = np.random.randint(2, size=100)
dict_item = {
    "policy_score" : policy_score,
    "label" : label
}
df = pd.DataFrame(dict_item)
get_best_score(df,"policy_score","label")
</code></pre>
</details> -->

<details>
<summary>2.1 訓練流程所需要的效能指標</summary>

```py
from hitrustai_lab.matrix.model_performance import ModelPerfornance

mp = ModelPerfornance(score_type='policy_score')
list_y_test, list_y_score = mp.model_train()
result = mp.performance_output(list_y_test, list_y_score)
print(result)
```
</details>


### 3.mysql
<details>
<summary>3.1 與DB連線</summary>
<pre><code>
from hitrustai_lab.mysql.connenction_db import open_connection
engine = open_connection(host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test")
sql = 'SELECT * FROM diia_test.deviceinfo' 
engine.execute(sql)
df = pd.read_sql(sql, engine)
engine.close()
</code></pre>
</details>

<details>
<summary>3.2 批次將db裡的資料轉為csv</summary>

<pre><code>
from hitrustai_lab.mysql.get_db_to_csv_batch import DBDownload
db_name = "diia_release"
table = "deviceinfo"
diia = DBDownload(
    db_name=db_name,
    user="root",
    passwd="root16313302",
    host="192.168.10.112",
    port=3305,
    table=table,
    batch_size=10000,
    file_name_csv="new_diia.csv",
    sql_time = "where udid like '154637530395207*%'"
)
sql_cmd = """
    SELECT * FROM %s.%s
""" % (db_name, table)
diia.run(sql_cmd)
print("---成功---")
</code></pre>
</details>


### 4.ORM

<details>
<summary>4.1 初始化orm(必須先做這引用這部分)</summary>
<pre><code>
from hitrustai_lab.orm import Orm
host = '192.168.10.201',
port = '3306',
db = 'acqfd_test'
user = 'acqfd',
pwd = 'acqfd16313302',
orm_profile = get_orm_profile(host=host, port=port, db=diia_db, user=db_user, pwd=db_pwd)
orm = Orm(profile=orm_profile)
</code></pre>
</details>

<details>
<summary>4.1.1 建表</summary>
<pre><code>
from sqlalchemy import Column, text, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata
class TestTable(Base):
    __tablename__ = 'udid_history'
    pk_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    sn = Column(String(120, 'utf8mb4_unicode_ci'), nullable=False)
    name = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    city = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    create_time = Column(TIMESTAMP(fsp=6), nullable=False,
                            server_default=text("CURRENT_TIMESTAMP(6)"))
orm.create_table(Base, TestTable)
print('Create table done.')
</code></pre>
</details>

<details>
<summary>4.1.2 刪除資料</summary>
<pre><code>
data = pd.DataFrame({
    'sn':['test1', 'test2'],
    'name':['John', 'Eric'], 
    'city':['Taipei', 'Tokyo']
})
orm.delete(data, TestTable)
</code></pre>
</details>

<details>
<summary>4.1.3 檢查資料是否存在(by SN)</summary>
<pre><code>
sn = 'test1'
result = orm.check_sn(TestTable.sn, sn)
print(result)
</code></pre>
</details>

<details>
<summary>4.1.4 Query</summary>
<pre><code>
from .Tables.TB3DS import ThreeDS1Detect
'''
參數說明:
1. limit: 要查詢的資料筆數，預設 = None (查全部資料)
2. order_by: 按照指定的欄位排序，預設 = None (不排序)
3. fields: 指定query的欄位，預設 = None (查全部欄位)
4. args: 其他查詢條件
'''  
limit = 10000
order_by = (ThreeDS1Detect.create_time, 'asc')
fields = [
    'create_time', 
    'client_info_id',
    'customer_servertime', 
    'sn', 
    'sp_tx_id', 
    'threeds_type'
]
tb = orm.query_filter(ThreeDS1Detect, limit, order_by, fields)
print(tb)
</code></pre>
</details>

<details>
<summary>4.1.5 Update 資料</summary>
<pre><code>
column_values = {'sn':'test1'}
update_content = {'city':'Los Angeles'}
orm.update(TestTable, column_values, update_content)
</code></pre>
</details>

<details>
<summary>4.1.6 檢查table 是否存在</summary>
<pre><code>
result = orm.check_exist(TestTable)
print(result)
</code></pre>
</details>

<details>
<summary>4.1.7 匯入資料</summary>
<pre><code>
data = pd.DataFrame({
    'sn':['test1', 'test2', 'test3', 'test4', 'test5'],
    'name':['John', 'Eric', 'Steven', 'Bruce', 'Chris'], 
    'city':['Taipei', 'Tokyo', 'Taipei', 'London', 'Liverpool']
})
orm.data_to_DB(data, TestTable)
</code></pre>
</details>

### 5.knoweloge_base
<details>
<summary>5.1 呼叫UA結果</summary>
<pre><code>
from hitrustai_lab.knoweloge_base.call_useranent_so import UserAgentDecoder
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.158 Safari/537.36"
width = "1680"
height = "1050"
ratio = "2"
platform = "iPad"
gpuName = "Apple GPU"
uad = UserAgentDecoder("../include/ua.so")
dict_ua = uad.run(ua, width, height, ratio, platform, gpuName)
print(dict_ua)
</code></pre>
</details>

<details>
<summary>5.2 呼叫mmdb</summary>
<pre><code>
from hitrustai_lab.knoweloge_base.geoip import Geoip
gp = Geoip("./nas/geoip_coordinate_v2.mmdb")
gp.get_diia(ip)
</code></pre>
</details>


### 6.AI訓練流程API
<details>
<summary>6.1訓練流程</summary>
- train不能有參數
- 需去diia專案下載pass.so

```sh
mkdir env
cd env
vi .env
```
.env
```sh
DB_ENGINE=mysql+pymysql
DB_NAME=diiadev
DB_HOST=192.168.10.201
DB_PORT=3306
DB_USERNAME=diia
DB_PASS=6357621dc964d476e0ad88d81b25518e

KAFKA_N=3
KAFKA_HOST_1=192.168.10.201
KAFKA_PORT_1=9092
KAFKA_HOST_2=192.168.10.202
KAFKA_PORT_2=9092
KAFKA_HOST_3=192.168.10.203
KAFKA_PORT_3=9092

SOURCE_PATH_DATASET=./data/dataset/
SOURCE_PATH_KNOWLEDGE=./data/kg/
SOURCE_PATH_LIB=./data/lib/
```

```py
from hitrustai_lab.model_train.ai_module_train import HitrustaiTrainTemple
from hitrustai_lab.algorithm.ahp import AHPWeight
from hitrustai_lab.orm.Tables.TBMarchant import TbMarchatriskValidationReport

path = "../../../nas/Bill/Code - 風險商店模型/即時預測/"
mr = MercahtRisk(file_path='./',
    inputData_Auth=path+'tb_auth_detect_211227_removeUnnecessaryCols.csv',
    inputData_AuthResult=path+'tb_auth_real_result_211227_removeUnnecessaryCols.csv',
    inputData_merchantInfo=path+'merchantInfo_211227_removeUncessaryCols.csv',
    inputData_merchantInfoCleaned=path+'merchantInfoCleaned_211227_removeUncessaryCols.csv', 
    save_path="./data/lib/")


dict_model = {
    "MercahtRisk": mr
}
ahp_weight = {
    "MercahtRisk": 1,
}
ahpw = AHPWeight(ahp_weight)
dict_weight = ahpw.output_weight()
htt = HitrustaiTrainTemple(dict_ahp_weight=dict_weight,dict_model=dict_model, so_name="./data/passwd.so")
manager_dict = htt.train()

tb = TbMarchatriskValidationReport(
    customer_id=htt.mq_info["customer_id"],
    model_id=htt.mq_info["model_id"],
    training_id=htt.mq_info["training_id"],
    source_start_date=htt.train_info["source_end_date"],
    source_end_date=htt.train_info["source_end_date"],
    model_name="mercaht_risk",
    training_sample_count=1000000,
    validation_sample_count=450,
    accuracy=htt.accuracy,
    precision=htt.precision,
    recall=htt.recall,
    f1_score=htt.f1_score,
    marchatrisk_weight=dict_weight["MercahtRisk"],
    marchatrisk_accuracy=manager_dict["MercahtRisk"]["report"]["accuracy"],
    marchatrisk_precision=manager_dict["MercahtRisk"]["report"]["precision"],
    marchatrisk_recall=manager_dict["MercahtRisk"]["report"]["recall"],
    marchatrisk_f1_score=manager_dict["MercahtRisk"]["report"]["f1_score"],
)
htt.orm_to_table(tb, manager_dict)
```

</details>
<details>
<summary>6.2 訓練常用的工具(效能指標,變數存取,排錯api)</summary>

```py
from hitrustai_lab.model_train.core.utils import AITrainUtilsAPI

class MyTrain(AITrainUtilsAPI):
    def train(self):
        try:
            ...
        except Exception as e:
            errMsg = self.err_reason(e)
            self.report("9909", reason="Fraud Detect-" + errMsg)

        # 存取變數
        self.save_variable((變數1,變數2), save_path + 'myself.pkl')
        # 讀取變數
        val = self.load_variavle(save_path + 'myself.pkl')
        result = self.confuse_classification_report(df['true_label'], df['predict_label'])

```
</details>


### 7.AI資料統計數據展示
<details>
<summary>7.1 偽冒偵測</summary>

#### 下載資料請參照3.2

```py
from hitrustai_lab.analysis.data_statistical_analyse import DataAnalyse

da = DataAnalyse()
da.read_fraud()
da.data_analyse()
da.df_all['UDID'] = da.df_all['UDID'].astype(str)
with pd.ExcelWriter('Courses.xlsx') as writer:
    da.df_all.to_excel(writer, sheet_name='異常')
    da.intersected_df_normal.to_excel(writer, sheet_name='正常')

```
</details>

### 8.Log
<details>
<summary>Log api</summary>

| 層級     | 說明                                              | 備註                                |
| -------- | ------------------------------------------------- | ----------------------------------- |
| DEBUG    | 詳細資訊, 除錯用                                  |                                     |
| INFO     | 警告。可用表示即將或已經發生的意外,但服務仍可運行 |                                     |
| ERROR    | 嚴重bug, 服務某些功能無法正常運行                 | *debug模式下會打印詳細traceback log |
| CRITICAL | 嚴重錯誤, 程序已不能正常運行                      | *debug模式下會打印詳細traceback log |


```py
from hitrustai_lab.log.log_handler import LogHandler

log_handler = LogHandler(service='CardTesting')
init_logger = log_handler.getlogger('INIT')
init_logger.info("success log")

log_handler.service = "set1"
log_handler.log_level = "ERROR" 
log_handler.set_logging()
init_logger = log_handler.getlogger('INIT')
init_logger.error("success log")
```
</details>


### 9.訓練流程API

<details>
<summary>9.1 訓練模型的效能指標送入DB</summary>

- `dict_add_column是新增欄位,如果沒有需要新增可以不帶入tmts.insert_db`
```py
from hitrustai_lab.model_train.ai_module_train import TrainModelToSQl
dict_add_column = {
    "add_column1": Column("add_column1", Integer, primary_key=True),
    "add_column2": Column("add_column2", Integer, primary_key=True)
}
dict_init_arg["add_column1"] = 0
dict_init_arg["add_column2"] = 0

tmts = TrainModelToSQl(
    host="192.168.10.203",
    port="3305",
    user="diia",
    passwd="diia16313302",
    db="service_report",
    table_name="test111111"
)

tmts.insert_db(data=dict_init_arg, dict_add_column=dict_add_column)
```
</details>

<details>
<summary>9.2 訓練流程模板套用</summary>

`env/.env`
```bash
# ENV_METHOD=apollo
ENV_METHOD=env
APOLLO_URL=http://192.168.10.201:18080
APOLLO_APPID=7d8b46de-cffc-4ff8-a077-00858e38d5dc
APOLLO_CLUSTER=default
APOLLO_SECRET=bd384166b0bb4c648679d2b9ef5bb5e0
APOLLO_NAMESPACE_INF=infrastructure
APOLLO_NAMESPACE_MODAL=fraud-detect-train
FILE_PATH= ../../../../nas/bruce/訓練資料/fraud_detect/
SOURCE_PATH_KNOWLEDGE = ./data/kg/
SOURCE_PATH_LIB = ./data/lib/

# CUSTOMER_ID = 001584054110001
# tag = 20220623000905
# PROFILE_ID = A01
# TRAINING_ID = MD1-F9AD62
MODEL_ID = MD1
BATCH_SIZE = 10000
TRUE_LABEL_COLUMN = resultInfo__trueLabelLast

DB_ENGINE = mysql+pymysql
DB_NAME = service_report
DB_HOST = 192.168.10.203
DB_PORT = 3305
DB_USERNAME = diia
DB_PASS = 6357621dc964d476e0ad88d81b25518e

```

### 訓練模板範例與說明

- `dict_add_column是新增欄位,如果沒有需要新增可以不帶入tmts.insert_db`
- `batch_read_csv_train為批次訓練的api,包括計算訓練時間等等資訊`
- `list_file_name將訓練的文件寫成一個list`
- `features將所需的特徵寫入此`
- `model 目前只支援partial_fit的訓練模式`
```py
from hitrustai_lab.model_train.core.utils import AITrainUtilsAPI
from hitrustai_lab.model_train.ai_module_train import HitrustaiTrainTemple
class ProjectName(AITrainUtilsAPI):
    def __init__(self, file_path="../../Python/ai_model_status/data/", save_path="data/lib/"):
        self.file_path = file_path
        self.save_path = save_path
    。
    。
    。
    def train(self, chunksize=100000, true_lable_name="resultInfo__trueLabelAuth"):
        self.true_lable_name = true_lable_name
        model = IncrementalPCA(n_components=feature_number)
        model = self.batch_read_csv_train(model, self.file_path, features, chunksize)
        。。。
        return self.report("xxxx", reason="...")

def main():
    file_path = "../../../../nas/bruce/訓練資料/"
    pn = ProjectName(file_path=file_path)
    htt = HitrustaiTrainTemple(dict_model=pn, so_name="./lib/passwd.so", init_logger=init_logger, model_name="FraudDetect")
    try:
        htt.train()
        htt.dict_init_arg["list_y_score"] = np.array(htt.dict_model.df["total_score_fd7"])
    except Exception:
        pass
    dict_add_column7 = {
        "personal_device_score": Column("personal_device_score", FLOAT),
    }
    htt.dict_init_arg["personal_device_score"] = htt.dict_model.w7["personal_device_score"]
    htt.insert_db(table_name="test111111",  dict_add_column=dict_add_column7)
    htt.output_txt( model_name="Fraud Detect", path='./data/lib/output.txt')
```
</details>
