# nu-schedule 0.2 alpha #

This is a simple GUI application (with support of any system that can run Python 3 and PyQt), which utilizes the power of Python, to help NU students with the time-consuming registration process.

<p align="center">
  <img src="https://github.com/ac130kz/nu-schedule/blob/master/res/mainscreen.png?raw=true" alt="GUI"/>
</p>

## Example report ##

<a href="https://github.com/ac130kz/nu-schedule/blob/master/examples/result1511188563.txt?raw=true">
<p align="center">
  Right here!
</p>
</a>

## How do I get set up? ##

* Setup <a href="https://www.python.org/downloads/">Python 3</a> environment and add it to the PATH (a checkbox during the installation), sometimes you want to make sure that pip package is installed.

* Install the required modules. In case of errors, run with root/admin permissions:
```
python3 -m pip install -r requirements.txt
```
* Download and unzip this repository or clone it.

* Then just run the app from the console:
```
python3 main.py
```

## TODOs ##

* HIGH: Implement __linking__ by probably filtering out the final results with a specific list or a GUI solution (binding R's together with L's for a specific teacher)

* MED: Write FAQ/usage to README

* LOW: Create a __true__ database for more robust experience? Request a fresh pdf -> db/old xlsx approach
	 
* LOW: Make a compact executable (in short, force nuitka to work)
