import hashlib
import platform
import uuid
from pathlib import Path
current_file =Path (__file__ ).resolve ()
BASE_DIR =current_file .parent .parent
APP_DIR =BASE_DIR /'spruce_ui'
class UniqueMachineCodeGenerator (object ):
    def __init__ (O0O00O00000O0000O ,):
        O0O00O00000O0000O .os_info =platform .platform ()
        O0O00O00000O0000O .mac_address =O0O00O00000O0000O .get_mac_address ()
    def get_mac_address (OO0O000OO0O00OOO0 ):
        OOOOOO00O0000O000 =':'.join (['{:02x}'.format ((uuid .getnode ()>>O0O00O0O00O0OOOOO )&0xff )for O0O00O0O00O0OOOOO in range (0 ,2 *6 ,2 )][::-1 ])
        return OOOOOO00O0000O000
    def generate_machine_code (OO000O00OOO0O0OOO ):
        with open (APP_DIR /'templatetags'/'.key')as OOO0OO000O00000O0 :
            OO00O0O0000OOO000 =OOO0OO000O00000O0 .read ()
        O0000000O0OOOOO00 =f"{OO000O00OOO0O0OOO.os_info}-{OO000O00OOO0O0OOO.mac_address}-spruce_ui-{OO00O0O0000OOO000}".encode ()
        OOOO00O0O00O00OO0 =hashlib .sha256 (O0000000O0OOOOO00 ).hexdigest ()
        return OOOO00O0O00O00OO0
    def get_init (OOO0O0O0O0O0O0OO0 ):
        return f"{OOO0O0O0O0O0O0OO0.os_info}-{OOO0O0O0O0O0O0OO0.mac_address}"
