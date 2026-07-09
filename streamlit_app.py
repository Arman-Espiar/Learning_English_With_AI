"""Learning Engilish with LLM by arman espiar"""

import asyncio
from typing import Final, Optional
import streamlit as st
import time
import dt_llm_utility
import learning_english_constants
from dt_utility import format_seconds
from dtx_ollama import chat

from dt_tts_edge import (
    convert_text_to_speech_async,
    VOICES_FEMALE,
)
from dt_audio_player import play_audio_file
from ae_remove_temp_files import clear_root_folder
from ae_show_offline_models import offline_models_list

__version__: Final[str] = "3.0.0"
VERSION: Final[str] = __version__

clear_root_folder()

st.set_page_config(
    # layout="wide",
    page_icon="🤖",
    page_title="Learning english with LLM",
)

st.markdown(
    body=learning_english_constants.STREAMLIT_STYLE,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("تنظیمات", divider="rainbow")

    model_names = offline_models_list()

    if (
        "selected_model" not in st.session_state
        or st.session_state.selected_model not in model_names
    ):
        st.session_state.selected_model = model_names[0] if model_names else None

    selected_model = st.selectbox(
        "Model",
        options=model_names,
        key="selected_model",
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

    response, completion_tokens, prompt_tokens, elapsed_time = chat(
        model_name=selected_model,
        messages=messages,
        temperature=0.0,
    )

    assistant_answer: Optional[str] = response

    if assistant_answer:

        fa_text, en_text = assistant_answer.split(
            "### 🌐 English Translation\n\n", maxsplit=1
        )

        fa_text = fa_text.strip()
        en_text = en_text.strip()

        AUTDIO_PATH_FA: str = "./temp/speech_fa.mp3"
        AUTDIO_PATH_EN: str = "./temp/speech_en.mp3"

        with st.container(border=True):
            st.write(fa_text)
            st.markdown(
                """
                <h3 dir="ltr" style="text-align:left;">
                    🌐 English Translation
                </h3>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div dir="ltr">{en_text}</div>',
                unsafe_allow_html=True,
            )
            st.divider()
            st.write(f"تعداد توکن های ورودی {prompt_tokens}")
            st.write(f"تعداد توکن های خروجی {completion_tokens}")
            st.write(f"تعداد کل توکن ها {completion_tokens + prompt_tokens}")
            st.write(
                f"زمان صرف شده برای تولید پاسخ: {format_seconds(elapsed_time)} (ثانیه)."
            )

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

                start_time_voice: float = time.perf_counter()
                play_audio_file(filename=AUTDIO_PATH_FA)
                play_audio_file(filename=AUTDIO_PATH_EN)
                end_time_voice: float = time.perf_counter()
                elapsed_time_voice: float = end_time_voice - start_time_voice
                st.write(
                    f"زمان صرف شده برای صدا: {format_seconds(elapsed_time)} (ثانیه)."
                )
