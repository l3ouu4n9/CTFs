import re
import sys
import json
import smtpd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BANNER = """
  `/hmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNmy/`  
 +NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN+ 
oMMMMMMMMMdoooooooooooooooooooooooooooooooooooooooooooooooooooooooooodMMMMMMMMM+
NMMMMMMMMMMd:                                                      :dMMMMMMMMMMm
MMMMM/+mMMMMMd:                                                  :dMMMMMm+/MMMMM
MMMMM: `+NMMMMMd:                                              :dMMMMMN+` :MMMMM
MMMMM:   `+NMMMMMd:                                          :dMMMMMN+`   :MMMMM
MMMMM:     `+mMMMMMd:                                      :dMMMMMm+`     :MMMMM
MMMMM:       `+NMMMMMd:                                  :dMMMMMN+`       :MMMMM
MMMMM:         `+NMMMMMd:                              :dMMMMMN+          :MMMMM
MMMMM:           `+NMMMMMd:                          :dMMMMMm+`           :MMMMM
MMMMM:             `+NMMMMMd:                      :dMMMMMN+`             :MMMMM
MMMMM:               `+mMMMMMd:                  :dMMMMMm+`               :MMMMM
MMMMM:                 :NMMMMMMd:              :dMMMMMMN:                 :MMMMM
MMMMM:               :hMMMMMMMMMMd:          :dMMMMMMMMMMh:               :MMMMM
MMMMM:             :hMMMMMN++NMMMMMd:      :dMMMMMN++NMMMMMh:             :MMMMM
MMMMM:           -hMMMMMNo`  `+NMMMMMd:  :dMMMMMN+`  `oNMMMMMh-           :MMMMM
MMMMM:         -hMMMMMNo`      `+NMMMMMmmMMMMMN+       `oNMMMMMh-         :MMMMM
MMMMM:       :hMMMMMNo`          `+NMMMMMMMMm+`          `oNMMMMMh:       :MMMMM
MMMMM:     :hMMMMMNo`              `/ydmmdy/`              `oNMMMMMh:     :MMMMM
MMMMM:   -hMMMMMN+`                                          `+NMMMMMh-   :MMMMM
MMMMM: :hMMMMMNo`                                              `oNMMMMMh: :MMMMM
NMMMMshMMMMMNo`                                                  `oNMMMMMhsMMMMN
+MMMMMMMMMMNsoooooooooooooooooooooooooooooooooooooooooooooooooooooosNMMMMMMMMMM+
 +NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN+ 
  `+hmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmy/`  
"""


class SMTP(smtplib.SMTP):
    class fake_socket(object):
        def sendall(self, *args):
            pass

    def _get_socket(self, host, port, timeout):
        return self.fake_socket()

    def getreply(self):
        return 220, ""

    def sendmail(self, *args):
        return args


class SMTPDebugger(object):
    _print_message_content = smtpd.DebuggingServer._print_message_content
    process_message = smtpd.DebuggingServer.process_message

    def __init__(self, from_addr, to_addrs, subject, message, **extra):
        self.from_addr = self.validate_email(from_addr)
        self.to_addrs = ";".join(map(self.validate_email, to_addrs.split(";")))
        self.subject = subject
        self.message = message
        self.extra = extra

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @staticmethod
    def get_flag():
        return "AppSec-IL{This_Is_Not_The_Flag!}"

    @staticmethod
    def validate_email(email):
        email = email.strip()
        res = re.match(
            r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@'
            r'((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',
            email
        )
        if not res:
            raise ValueError("'{email}' is bad email address!".format(email=email))
        return email

    def send_message(self):
        smtp = SMTP(host='localhost', port=1025)
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = self.to_addrs
        msg['Subject'] = self.subject.format(**self.extra)
        msg.attach(MIMEText(self.message.format(email=self, **self.extra), 'plain'))

        from_addr, to_addrs, flatmsg, mail_options, rcpt_options = smtp.send_message(msg)
        self.process_message("127.0.0.1", from_addr, to_addrs, flatmsg)

    @classmethod
    def run(cls):
        try:
            print(BANNER)
            kwargs = json.loads(input("Enter Email JSON: "))
            print()
            with cls(**kwargs) as smtp:
                smtp.send_message()
        except Exception as ex:
            print("\n[ERROR] {exception}".format(exception=ex), file=sys.stderr)
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(SMTPDebugger.run())
