'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Table Get Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableGetService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_GET
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str) -> dict:
        '''
        Call the Table Get Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :return: tables: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_get.py>`_
        '''
        return super().__call__(user=user)

    def set_input_configs(self, name:str):
        super().set_input_configs(name=name)

    @classmethod
    def call(self, user:str) -> dict:
        '''
        Call the Table Get Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :return: tables: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_get.py>`_
        '''
        return super().call(user=user)

