import asyncio
from selenium import webdriver
from .config import config
from .log import log, d

# from selenium.webdriver.common.proxy import Proxy, ProxyType


async def selenium_connect(proxy_url=None, options=None):
    chromedriver_path = (
        config.selenium_prefix
        + config.selenium_host
        + ":"
        + config.selenium_port
        + config.selenium_postfix
    )
    try:
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("window-size=1280,1024")
            # options.add_argument("--headless")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            # Set preferences to disable images and videos
            prefs = {
                "profile.managed_default_content_settings.images": 2,  # Disable images
                "profile.managed_default_content_settings.media_stream": 2,  # Disable media (videos)
            }

            options.add_experimental_option("prefs", prefs)

        if proxy_url:
            options.add_argument(f"--proxy-server={proxy_url}")

        driver = webdriver.Remote(
            command_executor=chromedriver_path,
            options=options,
        )
        # Set the maximum amount of time to wait for an action to be completed
        # Set the page load timeout
        driver.set_page_load_timeout(30)

        # # Set the maximum amount of time to wait for an element to be found
        # driver.implicitly_wait(10)  # Wait for up to 10 seconds

        # # Set the maximum amount of time to wait for an asynchronous script to finish execution
        # driver.set_script_timeout(20)  # Set the script timeout to 20 seconds

        # driver = webdriver.Chrome(options=options)
        # driver.get("https://google.com")
        return driver

    except Exception as exception:
        log.warning(f"{exception}")
        return None


async def selenium_disconnect(driver):
    if driver:
        driver.quit()
