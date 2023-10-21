---------
SDK Features
---------
* This package allows user to get list of all files in a specific workspace and project.
* This package allows user to upload the data to Catalyst Storage for a specific workspace and project.
 
---------
Prerequisite
---------
* User should be an active user of Catalyst AI.
* User should have a valid API key.
* User should specify the worksapce and project that he/she is looking for file details or file upload.

-----------
Build Guidelines
-----------
* To build module/package 
    * Add "setup.py" file in the base directory.
        * The setup.py file will contain information about your package, specifically the name of the package, its version platform-dependencies and a whole lot more.
    * Run "python setup.py sdist bdist_wheel" command in the base directory.
        * This will build all the necessary packages that Python will require. The sdist and bdist_wheel commands will create a source distribution and a wheel that you can later upload to PyPi.
    * Run "twine upload dist/*" (assuming twine is installed).
        * This command will upload the contents of the dist folder that was automatically generated when we ran python setup.py. You will get a prompt asking you for your PyPi username and password, so go ahead and type those in.

* To build module in local 
    * Run "py -m pip install -e ." command in the base directory. 
