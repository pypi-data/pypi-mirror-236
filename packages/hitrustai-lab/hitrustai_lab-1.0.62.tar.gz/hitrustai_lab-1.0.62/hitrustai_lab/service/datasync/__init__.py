import json
import pytz
import grpc
import decimal
import datetime

from . import datasync_pb2, datasync_pb2_grpc
from ..database.model_handler import ModelHandler


class DateEncoder(json.JSONEncoder):
    """
    自定义类，解决报错：
    TypeError: Object of type "datetime" is not JSON serializable
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.astimezone(pytz.UTC).strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class DataSyncHandler:
    def __init__(
            self, 
            db_settings: dict, 
            datasync_config: dict,
            logger
        ) -> None:
        self.DB_NAME = db_settings.get('db_name')
        self.DATASYNC_DATASOURCE = datasync_config.get('datasource')
        self.DATASYNC_USE = datasync_config.get('datasync_use')
        self.logger = logger
        self.db_handler = ModelHandler(
            db=db_settings.get('db'), 
            table_info=db_settings.get('table_info'), 
            table_result=db_settings.get('table_result'),
            logger=logger
        )

        self.channel = grpc.insecure_channel(datasync_config.get('grpc_domain'))
        self.stub = datasync_pb2_grpc.DataSyncStub(self.channel)
        
        
    def datasync_func(self, data, pk_id=0):
        if self.DATASYNC_USE != 'true':
            return None

        try:
            output = dict()
            output["data_source"] = self.DATASYNC_DATASOURCE
            output["schema"] = self.DB_NAME
            output["table"] = data.__tablename__
            output["payload"] = {x.name: getattr(data, x.name) for x in data.__table__.columns}
            output["pk_id"] = pk_id

            request = datasync_pb2.DataSyncRequest(value=json.dumps(output, cls=DateEncoder))
            response = self.stub.DataSync(request)
            response = json.loads(response.value)
            self.logger.info(
                f'[{data.serial_number}]DataSync {data.__tablename__} Result: {response["reason"][0]}')

        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                self.logger.error(
                    f"[{data.serial_number}]DataSync Catch an exception: DataSync Status Canceled")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                self.logger.error(
                    f"[{data.serial_number}]DataSync Catch an exception: DataSync Connection Unavaliable")

        except:
            self.logger.exception(f"[{data.serial_number}]DataSync Catch an exception:")


    def save_data_and_sync(self, data_type='info', pk_id=None, **data):
        datasync_content = self.db_handler.save_data(data_type, **data)

        if datasync_content:
            if data_type == 'info':
                info_PKID = datasync_content.pk_id
                self.datasync_func(datasync_content, pk_id=info_PKID)
                return info_PKID
            else:
                self.datasync_func(datasync_content, pk_id=pk_id)
                return pk_id

