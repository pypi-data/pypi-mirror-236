'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Answer Scoring Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class AnswerScoringIO(ServiceIO):
    service = ServiceString.ANSWER_SCORING
    required_input_fields = ["context","question","user_answer"]
    optional_input_fields = ["answer"]
    input_structure = {
        "context": str, 
        "question": str, 
        "answer": str, 
        "user_answer": str
    }

    output_structure = {
        "score": float,
        "reasoning": str
    }

