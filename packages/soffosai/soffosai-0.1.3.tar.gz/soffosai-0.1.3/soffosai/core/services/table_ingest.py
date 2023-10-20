'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Table Ingest Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableIngestService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_INGEST
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, table:list, document_name:str, description:str) -> dict:
        '''
        Call the Table Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param table: None
        :param document_name: None
        :param description: None
        :return: table_id: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_ingest.py>`_
        '''
        return super().__call__(user=user, table=table, document_name=document_name, description=description)

    def set_input_configs(self, name:str, table:Union[list, InputConfig], document_name:Union[str, InputConfig], description:Union[str, InputConfig]):
        super().set_input_configs(name=name, table=table, document_name=document_name, description=description)

    @classmethod
    def call(self, user:str, table:list, document_name:str, description:str) -> dict:
        '''
        Call the Table Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param table: None
        :param document_name: None
        :param description: None
        :return: table_id: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_ingest.py>`_
        '''
        return super().call(user=user, table=table, document_name=document_name, description=description)

