test_services.py 
output:
(venv) 
nerku@Kushal_Ner MINGW64 ~/OneDrive/Desktop/project/box_selection_system (main)
$ python manage.py test box_selector.test_services
Found 16 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................
----------------------------------------------------------------------
Ran 16 tests in 0.028s

OK
Destroying test database for alias 'default'...


test_api.py
output:
(venv)
nerku@Kushal_Ner MINGW64 ~/OneDrive/Desktop/project/box_selection_system (main)
$ python manage.py test box_selector.test_api
Found 11 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
C:\Users\nerku\OneDrive\Desktop\project\venv\Lib\site-packages\rest_framework\fields.py:1015: UserWarning: min_value should be an integer or Decimal instance.
  warnings.warn("min_value should be an integer or Decimal instance.")
...........
----------------------------------------------------------------------
Ran 11 tests in 0.067s

OK
Destroying test database for alias 'default'...