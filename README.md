# Save web page
Simple python function that provide you to take a whole web page screenshot from Selenium WebDriver using Pillow.

## Description

This functions save pages to files (more than 30 formats available).

I need this function for testing purposes, but I think it can be useful in another tasks.
``
It perfectly works in headless mode on macOS Mojave 10.14 with Google Chrome 75, 
on macOS High Sierra 10.13 with Google Chrome 64 and on Windows 10 with Google Chrome 64.

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

- [ ] Check other webdrivers support
- [ ] Add inline use (?)
