#!/usr/bin/env python3
from FileUpload.local_file_picker import local_file_picker

from nicegui import ui


async def pick_file() -> None:
    result = await local_file_picker('~', multiple=True)
    ui.notify(f'你选择了{result}')
    # 假设 result 是包含文件路径的列表
    file_path = result[0]  # 提取列表中的第一个文件路径
    ui.image(file_path)  # 将文件路径传递给 ui.image


ui.button('点击提交', on_click=pick_file, icon='folder')

ui.run()
