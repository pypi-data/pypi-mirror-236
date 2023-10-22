try:
    from .main import *
except:
    pass



try:
    from datetime import *
except:
    pass

try:
    from .database import *
except:
    pass

try:
    from .config import *
except:
    pass
from .premium import *

import os
try:
    from .admin import *
except:
    pass

from dkbotzpaid import *
