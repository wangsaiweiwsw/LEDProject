from nicegui import ui
import tempfile

tempfile_path = None  # 创建一个变量来存储临时文件的路径

def handle_upload(event):
    global tempfile_path
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(event.content.read())  # 保存上传文件的内容到临时文件
        tempfile_path = temp_file.name  # 获取临时文件的路径
    ui.notify(f'Uploaded {event.name}')
    ui.image(tempfile_path)  # 显示临时文件的内容

upload = ui.upload(on_upload=handle_upload).classes('max-w-full')

