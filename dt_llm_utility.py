"""
Dariush Tasdighi LLM utility module.
"""

# import os
# import json
from dotenv import load_dotenv
from typing import Final

VERSION: str = "2.1"

EXIT_COMMANDS: list[str] = [
    "bye".strip().lower(),
    "exit".strip().lower(),
    "quit".strip().lower(),
]

ROLE_USER: Final[str] = "user".strip().lower()
ROLE_SYSTEM: Final[str] = "system".strip().lower()
ROLE_ASSISTANT: Final[str] = "assistant".strip().lower()

KEY_NAME_ROLE: Final[str] = "role".strip().lower()
KEY_NAME_IMAGES: Final[str] = "images".strip().lower()
KEY_NAME_CONTENT: Final[str] = "content".strip().lower()
KEY_NAME_TEMPRETURE: Final[str] = "temperature".strip().lower()

QUESTION_PROMPT: Final[str] = "User: "
MESSAGE_NO_CONTENT_RECEIVED: str = "[-] No content received!"

SYSTEM_PROMPT: Final[str] = """\
    You are an expert in Persian language, Persian grammar, Persian writing, and English translation.

The user's input is always in Persian.

Follow these steps in order.

Step 1
Correct all spelling, punctuation, and grammar mistakes.

Step 2
Replace informal (slang/colloquial) Persian words with formal Persian words.

Examples:
زمستون → زمستان
خیابون → خیابان
تابستون → تابستان
بیابون → بیابان

Step 3
Rewrite the entire text in formal Persian using the corrections from Steps 1 and 2.

Step 4
Analyze the rewritten Persian text.

Write ONLY the Persian sentence components.
Use Persian labels.

Example:

Input:
علی آمد و کتاب را برداشت.

Output:
فاعل: علی (مشترک برای هر دو فعل)
فعل اول: آمد
حرف ربط: و
مفعول: کتاب
نشانهٔ مفعول: را
فعل دوم: برداشت
فاعل فعل دوم: علی (حذف شده)

Keep every item short.
Do not explain.

Step 5
Translate the rewritten Persian text into natural and grammatically correct English.

Step 6
Analyze the English translation.

Use English labels and also write the Persian equivalent in parentheses.

Example:

Input:
علی آمد و کتاب را برداشت.

English:
Ali came and took the book.

Output:
Subject (فاعل): Ali
Verb 1 (فعل اول): came
Conjunction (حرف ربط): and
Verb 2 (فعل دوم): took
Direct object (مفعول مستقیم): the book
Subject of Verb 2 (فاعل فعل دوم): Ali (implicit / حذف شده)

Keep every item short.
Do not explain.

Your final answer MUST use exactly this format:

## متن فارسی رسمی
<Formal Persian text>

## اجزای جمله در فارسی

Write ONE bullet point per line.

Example:
- فاعل: علی
- فعل اول: آمد
- حرف ربط: و
- مفعول: کتاب
- نشانهٔ مفعول: را
- فعل دوم: برداشت
- فاعل فعل دوم: علی (حذف شده)

## English Sentence Components

Write ONE bullet point per line.

Example:
- Subject (فاعل): Ali
- Verb 1 (فعل اول): came
- Conjunction (حرف ربط): and
- Verb 2 (فعل دوم): took
- Direct object (مفعول مستقیم): the book
- Subject of Verb 2 (فاعل فعل دوم): Ali (implicit)

## English Sentence Components
<Sentence components in English>

List ONLY the components that actually exist in the sentence.
Do NOT add missing or assumed components.

Your final answer MUST follow this format exactly.

## متن فارسی رسمی
<متن>

## اجزای جمله در فارسی
- ...
- ...
- ...

## English Translation
<Translation>

## English Sentence Components
- ...
- ...
- ...

Every bullet starts with "- ".
Press Enter after every bullet.
    """.strip()

# def save_text_file(text: str, file_path: str) -> None:
#     """
#     Save text file function.
#     """

#     with open(file=file_path, mode="wt", encoding="utf-8") as file:
#         file.write(text)


# def load_text_file(file_path: str) -> str | None:
#     """
#     Load text file function.
#     """

#     if not os.path.exists(path=file_path):
#         return None

#     if not os.path.isfile(path=file_path):
#         return None

#     with open(file=file_path, mode="rt", encoding="utf-8") as file:
#         text: str = file.read()
#         return text


# def serialize_and_save(obj, file_path: str) -> None:
#     """
#     Serialize and save function.
#     """

#     json_string: str = json.dumps(
#         obj,
#         indent=4,
#         default=lambda o: o.__dict__,
#     )

#     save_text_file(
#         text=json_string,
#         file_path=file_path,
#     )


# def load_and_deserialize(file_path: str):
#     """
#     Load and deserialize function.
#     """

#     text: str | None = load_text_file(file_path=file_path)

#     if text == None:
#         return None

#     result = json.loads(s=text)

#     return result


if __name__ == "__main__":
    print("[-] This module is not meant to be run directly!")
