## 天眼查爬虫说明文档
### 1.    环境搭建(windows)
  环境：Python3 + Selenium + Firefox火狐浏览器
  搭建：
  1）选择好python3的开发环境
  2)安装python所需要的包，在TYC文件目录下，
  windows下 在cmd中执行 pip freeze –r requirments.txt
  3)把 TYC目录下geckodriver.exe文件复制到火狐浏览器的安装目录
### 2.    目录结构（必须要有的目录结构，以下目录请勿更改，可创建其他目录自用）
    TYC-----------------------
    |--cookies（用户登陆信息）
    |
                   |--data（爬取数据存放）
                   |
                   |--excel（excel表格文件）
                   |
                   |--log--------------（log存放处，err 和 exception）
                   |                           |
                   |                           |--fail（没有成功获取的公司）
                   |
                   |--spiders（爬虫文件**请勿更改）
### 3.操作步骤
  1）        首次使用请运行set_cookie.py文件，建立新的用户数据
  2）        修改excel表格路径，先把表格文件放入到excel目录下。在tyc_companys.py中 最后，修改表格文件的全称例：companys.xlsx
  或者直接将excel文件名更改成companys.xlsx
  3）        Excel目录存放excel表格文件，要求表格的所有数据放在第一列且无头（第一行也为数据，没有标题）
  4）        运行命令 python  (爬虫文件绝对路径)
  例python C:\Users\45890\Desktop\TYC\spiders\tyc_company.py
  5）        当运行到，弹出百度的页面时，说明爬虫出现了问题。可能遇到了验证码，请按照提示，打开爬虫的页面，手动点击验证码，完成后在程序的提示页面（下面输入框）输入任意字符，按enter键继续
