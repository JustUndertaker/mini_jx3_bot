from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator, Optional

import jinja2
from playwright.async_api import Browser, Error, Page, async_playwright

from .config import config
from .log import logger


class MyBrowser():
    '''自定义浏览类'''
    _browser: Optional[Browser] = None
    _playwright = None
    _template_env: jinja2.Environment
    _base_url: str = None

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(MyBrowser, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    async def _launch_browser(self, **kwargs) -> Browser:
        return await self._playwright.chromium.launch(**kwargs)

    async def _get_browser(self, **kwargs) -> Browser:
        return self._browser or await self.init(**kwargs)

    @asynccontextmanager
    async def _get_new_page(self, **kwargs) -> AsyncIterator[Page]:
        browser = await self._get_browser()
        page = await browser.new_page(**kwargs)
        try:
            yield page
        finally:
            await page.close()

    async def _install_browser(self):
        '''安装浏览器'''
        logger.info("未检测到浏览器，正在安装 chromium……")
        import sys

        from playwright.__main__ import main
        sys.argv = ['', 'install', 'chromium']
        try:
            main()
        except SystemExit:
            pass

    async def _html_to_pic(self, pagename: str, html: str, wait: int = 0) -> bytes:
        """
        :说明
            html转图片

        :参数
            * pagename: 页面名称
            * html (str): html文本
            * wait (int, optional): 等待时间. Defaults to 0.

        :返回
            * bytes: 图片, 可直接发送
        """
        async with self._get_new_page(base_url=self._base_url) as page:
            await page.goto(pagename)
            await page.set_content(html, wait_until="networkidle")
            await page.wait_for_timeout(wait)
            element_handle = await page.query_selector("#main")
            img_raw = await element_handle.screenshot(type="jpeg", quality=100)
        return img_raw

    async def _template_to_html(self, template_name: str, **kwargs,) -> str:
        """
        :说明
            使用jinja2模板引擎通过html生成图片

        :参数
            * template_name (str): 模板名
            * **kwargs: 模板内容

        :返回
            * str: html
        """

        template = self._template_env.get_template(template_name)

        return await template.render_async(**kwargs)

    async def init(self) -> Browser:
        '''初始化playwright'''
        template_path = config.path['templates']
        path = Path(template_path).absolute()
        self._base_url = f"file://{path}/"
        self._playwright = await async_playwright().start()
        self._template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            enable_async=True,
        )
        try:
            self._browser = await self._launch_browser()
        except Error:
            await self._install_browser()
            self._browser = await self._launch_browser()
        return self._browser

    async def shutdown(self):
        '''关闭浏览器'''
        await self._browser.close()
        await self._playwright.stop()

    async def template_to_image(self, pagename: str, **kwargs) -> bytes:
        '''
        :说明
            将模板页面转化成图片

        :参数
            * pagename：模板文件名
            * **kwargs：注入的数据

        :返回
            * bytes：图片数据
        '''

        html = await self._template_to_html(template_name=pagename, **kwargs)
        return await self._html_to_pic(pagename, html)

    async def get_image_from_url(self, url: str, width: int) -> bytes:
        '''从url获取截图'''
        async with self._get_new_page() as page:
            viewport_size = {
                "width": width, "height": 480
            }
            await page.set_viewport_size(viewport_size)
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            return await page.screenshot(type="jpeg", quality=100, full_page=True)


browser = MyBrowser()
"""
浏览器模块，使用playwright控制浏览器截图，使用方法：
```
from src.utils.browser import browser

>>>await browser.init() # 初始化浏览器，使用前请先初始化
>>>await browser.template_to_image(pagename,**kwargs) # 模板截图，kwargs为截图参数
>>>await browser.get_image_from_url(url,width) # 从url获取图片，width为截图宽度
>>>await browser.shutdown() # 关闭浏览器
```
"""
