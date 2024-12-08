## 5001 final
Just a small project for 5001. We had around a month to actually work on this, in addition to other assignments. It is pretty barebones, but it has a simple GUI and performs the basic functions one would assume present in bill tracking
- Uses a sqlite3 database to store the bills
- has a few classes to deal with commonly used functions, Search, Database, and a GUI class
- under the unittesting directory there is a tests.py file that you can run all the tests from at once, with verbose output
  - Some do not have tests because they are tested through other unit tests
- Written pretty much entirely in python. It does have a requirements.txt but I think most of those are remnants from when i started it with the intention of using flask

If you are not testing on windows, you may need to install some additional packages. Since they are platform specific packages, I'm not going to list them all out, but for example, if trying to run/test on ubuntu you will most likely need to install python3-tk and sqlite via apt (if they are not already present and you are using apt for your package manager)
```bash
sudo apt install python3-tk
sudo apt install sqlite
```
You would also need to reinstall the venv if you are getting it from here. 
