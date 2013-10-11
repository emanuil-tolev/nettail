import requests
from time import sleep
from datetime import datetime
import sys

import config

log = None

def inform(msg):
    print msg
    log.write(msg.encode('utf-8') + '\n')


def main(argv=None):
    global log

    # standard template for allowing testing of the main() function
    # but note we don't actually use command line arguments right now
    if not argv:
        argv = sys.argv

    log = open('logs/nettail_' + datetime.strftime(
        datetime.now(), '%Y-%m-%d') + '.log',
               'wb')  # overwrite the nettail daily log
    try:
        process_log()
    except BaseException:
        # You shouldn't catch BaseException. Seriously, don't do it.
        # But this quickly / dirtily writes down the current log when
        # the script is interrupted, e.g. with Ctrl+C.
        # Which is the main usecase...
        log.close()
        raise

    log.close()


def process_log():
    last_log = ''
    while True:
        r = requests.get(config.LOG_LOCATION, auth=config.BASIC_AUTH)
        cur_log = r.text

        # We only want to print the changed lines for this to be a true
        # "tail" utility. We go over the last log, removing all of its
        # lines from the current log - pretty inefficient and painful,
        # but works.
        if cur_log != last_log:
            cur_log_lines = cur_log.splitlines()
            last_log_lines = last_log.splitlines()
            for line in last_log_lines:
                try:
                    cur_log_lines.remove(line)
                except ValueError:  # the last log has lines which the
                                    # current one does not, probably
                                    # router returned an error HTML doc
                    pass

            for line in cur_log_lines:
                inform(line)

        last_log = cur_log
        sleep(config.WAIT)


if __name__ == '__main__':
    main()
