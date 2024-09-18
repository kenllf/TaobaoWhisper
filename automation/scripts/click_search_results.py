from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from automation.utils.yaml_file import read_common


def click_search_results(driver):
    print("开始执行 click_search_results 函数")

    common_config = read_common()

    try:
        # 等待搜索结果加载
        print("等待搜索结果加载...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item"))
        )
        print("搜索结果加载完成")

        # 查找所有"旺旺在线"链接
        wangwang_links = driver.find_elements(By.CSS_SELECTOR, "a.ww-inline.ww-online")
        print(f"找到 {len(wangwang_links)} 个'旺旺在线'链接")

        for index, link in enumerate(wangwang_links):
            print(f"处理第 {index + 1} 个'旺旺在线'链接")

            # 随机等待1-2秒
            time.sleep(random.uniform(1, 2))

            main_window = driver.current_window_handle
            link.click()
            print("点击链接，等待新窗口打开...")

            # 等待新窗口打开并切换
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            new_window = [
                window for window in driver.window_handles if window != main_window
            ][0]
            driver.switch_to.window(new_window)
            print("切换到新打开的窗口")

            # 等待页面加载完成
            print("等待页面加载完成...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("页面加载完成")

            # 查找并切换到 iframe（如果存在）
            try:
                print("查找 iframe...")
                iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                )
                driver.switch_to.frame(iframe)
                print("切换到 iframe")
            except TimeoutException:
                print("未找到 iframe，继续在主文档中查找")

            # 等待对话内容加载
            print("等待对话内容加载...")
            time.sleep(5)  # 可以根据实际情况调整等待时间

            # 查找对话框中的对话数量
            try:
                print("查找对话框中的对话...")
                message_items = driver.find_elements(
                    By.CSS_SELECTOR, "div.message-item-line"
                )
                dialogue_count = len(message_items)
                print(f"对话框中有 {dialogue_count} 句对话")
                if dialogue_count <= 1:
                    try:
                        # 查找输入框
                        input_box = driver.find_element(
                            By.CSS_SELECTOR, "div.editBox pre.edit"
                        )
                        # 输入消息内容
                        input_box.send_keys(common_config["send_content"])
                        print(f"已输入消息: {common_config['send_content']}")

                        # 模拟人类输入后的短暂停顿
                        time.sleep(random.uniform(0.5, 1.5))

                        # 查找并点击 "发送" 按钮
                        send_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "button.send-btn")
                            )
                        )
                        send_button.click()
                        print("消息已发送")
                    except Exception as e:
                        print(f"输入或发送消息时发生错误: {str(e)}")

            except Exception as e:
                print(f"查找对话框中的对话时发生错误: {str(e)}")

            # 随机等待2-4秒，模拟查看新页面
            print("随机等待2-4秒，模拟查看新页面...")
            time.sleep(random.uniform(2, 4))

            # 关闭当前窗口并切回主窗口
            try:
                print("关闭当前窗口...")
                driver.close()  # 关闭当前窗口
                driver.switch_to.window(main_window)  # 切回主窗口
                print("关闭当前窗口并切回主窗口")
            except Exception as e:
                print(f"切换窗口时发生错误: {str(e)}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

    finally:
        # 确保切回主文档
        try:
            print("切回主文档...")
            driver.switch_to.default_content()
            print("切回主文档")
        except Exception as e:
            print(f"切回主文档时发生错误: {str(e)}")

        # 随机等待0.5-1秒，模拟人类操作
        print("随机等待0.5-1秒，模拟人类操作...")
        time.sleep(random.uniform(0.5, 1))

    print("已完成所有'旺旺在线'链接的点击和交互")


# 删除 interact_with_new_page 函数
