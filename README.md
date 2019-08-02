# Save web page
Simple python function that provide you to take a whole web page screenshot from Selenium WebDriver using Pillow.

## Description

This functions save pages to files (more than 30 formats available).

I need this function for testing purposes, but I think it can be useful in another tasks.

Check work with:
* Firefox (with headless mode)
* Chrome (with headless mode)

State of driver after script will be the same as before.

## Usage
#### Simple

```
from save_webpage import save_webpage
from selenium import webdriver


driver = webdriver.Chrome('./chromedriver')
driver.get('https://github.com/about')

save_webpage(driver, 'page.jpg')

driver.quit()
```

For **windows** in headless mode don't forget about `--disable-gpu` key.
#### Hide scrollbar
By default, script hide scroll bar. But you can manually disable it
```
from save_webpage import save_webpage
from selenium import webdriver


driver = webdriver.Chrome('./chromedriver')
driver.get('https://github.com/about')

save_webpage(driver, 'page.jpg', hide_scrollbar=False)

driver.quit()

```
#### PIL keywords

```


from save_webpage import save_webpage
from selenium import webdriver

image_options = {
        "format": "JPEG",
        "quality": 80
    }

driver = webdriver.Chrome('./chromedriver')
driver.get('https://github.com/about')

save_webpage(driver, 'page.jpg', **image_options)

driver.quit()
```

In this example shows how to save image in JPEG format with 80 quality (default parameters).

This functionality provided by PIL library. For more information see [docs](http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html)

## Other
#### TODOs

- [x] Check other webdrivers support
- [ ] Add inline use (?)
