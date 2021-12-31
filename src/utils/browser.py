import base64
import json
import os
from typing import Optional

from playwright.async_api import BrowserContext, async_playwright
from playwright.async_api._generated import Playwright as AsyncPlaywright

from .config import config
from .log import logger

playwright: AsyncPlaywright
'''全局playwright进程'''

browser: Optional[BrowserContext] = None
'''全局browser'''


def get_broser() -> Optional[BrowserContext]:
    global browser
    return browser


async def close_browser():
    '''
    关闭浏览器进程
    '''
    global playwright
    global browser
    await playwright.stop()
    browser = None


async def browser_init():
    '''初始化playwright'''
    global playwright
    global browser
    log = '初始化无头浏览器……'
    logger.info(log)
    user_data_dir = config.get('path').get('data')
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=True)
    log = "无头浏览器初始化完毕！"
    logger.info(log)


async def get_html_screenshots(pagename: str, data: dict = None) -> str:
    '''
    :说明
        获取页面截图

    :参数
        * page：需要截图的页面名称，在/resources/html/目录下
        * data：需要传输的数据

    :返回
        * str：截图数据base64编码数据
    '''
    global browser
    if browser is None:
        await browser_init()

    page = await browser.new_page()
    html_path: str = config.get('path').get('html')
    url = "file://"+os.getcwd()+html_path+pagename

    # 打开页面
    await page.goto(url)

    # 注入js
    if data is not None:
        data_str = json.dumps(data, ensure_ascii=False)
        js = f"data={data_str}\nhandle(data)"
        await page.evaluate(js)

    # 截图
    await page.wait_for_load_state("networkidle")
    element_handle = await page.query_selector("#main")
    screenshot_bytes = await element_handle.screenshot(type="jpeg", quality=100)
    base64_str = base64.b64encode(screenshot_bytes)
    req_str = 'base64://'+base64_str.decode()
    await page.close()
    return req_str


async def get_web_screenshot(url: str, width: int) -> str:
    '''
    :说明
        获取网络页面截图

    :参数
        * url：网页地址
        * width：页面宽度

    :返回
        * str：截图数据base64编码数据
    '''
    global browser
    if browser is None:
        await browser_init()

    page = await browser.new_page()
    # 打开页面
    viewport_size = {
        "width": width, "height": 480
    }
    await page.set_viewport_size(viewport_size)
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    screenshot_bytes = await page.screenshot(type="jpeg", quality=100, full_page=True)
    base64_str = base64.b64encode(screenshot_bytes)
    req_str = 'base64://'+base64_str.decode()
    await page.close()
    return req_str
