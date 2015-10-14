import win32clipboard
import win32con


submit_format ="""<EmailAccount>
<Account>%s@gmail.com</Account>
<Password>%s</Password>
</EmailAccount>"""

while(True):
    input_str = raw_input()
    account = input_str.split(",")
    email = account[0].strip()
    password = account[1].strip()
    output_str = submit_format % (email, password)

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, output_str)
    win32clipboard.CloseClipboard()


