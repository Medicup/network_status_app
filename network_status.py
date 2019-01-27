import requests
import requests.exceptions
import logger
import time
from ping3 import ping, verbose_ping
import static_references


def ping_check(url, ip_addr="8.8.8.8"):
    func_name = 'ping_check'
    attempts = 360
    logger.update_log_file('Starting ping_check, {}'.format(func_name))
    while attempts > 0:
        ping_results = ping(ip_addr)
        if ping_results is not None:
            attempts = 360
            logger.update_log_file('{}, Successfully pinged: {}, {}'.format(static_references.log_status_ok, ip_addr, ping_results))
            network_check(url)
        else:
            attempts -= 1
            time.sleep(10)
            logger.update_log_file(
                "{}, Unable to return successful ping, ATTEMPT = {}, Local error code, 900, {}".format(
                    static_references.log_status_err, attempts, func_name
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
                message = "{}, Successful ping of, {}, with status code - {}.".format(
                    static_references.log_status_ok, url, url_check.status_code, attempts
                )
                logger.update_log_file(message)
        except requests.exceptions.ConnectionError:
            attempts -= 1
            logger.update_log_file(
                "{}, There appears to be a problem with the network, local error code 903, Attempts remaining = {} ".format(
                    static_references.log_status_err, attempts
                )
            )
        except Exception as e:
            attempts -= 1
            logger.update_log_file(
                "Returned unknown exception error, Attempts = {}, -local error code 904: {}".format(attempts, e)
            )

    time.sleep(30)
    ping_check(url)
