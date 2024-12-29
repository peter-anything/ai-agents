import asyncio
import re

import Get_Person, Conformity_Preson, Get_Picture_Description, Get_Image, Download_Image
import SplitParagraphs

story: str = "一天，父亲的朋友带了一盘梨子，给孔融兄弟们吃。父亲叫孔融分梨，孔融挑了个最小的梨子，其余按照长幼顺序分给兄弟。孔融说：“我年纪小，应该吃小的梨，大梨该给哥哥们。”父亲听后十分惊喜，又问：“那弟弟也比你小啊?” 孔融说：“因为弟弟比我小，所以我也应该让着他。”孔融让梨的故事，很快传遍了汉朝。小孔融也成了许多父母教育子女的好例子。一天，父亲的朋友带了一盘梨子，给孔融兄弟们吃。父亲叫孔融分梨，孔融挑了个最小的梨子，其余按照长幼顺序分给兄弟。孔融说：“我年纪小，应该吃小的梨，大梨该给哥哥们。”父亲听后十分惊喜，又问：“那弟弟也比你小啊?” 孔融说：“因为弟弟比我小，所以我也应该让着他。”孔融让梨的故事，很快传遍了汉朝。小孔融也成了许多父母教育子女的好例子。"


async def main():
    # 获取人物信息
    dictionary = await Get_Person.main(story)
    # 获取分段
    context2 = await SplitParagraphs.main(story)
    context4 = ""
    for dir in dictionary:
        context3 = await Conformity_Preson.main(Information=str(dir))
        pattern = r'{"data":(.*)}'
        match1 = re.search(pattern, context3)
        code_text1 = match1.group(1) if match1 else context3
        pattern1 = r'"(.*)"'
        match = re.search(pattern1, code_text1)
        code_text = match.group(1) if match else code_text1
        context4 += code_text
        context4 += "\n"
    AllLink: str = ""

    for index, dir in enumerate(context2.get("partition")):
        Imagedescription = await Get_Picture_Description.main(content=dir.get("content"), All_Persona=context4,
                                                              Current_Person=dir.get("person"))
        Imagedescription1 = Imagedescription.content
        dictionary = eval(Imagedescription1)
        Imaged = dictionary.get("data")
        link = await Get_Image.main(content=Imaged)
        AllLink += dir.get("content")
        index_name = str(index + 1)
        name = "第{index_name}张图片.png"
        prompt = name.format(index_name=index_name)
        Download_Image.Download(prompt, link)
        AllLink += "\n"
        AllLink += link
        AllLink += "\n"
    print("--------最终内容---------")
    print(AllLink)


if __name__ == '__main__':
    asyncio.run(main())
