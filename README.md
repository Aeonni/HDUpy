# HDUpy

> ⚠️ This version of HDUpy won't be able to login due to the update of iHDU login page. Please use [HDUpy_v2](https://github.com/Aeonni/HDUpy_v2) instead.

#### There are 2 parts in 'Hdupy'
- ihdu.py , The API code
- tools.py , Some functions you can use with the API

#### **Examples:**
```Python
# Normal Operations

from Hdupy import ihdu

u = ihdu.User('userID', 'password')
u.login()
# Some get & post operations
u.Logout()
```
```Python
# Get your calendar

from Hdupy import ihdu
from Hdupy import tools

u = ihdu.User('userID', 'password')
u.login()

filename = '/your/path/Cal.ics'
tools.GetCal(u,'20170918').save(filename)

u.Logout()
```


### ihdu.py
- Class User
    - Every object will maintain a `requests.session()` object in it's lifetime.
    - **Main functions:**
    ```Python
    __init__(self, usn, pwd)
    ```
    ```Python
    login(self)
    ```
    ```Python
    Logout(self)
    ```
    ```Python
    get(self, url, **kwargs)
    # The same as requests.session.get()
    ```
    ```Python
    post(self, url, data=None, json=None, **kwargs)
    # The same as requests.session.post()
    ```
    - **Other functions:**
    ```Python
    gotoSubPage(self, index)
    ```
    ```Python
    gotoPage(self, index)
    ```
    ```Python
    BackHome(self)
    ```
    
