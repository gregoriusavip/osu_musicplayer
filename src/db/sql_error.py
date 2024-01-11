import logging

def sql_error_handler(e, task):
    """
    Helper function to handle when an error occured during sqlite operation.

    :param1 `e`: the exception that was caught on the catch block
    :param2 `message`: the task operation that was attempted

    :return: no return value
    """
    reason = "Task: " + task + " could not be completed."
    logging.critical(reason)
    logging.error('Sql error: %s' % (' '.join(e.args)))
    logging.error("Exception class is: ", e.__class__)