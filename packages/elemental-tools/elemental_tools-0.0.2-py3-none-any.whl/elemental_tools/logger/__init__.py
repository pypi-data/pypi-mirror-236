import os

from datetime import datetime

from elemental_tools.design import unicode_colors

def relative(path):
    return os.path.join(os.path.dirname(__file__), path)


class Logger:
    
    def __init__(self, app_name: str, owner: str, log_path: str = './', environment: str = ''):
        if app_name is None:
            self.app_name_upper = 'LOGGER'
        else:
            self.app_name_upper = str(app_name).upper()

        self.log_path = log_path
        self.environment = environment
        self.owner = owner
                
    def log(self, level: str, message):
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        level = level.upper()
        owner = self.owner.upper()
        correspondent_clr = unicode_colors.reset

        def log_path():
            if self.environment:
                self.log_path = str(self.log_path + f"_{self.environment}")

            os.makedirs(self.log_path, exist_ok=True)
            filename = datetime.now().strftime('%d-%m-%Y') + ".log"
            self.log_path = relative(os.path.join(self.log_path, filename))
            return self.log_path

        content = f"{timestamp} [{self.app_name_upper}] [{owner}] [{level}]: {str(message)}"

        with open(log_path(), 'a') as f:
            f.write(str(content))

        if level == 'INFO' or level == 'START':
            correspondent_clr = unicode_colors.success_cyan
        elif level == 'WARNING' or level == 'ALERT':
            correspondent_clr = unicode_colors.alert
        elif level == 'SUCCESS' or level == 'OK':
            correspondent_clr = unicode_colors.success
        elif level in ['CRITICAL', 'ERROR', 'FAULT', 'FAIL', 'FATAL']:
            correspondent_clr = unicode_colors.fail

        content = f"{timestamp} [{self.app_name_upper}] [{owner}] [{level}]: {str(message)}"
        print(correspondent_clr, content, unicode_colors.reset)

        return content
        

logger = Logger('log', 'me')
logger.log('info', 'test message')