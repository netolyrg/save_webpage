# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import BytesIO
from PIL import Image


DEFAULT_IMAGE_FORMAT = "JPEG"
DEFAULT_IMAGE_QUALITY = 80


TIME_TO_WAIT = 6


def save_webpage(driver_path, url, file_name, options=None, cookies=None, **image_options):
    """

    :param driver_path: path to google chrome driver
    :param url: valid url
    :param file_name:
    :param options: browser options
    :param cookies: list of additional cookies
    :param image_options: keywords parameters to pillow save function
    :type url: str
    :type file_name: str
    :type cookies: list
    :type image_options: dict
    :return: name of file
    """

    # necessary javascript
    device_pixel_ratio_js = "return window.devicePixelRatio"
    scroll_height_js = "return document.body.scrollHeight"
    inner_height_js = "return window.innerHeight"
    scroll_to_js = "window.scrollTo(0, {})"

    # define necessary image properties
    image_options["format"] = image_options.get("format") or DEFAULT_IMAGE_FORMAT
    image_options["quality"] = image_options.get("quality") or DEFAULT_IMAGE_QUALITY

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

    screenshot.save(file_name, **image_options)
    driver.quit()

    return file_name
