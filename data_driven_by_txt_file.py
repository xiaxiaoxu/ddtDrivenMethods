#encoding=utf-8
from selenium import webdriver
import time
with open(u"e:\\数据驱动\\data.txt") as fp:
    data=fp.readlines()

driver=webdriver.Ie(executable_path="e:\\IEDriverServer")
test_result=[]
for i in range(len(data)):
    try:
        driver.get("http://www.baidu.com")
        driver.find_element_by_id("kw").send_keys(\
        data[i].split("||")[0].strip().decode("gbk"))
        driver.find_element_by_id("su").click()
        time.sleep(3)
        assert data[i].split('||')[1].strip().decode('gbk')\
        in driver.page_source
        test_result.append(data[i].strip()+u"||成功\n".encode("gbk"))
        print data[i].split('||')[0].strip().decode('gbk')+u"搜索测试执行成功"
    except AssertionError,e:
        print data[i].split('||')[1].strip().decode('gbk')+u"测试断言失败"
        test_result.append(data[i].strip()+u"||断言失败\n".encode("gbk"))
    except Exception,e:
        print data[i].split('||')[1].strip().decode('gbk')+u"测试执行失败"
        test_result.append(data[i].strip()+u"||异常失败\n".encode("gbk"))

with open(u"e:\\数据驱动\\result.txt","w") as fp:
            fp.writelines(test_result)
driver.quit()