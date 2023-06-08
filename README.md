# competitive programming platform statstics
Fetch ranking and points from competitive programming sites like codeforces, kattis, leetcode, CSES, hackerrank, hackerearth, project euler, ... 


## Leetcode stats
 
```python
from stats import Codeforces, Leetcode


leetcode = Leetcode("mukeremali112")
leetcode.fetch()

codeforces = Codeforces("mukeremali")
codeforces.user_info()
```