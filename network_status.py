import requests
import requests.exceptions
import logger
import time
from ping3 import ping

log_status_ok = "LOG_OK-"
log_status_err = "LOG_ERROR-"
log_status_failed = "LOG_CRITICAL_FAIL-"


def ping_check(url, ip_addr="8.8.8.8"):
    attempts = 360
    while attempts > 0:
        ping_results = ping(ip_addr)
        print(ping_results)
        if ping_results is not None:
            attempts = 360
            network_check(url)
        else:
            attempts -= 1
            time.sleep(10)
            logger.update_log_file(
                "{}: Unable to return successful ping. ATTEMPT = {}. Local error code: 900".format(
                    log_status_err, attempts
                )
            )
    logger.update_log_file("total failure of the log system. Exiting...")


def network_check(url):
    attempts = 12
    logger.update_log_file("Initiating URL check")
    while attempts > 0:
        time.sleep(5)
        try:
            url_check = requests.get(url, timeout=5)
            if url_check.status_code == 200:
                attempts = 12
                message = "{}: Successful ping of {} with status code - {}.".format(
                    log_status_ok, url, url_check.status_code, attempts
                )
                logger.update_log_file(message)
        except requests.exceptions.ConnectionError:
            attempts -= 1
            logger.update_log_file(
                "{}: There appears to be a problem with the network: local error code 903. Attempts remaining = {} ".format(
                    log_status_err, attempts
                )
            )
        except Exception as e:
            attempts -= 1
            print("Attempts = {}".format(attempts))
            logger.update_log_file(
                "Returned unknown exception error, local error code 904: {}".format(e)
            )

    time.sleep(30)
    ping_check(url)
