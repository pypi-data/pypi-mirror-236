'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Table Delete Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableDeleteService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_DELETE
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, table_ids:list) -> dict:
        '''
        Call the Table Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param table_ids: None
        :return: success: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_delete.py>`_
        '''
        return super().__call__(user=user, table_ids=table_ids)

    def set_input_configs(self, name:str, table_ids:Union[list, InputConfig]):
        super().set_input_configs(name=name, table_ids=table_ids)

    @classmethod
    def call(self, user:str, table_ids:list) -> dict:
        '''
        Call the Table Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param table_ids: None
        :return: success: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_delete.py>`_
        '''
        return super().call(user=user, table_ids=table_ids)

