import os
import shutil
import configparser
import xlwings as xw
from tkinter import filedialog


class Excel:
    def __init__(self, content="", promote="", column="D", source_path=None, aim_path=None):
        self.name_list = []
        self.content = content
        self.promote = promote
        self.column = column
        self.aim_path = aim_path
        self.source_path = source_path
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/SETTINGS.ini')
        self.settings = configparser.ConfigParser()
        self.settings.read(file_path)

    def reform_by_jielong(self):
        """ reform by WeChat Jielong """
        line = self.content.split("\n")
        for ele in line:
            pre_name = ele.split(".")[1].split("1")[0]
            self.name_list.append(pre_name.replace(" ", ""))

    def reform_by_separator(self, separators="，、,.\n"):
        """ reform by Separator, such as ,.，、 """
        def my_split(s, ds):
            res = [s]
            for d in ds:
                t = []
                list(map(lambda x: t.extend(x.split(d)), res))
                res = t
            # 使用列表解析过滤空字符串
            return [x for x in res if x]
        for i in my_split(self.content, separators):
            self.name_list.append(i)

    def reform_by_space(self):
        """ reform by Blank Space """
        rough = self.content.split(" ")
        for i in rough:
            self.name_list.append(i.replace(" ", "").replace("\n", ""))

    def run(self, i_column="B"):
        """ 目前姓名要排在第B列 """
        if not self.source_path:
            self.source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            "static/"+self.settings.get("static", "default"))
        if not self.aim_path:
            self.aim_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("excel文件", [".xlsx", ".xls"])])
            print(self.aim_path)
        shutil.copy(self.source_path, self.aim_path)

        app = xw.App(visible=True, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        wb = app.books.open(self.aim_path)

        sheet1 = wb.sheets["sheet1"]
        for i in range(1, len(self.name_list)):
            i_name = i_column + str(i)
            if sheet1.range(i_name).value in self.name_list:
                sheet1.range(self.column + str(i)).value = self.promote

        wb.save()
        wb.close()
        app.quit()

    def add_column(self, i_column="B", start_line=2):
        """ start_lint: 开始填入的行数 """
        if not self.source_path:
            self.source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            "static/"+self.settings.get("static", "default"))
        if not self.aim_path:
            self.aim_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("excel文件", [".xlsx", ".xls"])])
        shutil.copy(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/origin.xlsx'), self.aim_path)

        app = xw.App(visible=True, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        wb = app.books.open(self.aim_path)

        sheet1 = wb.sheets["sheet1"]
        # print(self.name_list)
        for i in range(0, len(self.name_list)):
            i_name = i_column + str(i+start_line)
            sheet1.range(i_name).value = self.name_list[i]

        wb.save()
        wb.close()
        app.quit()

