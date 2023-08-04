# Configure the interface information of openai and azure. If a certain type of interface is not needed, please completely delete the corresponding element (openai\azure). 
# Configure the interface information of openai and azure (replace sk-xxxx with your key), if you do not need a certain type of interface, please delete the corresponding element (openai\azure), [Note] after the last element in the array Do not add a comma, you may need to enable the global proxy to access the API interface
# 配置 openai 和 azure 的接口信息（替换 sk-xxxx 为你的 key），如果不需要某个类型的接口，请将对应的元素整个删除掉（openai\azure），【注意】数组中最后一个元素后面不要加逗号、您可能需要开启全局代理来访问API接口
GPT_KEYS: |
    {
        "openai": {
            "keys": [
                {"sk-xxxx": {"count": 0, "timestamp": 0}}
            ],
            "api_type": "open_ai",
            "api_base": "https://api.openai.com/v1",
            "api_version": "2020-11-07"
        }
#        ,
#        "azure": {
#            "keys": [
#                {"sk-xxxx": {"count": 0, "timestamp": 0}}
#            ],
#            "api_type": "azure",
#            "api_base": "https://example-gpt.openai.azure.com/",
#            "api_version": "2023-05-15",
#            "deployment_id": "deployment-name"
#        }
    }

# Configure the model used (do not use less than 16k token model), [note] openai plus members and API members are different, you opena plus member does not mean that you can use gpt4 model, specifically consult the official documentation of openai#
# Configure the model used (do not use a model with less than 16k tokens), [Note] openai's plus membership and API membership are different, you have opened a plus membership does not mean that you can use the gpt4 model, please refer to the official documentation of openai
# 配置使用的模型（不要使用小于16k token的模型），【注意】openai的plus会员和API会员是不同的，你开通了plus会员不代表可以用gpt4的模型，具体查阅openai的官方文档
LLM_MODEL: "gpt-3.5-turbo-16k-0613"  

LANGUAGE: 'en'  # en、zh
FRONTEND_PORT: 8080
BACKEND_PORT: 8081
# The url that the back end allows cross-domain access (front-end access address)
# 后端允许跨域访问的url（前端访问地址）
AICODER_ALLOWED_ORIGIN: 'http://127.0.0.1:8080'  

BACKEND_HOST: '0.0.0.0'
BACKEND_DEBUG: true
APP_SECRET_KEY: 'Es*lsnGptDevOps'
WORKSPACE_PATH: './workspace/'
SQLALCHEMY_DATABASE_URI: 'sqlite:///app.db'
DEMO_TASK_ID:  'demo-task'
MODE: "REAL" # FAKE、REAL
GRADE: "base"
DEVOPS_TOOLS: "local"
GITLAB_URL: ""
GITLAB_CLONE_URL: ""
GITLAB_TOKEN: ""
AUTO_LOGIN: true
USERS: |
  {
    "demo_user": "123456"
  }

# APPS: Large concept, including multiple services, services: such as back-end services, front-end services, microservices
# - name、intro: for display only
# - project.struct（File directory structure information for the services）
#     setp1Task（The word splitting process is used in the molecule splitting task）
# - project.intro（Basic information about the services）
#     setpReqChooseLib（Analyze which lib packages to use in conjunction with service information）
# - project.lib（The service's lib package usage specification information）
#     setpReqChooseLib（Analyze which lib packages to use in conjunction with the lib list）
# - api_doc_url
#     To keep this one unique, we'll match it with api_doc
APPS: |
  [
    {
        "id": 3,
        "name": "Demo applications that support any development needs (demo applications that support any development needs)",
        "intro": "Demo applications that support any development needs, You can submit any development requirements.",
        "default_source_branch": "master",
        "default_target_branch": "dev",
        "service": [
            {
                "name": "free_demo",
                "base_prompt": "You can choose any appropriate development language",
                "intro": "service name: free_demo\nrole of service: used to develop any requirements\ndevelopment language: no limit\ndevelopment framework: no limit",
                "api_doc_url": "3",
                "api_doc": "",
                "struct": "no limit",
                "lib": "no limit",
                "specification": {
                    "Default": "- You can choose any appropriate development language"
                }
            }
        ]
    },
    {
        "id": 2,
        "name": "Demo application with python+html front-end and back-end separation",
        "intro": "This is a python+html front-end and back-end separation application, back-end use python flask, front-end use html+jquery+semantic-ui. Front-end and back-end define interaction interfaces through Swagger documentation.",
        "default_source_branch": "master",
        "default_target_branch": "dev",
        "service": [
            {
                "name": "python_demo",
                "base_prompt": "You need to develop both front-end and back-end code",
                "intro": "service name: python_demo\nrole of service: used to develop front-end and back-end requirements\ndevelopment language: python and html\ndevelopment framework: flask and jquery+semantic-ui",
                "api_doc_url": "2",
                "api_doc": "{\"swagger\":\"2.0\",\"info\":{\"description\":\"API documentation for AI Assistant\",\"version\":\"1.0\",\"title\":\"AI Assistant API Documentation\",\"contact\":{\"name\":\"AI Assistant\",\"url\":\"www.xxx.com\",\"email\":\"xxx@xxx.com\"}},\"host\":\"localhost:8086\",\"basePath\":\"/\"}",
                "struct": "- dir: backend, description:Back-end service directory\n- dir: frontend, description:Front-end service directory",
                "lib": "- flask(python Web framework)\n- jquery(JavaScript library)\n- semantic-ui(User interface library)\n- openai(chatgpt sdk)",
                "specification": {
                    "name": "python_demo",
                    "flask": "- python uses flask to provide web services",
                    "jquery": "- js uses the jQuery framework",
                    "openai": "- sdk for openai's chartgpt",
                    "semantic-ui": "- The front page uses the semantic-ui style library",
                    "Default": "- You need to develop both front-end and back-end code"
                }
            }
        ]
    },
    {
        "id": 1,
        "name": "Demo application with python+html front-end and back-end separation (front-end separation application java+html)",
        "intro": "This is a java+html front-end and back-end separation project, back-end 'java_demo_backend' use spring mvc framework, front-end 'java_demo_frontend' use html+jquery+semantic-ui. Front-end and back-end define interaction interfaces through Swagger documentation.",
        "default_source_branch": "master",
        "default_target_branch": "feat/xxx",
        "service": [
            {
                "name": "java_demo_backend",
                "base_prompt": "As a senior JAVA system architect, develop in a Java project based on the MVC design framework and use Spring Boot and MyBatis3 as the development framework",
                "intro": "service name: java_demo_backend\nrole of service: used to develop back-end requirements\ndevelopment language: Java\ndevelopment framework: SpringBoot+Mybatis3\ndatabase: SQLite",
                "api_doc_url": "1",
                "api_doc": "{\"swagger\":\"2.0\",\"info\":{\"description\":\"API documentation for AI Assistant\",\"version\":\"1.0\",\"title\":\"AI Assistant API Documentation\",\"contact\":{\"name\":\"AI Assistant\",\"url\":\"www.xxx.com\",\"email\":\"xxx@xxx.com\"}},\"host\":\"localhost:8086\",\"basePath\":\"/\",\"tags\":[{\"name\":\"TargetController\",\"description\":\"Target Controller\"}],\"paths\":{\"/addTarget\":{\"post\":{\"tags\":[\"TargetController\"],\"summary\":\"Add a new target\",\"operationId\":\"addTargetUsingPOST\",\"consumes\":[\"application/json\"],\"produces\":[\"*/*\"],\"parameters\":[{\"in\":\"body\",\"name\":\"target\",\"description\":\"target\",\"required\":true,\"schema\":{\"$ref\":\"#/definitions/Target\"}}],\"responses\":{\"200\":{\"description\":\"OK\",\"schema\":{\"$ref\":\"#/definitions/ResultModel\"}},\"201\":{\"description\":\"Created\"},\"401\":{\"description\":\"Unauthorized\"},\"403\":{\"description\":\"Forbidden\"},\"404\":{\"description\":\"Not Found\"}},\"deprecated\":false}},\"/getTargetList\":{\"get\":{\"tags\":[\"TargetController\"],\"summary\":\"Get target list\",\"operationId\":\"getTargetListUsingGET\",\"produces\":[\"*/*\"],\"responses\":{\"200\":{\"description\":\"OK\",\"schema\":{\"$ref\":\"#/definitions/ResultPageModel«Target»\"}},\"401\":{\"description\":\"Unauthorized\"},\"403\":{\"description\":\"Forbidden\"},\"404\":{\"description\":\"Not Found\"}},\"deprecated\":false}}},\"definitions\":{\"Exception\":{\"type\":\"object\",\"properties\":{\"cause\":{\"$ref\":\"#/definitions/Throwable\"},\"localizedMessage\":{\"type\":\"string\"},\"message\":{\"type\":\"string\"},\"stackTrace\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/StackTraceElement\"}},\"suppressed\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Throwable\"}}},\"title\":\"Exception\"},\"ResultModel\":{\"type\":\"object\",\"properties\":{\"code\":{\"type\":\"integer\",\"format\":\"int32\"},\"data\":{\"type\":\"object\"},\"exception\":{\"$ref\":\"#/definitions/Exception\"},\"msg\":{\"type\":\"string\"}},\"title\":\"ResultModel\"},\"ResultPageModel«Target»\":{\"type\":\"object\",\"properties\":{\"firstIndex\":{\"type\":\"integer\",\"format\":\"int32\"},\"list\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Target\"}},\"pageNo\":{\"type\":\"integer\",\"format\":\"int32\"},\"pageSize\":{\"type\":\"integer\",\"format\":\"int32\"},\"totalPage\":{\"type\":\"integer\",\"format\":\"int32\"},\"totalRecords\":{\"type\":\"integer\",\"format\":\"int32\"}},\"title\":\"ResultPageModel«Target»\"},\"StackTraceElement\":{\"type\":\"object\",\"properties\":{\"className\":{\"type\":\"string\"},\"fileName\":{\"type\":\"string\"},\"lineNumber\":{\"type\":\"integer\",\"format\":\"int32\"},\"methodName\":{\"type\":\"string\"},\"nativeMethod\":{\"type\":\"boolean\"}},\"title\":\"StackTraceElement\"},\"Target\":{\"type\":\"object\",\"properties\":{\"id\":{\"type\":\"integer\",\"format\":\"int32\"},\"targetName\":{\"type\":\"string\"},\"targetType\":{\"type\":\"string\"}},\"title\":\"Target\"},\"Throwable\":{\"type\":\"object\",\"properties\":{\"cause\":{\"$ref\":\"#/definitions/Throwable\"},\"localizedMessage\":{\"type\":\"string\"},\"message\":{\"type\":\"string\"},\"stackTrace\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/StackTraceElement\"}},\"suppressed\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Throwable\"}}},\"title\":\"Throwable\"}}}",
                "struct": "- dir:src/main/resources/db/migration,description:flywayDatabase version management sql script file, add and modify table fields\n- dir:src/main/java/com/aiassistant/model,description:Database field mapping entity class\n- dir:src/main/java/com/aiassistant/mapper,description:Define the database interaction Mapper interface\n- dir:src/main/resources/mapper,description:The file type is xml, which is the mapping between database operation SQL statements and Mapper\n- dir:src/main/java/com/aiassistant/service,description:Business layer Service interface definition\n- dir:src/main/java/com/aiassistant/service/impl,description:The specific implementation of the Service interface of the business layer\n- dir:src/main/java/com/aiassistant/controller,description:External service interface\n- dir:src/main/java/com/aiassistant/utils,description:General Tools Catalog",
                "lib": "- Lombok\n- OkHttp\n- Jsoup\n- Gson\n- Flyway\n- MyBatis3",
                "specification": {
                    "MyBatis3": "- Sql script file naming rules VyyyymmddHHMM__description.sql, for example: V202307081234__create_target.sql. ",
                    "Flyway": "- Sql script file naming rules VyyyymmddHHMM__description.sql, for example: V202307081234__create_target.sql.",
                    "SQLite": "- Sql scripts must conform to the SQLite syntax.",
                    "OkHttp": "- Using the OkHttp component, the project has been imported, regardless of import dependencies. ",
                    "Gson": "- Using Gson components, the project has been imported, regardless of import dependencies. ",
                    "Jsoup": "- Using the Jsoup component, the project has been introduced, regardless of import dependencies. ",
                    "Default": "- Use the Spring development paradigm. \n- Develop in an existing project, regardless of project configuration. \n- Note the package reference to the Java file. \n- Use the Lombok plugin to simplify your code."
                }
            },
            {
                "name": "java_demo_frontend",
                "base_prompt": "",
                "intro": "service name: java_demo_frontend\nrole of service: used to develop frontend-end requirements\ndevelopment_language: html+js\ndevelopment_framework: jquery+semantic-ui",
                "struct": "- dir:html,description:html files\n- dir:js,description:JavaScript files\n- dir:css,description:css files",
                "lib": "- Semantic-ui\n- jQuery",
                "specification": {
                    "Semantic-ui": "- use Semantic-ui frontend framework",
                    "jQuery": "- use jQuery framework",
                    "Default": "- Make sure the page looks good"
                }
            }
        ]
    }
  ]
