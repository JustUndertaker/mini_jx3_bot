from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

import jinja2
from playwright.async_api import Browser, Error, Page, async_playwright

from .config import config
from .log import logger

TEMPLATES_PATH: str = config.path['templates']

env = jinja2.Environment(
    extensions=["jinja2.ext.loopcontrols"],
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    enable_async=True,
)


class MyBrowser():
    '''自定义浏览类'''
    _browser: Optional[Browser] = None
    _playwright = None

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(MyBrowser, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

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

    async def _html_to_pic(self, html: str, wait: int = 0, **kwargs) -> bytes:
        """
        :说明
            html转图片

        :参数
            * html (str): html文本
            * wait (int, optional): 等待时间. Defaults to 0.

        :返回
            * bytes: 图片, 可直接发送
        """
        async with self._get_new_page(**kwargs) as page:
            await page.set_content(html, wait_until="networkidle")
            await page.wait_for_timeout(wait)
            img_raw = await page.screenshot(type="jpeg", quality=100)
        return img_raw

    @classmethod
    async def _template_to_html(cls, template_path: str, template_name: str, **kwargs,) -> str:
        """
        :说明
            使用jinja2模板引擎通过html生成图片

        :参数
            * template_path (str): 模板路径
            * template_name (str): 模板名
            * **kwargs: 模板内容

        :返回
            * str: html
        """

        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            enable_async=True,
        )
        template = template_env.get_template(template_name)

        return await template.render_async(**kwargs)

    async def init(self):
        '''初始化playwright'''
        self._playwright = await async_playwright().start()
        try:
            self._browser = await self._launch_browser()
        except Error:
            await self._install_browser()
            self._browser = await self._launch_browser()

    async def shutdown(self):
        '''关闭浏览器'''
        await self._browser.close()
        await self._playwright.stop()

    async def template_to_image(self, pagename: str, **kwargs) -> bytes:
        '''
        :说明
            将页面转化成图片

        :参数
            * pagename：模板文件名
            * **kwargs：注入的数据

        :返回
            * bytes：图片数据
        '''

        html = await self._template_to_html(template_path=TEMPLATES_PATH, template_name=pagename, **kwargs)
        return await self._html_to_pic(html)


browser = MyBrowser()
'''全局浏览器'''
