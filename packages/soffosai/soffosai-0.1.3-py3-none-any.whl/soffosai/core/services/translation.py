'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Translation Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TranslationService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TRANSLATION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, auto_detect:bool=True, source_language_code:str=None, target_language_code:str=None) -> dict:
        '''
        Call the Translation Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Missing Documentation
        :param auto_detect: Missing Documentation
        :param source_language_code: Missing Documentation
        :param target_language_code: Missing Documentation
        :return: target_language_code: Missing Documentation
        translation: Missing Documentation
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/translation.py>`_
        '''
        return super().__call__(user=user, text=text, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], auto_detect:Union[bool, InputConfig]=None, source_language_code:Union[str, InputConfig]=None, target_language_code:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)

    @classmethod
    def call(self, user:str, text:str, auto_detect:bool=None, source_language_code:str=None, target_language_code:str=None) -> dict:
        '''
        Call the Translation Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Missing Documentation
        :param auto_detect: Missing Documentation
        :param source_language_code: Missing Documentation
        :param target_language_code: Missing Documentation
        :return: target_language_code: Missing Documentation
        translation: Missing Documentation
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/translation.py>`_
        '''
        return super().call(user=user, text=text, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)

