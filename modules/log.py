import logging
import logging.handlers
import sys
import os.path


class Logger(object):
    """
       Logger objects with initialized File and Syslog logger.
    """
    logger = None

    def _init_stdout(self):
        lfs = '%(levelname)s ' + self._caller + ' - %(message)s'
        lf = logging.Formatter(lfs)
        lv = logging.INFO

        logging.basicConfig(format=lfs, level=lv, stream=sys.stdout)
        self.logger = logging.getLogger(self._caller)

    def _init_syslog(self):
        lfs = '%(name)s[%(process)s]: %(levelname)s ' + self._caller + ' - %(message)s'
        lf = logging.Formatter(lfs)
        lv = logging.INFO

        sh = logging.handlers.SysLogHandler('/dev/log', logging.handlers.SysLogHandler.LOG_USER)
        sh.setFormatter(lf)
        sh.setLevel(lv)
        self.logger.addHandler(sh)

    def __init__(self, caller):
        self._caller = os.path.basename(caller)
        try:
            self._init_stdout()
            self._init_syslog()
        except (OSError, IOError) as e:
            sys.stderr.write('ERROR ' + self._caller + ' - ' + str(e) + '\n')
            raise SystemExit(1)

    def get(self):
        return self.logger

