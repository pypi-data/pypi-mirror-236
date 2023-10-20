'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Question Answering Service
-----------------------------------------------------
'''
import typing as t
from .service_io import ServiceIO
from ..constants import ServiceString


class QuestionAnsweringIO(ServiceIO):
    service = ServiceString.QUESTION_ANSWERING
    required_input_fields = ["message"]
    optional_input_fields = ["document_text","document_ids","check_ambiguity","check_query_type","generic_response","meta","message_id"]
    input_structure = {
        "message": str, 
        "document_text": str, 
        "document_ids": list, 
        "check_ambiguity": bool, 
        "check_query_type": bool, 
        "generic_response": bool, 
        "meta": dict, 
        "message_id": str
    }

    output_structure = {
        "message_id": str,
        "answer": str,
        "context": str,
        "valid_query": bool,
        "no_answer": bool,
        "highlights": dict,
        "passages": dict
    }


    @classmethod
    def special_validation(self, payload):
        
        document_text: t.Optional[str] = payload.get('document_text')
        document_ids: t.Optional[t.List[str]] = payload.get('document_ids')
        client_id: t.Optional[str] = payload.get('client_id')

        # Validate only 1 of the 3 document fields are supplied.
        if sum(
            0 if document_field is None else 1
            for document_field in [document_text, document_ids]
        ) != 1:
            return False, 'Only 1 of document_text, document_ids must be provided.'

        # Validate all ids are provided.
        if document_ids is not None:
            if client_id is None:
                return False, 'client_id required'

        return super().special_validation(payload)