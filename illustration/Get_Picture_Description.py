import asyncio
from builtins import str

from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

DIRECTORY_STRUCTION = """
你现在是一个动画设计这,你要对下方文字设计个图片
"""
Content = """
内容如下:
{content}
所有人物形象如下:
{All_Persona}
当前图片有的人物为:
{Current_Person}

对于这个图片的描述:
1.输出语言为中文
2.根据给的内容,进行设计一个图片,例如:一个什么颜色头发的孩子正在做什么动作
3.严格按照字典格式进行回答,如{{"data":"description"}}
4.description为对这个图片的描述
5.不要有多余的空格或换行符
"""
# 实例化一个ActionNode，输入对应的参数
DIRECTORY_WRITE = ActionNode(
    # ActionNode的名称
    key="Partition",
    # 期望输出的格式
    expected_type=str,
    # 命令文本
    instruction=DIRECTORY_STRUCTION,
    # 例子输入，在这里我们可以留空
    example="",
)


class Get_Picture_Description(Action):
    async def run(self, content: str, All_Persona: str, Current_Person: str, *args, **kwargs) -> str:
        prompt = Content.format(content=content, All_Persona=All_Persona, Current_Person=Current_Person)
        # print(prompt)
        resp_node = await DIRECTORY_WRITE.fill(context=prompt, llm=self.llm, schema="raw")
        # # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        # print(resp)
        # return OutputParser.extract_struct(resp, dict)
        return resp


class Get_Picture_DescriptionActionNode(Role):
    name: str = "PersonActionNode"
    profile: str = "reader"
    story: str = ""
    content: str = ""
    All_Persona: str = ""
    Current_Person: str = ""

    def __init__(self, content: str, All_Persona: str, Current_Person: str, **kwargs):
        super().__init__(**kwargs)
        self._init_action(Get_Picture_Description())
        # self._init_actions([Get_Picture_Description()])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
        self.content = content
        self.All_Persona = All_Persona
        self.Current_Person = Current_Person

    async def _act(self) -> Message:
        todo = self.rc.todo
        resp = await todo.run(content=self.content, All_Persona=self.All_Persona, Current_Person=self.Current_Person)
        return Message(content=resp, role=self.profile)


async def main(content: str, All_Persona: str, Current_Person: str):
    role = Get_Picture_DescriptionActionNode(content=content, All_Persona=All_Persona, Current_Person=Current_Person)
    # await role.run(story)
    return_code = await role.run("1")
    return return_code
