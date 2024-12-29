from metagpt.actions import Action
from metagpt.roles.role import Role, RoleReactMode
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="f1de3f5bfb26e3bc2d20302285a41738.ZectlvqNS9vo07Yj")  # 这个不能给你们看


# 生成图片

class WriteContentWithActionNode(Action):
    Prompt: str = """
{content}
"""

    async def run(self, content: str, *args, **kwargs) -> str:
        prompt = self.Prompt.format(content=content)
        print(prompt)
        response = client.images.generations(
            model="cogview-3-plus",  # 填写需要调用的模型名称
            prompt=prompt,
        )
        print(response.data[0].url)
        return response.data[0].url


class TutorialAssistantWithActionNode(Role):
    name: str = "Stitch"
    profile: str = "Tutorial Assistant"
    topic: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteContentWithActionNode()])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> str:
        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        resp = await todo.run(content=msg.content)
        print(type(resp))
        print(resp)
        return resp


async def main(content: str):
    role = TutorialAssistantWithActionNode()
    data = await role.run(content)
    return data
