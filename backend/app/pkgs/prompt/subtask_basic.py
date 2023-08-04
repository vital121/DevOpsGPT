import json
import time
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.subtask_interface import SubtaskInterface
from app.pkgs.knowledge.app_info import getServiceSpecification, getServiceStruct
from config import MODE
from app.pkgs.tools.i18b import getCurrentLanguageName

class SubtaskBasic(SubtaskInterface):
    def splitTask(self, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        if MODE == "FAKE":
            time.sleep(10)
            return TEST_RESULT, True

        

        data, success = setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib)
        code_require = []
        default_msg, _ = getServiceSpecification(appID, serviceName, "Default")
        code_require.append(default_msg)
        for t in data:
            name = t['name']
            require_msg, _ = getServiceSpecification(appID, serviceName, name)
            code_require.append(require_msg)

        code_require = list(set(code_require))
        print(f"==============================={code_require}")
        specification = '\n'.join(code_require)

        message, ctx, success = setp1Task(feature, appBasePrompt, serviceStruct, specification)
        if success:
            ctx_clone = ctx[:]
            #message, ctx, success = setp2Again(message, ctx, msg)
            return setp3Code(message, ctx_clone, appBasePrompt, specification, serviceName)
        else:
            return message, False


def setp3Code(message, context, appBasePrompt, msg, serviceName):
    context.append({
        "role": "assistant",
        "content": message
    })

    serviceNameStr = '"'+serviceName+'"'

    context.append({
        "role": "user",
        "content": appBasePrompt + """。

According to all sub-steps after splitting in"""+serviceNameStr+"""Write a complete runnable code under the service
Require：
""" + msg + """

You will write a very long answer. Make sure that every detail of the architecture is, in the end, implemented as code.
Make sure that every detail of the architecture is, in the end, implemented as code.
Make sure that every detail of the architecture is, in the end, implemented as code.
Think step by step and reason yourself to the right decisions to make sure we get it right.
Please note that the code should be fully functional. No placeholders. Constantly rethinking whether the code is complete.
Then you will output the content of each file including ALL code. 
Each file must strictly follow a JSON code block format as below.

Format example:
```
[{
  "service-name": """+serviceNameStr+""",
  "files": [{
      "file-path": "src/aaa.java",
      "reference-file": "reference-file",
      "code": "import org.springframework.web.bind.annotation.RestController;\\n@RestController\\npublic class TargetController",
      "code-interpreter": "Add a new method getFile in the code, input: repopath, filepath, return: filecontent",
    },
    {
      "file-path": "main.go",
      "reference-file": "reference-file",
      "code": "package main\\n func readFile(filePath str)\\n{\\n  return io.readFile(filePath)\\n}",
      "code-interpreter": "Add a new interface readFile in the entry file, input: filePath, call the io package to read the file content, and return: fileContent"
    }
  ]
}
]
Do not explain the code, just give the JSON, Ensure the response can be parsed by Python json.loads.

JSON Field description:
```
0. "service-name": the value only can be """+serviceName+""".
1. "code-interpreter": field must be in chinese.
2. "code": Please note that the code should be fully functional. No placeholders, and should not contain pseudocode or unfinished code or todo code. Ensure correlation and integrity between different code files to ensure that all code works correctly.
3. "code-interpreter": As a senior developer, you must explain the "code" you provide in detail in "code-interpreter" field, and this explain should be independent. For example: specific variable names and types to be added and modified, method names to be added or modified, parameter names, and so on.
4. "file-path": Do not include "service-name" in the path. 
5. "files" need to be group by "service-name"
6. "reference-file": Inference only based on the "Directory structure" "reference-file" filed above, if you don't know leave it blank.
```
        """
    })

    data, success = chatCompletion(context)
    
    data = fix_llm_json_str(data)

    if data.startswith('{') and data.endswith('}'):
        data = "[" + data + "]"

    return json.loads(data), success


def setp2Again(message, context, msg):
    context.append({
        "role": "assistant",
        "content": message
    })

    context.append({
        "role": "user",
        "content": """Combine the sub-steps that have been split, and check it again as required. Think step by step, and then carefully analyze the sub-steps, and describe each sub-step in as much detail as possible. Be careful not to write code.

Require:
""" + msg + """
"""
    })

    message, success = chatCompletion(context)

    return message, context, success


def setp1Task(feature, appBasePrompt, serviceStruct, specification):
    context = []
    content = appBasePrompt + """. Your task is to think step by step according to the basic information "Application Information" and "Development Requirements" of the application provided below, and split the "Development Tasks" provided below into multiple operation steps from the perspective of completing code development, each Steps cannot be repeated and are described in as much detail as possible.
Pay attention to only analyze the steps and not write codes, the decomposition should be appropriate and reasonable, neither excessive splitting nor missing key steps.
Note that the steps should not contain content that is not related to coding work, such as: preparing the environment, performing tests, performing package deployment, etc.

Application Information (Note: directory_structure is the directory structure description of the project.)：
```
""" + serviceStruct + """
```

Development requirements:
""" + specification + """  

Development Tasks:
```
""" + feature + """
````
"""
    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    return message, context, success


# choose lib by req
def setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib):
    context = []
    content = appBasePrompt + """，Your task is to analyze the requirements to find the appropriate component name. Think step by step, combine the existing project information and the list of existing components, analyze which components are used for the requirements input by the user, and only select among the existing components. Be careful not to write code

Note that the returned component name only needs to contain the name without the description, and the component name must be exactly the same as that in the component list.

Project information:
```
""" + projectInfo + """
```
    
Component list:
```
""" + projectLib + """
```

need:
```
""" + feature + """
```
    """
    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    context.append({
        "role": "assistant",
        "content": message
    })

    context.append({
        "role": "user",
        "content": """Summary of the components chosen above.you will provide only the output in the exact format specified below with no explanation or conversation.

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
```
[{"name":"{the name without a description}","reason":"reason","description":"description"}]
```
"""
    })

    data, success = chatCompletion(context)

    return json.loads(data), success


# Analysis Requirements Classification
def setpReqCls(feature):
    context = []
    content = """As a system architect, your task is to analyze user requirements and determine the type of requirement. When developing within an existing project, you should think step by step.
    
Requirement classifications:
```
System Integration Requirements(SIR): These involve integrating different systems, components, or modules together to achieve a broader range of functionality or business objectives.
System Management Requirements(SMR): These involve managing and maintaining various resources and data within the system.
Web Scraping Requirements(WSR): These refer to automated programs that gather information from the internet, typically by parsing web page content to extract the desired data.
Composite Requirements(CMR): These refer to combining multiple independent functional requirements to achieve a more comprehensive and complex business objective.
```

The user will provide the requirements, you will provide only the output in the exact format specified below with no explanation or conversation.
```
{"type":"type","reason":"reason"}
```

Requirement：
```
""" + feature + """
```

Note: Keep conversations in """ + getCurrentLanguageName() + """.
    """

    context.append({"role": "system", "content": content})
    data, success = chatCompletion(context)

    return json.loads(data), success


# just for test
TEST_RESULT = [{
    "service-name": "java_demo_backend",
    "files": [
        {
            "file-path": "src/main/resources/db/migration/V202307081234__create_member_table.sql",
            "reference-file": "src/main/resources/db/migration/V202301__create_target_table.sql",
            "code": "CREATE TABLE t_member (\n  id INTEGER PRIMARY KEY AUTOINCREMENT,\n  member_name TEXT,\n  member_email TEXT,\n  member_nickname TEXT,\n  member_phone TEXT,\n  gender TEXT,\n  birthday TEXT\n);",
            "code-interpreter": "Create the database table t_member, including the fields: member name, member email, member nickname, member mobile number, gender, birthday."
        },
        {
            "file-path": "src/main/java/com/aiassistant/model/Member.java",
            "reference-file": "src/main/java/com/aiassistant/model/Target.java",
            "code": "package com.aiassistant.model;\n\nimport lombok.Data;\n\n@Data\npublic class Member {\n  private Integer id;\n  private String memberName;\n  private String memberEmail;\n  private String memberNickname;\n  private String memberPhone;\n  private String gender;\n  private String birthday;\n}",
            "code-interpreter": "Adds a mapping of the membership management-related fields in the target entity class Member."
        },
        {
            "file-path": "src/main/java/com/aiassistant/mapper/MemberMapper.java",
            "reference-file": "src/main/java/com/aiassistant/mapper/TargetMapper.java",
            "code": "package com.aiassistant.mapper;\n\nimport com.aiassistant.model.Member;\nimport org.apache.ibatis.annotations.Insert;\nimport org.apache.ibatis.annotations.Mapper;\n\n@Mapper\npublic interface MemberMapper {\n  @Insert(\"INSERT INTO t_member (member_name, member_email, member_nickname, member_phone, gender, birthday) VALUES (#{memberName}, #{memberEmail}, #{memberNickname}, #{memberPhone}, #{gender}, #{birthday})\")\n  void addMember(Member member);\n}",
            "code-interpreter": "Adds a method to add a member to the target Mapper interface MemberMapper."
        },
        {
            "file-path": "src/main/resources/mapper/MemberMapper.xml",
            "reference-file": "src/main/resources/mapper/TargetMapper.xml",
            "code": "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<!DOCTYPE mapper PUBLIC \"-//mybatis.org//DTD Mapper 3.0//EN\" \"http://mybatis.org/dtd/mybatis-3-mapper.dtd\">\n<mapper namespace=\"com.aiassistant.mapper.MemberMapper\">\n  <insert id=\"addMember\" parameterType=\"com.aiassistant.model.Member\">\n    INSERT INTO t_member (member_name, member_email, member_nickname, member_phone, gender, birthday)\n    VALUES (#{memberName}, #{memberEmail}, #{memberNickname}, #{memberPhone}, #{gender}, #{birthday})\n  </insert>\n</mapper>",
            "code-interpreter": "Add the SQL statement for adding a member to MemberMapper.xml in the SQL mapping file of the target Mapper interface."
        },
        {
            "file-path": "src/main/java/com/aiassistant/service/MemberService.java",
            "reference-file": "src/main/java/com/aiassistant/service/TargetService.java",
            "code": "package com.aiassistant.service;\n\nimport com.aiassistant.model.Member;\n\npublic interface MemberService {\n  void addMember(Member member);\n}",
            "code-interpreter": "Adds a method declaration for adding a member to the target Service interface MemberService."
        },
        {
            "file-path": "src/main/java/com/aiassistant/service/impl/MemberServiceImpl.java",
            "reference-file": "src/main/java/com/aiassistant/service/impl/TargetServiceImpl.java",
            "code": "package com.aiassistant.service.impl;\n\nimport com.aiassistant.mapper.MemberMapper;\nimport com.aiassistant.model.Member;\nimport com.aiassistant.service.MemberService;\nimport lombok.RequiredArgsConstructor;\nimport org.springframework.stereotype.Service;\n\n@Service\n@RequiredArgsConstructor\npublic class MemberServiceImpl implements MemberService {\n  private final MemberMapper memberMapper;\n\n  @Override\n  public void addMember(Member member) {\n    memberMapper.addMember(member);\n  }\n}",
            "code-interpreter": "The method to add a member is implemented in the target Service interface implementation class MemberServiceImpl."
        },
        {
            "file-path": "src/main/java/com/aiassistant/controller/MemberController.java",
            "reference-file": "src/main/java/com/aiassistant/controller/TargetController.java",
            "code": "package com.aiassistant.controller;\n\nimport com.aiassistant.model.Member;\nimport com.aiassistant.service.MemberService;\nimport io.swagger.annotations.Api;\nimport io.swagger.annotations.ApiOperation;\nimport lombok.RequiredArgsConstructor;\nimport org.springframework.web.bind.annotation.PostMapping;\nimport org.springframework.web.bind.annotation.RequestBody;\nimport org.springframework.web.bind.annotation.RequestMapping;\nimport org.springframework.web.bind.annotation.RestController;\n\n@RestController\n@RequestMapping(\"/members\")\n@Api(tags = \"Member Management\")\n@RequiredArgsConstructor\npublic class MemberController {\n  private final MemberService memberService;\n\n  @PostMapping\n  @ApiOperation(\"Add Member\")\n  public void addMember(@RequestBody Member member) {\n    memberService.addMember(member);\n  }\n}",
            "code-interpreter": "Adds an interface method for adding members to the target Controller."
        }
    ]
}]
