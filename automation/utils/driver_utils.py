import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from automation.utils.yaml_file import read_common

common_config = read_common()

driver = None


def is_driver_alive(driver):
    try:
        # 尝试访问当前窗口，如果失败则说明 driver 已经失效
        driver.current_window_handle
        return True
    except (NoSuchWindowException, WebDriverException):
        return False


def ensure_driver():
    global driver
    if driver is None or not is_driver_alive(driver):
        # 关闭现有的 driver（如果存在）
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

        # 初始化 driver
        # 启动浏览器驱动服务
        service = selenium.webdriver.chrome.service.Service(
            common_config["service_location"]
        )
        # Chrome 的调试地址
        debugger_address = common_config["debugger_address"]
        # 创建Chrome选项，重用现有的浏览器实例
        options = selenium.webdriver.chrome.options.Options()
        options.page_load_strategy = (
            "normal"  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
        )
        options.add_experimental_option("debuggerAddress", debugger_address)
        # 使用服务和选项初始化WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(10)  # 设置隐式等待时间为 10 秒

    return driver
