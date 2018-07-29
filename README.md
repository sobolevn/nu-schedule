# nu-schedule 0.22 #

This is a simple GUI application (with support of any system that can run Python 3 and PyQt), which utilizes the power of Python, to help NU students with the time-consuming registration process. [Example report](https://github.com/ac130kz/nu-schedule/blob/master/examples/result1532841466.735346.txt?raw=true).

<p align="center">
  <img src="https://github.com/ac130kz/nu-schedule/blob/master/res/mainscreen.png?raw=true" alt="GUI"/>
</p>

## How to run? ##

* Setup <a href="https://www.python.org/downloads/">Python 3</a> environment and add it to the PATH (a checkbox during the installation on Windows), sometimes you want to make sure that pip package is installed.

* Download and unzip this repository or clone it.

* Install the required modules. In case of errors, run with root/admin permissions:
```bash
python3 -m pip install -r requirements.txt
```
* Then just run the app from the console:
```bash
python3 main.py
```

## FAQ ##

1. Get a clearly formatted xlsx/xls with courses for this I recommend a program called [PDF2XL](https://www.cogniview.com/download), have a look at the sample lists in /samples. To make your own list, open the pdf in PDF2XL, select tables one by one, split and merge vertically where appropriate (again check the samples), right click the selection - select __Table Structure__ - then __Create rows between column text__. This will automatically do the difficult part. Finally, convert this table and add its contents to your new list.
2. Select your prepared xlsx/xls file with the |Open| button, to load the courses into the app
3. With |Edit| button access the selection menu, added courses will appear on the Main window.
4. Use |Generate| button to generate and save your schedule as result<unixtimestamp>.txt

## TODOs/Known issues ##

- [ ] Implement __linking__ by probably filtering out the final results with a specific list or a GUI solution (binding R's together with L's for a specific teacher)

- [ ] Implement a fix for courses with complex schedule (separate entries)
	 
- [ ] Make a compact executable (in short, force nuitka to work)

- [ ] Get rid of manual creation of xslx (use PDFMiner) and always get the latest pdf (use requests)/Create a __true__ database for more robust experience? Request a fresh pdf -> db/old xlsx approach
