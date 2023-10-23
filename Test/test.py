from nicegui import ui
import tempfile
from FileUpload.local_file_picker import local_file_picker

tempfile_path = None  # 创建一个变量来存储上传的文件路径

def handle_upload(event):
    global tempfile_path
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(event.content.read())  # 保存上传文件的内容到临时文件
        tempfile_path = temp_file.name  # 获取临时文件的路径
    ui.notify(f'Uploaded {event.name}')
    display_image_and_button()  # 显示图片和确认按钮

def confirm_recognition():
    if tempfile_path:
        # 在这里执行确认识别的操作，可以使用tempfile_path来获取图片路径
        ui.notify(f'Confirmed recognition for {tempfile_path}')

def display_image_and_button():
    with ui.card():
        ui.image(tempfile_path).style('margin-right: 10px;')
        ui.button('确认识别', on_click=confirm_recognition)  # 点击按钮时调用confirm_recognition方法

with ui.card():
    ui.upload(on_upload=handle_upload).classes('max-w-full')

with ui.card():
    display_image_and_button()

ui.run()
撒发生