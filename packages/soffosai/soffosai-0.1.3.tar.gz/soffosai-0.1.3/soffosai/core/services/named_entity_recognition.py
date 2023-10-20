'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Easily use N E R Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union



class NERService(SoffosAIService):
    '''
    Identifies named entities in text. It supports custom labels. Below are the
    default entities and their labels: | tag | type | | ----------- |
    -------------------- | | CARDINAL | cardinal value | | DATE | date value | |
    EVENT | event name | | FAC | building name | | GPE | geo-political entity | |
    LANGUAGE | language name | | LAW | law name | | LOC | location name | | MONEY |
    money name | | NORP | affiliation | | ORDINAL | ordinal value | | ORG |
    organization name | | PERCENT | percent value | | PERSON | person name | |
    PRODUCT | product name | | QUANTITY | quantity value | | TIME | time value | |
    WORK_OF_ART | name of work of art | However, this module is extremely versatile
    as the labels can be defined by the user. See the below example on how this can
    be applied to a medical use-case.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.N_E_R
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, labels:dict=None) -> dict:
        '''
        Call the N E R Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Input text to be analyzed for named entities.
        :param labels: When providing labels, the module will extract entities that match your
            labels and descriptions. This gives enough flexibility to deal with any
            use-case.
        :return: named_entities: A list of dictionaries representing identified named entities. Each
            dictionary contains the following fields: text: The text of the entity.
            tag: Label of the entity. span: A list with the start and end offset of
            the entity in the original text.
        entity_counts: A list of dictionaries with entities and their counts. The dictionaries
            contain the following fields: text: The name of the entity. tag: Label of
            the entity. count: Number of occurrences of the entity in the text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/named_entity_recognition.py>`_
        '''
        return super().__call__(user=user, text=text, labels=labels)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], labels:Union[dict, InputConfig]=None):
        super().set_input_configs(name=name, text=text, labels=labels)

    @classmethod
    def call(self, user:str, text:str, labels:dict=None) -> dict:
        '''
        Call the N E R Service
        
        :param user: The ID of the user accessing the Soffos API.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        
        :param text: Input text to be analyzed for named entities.
        :param labels: When providing labels, the module will extract entities that match your
            labels and descriptions. This gives enough flexibility to deal with any
            use-case.
        :return: named_entities: A list of dictionaries representing identified named entities. Each
            dictionary contains the following fields: text: The text of the entity.
            tag: Label of the entity. span: A list with the start and end offset of
            the entity in the original text.
        entity_counts: A list of dictionaries with entities and their counts. The dictionaries
            contain the following fields: text: The name of the entity. tag: Label of
            the entity. count: Number of occurrences of the entity in the text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/named_entity_recognition.py>`_
        '''
        return super().call(user=user, text=text, labels=labels)

