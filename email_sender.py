import smtplib
import json


def set_mail_cred(data):
    json_string = json.dumps(data)
    with open("data_file.json", "w") as write_file:
        write_file.write(json_string)


def get_mail_cred():
    with open("data_file.json", "r") as read_file:
        return json.load(read_file)


def send_confirm_mail(to, link):
    subject = 'SoftHouse'
    msg = 'Confirm your account: \n\t' + link
    text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (get_mail_cred()["login"], ", ".join(to), subject, msg)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(get_mail_cred()["login"], get_mail_cred()["password"])
        server.sendmail(get_mail_cred()["login"], to, text)
        server.close()
    except:
        print('Something went wrong with email')


if __name__ == '__main__':
    data = {"login": "", "password": ""}
    set_mail_cred("")