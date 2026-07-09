"""list of offline models"""
import ollama
from ollama import ListResponse

def offline_models_list()-> list[str]:
    """total offline models"""
    ollama_list: ListResponse = ollama.list()
    models = ollama_list.models

    model_names: list[str] = []
    for model_item in models:
        if model_item.model:
            model_names.append(model_item.model)
    model_names.sort()
    return model_names
