def skip_starting_http_connection_logs(record):
    """
    Skip logs of the form "urllib3.connectionpool    DEBUG    Starting new HTTP connection (1): 127.0.0.1"
    :param record: Record to be checked for logging.
    :return: Bool; False if record should not be logged, True if it should.
    """
    if record.msg[:28] == 'Starting new HTTP connection':
        return False
    else:
        return True
