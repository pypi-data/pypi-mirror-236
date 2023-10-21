import os
import pytz
import shutil
from pathlib import Path
from datetime import datetime

prev_hour = None
prev_day = None

def datetime_format():
    '''
    Extract daterime now to get year month day hour minute second and microsecond now
    '''
    datetime_now    = datetime.now(ist)
    year            = str(datetime_now.year)
    month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
    day             = '0'+str(datetime_now.day) if len(str(datetime_now.day)) == 1 else str(datetime_now.day)
    hour            = '0'+str(datetime_now.hour) if len(str(datetime_now.hour)) == 1 else str(datetime_now.hour)
    minute          = '0'+str(datetime_now.minute) if len(str(datetime_now.minute)) == 1 else str(datetime_now.minute)
    second          = '0'+str(datetime_now.second) if len(str(datetime_now.second)) == 1 else str(datetime_now.second)
    microsecond     = '0'+str(datetime_now.microsecond) if len(str(datetime_now.microsecond)) == 1 else str(datetime_now.microsecond)
    return year, month, day, hour, minute, second, microsecond

def asctime():
    '''
    Get asctime for message log
    '''
    year, month, day, hour, minute, second, microsecond = datetime_format()
    return f'{year}-{month}-{day} {hour}:{minute}:{second},{str(microsecond)[:3]}'

def get_path_log():
    '''
    Set path log in path logging/yaer/month/day/log_name.log
    '''
    year, month, day, hour, _, _, _ = datetime_format()
    path_name = f'{dir_log}/{year}/{month}/{day}'
    Path(path_name).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging_{hour}, {day}-{month}-{year}.log'
    log_file_full_name = os.path.join(path_name, log_filename)
    return log_file_full_name

def get_path_log_new():
    Path(dir_log).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging.log'
    log_file_full_name = os.path.join(dir_log, log_filename)
    return log_file_full_name

def check_and_move(prev_hour=None):
    year, month, day, _, _, _, _ = datetime_format()
    path_name = f'{dir_log}/{year}/{month}/{day}'
    Path(path_name).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging_{prev_hour}, {prev_day}-{month}-{year}.log'
    log_file_new = os.path.join(path_name, log_filename)
    log_file_old = os.path.join(dir_log, 'logging.log')
    shutil.move(log_file_old, log_file_new)

class SetupLogger:
    '''
        Dinamic Logging set as datetime directory
        Args:
            directory_log(str)  : root directory log
            print_log(boolean)  : print or skip print log
    '''
    def __init__(self, directory_log: str='./', time_zone: str='Asia/Jakarta'):
        global ist; ist = pytz.timezone(time_zone)
        global dir_log; dir_log = directory_log
    
class logging:
    
    '''
    Add class method for level log : info error and debug
    '''
    @classmethod
    def info(self, msg):
        self.__write_log(self, msg, level='INFO')
    @classmethod    
    def error(self, msg):
        self.__write_log(self, msg, level='ERROR')
    @classmethod
    def debug(self, msg):
        self.__write_log(self, msg, level='DEBUG')

    def __write_log(self, message, level):
        '''
        Write text log in path log
        '''
        global prev_day, prev_hour

        if not prev_day: prev_day = datetime_format()[2]
        if not prev_hour: prev_hour = datetime_format()[3]
        path_log = get_path_log_new()
        log_file = open(path_log, 'a+')
        text = f'{asctime()} | {level} : {message}'
        log_file.write(f'{text} \n')
        print(text)
        log_file.close()
        
        curr_hour = datetime_format()[3]
        if not prev_hour == curr_hour:
            check_and_move(prev_hour)
            prev_hour = curr_hour

        curr_day = datetime_format()[2]
        if not prev_day == curr_day:
            os.remove(path_log)
            prev_day = curr_day
