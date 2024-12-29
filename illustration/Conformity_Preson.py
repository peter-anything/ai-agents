import asyncio
from builtins import str

from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

DIRECTORY_STRUCTION = """
你现在是一个读者,你要对下方文字中的人物进行设计
"""

Content = """
信息如下:
{Information}

1.对传入的数据进行整合
2.例如,传入的数据为:{{'name': '孔融', 'features': '一个黑发，年幼的小男孩，大约六岁，眼睛明亮'}},那么返回的结果:{{"data":"孔融是一个黑发，大约六岁，眼睛明亮，年幼的小男孩"}}
3.返回的结果为一个字典,不要有其他的任何内容和符号和换行
"""

# 实例化一个ActionNode，输入对应的参数
DIRECTORY_WRITE = ActionNode(
    # ActionNode的名称
    key="Conformity_Preson",
    # 期望输出的格式
    expected_type=str,
    # 命令文本
    instruction=DIRECTORY_STRUCTION,
    # 例子输入，在这里我们可以留空
    example="",
)
class Conformity_Preson(Action):
    async def run(self, Information: str, *args, **kwargs) -> str:
        prompt = Content.format(Information=Information)
        # prompt = Content.format(story=story)
        # print(prompt)
        resp_node = await DIRECTORY_WRITE.fill(context=prompt, llm=self.llm, schema="raw")
        # # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        # print(resp)
        # return OutputParser.extract_struct(resp, dict)
        return resp

class Conformity_PresonActionNode(Role):
    name: str = "PersonActionNode"
    profile: str = "reader"
    story: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Conformity_Preson()])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)


    async def _act(self) -> Message:
        todo = self.rc.todo
        Information = self.get_memories(k=1)[0]
        resp = await todo.run(Information=Information.content)
        return Message(content=resp, role=self.profile)


async def main(Information :str):
    # Information :str = "{'name': '孔融', 'features': '一个黑发，年幼，大约六七岁的小孩子，眼睛明亮'}"
    role = Conformity_PresonActionNode()
    # await role.run(story)
    return_code = await role.run(Information)
    return return_code.content
