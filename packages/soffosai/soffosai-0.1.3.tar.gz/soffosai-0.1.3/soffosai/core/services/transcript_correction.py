'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Transcript Correction Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TranscriptCorrectionService(SoffosAIService):
    '''
    This module cleans up and corrects poorly transcribed text from Speech-To-Text
    (STT) systems. It can handle cases where STT produced the wrong word or phrase
    by taking into account the surrounding context and choosing the most fitting
    replacement. Although this is meant for correcting STT outpus, it can also be
    used to correct grammar, misspellings and syntactical errors.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TRANSCRIPT_CORRECTION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str) -> dict:
        '''
        Call the Transcript Correction Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Text to be corrected.
        :return: corrected: Corrected text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/transcript_correction.py>`_
        '''
        return super().__call__(user=user, text=text)

    def set_input_configs(self, name:str, text:Union[str, InputConfig]):
        super().set_input_configs(name=name, text=text)

    @classmethod
    def call(self, user:str, text:str) -> dict:
        '''
        Call the Transcript Correction Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Text to be corrected.
        :return: corrected: Corrected text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/transcript_correction.py>`_
        '''
        return super().call(user=user, text=text)

