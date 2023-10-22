

try:
    from config import DKBOTZ_DATABASE
except:
    try:
        from configs import DKBOTZ_DATABASE
    except:
        try:
            from paid import DKBOTZ_DATABASE
        except:
            DKBOTZ_DATABASE = "mongodb+srv://dkbotzai:786@cluster0.fsrezwp.mongodb.net/?retryWrites=true&w=majority"


try:
    from config import DKBOTZ_DATABASE_NAME
except:
    try:
        from configs import DKBOTZ_DATABASE_NAME
    except:
        try:
            from paid import DKBOTZ_DATABASE_NAME
        except:
            DKBOTZ_DATABASE_NAME= "DKBOTZ"



MANGODB_URL = DKBOTZ_DATABASE_NAME
SESSION_NAME = DKBOTZ_DATABASE
