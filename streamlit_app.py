"""Learning Engilish with LLM by arman espiar"""

import asyncio
from typing import Final, Optional
import streamlit as st
import dt_llm_utility
import learning_english_constants
from dt_utility import format_seconds
from dtx_ollama import (
    chat,
    MODEL_NAME_OFFLINE,
)
from dt_tts_edge import (
    convert_text_to_speech_async,
    VOICES_FEMALE,
)
from dt_audio_player import play_audio_file
from ae_remove_temp_files import clear_root_folder


__version__: Final[str] = "2.0.0"
VERSION: Final[str] = __version__

clear_root_folder()

st.set_page_config(
    # layout="wide",
    page_icon="🤖",
    page_title="Learning english with LLM",
)
st.title(body="یادگیری انگلیسی و تقویت فارسی با هوش مصنوعی 🤖")


user_prompt: str = st.text_input(
    icon="🧑",
    label="متن فارسی",
    placeholder="لطفا متن فارسی خود را اینجا بنویسید و سپس دکمه Enter را فشار دهید.",
)

user_prompt = user_prompt.strip()

if user_prompt:
    messages: list[dict] = []

    SYSTEM_MESSAGE: dict = {
        dt_llm_utility.KEY_NAME_ROLE: dt_llm_utility.ROLE_SYSTEM,
        dt_llm_utility.KEY_NAME_CONTENT: learning_english_constants.SYSTEM_PROMPT,
    }
    messages.append(SYSTEM_MESSAGE)

    user_message: dict = {
        dt_llm_utility.KEY_NAME_ROLE: dt_llm_utility.ROLE_USER,
        dt_llm_utility.KEY_NAME_CONTENT: user_prompt,
    }

    messages.append(user_message)

    response, completion_tokens, prompt_tokens = chat(
        model_name=MODEL_NAME_OFFLINE,
        messages=messages,
        temperature=0.0,
    )

    assistant_answer: Optional[str] = response

    if assistant_answer:

        paragraphs: list[str] = assistant_answer.split(
            sep="English Translation", maxsplit=2
        )
        fa_text: str = paragraphs[0]
        en_text: str = paragraphs[1]

        AUTDIO_PATH_FA: str = "./temp/speech_fa.mp3"
        AUTDIO_PATH_EN: str = "./temp/speech_en.mp3"

        with st.container(border=True):
            st.write(assistant_answer)
            st.divider()
            st.write(f"تعداد توکن های ورودی {prompt_tokens}")
            st.write(f"تعداد توکن های خروجی {completion_tokens}")
            st.write(f"تعداد کل توکن ها {completion_tokens + prompt_tokens}")

            Play: bool = st.button(label="Play Audio", icon="▶️")
            if Play:
                word_count_fa, elapsed_time_fa = asyncio.run(
                    convert_text_to_speech_async(
                        text=fa_text,
                        rate="-2%",
                        audio_file_path=AUTDIO_PATH_FA,
                    )
                )
                word_count_en, elapsed_time_en = asyncio.run(
                    convert_text_to_speech_async(
                        text=en_text,
                        rate="-3%",
                        audio_file_path=AUTDIO_PATH_EN,
                        voice=VOICES_FEMALE[1],
                    )
                )

                st.divider()

                st.write(
                    f"تعداد کلمات فارسی {word_count_fa} و مدت زمان ساخت {format_seconds(elapsed_time_fa)} (ثانیه)."
                )
                st.write(
                    f"تعداد کلمات انگلیسی {word_count_en} و مدت زمان ساخت {format_seconds(elapsed_time_en)} (ثانیه)."
                )

                play_audio_file(filename=AUTDIO_PATH_FA)
                play_audio_file(filename=AUTDIO_PATH_EN)
