'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Search Recommendations Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union



class SearchRecommendationsService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.SEARCH_RECOMMENDATIONS
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, document_ids:list) -> dict:
        '''
        Call the Search Recommendations Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: None
        :param document_ids: None
        :return: recommendations: None
        recommendations_no_info: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/search_recommendations.py>`_
        '''
        return super().__call__(user=user, text=text, document_ids=document_ids)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], document_ids:Union[list, InputConfig]):
        super().set_input_configs(name=name, text=text, document_ids=document_ids)

    @classmethod
    def call(self, user:str, text:str, document_ids:list) -> dict:
        '''
        Call the Search Recommendations Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: None
        :param document_ids: None
        :return: recommendations: None
        recommendations_no_info: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/search_recommendations.py>`_
        '''
        return super().call(user=user, text=text, document_ids=document_ids)

