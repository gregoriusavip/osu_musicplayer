import logging

def error_handler(e, task: str):
    """
    Helper function to log when an error occured during the program runtime.

    :param1 `e`: the exception that was caught on the catch block
    :param2 `message`: the task operation that was attempted

    :return: no return value
    """
    reason = "Task: " + task + " could not be completed."
    logging.critical(reason)
    logging.error('Error: %s' % (' '.join(e.args)))