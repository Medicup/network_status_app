from logger import update_log_file
import network_status
import send_mail

url = "http://google.com"
ip_address = "8.8.8.8"


def main():
    send_mail.send_mail()
    update_log_file("STARTUP", "Starting program.py")
    network_status.network_check(url, ip_address)


if __name__ == "__main__":
    main()
