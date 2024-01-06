import logging

def sql_error_handler(e, message):
    reason = "Task " + message + " could not be completed."
    logging.critical(reason)
    logging.error('Sql error: %s' % (' '.join(e.args)))
    logging.error("Exception class is: ", e.__class__)