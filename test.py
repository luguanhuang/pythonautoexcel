# import datetime
 
# def int_to_time(timestamp):
#     return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
 
# # 示例
# timestamp = 1617186877
# time_str = int_to_time(timestamp)
# print(time_str)  # 输出: 2021-03-31 14:47:57


# if "1" in "1234":
#     print("i am here")

# a = [1,2,3,4,5,6,7,8]
# for i in range(len(a)):
#     if i == 5 or i == 2:
#         if i==5:
#         #  print("i=", 5)
#             a.remove(8)
#         elif i==2:
#             a.remove(7)
#     else:
#        pass

#     # print(a)

# # for i in a:
# print(a)


# array = [1, 2, 3, 4, 5]
 
# # 我们想删除所有索引为奇数的元素
# indices_to_remove = [i for i in range(len(array)) if i == 1]
 
# # 使用列表推导式创建一个不包含要删除元素的新数组
# array = [item for i, item in enumerate(array) if i not in indices_to_remove]
 
# print(array)  # 输出将会是 [1, 3, 5]




# my_dict = {"a": 1, "b": 2, "c": 3}
# key_count = len(my_dict)
# print("len=", key_count)

# my_dict = {'a': 1, 'b': 2, 'c': 3}

# # 直接使用next()函数取得第一个元素
# first_element = next(iter(my_dict))

# print(first_element)
# print(my_dict[first_element])


# import win32com.client as win32
# import win32com
# # excel = win32.gencache.EnsureDispatch('Excel.Application')
# # wb = excel.Workbooks.Open('d:/20240811.xlsx')
# # ws = wb.ActiveSheet
# # display_headings = ws.DisplayHeadings
# # # excel.DisplayHeadings = True
# # # excel.DisplayWorkbookTabs = True
# # wb.Save()
# # wb.Close()
# # excel.Quit()


# # 假设你正在尝试操作的对象是 Excel Application
# excel_app = win32com.client.Dispatch("Excel.Application")
 
# # 使用 dir() 查看所有可用的属性和方法
# print(dir(excel_app))
 



# import win32com.client as win32
 
# excel = win32.gencache.EnsureDispatch('Excel.Application')
# wb = excel.Workbooks.Open('d:/20240811.xlsx')
# ws = wb.Worksheets('Sheet1')
 
# # 隐藏页眉和页脚
# excel.DisplayHeadings = False
# excel.DisplayWorkbookTabs = False
 
# wb.Save()
# wb.Close()
# excel.Quit()



# import win32com.client

# # 启动Excel
# excel = win32com.client.Dispatch("Excel.Application")
 
# # 打开一个Excel工作簿
# workbook = excel.Workbooks.Open('d:/20240811.xlsx')
 
# # 获取活动的工作表
# sheet = workbook.ActiveSheet
 
# # 获取DisplayHeadings的值
# display_headings = sheet.DisplayHeadings
# print(f"DisplayHeadings is {'On' if display_headings else 'Off'}.")
 
# # 关闭Excel工作簿，不保存更改
# workbook.Close(SaveChanges=False)
 
# # 退出Excel应用程序
# excel.Quit()



import win32com.client as win32
 
# 启动Excel应用程序
excel = win32.gencache.EnsureDispatch('Excel.Application')
 
# 打开一个现有的工作簿
wb = excel.Workbooks.Open(r'd:/20240811.xlsx')
 
# 设置工作簿视图为页面布局
wb.ActiveSheet.PageSetup.Zoom = 100  # 设置缩放比例为100%
# wb.ActiveSheet.PageSetup.PaperSize = xlPaperA4  # 设置纸张大小为A4
wb.ActiveSheet.PageSetup.FitToPagesWide = 1  # 设置宽度适应一页
wb.ActiveSheet.PageSetup.FitToPagesTall = 1  # 设置高度适应一页
 
# 保存工作簿，注意这里不是直接保存为页面布局视图模式，而是通过调整页面设置
wb.Save()
 
# 关闭工作簿，不保存
wb.Close(SaveChanges=False)
 
# 退出Excel应用程序
excel.Quit()