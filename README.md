# competitive programming platform statstics
Fetch ranking and points from competitive programming sites like codeforces, kattis, leetcode, CSES, hackerrank, hackerearth, project euler, ... 


## Leetcode stats
 
```python
from stats import Leetcode

info = Leetcode("mukeremali112")
info.fetch()
```

## Codeforces stats
 
```python
from stats import Codeforces

info = Codeforces("mukeremali")
info.user_info()
```


## Kattis stats
 
```python
from stats import Kattis

info = Kattis("mukerem")
info.user_info()
```