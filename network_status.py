import requests
import requests.exceptions
import logger
import time
from ping3 import ping
from static_references import (
    log_status_ok,
    log_status_failed,
    log_status_err,
    log_directory,
)


def network_check(url, ip_addr="8.8.8.8"):
    func_name = "ping_check"
    attempts = 360
    logger.update_log_file(log_status_ok, "Starting ping_check {}".format(func_name))
    while attempts > 0:
        ping_results = ping(ip_addr)
        ping_check(ip_addr)
        if ping_results is not None:
            attempts = 360
            logger.update_log_file(
                log_status_ok,
                "Successfully pinged: {} | {}".format(ip_addr, ping_results),
            )
            url_checker(url)
        else:
            attempts -= 1
            time.sleep(10)
            logger.update_log_file(
                log_status_err,
                "Unable to return successful ping. ATTEMPT = {}. Local error code: 900 | {}".format(
                    attempts, func_name
                ),
            )
    logger.update_log_file(
        log_status_failed, "total failure of the log system. Exiting..."
    )


def url_checker(url):
    func_name = "network_check"
    attempts = 12
    logger.update_log_file(log_status_ok, "Initiating URL check")
    while attempts > 0:
        time.sleep(5)
        try:
            url_check = requests.get(url, timeout=5)
            if url_check.status_code == 200:
                attempts = 12
                message = "Successful ping of {} with status code: {}.".format(
                    url, url_check.status_code, attempts
                )
                logger.update_log_file(log_status_ok, message)
        except requests.exceptions.ConnectionError:
            attempts -= 1
            logger.update_log_file(
                log_status_err,
                "There appears to be a problem with the network. Local error code 903. Attempts remaining = {} | {} ".format(
                    attempts, func_name
                ),
            )
        except Exception as e:
            attempts -= 1
            logger.update_log_file(
                log_status_err,
                "Returned unknown exception error. Attempts = {}. Local error code 904: {} | {}".format(
                    attempts, e, func_name
                ),
            )

    time.sleep(30)
    network_check(url)


def ping_check(ip_address):
    count = 4
    while count > 0:
        results = ping(ip_address)
        if results is not None:
            logger.update_log_file(log_status_ok, results)
            count -= 1
        else:
            logger.update_log_file(
                log_status_err, "Unable to ping {}".format(ip_address)
            )
