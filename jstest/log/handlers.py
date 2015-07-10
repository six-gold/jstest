# coding=utf-8

"""
Overload python's inner logging.handlers.TimedRotatingFileHandler, since its not process safe.
When running python's inner logging.handlers.TimedRotatingFileHandler in multi process, when the file is rorating,
this handler will remove the old log file and write to the new log file, and rename the log file, this will cause
two log files be writen in at the same time and delete the wrong log file.
"""

import os, time, socket, re
from logging.handlers import TimedRotatingFileHandler

class MultiProcessTimedRotatingFileHandler(TimedRotatingFileHandler):

    _Exp = re.compile(r'\$\$(\w+?)\$\$', flags=re.IGNORECASE)

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        """
        Hack the default __init__ method to get the proper log filename we wanted.
        Since %(macro)s has been used by python ConfigParser, Filename set in logger.conf support macros like "$$macro$$".
        """

        filename = re.sub(self._Exp, self.replace_macro, filename)
        super(MultiProcessTimedRotatingFileHandler, self).__init__(filename, \
                when, interval, backupCount, encoding, delay, utc)

    def doRollover(self):
        """
        Do not remove log file if there is a file with the same name of rotating file
        """

        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(self.baseFilename) and not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.mode = 'a'
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def replace_macro(self, matchobj):
        """
        Replace macros in log filename set in log config
        """

        if not isinstance(matchobj.group(1), basestring):
            return None
        return ({
            'hostname': socket.gethostname(),
            'date': time.strftime('%Y%m%d'),
            }).get(str.lower(matchobj.group(1)))
