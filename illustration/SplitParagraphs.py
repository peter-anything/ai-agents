from builtins import str
from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.roles.role import Role, RoleReactMode

DIRECTORY_STRUCTION = """
你现在是一个读者,你要对下方文字进行分割
"""
Content = """
故事如下
{story}

对于这个故事
1.输出语言为中文
2.对每句完整的话进行分割,对句号和分段进行分割
3.严格按照字典格式进行回答,如{{"partition":[{{"person":[{{"person1","person2}}],"content":"content1"}}]}}
4.person为一个存放集合,用于存放这个分段中出现的所有人物
5.不要有空格和换行
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


class Partition(Action):
    async def run(self, story: str, *args, **kwargs) -> dict:
        prompt = Content.format(story=story)
        resp_node = await DIRECTORY_WRITE.fill(context=prompt, llm=self.llm, schema="raw")
        # # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        dictionary = eval(resp.replace('```', ''))
        return dictionary


class PartitionActionNode(Role):
    name: str = "PartitionActionNode"
    profile: str = "reader"
    story: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Partition()])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> dict:
        todo = self.rc.todo
        story = self.get_memories(k=1)[0]
        resp = await todo.run(story=story.content)
        return resp


async def main(story):
    role = PartitionActionNode()
    return_code = await role.run(story)
    print(type(return_code))
    print(return_code)
    return return_code
