# nu-schedule 0.2 alpha #

This is a simple GUI application, which utilizes the power of Python, to help NU students with the time-consuming registration process.

![Optional Text](../master/res/mainscreen.png)

## How do I get set up? ##

* Setup Python 3 environment and add it to the PATH, make sure that pip package is installed.

* Install the required modules. In case of errors, run with root/admin permissions:
```
python3 -m pip install -r requirements.txt
```

* Then just run the app
```
python3 main.py
```

## TODOs ##

* HIGH: Implement __linking__ by probably filtering out the final results with a specific list or a GUI solution (binding R's together with L's for a specific teacher)

* MED: Write FAQ/usage to README

* LOW: Create a __true__ database for more robust experience? Request a fresh pdf -> db/old xlsx approach
	 
* LOW: Make a compact executable (in short, force nuitka to work)
