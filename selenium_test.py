import asyncio
from selenium import webdriver
from config import config
from log import log, d

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
                "profile.default_content_setting_values.notifications": 2,
            }
            # Disable bundled Flash plugin and extensions
            options.add_argument("--disable-bundled-ppapi-flash")
            # options.add_argument("--disable-extensions")

            options.add_experimental_option("prefs", prefs)

            # options.add_argument("--disable-gpu")
            # options.add_argument("--disable-hardware-acceleration")
            # options.add_argument("--disable-logging")
            # options.add_argument("--disable-javascript")
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


async def test():
    driver = None
    try:
        driver = await selenium_connect()
        if not driver is None:
            # driver.get("https://app.slack.com/client/T03HT68PM7Z/C03JLDW6WQH")
            driver.get(
                "https://andreydmitr21.slack.com/sign_in_with_password?redir=%2Fgantry%2Fauth%3Fapp%3Dclient%26lc%3D1701551065%26return_to%3D%252Fclient%252FT03HT68PM7Z%252FC03JLDW6WQH%26teams%3D"
            )
            while True:
                await asyncio.sleep(1)
    finally:
        await selenium_disconnect(driver)


if __name__ == "__main__":
    asyncio.run(test())
