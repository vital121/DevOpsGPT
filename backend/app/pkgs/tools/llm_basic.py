import threading
import time
import openai
from app.pkgs.tools.llm_interface import LLMInterface
from config import LLM_MODEL, LLM_MODEL4
from config import GPT_KEYS

api_keys = GPT_KEYS

api_key_index = 0
provider_index = 0
lock = threading.Lock()

def get_next_api_key():
    print("get_next_api_key:", flush=True)
    print(api_keys, flush=True)
    global api_key_index, provider_index
    current_time = int(time.time())
    with lock:
        provider = list(api_keys.keys())[provider_index]
        provider_data = api_keys[provider]
        keys = provider_data["keys"]
        key_data = keys[api_key_index]
        key = list(key_data.keys())[0]
        if current_time - key_data[key]["timestamp"] >= 80:
            key_data[key]["count"] = 0
            key_data[key]["timestamp"] = current_time
            api_key_index = (api_key_index + 1) % len(keys)
            if api_key_index == 0:
                provider_index = (provider_index + 1) % len(api_keys)
            return provider_data, key
        elif key_data[key]["count"] < 2:
            key_data[key]["count"] += 1
            api_key_index = (api_key_index + 1) % len(keys)
            if api_key_index == 0:
                provider_index = (provider_index + 1) % len(api_keys)
            return provider_data, key
    time.sleep(80)
    return get_next_api_key()

class LLMBase(LLMInterface):
    def __init__(self, usegpt4=False):
        self.model = LLM_MODEL4 if usegpt4 else LLM_MODEL
        self.max_tokens = 8191 if usegpt4 else 10000
        
    def chatCompletion(self, context):
        print("chartGPT - message:", flush=True)
        print(context, flush=True)
        provider_data, key = get_next_api_key()
        
        openai.api_key = key
        openai.api_type = provider_data["api_type"]
        openai.api_base = provider_data["api_base"]
        openai.api_version = provider_data["api_version"]
        print("chartGPT - get api key:"+openai.api_key, flush=True)

        response = openai.ChatCompletion.create(
            model= self.model,
            deployment_id = provider_data.get("deployment_id", None),
            messages=context,
            max_tokens=self.max_tokens,
            temperature=0,
        )

        response_text = response["choices"][0]["message"]["content"]
        print("chartGPT - response_text:"+response_text, flush=True)
        return response_text, True
