

import textwrap

GLOBAL="global"

LIBRARY_BLOCK = """        
library identifier: 'trasn-JSL@main', retriever: modernSCM(
     [$class       : 'GitSCMSource',
      remote       : 'https://github.com/houdini91/trans_JSL.git'])
"""
POST_STEP = """PublishHTML()"""


class Trans_error(Exception):
    def __init(self, *args):
        self.args = args

class Unsupported_type(Trans_error):
    """Unsupported type"""
    pass

class Unknown_stage(Trans_error):
    def  __str__(self):
        return "Unknown stage: {0}".format(self.args)

class Only_global_allowed(Trans_error):
    def  __str__(self):
        return "Only global stage allowed: {0}".format(self.args)


class BasePipeline:
    GLOBAL_MOCK_STAGE = "global"

    def __init__(self):
        self.stages = {}
        self.params = []
        self.add_stage(self.GLOBAL_MOCK_STAGE, None)

    def generate_header_block(self):
        return LIBRARY_BLOCK

    def generate_jenkinsfile(self):
        pipeline_format = """{header_block}\npipeline {{\n\tagent any\n{env_param_block}\n{stages_block}\n}}"""

        header_block = self.generate_header_block()
        env_param_block = self.generate_env_param_block(self.GLOBAL_MOCK_STAGE)

        stage_list = self.generate_stage_list()        
        stage_str = self.generate_list(stage_list, tok="\n")
        stages_block = self.generate_stages_block(stage_str)

        env_param_block = textwrap.indent(env_param_block, "\t")
        stages_block = textwrap.indent(stages_block, "\t")
        pipeline_str = pipeline_format.format(header_block=header_block, env_param_block=env_param_block, stages_block=stages_block)

        print(pipeline_str)

    #################### Blocks ############################
    def generate_env_param_block(self, stage_name):
        env_param_format = """{env_block}\n{param_block}"""
        param_list = self.generate_param_list(stage_name)
        param_str = self.generate_list(param_list, tok="\n")
        param_block = self.generate_param_block(param_str)

        env_list = self.generate_env_list(stage_name)
        if stage_name == "global":
            env_list.extend(self.generate_cred_list(stage_name))

        env_str = self.generate_list(env_list, tok="\n")
        env_block = self.generate_env_block(env_str)

        if len(env_list) == 0 and len(param_list) == 0:
            env_param_format = ""
        elif len(env_list) == 0:
            env_param_format = """{param_block}"""
        elif  len(param_list) == 0:
            env_param_format = """{env_block}"""

        env_param_block = env_param_format.format(env_block=env_block, param_block=param_block)
        return env_param_block

    def generate_stages_block(self, stage_str):
        stage_str = textwrap.indent(stage_str, "\t")
        stages_format = """stages {{\n{stage_str}\n}}"""
        return stages_format.format(stage_str=stage_str)

    def generate_param_block(self, param_str):
        param_str = textwrap.indent(param_str, "\t")
        params_format = """parameters {{\n{param_str}\n}}"""
        return params_format.format(param_str=param_str)

    def generate_env_block(self, env_str):
        env_str = textwrap.indent(env_str, "\t")
        env_block_format = """environment {{\n{env_str}\n}}"""
        return env_block_format.format(some="test", env_str=env_str)

    def generate_steps_block(self, step_str):
        step_str = textwrap.indent(step_str, "\t")
        step_block_format = """steps {{\n{step_str}\n}}"""
        return step_block_format.format(step_str=step_str)

    def generate_post_steps_block(self, post_step_str):
        post_step_str = textwrap.indent(post_step_str, "\t")
        post_step_block_format = """post {{\n\talways \t{{\n\t\t{post_step_str}\n\t}}\n}}"""
        return post_step_block_format.format(post_step_str=post_step_str)

    def generate_with_cred_block(self, stage_name, step_str):
        step_str = textwrap.indent(step_str, "\t")
        cred_list = self.generate_cred_list(stage_name)
        cred_str = self.generate_list(cred_list, tok=",\n")

        cred_block_format = """withCredentials([{cred_str}]){{\n{step_str}\n}}"""
        return cred_block_format.format(cred_str=cred_str, step_str=step_str)

    #################### List ############################
    def generate_stage_list(self):
        list_obj = []

        next_stage = self.initial
        counter = 0
        while next_stage != None and counter < len(self.stages):
            stage_name = next_stage
            if not stage_name in self.stages or stage_name == self.GLOBAL_MOCK_STAGE:
                raise Unknown_stage(stage_name)

            stage_format = """stage('{stage_name}') {{\n{env_block}\n{steps_block}\n{post_steps_block}\n}}"""
            stage = self.stages[stage_name]
            
            env_block = self.generate_env_param_block(stage_name)
            
            env_list = self.generate_env_list(stage_name)
            env_str = self.generate_list(env_list, tok="\n")
            env_block = self.generate_env_block(env_str)

            if len(env_list) == 0:
                stage_format = """stage('{stage_name}') {{\n{steps_block}\n{post_steps_block}\n}}"""


            step_list = self.generate_step_list(stage_name)
            step_str = self.generate_list(step_list, tok="\n")
            if len(stage["cred"]) > 0:
                step_str = self.generate_with_cred_block(stage_name, step_str)

            steps_block = self.generate_steps_block(step_str)
            post_steps_block = self.generate_post_steps_block(POST_STEP)
            
            env_block = textwrap.indent(env_block, "\t")
            steps_block = textwrap.indent(steps_block, "\t")
            post_steps_block = textwrap.indent(post_steps_block, "\t")

            obj = stage_format.format(stage_name=stage_name, env_block=env_block, steps_block=steps_block, post_steps_block=post_steps_block)
            list_obj.append(obj)
            next_stage = stage["next_stage"]

        return list_obj

    def generate_param_list(self, stage_name):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        list_obj = []
        for param in self.stages[stage_name]["params"]:
            obj = self.generate_func(param["type"], param["params"], True)
            list_obj.append(obj)

        return list_obj

    def generate_func(self, func_name, func_args, named, delimiter=":"):
        func_format = """{func_name}({func_str})"""
        func_str = self.generate_argument_str(func_args, named, delimiter)
        return func_format.format(func_name=func_name, func_str=func_str)

    def generate_cred_list(self, stage_name):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        list_obj = []
        for cred in self.stages[stage_name]["cred"]:
            if stage_name == self.GLOBAL_MOCK_STAGE:
                cred_format = """{variable} = credentials('{credentialsId}')"""
                obj = cred_format.format(credentialsId=cred["credentialsId"], variable=cred["variable"])
                list_obj.append(obj)
            else:
                obj = self.generate_func(cred["cred_type"], {"credentialsId": cred["credentialsId"],"variable": cred["variable"]}, True)
                list_obj.append(obj)
                 
        return list_obj

    def generate_env_list(self, stage_name):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        list_obj = []
        for env in self.stages[stage_name]["env"]:
            env_format = """{env_key} = '{env_value}'"""
            obj = env_format.format(env_key=env["env_key"], env_value=env["env_value"])
            list_obj.append(obj)

        return list_obj

    def generate_step_list(self, stage_name):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        list_obj = []
        for step in self.stages[stage_name]["step"]:
            if step["type"] == "sh":
                obj = self.generate_func(step["type"], step["args"], True)
            if  step["type"] == "InVirtualEnv" or \
                step["type"] == "CreateVirtualEnv":
                obj = self.generate_func(step["type"], step["args"], False)


                list_obj.append(obj)

        return list_obj

    def generate_argument_str(self, field_dict, named, delimiter):
        res = ""
        for index, key in enumerate(field_dict):
            value = field_dict[key]
            if value == None:
                continue

            if index > 0:
                res += ", "

            if type(value) == str:
                value_format = "'{value}'"
            else:
                value_format = "{value}"

            if named:
                key_value_format = "{key}" + delimiter+ value_format
            else:
                key_value_format = value_format

            res += key_value_format.format(key=key, value=field_dict[key])
        return res

    def generate_list(self, list_obj, tok=","):
        res = ""

        for index in range(len(list_obj)):
            obj = list_obj[index]
            if obj == None:
                continue

            if index > 0:
                res += tok

            res += "{obj}".format(obj=obj)
        return res

    #################### add params ########################
    def add_boolean_param(self, stage_name, name, defaultValue, description=None):
        if type(defaultValue) != bool:
            raise Unsupported_type

        d = {"name": name, "defaultValue": defaultValue, "description":description}
        return self.add_base_param(stage_name, "booleanParam", d)

    def add_password_param(self, stage_name, name, defaultValue, description=None):
        d = {"name": name, "defaultValue": defaultValue, "description":description}
        return self.add_base_param(stage_name, "password", d) 

    def add_text_param(self, stage_name,  name, defaultValue, description=None):
        d = {"name": name, "defaultValue": defaultValue, "description":description}
        return self.add_base_param(stage_name, "text", d) 

    def add_string_param(self, stage_name, name, defaultValue, description=None):
        d = {"name": name, "defaultValue": defaultValue, "description":description}
        return self.add_base_param(stage_name, "string",d) 

    def add_choice_param(self, stage_name, name, choices, description=None):
        d = {"name": name, "choices": choices, "description":description}
        return self.add_base_param(stage_name, "choice", d) 

    def add_base_param(self, stage_name, param_type, params):
        if stage_name != "global":
            raise Only_global_allowed(stage_name)

        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        self.stages[stage_name]["params"].append({"type":param_type, "params": params})

    #################### add cred ########################
    def add_cred(self, stage_name, cred_type, cred_id, cred_param):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        self.stages[stage_name]["cred"].append({"cred_type":cred_type, "credentialsId":cred_id, "variable":cred_param})
        
    #################### add env ########################
    def add_env(self, stage_name, env_key, env_value):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        self.stages[stage_name]["env"].append({"env_key":env_key, "env_value":env_value})

    #################### add stage ########################
    def add_stage(self, stage_name, next_stage, is_initial=False):
        if not stage_name in self.stages:
            self.stages[stage_name] = {"params": [], "cred": [], "env": [], "step": []}

        if is_initial:
            self.initial = stage_name

        self.stages[stage_name]["next_stage"] = next_stage  

    #################### add step ########################
    def add_sh_step(self, stage_name, sh_cmd, label=None, returnStdout=None):
        d = {"script": sh_cmd, "label":label, "returnStdout":returnStdout}
        self.add_base_step(stage_name, "sh", d)

    def add_virtual_env_step(self, stage_name, name="venv", command="python --version"):
        d = {"name":name , "command": command}
        self.add_base_step(stage_name, "InVirtualEnv", d)

    def add_create_virtual_env_step(self, stage_name, name="venv"):
        d = {"name":name}
        self.add_base_step(stage_name, "CreateVirtualEnv", d)

    def add_base_step(self, stage_name, step_type, step_args):
        if not stage_name in self.stages:
            raise Unknown_stage(stage_name)

        self.stages[stage_name]["step"].append({"type":step_type, "args": step_args})


# class Pipeline(BasePipeline):
#     def __init__(self):
#         super().__init__()

#         super().add_stage("collector", "filter", is_initial=True)
#         super().add_stage("filter", None)

#         super().add_cred("global",'string','FINHUB_TOKEN_IDGLOBAL','TOKEN')
#         super().add_cred("collector",'string','FINHUB_TOKEN_ID_COLLECTOR','TOKEN')
#         super().add_cred("filter",'string','FINHUB_TOKEN_ID2_FILTER','TOKEN')
#         super().add_cred("filter",'usernamePassword','API_USER_PASS_ID','API_USER_PASS_PARAM')

#         super().add_choice_param("collector", "CHOICE_PARAM", ["A", "B", "C"], "Test")
#         super().add_string_param("collector", "STRING_PARAM", "SomethingDefualt")
#         super().add_text_param("global", "TEXT_PARAM", "SomethingDefualt")
#         super().add_boolean_param("filter", "BOOL_PARAM", True)

#         super().add_env("global", "GLOBAL_ENV", "VALUE")
#         super().add_env("collector", "COLLECTOR_ENV", "VALUE")
#         super().add_env("filter", "FILTER_ENV", "VALUE")

#         super().add_sh_step("collector", "python3 collector $FINHUB_TOKEN_ID_COLLECTOR", label="run_collector")
#         super().add_sh_step("filter", "python3 collector $FINHUB_TOKEN_ID_COLLECTOR")
#         super().add_sh_step("filter", "bash run_second_step.sh", label="second_step")

#         super().generate_jenkinsfile()