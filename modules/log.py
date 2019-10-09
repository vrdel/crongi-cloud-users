import logging
import logging.handlers
import sys
import os.path


class Logger(object):
    logger = None

    def _init_stdout(self):
        lfs = '%(levelname)s ' + self._caller + ' - %(message)s'
        lf = logging.Formatter(lfs)
        lv = logging.INFO

        logging.basicConfig(format=lfs, level=lv, stream=sys.stdout)
        self.logger = logging.getLogger(self._caller)

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

