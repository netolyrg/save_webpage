# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import BytesIO
from PIL import Image


DEFAULT_IMAGE_EXTENSION = "JPEG"
DEFAULT_IMAGE_QUALITY = 80


TIME_TO_WAIT = 6


def save_webpage(driver_path, url, file_name, options=None, cookies=None, image_options=None):
    """

    :param driver_path: path to webdriver
    :param url:
    :param file_name:
    :param options: browser options
    :param cookies: list of additional cookies
    :param image_options: contains information about output file quality and extension
    :type url: str
    :type file_name: str
    :type cookies: list
    :type image_options: dict
    :return: name of file if all is OK
    """

    # necessary javascript
    device_pixel_ratio_js = "return window.devicePixelRatio"
    scroll_height_js = "return document.body.scrollHeight"
    inner_height_js = "return window.innerHeight"
    scroll_to_js = "window.scrollTo(0, {})"

    # define necessary image properties
    if image_options is None:
        image_options = {}
    image_extension = image_options.get("extension") or DEFAULT_IMAGE_EXTENSION
    image_quality = image_options.get("quality") or DEFAULT_IMAGE_QUALITY

    # if have browser options - just add it
    chrome_options = Options()
    if options:
        for option in options:
            logger.debug("adding {} option".format(option))
            chrome_options.add_argument(option)

    driver = webdriver.Chrome(
        executable_path=driver_path,
        options=chrome_options
    )

    driver.get(url)

    # set cookies
    if cookies:
        for cookie in cookies:
            driver.add_cookie(cookie)

        # we need to 'activate' cookies
        driver.refresh()

    # TODO do better wait
    driver.implicitly_wait(TIME_TO_WAIT)

    inner_height = driver.execute_script(inner_height_js)
    scroll_height = driver.execute_script(scroll_height_js)
    device_pixel_ratio = driver.execute_script(device_pixel_ratio_js)

    # hide scrollbar coz it's lame
    driver.execute_script("document.documentElement.style.overflow = 'hidden'")

    actual_page_size = scroll_height*device_pixel_ratio

    slices = []

    for offset in range(0, scroll_height+1, inner_height):
        driver.execute_script(scroll_to_js.format(offset))
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        slices.append(img)

    # create image
    screenshot = Image.new('RGB', (slices[0].size[0], actual_page_size))

    for i, img in enumerate(slices[:-1]):
        screenshot.paste(img, (0, i * inner_height * device_pixel_ratio))
    else:
        screenshot.paste(slices[-1], (0, (scroll_height - inner_height) * device_pixel_ratio))

    screenshot.save(file_name, image_extension, quality=image_quality, optimize=True, progressive=True)
    driver.quit()

    return file_name
