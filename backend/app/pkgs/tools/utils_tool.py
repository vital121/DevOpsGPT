import json
import re

from app.pkgs.tools.llm import chatCompletion


def detect_programming_language(file_path):
    file_extension = file_path.split('.')[-1]

    language_extensions = {
        'Python': ['py'],
        'JavaScript': ['js'],
        'Java': ['java'],
        'C++': ['cpp', 'cxx', 'cc'],
        'C': ['c'],
        'Ruby': ['rb'],
        'Go': ['go'],
        'Swift': ['swift'],
    }

    for language, extensions in language_extensions.items():
        if file_extension.lower() in extensions:
            print("detect_programming_language: ",language)
            return language

    return 'Unknown'

def get_last_n_lines(text, need_lens):
    lines = text.split('\n')
    lines_count = len(lines)

    if lines_count < need_lens:
        return text

    last_10_lines = lines[-1*need_lens:]
    result = '\n'.join(last_10_lines)
    return result

def fix_llm_json_str(string):
    new_string = string.strip()
    try:
        json.loads(new_string)
        return new_string
    except Exception as e:
        print("fix_llm_json_str failed 1:", e)
        try:
            pattern = r'```json(.*?)```'
            match = re.findall(pattern, new_string, re.DOTALL)
            if match:
                new_string = match[-1]
            
            json.loads(new_string)
            return new_string
        except Exception as e:
            print("fix_llm_json_str failed 2:", e)
            try:
                new_string = new_string.replace("\n", "\\n")
                json.loads(new_string)
                return new_string
            except Exception as e:
                print("fix_llm_json_str failed 3:", e)
                
                ctx = [{
                    "role": "system",
                    "content": """Do not change the specific content, fix the json, directly return the repaired JSON, without any explanation and dialogue.
                    ```
                    """+new_string+"""
                    ```"""
                }]

                message, success = chatCompletion(ctx)
                pattern = r'```json(.*?)```'
                match = re.findall(pattern, message, re.DOTALL)
                if match:
                    return match[-1]

                return message
