import imaplib


def login_credentials():
    return "butchershopbigdave@mail.ru", "RgeAyRI11ri_"


def connect_imap():
    m = imaplib.IMAP4_SSL("imap.mail.ru", 993)
    details = login_credentials()
    m.login(details[0], details[1])
    return m


m = connect_imap()
m.select("INBOX")
result, data = m.uid('search', None)
print(data)
