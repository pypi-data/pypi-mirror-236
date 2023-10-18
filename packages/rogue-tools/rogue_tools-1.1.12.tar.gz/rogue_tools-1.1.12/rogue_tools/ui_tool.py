import os
import sys
import time
import traceback

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from rogue_tools import file_tool,path_tool,thread_tool


class mainUI():
    def __init__(self,w,h,title='PyQt5 - UI by [rogue_tools]',is_center=True):
        self.config_path        = 'save_params.txt'
        self.save_dic           = self.load_input()
        self.editor_dic         = {}
        self.ui_width           = w
        self.ui_height          = h
        self.pool               = thread_tool.ThreadPool()
        self.app                = QApplication(sys.argv)
        self.windows            = QWidget()
        self.windows.resize(self.ui_width,self.ui_height)
        self.windows.setWindowTitle(title)
        # 居中
        if is_center:
            qr = self.windows.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.windows.move(qr.topLeft())


    def show(self):
        #show()方法在屏幕上显示出widget组件
        self.windows.show()
        #循环执行窗口触发事件，结束后不留垃圾的退出，不添加的话新建的widget组件就会一闪而过
        exe_code = self.app.exec_()
        print(exe_code)
        self.exit_exe()
        sys.exit(exe_code)
    
    def add_label(self,line_index,title, start_pos = (0,0),obj_w=200,obj_h=20):
        label = QLabel(self.windows)
        label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        label.setGeometry(QtCore.QRect(start_pos[0] , obj_h * line_index+start_pos[1] , obj_w , obj_h))
        label.setText(title)

    def add_btn(self,line_index,title, start_pos = (0,0),obj_w=100,obj_h=20,call_func=None,in_thread=False,func_parms=[]):
        '''竖着放按钮'''
        #设置按钮并给按钮命名
        btn = self._add_btn(title,start_pos[0] , obj_h * line_index+start_pos[1] , obj_w , obj_h,call_func,in_thread,func_parms)
        return btn

    def add_btn_horizontal(self,line_index,title, start_pos = (0,0),obj_w=100,obj_h=20,call_func=None,in_thread=False, func_parms=[]):
        '''横着放按钮'''
        #设置按钮并给按钮命名
        btn = self._add_btn(title,obj_w * line_index+start_pos[0],start_pos[1] , obj_w , obj_h,call_func,in_thread,func_parms)
        return btn

    def _add_btn(self,title,x,y,w,h,call_func,in_thread,func_parms):
        '''谨慎使用in_thread,通常界面元素无法在多线程中操作,一般用于无界面的情况'''
        def run():
            if in_thread:
                self.pool.add_task(title,call_func,*func_parms)
            else:
                call_func(*func_parms)
        btn = QPushButton(title,self.windows)
        btn.setGeometry(x,y,w,h)
        if call_func:
            btn.clicked.connect(run)
        return btn

    def add_input_editor(self,line_index,title, start_pos = (0,0),obj_w_1=70,obj_w_2=200,obj_h = 20 ,edit_text='',edit_tips=''):
        input_str = self.save_dic.get(title,'') if edit_text=='' else edit_text
        # 显示标签
        label = QLabel(self.windows)
        label.setGeometry(QtCore.QRect(start_pos[0] , obj_h * line_index+start_pos[1] , obj_w_1 , obj_h))
        label.setText(title)
        # 输入框
        edit = QLineEdit(self.windows)
        edit.setPlaceholderText(str(edit_tips))
        edit.setText(str(input_str))
        edit.setGeometry(QtCore.QRect(obj_w_1+start_pos[0] , obj_h * line_index+start_pos[1] , obj_w_2 , obj_h))
        # 管理内容
        self.editor_dic[title] = edit.text
        return edit
    
    def add_combo_box(self,line_index,title, start_pos = (0,0),obj_w_1=70,obj_w_2=200,obj_h = 20,item_list=[]):
        currentText = self.save_dic.get(title,'')
        # 显示标签
        label = QLabel(self.windows)
        label.setGeometry(QtCore.QRect(start_pos[0] , obj_h * line_index+start_pos[1] , obj_w_1 , obj_h))
        label.setText(title)
        # 下拉框
        comb_box = QComboBox(self.windows)
        comb_box.addItems(item_list)
        comb_box.setGeometry(QtCore.QRect(start_pos[0]+obj_w_1 , obj_h * line_index+start_pos[1] , obj_w_2 , obj_h))
        comb_box.setCurrentText(currentText)
        self.editor_dic[title]=comb_box.currentText
        return comb_box

    def add_scrollableTextEdit(self,line_index,title, start_pos = (0,0),obj_w=500,obj_h = 200):
        currentText = self.save_dic.get(title,'')
        ed = QTextEdit(self.windows)
        ed.setGeometry(QtCore.QRect(QtCore.QRect(start_pos[0] , obj_h * line_index+start_pos[1] , obj_w , obj_h)))
        ed.setPlainText(currentText)
        ed.verticalScrollBar().setValue(ed.verticalScrollBar().maximum())
        return ed

    def scrollableTextEdit_append(self,ed:QTextEdit,text):
        lines = [] if ed.toPlainText()=='' else ed.toPlainText().split('\n')
        lines.append('    '+text)
        new_text = self._format_text(lines)
        ed.setPlainText(new_text)
        # 滚动到文本框的底部，以显示最新行
        ed.verticalScrollBar().setValue(ed.verticalScrollBar().maximum())

    def _format_text(self,lines):
        new_text = ''
        for i in range(0,len(lines)):
            head = f'{i}:'.ljust(4)
            body = lines[i][4:]
            new_text = f'{new_text}{head}{body}\n'
        return new_text[:-1]

    def exit_exe(self):
        self.pool.is_stop=True
        self.pool.shutdown(wait=False)
        QtCore.QCoreApplication.instance().quit()

    def msgbox(self,msg_str,title=''):
        QMessageBox.about(self.windows, title,msg_str)

    def save_input(self):
        write_lines=[]
        for key in self.editor_dic:
            write_lines.append(f'{key}={self.editor_dic[key]()}')
        print(f'save:{write_lines}')
        file_tool.write_lines(self.config_path,write_lines,'w+')

    def load_input(self):
        rs_dic = {}
        if not path_tool.is_exists(self.config_path):
            return rs_dic
        lines = file_tool.read_simple_text(self.config_path)
        
        for line in lines:
            temp  = line.split('=')
            if len(temp)==2:
                rs_dic[temp[0]]=temp[1]
        return rs_dic

if __name__ == '__main__':
    from rogue_tools import string_tool
    def test(k):
        # 示范多线程
        key =f'{string_tool.rnd_str(5), k, input.text(), box.currentText()}'
        print(f'3秒后输出{key}')
        time.sleep(3)
        print(key)

    ui = mainUI(300,600)
    start_pos=(10,10)
    btn1     = ui.add_btn(0,'竖着放1',start_pos, call_func= test, func_parms=['竖着放1111'])
    btn2     = ui.add_btn(1,'竖着放2',start_pos, call_func= test, func_parms=['竖着放2222'])

    start_pos=(10,60)
    btn3     = ui.add_btn_horizontal(0,'横着放1',start_pos, call_func= test, func_parms=['横着放1111'])
    btn4     = ui.add_btn_horizontal(1,'横着放2',start_pos, call_func= test, func_parms=['横着放2222'])

    start_pos=(10,110)
    input   = ui.add_input_editor(0,'input0',start_pos,edit_text='删掉显示提示',edit_tips='提示')
    box     = ui.add_combo_box(1,'box0',start_pos,item_list=['box_str_1','box_str_2','box_str_3'])
    label   = ui.add_label(2,'label0',start_pos)
    ui.show()