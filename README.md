# Save web page
Simple python function that let you save a whole web page using Selenium and Pillow libraries.

## Description

This functions save pages to files (more than 30 formats available) and support cookies and browser options such as `--headless` and others.

I need this function for testing purposes, but I think it can be useful in another tasks.

It perfectly works in headless mode on macOS High Sierra 10.13 with Google Chrome 64.
And works with headless mode on Windows 10 with Google Chrome 64.


## Usage
#### Simple

```
save_webpage(
    "path/to/driver",
    "https://google.com/",
    "google.jpg"
    )
```

it's simple usage of function. In your folder you found google.jpg image of whole google.com page.

#### Additional browser options support

```
options = ["--headless", "--window-size=1280, 720"]

save_webpage(
    "path/to/driver",
    "https://google.com/",
    "google.jpg",
    options=options
    )
```

In this example chrome starts in headless mode with window size 1280x720.

For **windows** in headless mode don't forget about `--disable-gpu` key.

#### Cookies support

```
cookies = [
    {
        "name": "some_cookie_name",
        "value": "some_cookie_value",
        "domain": "some_domain.com"
    }
        ]

save_webpage(
    "path/to/driver",
    "https://google.com/",
    "google.jpg",
    cookies=cookies
    )
```

This example shows how to load page with cookies.

Actually, it load page, add cookies and then reload page. This happens due to selenium specific behavior. For addition information about selenium and cookies see [docs](http://www.seleniumhq.org/docs/03_webdriver.jsp).

#### PIL keywords

```
image_options = {
        "format": "JPEG",
        "quality": 80
    }

save_webpage(
    "path/to/driver",
    "https://google.com/",
    "google.jpg",
    **image_options
    )
```

In this example shows how to save image in JPEG format with 80 quality (default parameters).

This functionality provided by PIL library. For more information see [docs](http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html)

#### Retina

If you using retina display and `--window-size` option, set it to half of your requirements. Otherwise your resulting pictures' resolution will be twice bigger.

For example:

```

options = ["--window-size=2560//2, 1600//2"]
```

This required because of retina display pixel ratio (==2).

## Other
#### TODOs

- [ ] Add other webdrivers support
- [x] Fix image_options
- [ ] Make simple retina display support
- [ ] Add inline use (?)
