# PS_Scraper
## Powerschool Scraper

<img src=ps_logo.jpg width=100 height=100 align="middle">

This CLI software will query any Powerschool website and write student grades to an Excel document.

[![Build Status](https://travis-ci.org/jarulsamy/ps_scraper.svg?branch=master)](https://travis-ci.org/jarulsamy/ps_scraper.svg?branch=master)

---

## Usage

### Option 1: Windows Only Release Executable
Download the latest version from the releases tab. Double-click on the executable and enter your username and password. Note, Windows may sound a firewall warning, this can be safely ignored.

> **Selenium** is required for this application when running with python. Please install selenium and the **Firefox Gecko Webdriver**. Add it to your platform specific PATH based on the [Selenium Documentation](https://selenium-python.readthedocs.io/index.html).


### Option 2: Clone and Run With Python (Windows, OSX, Linux)

Clone this repo to your local machine using `https://github.com/jarulsamy/ps_scraper`

#### Setup

This software is only compatible with **Python 3.6** or greater.

Install the required dependencies using the `requirements.txt` file.

```
pip install -r requirements.txt
```

> **Selenium** is required for this application when running with python. Please install selenium and the **Firefox Gecko Webdriver**. Add it to your platform specific PATH based on the [Selenium Documentation](https://selenium-python.readthedocs.io/index.html).

#### Run

Call the python script `main.py` and enter your powerschool username and password to create an Excel workbook.

---

## Support

Reach out to me at one of the following places!

- Email (Best) at joshua.gf.arul@gmail.com
- Twitter at <a href="http://twitter.com/joshuaa9088" target="_blank">`@joshuaa9088`</a>

---
