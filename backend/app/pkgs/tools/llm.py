import traceback
from app.pkgs.tools.llm_pro import LLMPro
from app.pkgs.tools.llm_basic import LLMBase
from config import GRADE

def chatCompletion(context, usegpt4=False):
    if GRADE == "base":
        obj = LLMBase(usegpt4=usegpt4)
    else:
        obj = LLMPro(usegpt4=usegpt4)

    message = "" 
    success = False
    try:
        print(context)
        message, success = obj.chatCompletion(context)
        print(message)
        print(success)
    except Exception as e:
        print("chatCompletion failed first time:" + str(e))
        try:
            print(context)
            message, success = obj.chatCompletion(context)
            print(message)
            print(success)
        except Exception as e:
            print("chatCompletion failed second time:" + str(e))
            traceback.print_exc()
            message = ""
            success = False
    return message, success
