return_code = {
    
    'Success': '4001',                  # API調用成功
    'SaveSuccess': '4002',              # 資料儲存成功
    'PredictSucess': '4003',            # 模型預測成功
    'ServiceRegisterSuccess': '4004',   # 服務註冊成功
    'TaskAssignSuccess': '4005',        # 排成建立成功
    'ServiceStart': '4006',             # 服務啟動成功
    'TrainFinished': '4007',            # 模型訓練完成
    'TrainInProgress': '4008',          # 模型訓練進行中

    'InvalidAPIKey': '0101',            # API key為空
    'InvalidInput': '0102',             # 輸入資料格式錯誤
    'MacInvalid': '0103',               # mac 無法取得
    'TimeStampInvalid': '0104',         # timestamp 無法取得
    'RequiredFieldsEmpty': '0105',      # 必要欄位為空值

    'ValidationFailed': '9903',         # mac 驗證失敗
    'ModelBuildFailed': '9904',         # 模型啟動失敗
    'PredictFailed': '9905',            # 模型預測失敗
    'ServiceRegisterFailed': '9906',    # 服務註冊失敗
    'ServiceStartFailed': '9908',       # 服務啟動失敗
    'TrainFailed': '9909',              # 模型訓練失敗
    'StopRetry': '9910',                # 終止重複執行
    'DatabaseError':'9923',            # DB Error
    'RedisConnectionError': '9924',     # Redis連線失敗
    'CodisConnectionError': '9925',     # Codis連線失敗

    'InidentifyInput': '2001',          # 無法識別資料
    'SystemError': '9999'               # 系統錯誤
    
}