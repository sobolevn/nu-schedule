# nu-schedule 0.3 #

This is a simple GUI application (with support of any system that can run Python 3 and PySide2), which utilizes the power of Python, to help NU students with the time-consuming registration process. [Example report](https://github.com/ac130kz/nu-schedule/blob/master/examples/result1532841466.735346.txt?raw=true).

<p align="center">
  <img src="https://github.com/ac130kz/nu-schedule/blob/master/res/mainscreen.png?raw=true" alt="GUI"/>
</p>

## How to run? ##

* Setup <a href="https://www.python.org/downloads/">Python 3</a> environment and add it to the PATH (a checkbox during the installation on Windows), sometimes you want to make sure that `pip` package is installed.

* Download and unzip this repository or clone it.

* Install the required modules. In case of errors, run with root/admin permissions:
```bash
python -m pip install --upgrade -r requirements.txt
```
* Then just run the app from the console:
```bash
python main.py
```

## How to use? ##

1. Press |Load| to get the latest version of the Undergradute data for the current semester.
2. With |Edit| button access the selection menu, added courses will appear on the Main window.
3. Use |Generate| button to generate and save your schedule as result<unixtimestamp>.txt

## TODOs/Known issues ##

- [ ] Implement __linking__ by probably filtering out the final results with a specific list or a GUI solution (binding R's together with L's for a specific teacher)

- [ ] Implement a fix for courses with complex schedule (separate entries)
	 
- [ ] Make a compact executable (in short, force nuitka to work)
