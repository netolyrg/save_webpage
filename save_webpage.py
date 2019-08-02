# -*- coding: utf-8 -*-
from io import BytesIO

from PIL import Image

DEFAULT_IMAGE_FORMAT = 'JPEG'
DEFAULT_IMAGE_QUALITY = 80

HIDDEN_SCROLL_BAR = 'hidden'
DEFAULT_SCROLL_BAR = 'visible'


def save_webpage(driver, file_name, hide_scrollbar=True, **kwargs):
    """

    :param driver: selenium driver object
    :param file_name:
    :param hide_scrollbar:
    :param kwargs: keywords parameters to pillow save function

    :type file_name: str

    :return: name of file
    """
    # define necessary image properties
    image_options = dict()
    image_options['format'] = kwargs.get('format') or DEFAULT_IMAGE_FORMAT
    image_options['quality'] = kwargs.get('quality') or DEFAULT_IMAGE_QUALITY

    device_pixel_ratio = get_device_pixel_ratio(driver)

    # if device_pixel_ratio > 1:
    #     resize_window(driver, device_pixel_ratio)

    initial_offset = get_y_offset(driver)
    inner_height = get_inner_height(driver)
    scroll_height = get_scroll_height(driver)
    actual_page_size = scroll_height * device_pixel_ratio

    if hide_scrollbar:
        set_scrollbar(driver, HIDDEN_SCROLL_BAR)

    slices = make_screen_slices(driver, inner_height, scroll_height)

    glue_slices_into_image(slices, file_name, image_options, actual_page_size, device_pixel_ratio, inner_height,
                           scroll_height)

    # state of driver after script should to be the same as before
    if hide_scrollbar:
        set_scrollbar(driver, DEFAULT_SCROLL_BAR)

    if initial_offset != get_y_offset(driver):
        scroll_to(driver, initial_offset)

    return file_name


def get_y_offset(driver):
    y_offset_js = 'return window.pageYOffset;'
    return driver.execute_script(y_offset_js)


def glue_slices_into_image(slices, file_name, image_options, actual_page_size, device_pixel_ratio, inner_height,
                           scroll_height):
    image_file = Image.new('RGB', (slices[0].size[0], actual_page_size))

    for i, img in enumerate(slices[:-1]):
        image_file.paste(img, (0, i * inner_height * device_pixel_ratio))
    else:
        image_file.paste(slices[-1], (0, (scroll_height - inner_height) * device_pixel_ratio))

    image_file.save(file_name, **image_options)


def make_screen_slices(driver, inner_height, scroll_height):
    slices = []

    for offset in range(0, scroll_height + 1, inner_height):
        scroll_to(driver, offset)
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        slices.append(img)

    return slices


def get_scroll_height(driver):
    scroll_height_js = 'return document.body.scrollHeight;'
    return driver.execute_script(scroll_height_js)


def get_inner_height(driver):
    inner_height_js = 'return window.innerHeight;'
    return driver.execute_script(inner_height_js)


def get_device_pixel_ratio(driver):
    device_pixel_ratio_js = 'return window.devicePixelRatio;'
    return driver.execute_script(device_pixel_ratio_js)


def set_scrollbar(driver, style):
    scrollbar_js = 'document.documentElement.style.overflow = \"{}\"'.format(style)
    driver.execute_script(scrollbar_js)


def scroll_to(driver, offset):
    scroll_to_js = 'window.scrollTo(0, {});'
    driver.execute_script(scroll_to_js.format(offset))


def resize_window(driver, device_pixel_ratio):
    old_width = driver.get_window_size()['width']
    old_height = driver.get_window_size()['height']
    driver.set_window_size(old_width // device_pixel_ratio, old_height // device_pixel_ratio)
