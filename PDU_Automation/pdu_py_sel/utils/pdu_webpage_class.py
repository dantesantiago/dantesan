# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-09-02

class PDU_WEBPAGE_CLASS:
    def __init__(self, **kwargs):
        self._ip_address = \
            kwargs['ip_address'] if 'ip_address' in kwargs else "172.30.201.18"
        self._username = kwargs['username'] if 'username' in kwargs else "admin"
        self._password = kwargs['password'] if 'password' in kwargs else "panduit#1"
        self._webpage_string = \
        kwargs['webpage_string'] if 'webpage_string' in kwargs \
                                 else "Monitored & Switched Per Outlet PDU"

    def ip_address(self, i=None):
        if i:
            self._ip_address = i
        return self._ip_address

    def username(self, u=None):
        if u:
            self._username = u
        return self._username

    def password(self, p=None):
        if p:
            self._password = p
        return self._password

    def webpage_string(self, s=None):
        if s:
            self._webpage_string = s
        return self._webpage_string

    IP_ADDRESS = "172.30.201.18"
    #AUTOMATION_PDU_WEBPAGE = "https://172.30.201.18/#/login?_k=f4wu0l"
    AUTOMATION_PDU_TITLE = "Panduit"
    USERNAME = "admin"
    PASSWD = "panduit#1"
    WEBPAGE_STRING = "Monitored & Switched Per Outlet PDU"


def print_pdu_webpage_class(o):
    if not isinstance(o, PDU_WEBPAGE_CLASS):
        raise TypeError('print_not_certified(): requires PDU_WEBPAGE_CLASS data.')
    #write_log("{} - {}".format(print_not_certified.__name__, o.red_cc.upper())) #RED
    return ('{},{},{},{},{} - {}'.format(o.username(), o.password()," "," ", 
            o.cellColor(), o.webpage_string()))


    

# --------------------------------------- END --------------------------------
