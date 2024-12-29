import json
from builtins import str
from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.roles.role import Role, RoleReactMode

DIRECTORY_STRUCTION = """
你现在是一个读者,你要对下方文字中的人物进行设计
"""
Content = """
故事如下
{story}

对于这个故事
1.输出语言为中文
2.分析故事中出现的每一个人,并随机返回每一个人的特征,如,性别,发色,年龄,例如:一个头发颜色为xxx色,眼睛为xxx色的小孩子,不要存在可能等不确定的字样,是什么颜色是你说的算
3.严格按照字典格式进行回答,如{{"person":[{{"name":"name1","features":"features1"}},{{"name":"name2","features":"features2"}}]}}
4.name存放这个人的姓名,features存放这个人的特征
5.不要有多余的空格或换行符
6.只回答字典格式
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


class Person(Action):
    async def run(self, story: str, *args, **kwargs) -> dict:
        prompt = Content.format(story=story)
        resp_node = await DIRECTORY_WRITE.fill(context=prompt, llm=self.llm, schema="raw")
        # # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        dictionary = eval(resp.replace('json', '').replace('```', ''))
        return dictionary


class PersonActionNode(Role):
    name: str = "PersonActionNode"
    profile: str = "reader"
    story: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Person()])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> dict:
        todo = self.rc.todo
        story = self.get_memories(k=1)[0]
        resp = await todo.run(story=story.content)
        return resp


async def main(story: str):
    role = PersonActionNode()
    return_code = await role.run(story)
    return return_code
