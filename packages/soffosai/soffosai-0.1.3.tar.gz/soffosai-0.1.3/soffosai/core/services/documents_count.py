'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Documents Count Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union



class DocumentsCountService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DOCUMENTS_COUNT
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param filters: None
        :param date_from: None
        :param date_until: None
        :return: documents: None
        count: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_count.py>`_
        '''
        return super().__call__(user=user, filters=filters, date_from=date_from, date_until=date_until)

    def set_input_configs(self, name:str, filters:Union[dict, InputConfig]=None, date_from:Union[str, InputConfig]=None, date_until:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, filters=filters, date_from=date_from, date_until=date_until)

    @classmethod
    def call(self, user:str, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param filters: None
        :param date_from: None
        :param date_until: None
        :return: documents: None
        count: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_count.py>`_
        '''
        return super().call(user=user, filters=filters, date_from=date_from, date_until=date_until)

