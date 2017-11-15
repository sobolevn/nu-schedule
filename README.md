# nu-schedule 0.0.2 #

This is a simple GUI application which utilizes the power of Python to help NU students with the time-consuming registration process.

## How do I get set up? ##

* Setup Python 3 environment and add it to the PATH, pip package installed.

* Install the required modules. In case of errors, run with root/admin permissions:
```
pip3 install -r requirements.txt
```

* Then just run the app
```
python3 main.py
```

## TODOs ##

* Implement "linking" (binding R's together with L's for a specific teacher) 
	// Probably filter out the final results with a specific list or a GUI solution
* Help and about windows fun
* Improve database creation (mainly dealing with slow parser engine)
	
	// Multithreading???
	
	// True db???
	
	// without PM: pip install ciso8601 (https://github.com/closeio/ciso8601) (https://hack.close.io/posts/ciso8601) https://stackoverflow.com/questions/13468126/a-faster-strptime http://ze.phyr.us/faster-strptime/
	 
* Make a compact executable (in short, force nuitka to work)
