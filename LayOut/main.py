from nicegui import ui
import tempfile

tempfile_path = None  # 创建一个变量来存储临时文件的路径



def handle_upload(event): # 默认上传方法
    global tempfile_path # 设置一个全局变量存储图片地址
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(event.content.read())  # 保存上传文件的内容到临时文件
        tempfile_path = temp_file.name  # 获取临时文件的路径
    ui.notify(f'上传 {event.name}成功！')
    ui.image(tempfile_path).style()  # 显示临时文件的内容
    ui.button('确认识别', on_click=confirm_recognition)  # 点击按钮时调用confirm_recognition方法

# 这是总体布局
def page_layout():
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'): # 头部布局
        ui.label('头部')

    #主要内容直接平行放就行
    with ui.row(): # 这里用了 row card column 三层布局
        with ui.card():
            ui.label("选择需要识别的照片")
            with ui.column().style('flex: 1;'): # flex: 1; 样式将确保每个列平均分配可用的宽度
                ui.upload(on_upload=handle_upload).classes('max-w-full') # 这个是nicegui中的上传操作
        with ui.card():
            with ui.column().style('flex: 1;'):
                ui.upload(on_upload=handle_upload).classes('max-w-full')

    # 这是右侧抽屉放置处
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('设置')

    # 这是底部布局
    with ui.footer().style('background-color: #3874c8'):
        ui.label('脚部')

# 这是识别用的具体方法
def confirm_recognition():
    if tempfile_path:
        # 在这里执行确认识别的操作，可以使用tempfile_path来获取图片路径
        ui.notify(f'Confirmed recognition for {tempfile_path}')

# 调用布局方法
page_layout()
# 启动nicegui服务
ui.run()