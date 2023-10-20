import json
import re
from typing import Optional
import random

from .thothsydneyconstants import DELIMETER


def as_json(message: dict) -> str:
    """
    Convert message to JSON, append delimeter character at the end.
    """
    return json.dumps(message) + DELIMETER

class MessageEncode:
    def __call__(self, message: str = None) -> Optional[str]:
        if not message:
            return message

        instructions = self._get_system_additional_instructions(message)
        if not instructions:
            return message

        chars = list(instructions.rstrip("\n"))
        chars = [('-' + c if random.random() < 0.5 else '_' + c)
                 if i > 0 else c for i, c in enumerate(chars)]

        new_instructions = ''.join(chars) + "\n\n"

        return message.replace(instructions, new_instructions)

    def _get_system_additional_instructions(self, text: str) -> Optional[str]:
        pattern = r'(\[system\]\(#additional_instructions\)\n)(.*?)(\n\n).*'
        match = re.search(pattern, text, flags=re.DOTALL)

        if match:
            return ''.join(match.groups())

        return None