import logging
import colorlog
from ..s0_dataset import DSTree

tree = DSTree.tree


class UMLog(object):
    def __init__(self):
        self.log_colors_config = {'DEBUG': 'white', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red',
                                  'CRITICAL': 'bold_red'}
        self.logger = logging.getLogger('logger_name')
        self.console_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(filename=tree.logpath, mode='a', encoding='utf8')

        # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        self.logger.setLevel(logging.INFO)
        self.console_handler.setLevel(logging.INFO)
        self.file_handler.setLevel(logging.INFO)

        # 日志输出格式
        self.file_formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(levelname)s] : %(message)s',
                                                datefmt='%Y-%m-%d  %H:%M:%S')

        self.console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S', log_colors=self.log_colors_config)

        self.console_handler.setFormatter(self.console_formatter)
        self.file_handler.setFormatter(self.file_formatter)

        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)
            self.logger.addHandler(self.file_handler)

        self.console_handler.close()
        self.file_handler.close()

    def log_debug(self, mesg):
        self.logger.debug(mesg)

    def log_info(self, mesg):
        self.logger.info(mesg)

    def log_warning(self, mesg):
        self.logger.warning(mesg)

    def log_error(self, mesg):
        self.logger.error(mesg)

    def log_critical(self, mesg):
        self.logger.critical(mesg)


logger = UMLog()

logDEBUG = logger.log_debug
logINFO = logger.log_info
logWARNING = logger.log_warning
logERROR = logger.log_error
logCRITICAL = logger.log_critical
