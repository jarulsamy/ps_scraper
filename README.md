# PS_Scraper
## Laramie High School Powerschool Scraper

<img src=ps_logo.jpg width=100 height=100 align="middle"> <img src="lhs_logo.jpg" width=100 height =100 align='middle'>

This CLI software will query the Albany County School District #1 Powerschool website and write student grades to an Excel document.


[![Build Status](https://travis-ci.org/jarulsamy/ps_scraper.svg?branch=master)](https://travis-ci.org/JoshuaA9088/ps_scraper.svg?branch=master)

---

## Usage

### Option 1: Windows Only Release Executable
Download the latest version from the releases tab. Double-click on the executable and enter your username and password. Note, Windows may sound a firewall warning, this can be safely ignored.

> By default, if no output directory is specified, a Downloads folder containing the HTML files for each class will be created and auto deleted. If the folder, for some reason, is not automatically deleted, it can be safely discarded after run completion.

### Option 2: Clone and Run With Python (Windows, OSX, Linux)

Clone this repo to your local machine using `https://github.com/JoshuaA9088/ps_scraper`

#### Setup

This software is only compatible with **Python 3.6** or greater.

Install the required dependencies using the `requirements.txt` file.

```
pip install -r requirements.txt
```

> **Selenium** is required for this application when running with python. Please install selenium and the **Chrome Driver**. Add to your platform specific PATH based on the [Selenium Documentation](https://selenium-python.readthedocs.io/index.html).

#### Run

Call the python script `main.py` and enter your powerschool username and password to grab HTML files and create Excel workbook.

> By default, if no output directory is specified, a Downloads folder containing the HTML files for each class will be created and auto deleted. This folder can be preserved with the `-nc` flag. If the folder, for some reason, is not automatically deleted, it can be safely discarded after run completion.

---

## Contributing

To get started...

### Step 1

- **Option 1**
    - 🍴 Fork this repo!
- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/JoshuaA9088/ps_scraper`

### Step 2
- **HACK AWAY!** 🔨🔨🔨

### Step 3
- 🔃 Create a new pull request using <a href="https://github.com/JoshuaA9088/ps_scraper" target="_blank">`https://github.com/JoshuaA9088/ps_scraper`</a>.
---

## Support

Reach out to me at one of the following places!

- Email (Best) at joshua.gf.arul@gmail.com
- Twitter at <a href="http://twitter.com/joshuaa9088" target="_blank">`@joshuaa9088`</a>

---
