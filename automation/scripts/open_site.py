from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automation.utils.driver_utils import ensure_driver
from automation.utils.yaml_file import read_common
import time
import random
from automation.scripts.click_search_results import click_search_results


def human_like_type(element, text):
    # 模拟人类输入
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # 更自然的输入间隔


def human_like_scroll(driver, scroll_amount):
    # 模拟人类滚动
    for _ in range(scroll_amount // 100):  # 每次滚动100像素
        driver.execute_script(f"window.scrollBy(0, {random.randint(80, 120)});")
        time.sleep(random.uniform(0.1, 0.3))


def open_site():
    start_time = time.time()

    driver = ensure_driver()
    common_config = read_common()  # 读取配置文件
    site = common_config["site"]
    driver.get(site)

    load_time = time.time()
    print(f"页面加载时间: {load_time - start_time:.2f} 秒")

    # 随机等待一段时间,模拟页面加载和人类反应时间
    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)
    print(f"初始等待时间: {wait_time:.2f} 秒")

    # 找到搜索输入框
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "q"))
    )

    # 模拟鼠标移动到搜索框
    actions = ActionChains(driver)
    actions.move_to_element(search_input).perform()
    move_time = random.uniform(0.3, 0.8)
    time.sleep(move_time)

    # 点击搜索框
    search_input.click()
    time.sleep(random.uniform(0.2, 0.5))

    # 清除输入框内容
    search_input.clear()
    time.sleep(random.uniform(0.1, 0.3))

    # 模拟人类输入
    human_like_type(search_input, common_config["search_keyword"])

    # 随机等待一下,模拟思考时间
    time.sleep(random.uniform(0.5, 1.5))

    # 查找并点击搜索按钮
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn-search[type='submit']")
        )
    )
    actions.move_to_element(search_button).perform()
    time.sleep(random.uniform(0.2, 0.5))
    search_button.click()

    print(f"搜索关键词: {common_config['search_keyword']}")

    # 等待搜索结果加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.item"))
    )

    # 模拟浏览搜索结果
    human_like_scroll(driver, random.randint(300, 700))

    # 处理搜索结果和翻页
    max_pages = common_config.get("max_pages", 5)  # 默认最多处理5页
    current_page = 1

    while current_page <= max_pages:
        print(f"正在处理第 {current_page} 页")
        click_search_results(driver)

        # 检查是否有下一页
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next",
                    )
                )
            )

            # 检查是否是最后一页
            if "next-disabled" in next_button.get_attribute("class"):
                print("已经是最后一页，停止处理")
                break

            # 模拟人类滚动到下一页按钮
            actions.move_to_element(next_button).perform()
            human_like_scroll(driver, random.randint(200, 500))
            time.sleep(random.uniform(1, 2))

            next_button.click()
            print("点击下一页")

            # 等待新页面加载
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
            print("新页面加载完成")

            current_page += 1

            # 随机等待1-3秒，模拟人类行为
            time.sleep(random.uniform(1, 3))

            # 模拟人类滚动
            human_like_scroll(driver, random.randint(200, 500))

        except Exception as e:
            print(f"点击下一页或等待新页面加载时发生错误: {str(e)}")
            break

    end_time = time.time()
    total_time = end_time - start_time
    print(f"总执行时间: {total_time:.2f} 秒")

    driver.quit()
