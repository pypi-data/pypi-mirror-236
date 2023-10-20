'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use Question Answering Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union



class QuestionAnsweringService(SoffosAIService):
    '''
    This module is a combination of various sub-modules that enable users to get
    accurate answers on questions posed on a large amount of content. It includes
    basic intent recognition capabilities to enable appropriate responses to
    incorrect or profane language, or typical personal questions like "How are
    you?" and greetings.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.QUESTION_ANSWERING
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, question:str, document_text:str=None, document_ids:list=None, check_ambiguity:bool=True, check_query_type:bool=True, generic_response:bool=None, meta:dict=None, message_id:str=None) -> dict:
        '''
        Call the Question Answering Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param question: A natural language query/question.
        :param document_text: The text to be used as the context to formulate the answer.
        :param document_ids: A list of unique IDs referencing pre-ingested documents to be used as the
            context to formulate the answer.
        :param check_ambiguity: None
        :param check_query_type: None
        :param generic_response: None
        :param meta: None
        :param message_id: None
        :return: message_id: None
        answer: None
        context: None
        valid_query: None
        no_answer: None
        highlights: None
        passages: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/question_answering.py>`_
        '''
        return super().__call__(user=user, question=question, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)

    def set_input_configs(self, name:str, question:Union[str, InputConfig], document_text:Union[str, InputConfig]=None, document_ids:Union[list, InputConfig]=None, check_ambiguity:Union[bool, InputConfig]=True, check_query_type:Union[bool, InputConfig]=True, generic_response:Union[bool, InputConfig]=None, meta:Union[dict, InputConfig]=None, message_id:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, question=question, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)

    @classmethod
    def call(self, user:str, question:str, document_text:str=None, document_ids:list=None, check_ambiguity:bool=True, check_query_type:bool=True, generic_response:bool=None, meta:dict=None, message_id:str=None) -> dict:
        '''
        Call the Question Answering Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param question: A natural language query/question.
        :param document_text: The text to be used as the context to formulate the answer.
        :param document_ids: A list of unique IDs referencing pre-ingested documents to be used as the
            context to formulate the answer.
        :param check_ambiguity: None
        :param check_query_type: None
        :param generic_response: None
        :param meta: None
        :param message_id: None
        :return: message_id: None
        answer: None
        context: None
        valid_query: None
        no_answer: None
        highlights: None
        passages: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/question_answering.py>`_
        '''
        return super().call(user=user, question=question, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)

