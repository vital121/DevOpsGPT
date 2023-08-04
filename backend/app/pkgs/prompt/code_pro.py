import json
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.i18b import getCurrentLanguageName
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.code_interface import CodeInterface

class CodeBasic(CodeInterface):
    def _generate_prompt(self, task_description, reference_code=None, file_task=None, new_code=None, solution=None):
        """Helper function to generate a prompt for chatCompletion"""
        prompt = f"As a senior full stack developer. {task_description}"
        if reference_code:
            prompt += f"\n\nreference code:\n```\n{reference_code}\n```"
        if file_task:
            prompt += f"\n\ndevelopment task:\n```\n{file_task}\n```"
        if new_code:
            prompt += f"\n\ndevelopment task corresponding code:\n```\n{new_code}\n```"
        if solution:
            prompt += f"\n\nsolution:\n```\n{solution}\n```"
        prompt += f"\n\nUse {getCurrentLanguageName()} dialogue"
        return prompt

    def _process_prompt(self, prompt):
        """Helper function to process a prompt with chatCompletion and return the result"""
        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success

    def aiReferenceRepair(self, newCode, referenceCode, fileTask):
        task_description = "Your task is to analyze the following 'reference code' style and specification..."
        prompt = self._generate_prompt(task_description, referenceCode, fileTask, newCode)
        return self._process_prompt(prompt)

    def aiAnalyzeError(self, message):
        task_description = "Your task is to analyze code execution error messages..."
        prompt = self._generate_prompt(task_description, message)
        return self._process_prompt(prompt)

    def aiFixError(self, solution, code):
        task_description = "Your task is to fix errors in the 'initial code'..."
        prompt = self._generate_prompt(task_description, solution=solution, new_code=code)
        return self._process_prompt(prompt)

    def aiCheckCode(self, fileTask, code):
        task_description = "Your task is to check whether the following 'initial code' has obvious syntax errors..."
        prompt = self._generate_prompt(task_description, file_task=fileTask, new_code=code)
        return self._process_prompt(prompt)

    def aiMergeCode(self, task, baseCode, newCode):
        task_description = "Your task is to integrate with existing code according to the 'Development Task'..."
        prompt = self._generate_prompt(task_description, file_task=task, reference_code=baseCode, new_code=newCode)
        return self._process_prompt(prompt)

    def aiGenCode(self, fileTask, newTask, newCode):
        task_description = "You need to modify the 'basic code' based on the 'change suggestions'..."
        prompt = self._generate_prompt(task_description, file_task=newTask, new_code=newCode)
        return self._process_prompt(prompt)
