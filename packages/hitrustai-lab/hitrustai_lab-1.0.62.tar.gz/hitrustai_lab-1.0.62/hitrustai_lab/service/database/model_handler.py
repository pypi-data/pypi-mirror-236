

class ModelHandler:
    def __init__(self, db, table_info, table_result, logger):
        self.db = db
        self.info = table_info
        self.result = table_result
        self.logger = logger

    def save_data(self, data_type='info', **input_data):
        try:
            if data_type == 'info':
                input_model = self.info(**input_data)
            else:
                input_model = self.result(**input_data)

            self.db.session.add(input_model)
            self.db.session.commit()
            return input_model

        except:
            self.db.session.rollback()
            self.logger.exception(
                f"[{input_model.serial_number}]Save data into {input_model.__tablename__} failed")
