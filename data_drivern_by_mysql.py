# encoding=utf-8
from selenium import webdriver
import unittest, time
import logging, traceback
import ddt
from MysqlUtil import MyMySQL
from selenium.common.exceptions import NoSuchElementException

# 初始化日志对象
logging.basicConfig(
    # 日志级别
    level = logging.INFO,
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    # 打印日志的时间
    datefmt = '%a, %Y-%m-%d %H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename = 'e:/dataDriveRreport.log',
    # 打开日志文件的方式
    filemode = 'w'
)

def getTestDatas():
    db = MyMySQL(
        host="localhost",
        port=3306,
        dbName="gloryroad",
        username="root",
        password="gloryroad",
        charset="utf8"
    )
    # 从数据库测试表中获取测试数据
    testData = db.getDataFromDataBases()
    # 关闭数据库连接
    db.closeDatabase()
    return testData

@ddt.ddt
class TestDemo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Ie(executable_path = "e:\\IEDriverServer")

    @ddt.data(*getTestDatas())
    def test_dataDrivenByDatabase(self, data):
        # 对获得的数据进行解包
        testData, expectData = data
        url = "http://www.baidu.com"
        # 访问百度首页
        self.driver.get(url)
        # 将浏览器窗口最大化
        self.driver.maximize_window()
        print testData, expectData
        # 设置隐式等待时间为10秒
        self.driver.implicitly_wait(10)
        try:
            # 找到搜索输入框，并输入测试数据
            self.driver.find_element_by_id("kw").send_keys(testData)
            # 找到搜索按钮，并点击
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            # 断言期望结果是否出现在页面源代码中
            self.assertTrue(expectData in self.driver.page_source)
        except NoSuchElementException, e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："\
                          + str(traceback.format_exc()))
        except AssertionError, e:
            logging.info(u"搜索“%s”，期望“%s”，失败" %(testData, expectData))
        except Exception, e:
            logging.error(u"未知错误，错误信息：" + str(traceback.format_exc()))
        else:
            logging.info(u"搜索“%s”，期望“%s”通过" %(testData, expectData))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
