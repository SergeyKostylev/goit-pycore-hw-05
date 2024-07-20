import sys
import syslog
from datetime import datetime
from collections import defaultdict
from prettytable import PrettyTable

# TODO: I don’t really like the structure of functions (we do it in a loop many times)
#      but I did it this way because it’s described in the task

LOG_INFO = "INFO"
LOG_DEBUG = "DEBUG"
LOG_ERROR = "ERROR"
LOG_WARNING = "WARNING"

ALLOWED_LOGS = [
    LOG_INFO,
    LOG_DEBUG,
    LOG_ERROR,
    LOG_WARNING
]

KEY_TIME = 'Time'
KEY_LOG_LEVEL = 'LogLevel'
KEY_LOG_MESSAGE = 'LogMessage'


def load_logs(file_path: str) -> list:
    log_lines = []
    try:
        with open(file_path, 'r') as file:
            log_lines = file.readlines()
    except (FileNotFoundError, PermissionError):
        handle_error(f"File not found or can't be read: {file_path}")

    res = []
    for log_lone in log_lines:
        parsed_data = parse_log_line(log_lone)
        if parsed_data is not None:
            res.append(parsed_data)

    return res


def parse_log_line(line: str) -> dict:
    try:
        log_time = line[0:19]
        datetime.strptime(log_time, "%Y-%m-%d %H:%M:%S")  # validate time of log
        log_level_and_message = line[20:].split(' ', 1)

        if len(log_level_and_message) != 2:
            raise ValueError(f"Invalid log level or log message")

        log_level = log_level_and_message[0]

        if log_level not in ALLOWED_LOGS:
            raise ValueError(f"Unknown log level: {log_level}")

    except ValueError as e:
        handle_error(f"The logline could not be parsed: '{line}'. Error: {e}")

        return None

    return {
        KEY_TIME: log_time,
        KEY_LOG_LEVEL: log_level,
        KEY_LOG_MESSAGE: log_level_and_message[1].rstrip(),
    }


def filter_logs_by_level(logs: list, level: str) -> list:
    return filter(lambda x: x[KEY_LOG_LEVEL] == level, logs)


def count_logs_by_level(logs: list) -> dict:
    res = defaultdict(int)
    for log in logs:
        res[log[KEY_LOG_LEVEL]] += 1

    return res


def display_log_counts(counts: dict):
    table = PrettyTable()
    table.align = "l"
    table.field_names = ["Рівень логування", "Кількість"]
    for log_type, amount in counts.items():
        table.add_row([log_type, amount])

    print(table)


def handle_error(message: str):
    print(message)
    syslog.syslog(syslog.LOG_INFO, message)


def main(file_path: str, log_level: str):
    log_list = load_logs(file_path)
    error_counts = count_logs_by_level(log_list)
    display_log_counts(error_counts)

    if log_level is not None:
        print(f"Деталі логів для рівня {log_level}:")
        for log in filter_logs_by_level(log_list, log_level):  # TODO: move to a separate method
            print(f"{log[KEY_TIME]} - {log[KEY_LOG_MESSAGE]}")


if __name__ == '__main__':
    default_file_path = 'log.txt'
    argv = sys.argv
    if len(argv) < 2:
        exit("Error: Missing arguments")

    file_path = argv[1]
    error_log = argv[2].upper() if len(argv) > 2 else None

    main(file_path, error_log)
