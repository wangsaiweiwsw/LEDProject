from nicegui import ui
import cv2
import tempfile

import ExamineNumber.examinenumber

tempfile_path = None  # 创建一个变量来存储临时文件的路径

def handle_upload(event):
    global tempfile_path
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(event.content.read())
        tempfile_path = temp_file.name

    confirm_recognition()

def confirm_recognition():
    if tempfile_path:
        image = cv2.imread(tempfile_path)
        result = ExamineNumber.examinenumber.number(image)
        ui.page('/result').run()
        ui.label(result)

def page_layout():
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('头部')

    with ui.row():
        with ui.card():
            ui.label("选择需要识别的照片")
            with ui.column().style('flex: 1;'):
                ui.upload(on_upload=handle_upload).classes('max-w-full')

    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('设置')

    with ui.footer().style('background-color: #3874c8'):
        ui.label('脚部')

ui.page('/result', page_layout)  # 创建名为 '/result' 的页面
page_layout()
ui.run()
