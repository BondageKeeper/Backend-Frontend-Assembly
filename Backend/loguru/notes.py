#main levels:
from loguru import logger
logger.debug() - detailed information for developer
logger.info() - plain event(user just join the server)
logger.warning() - something is wrong but server works(disk has run out of memory)
logger.error() - error happened , function was broken but server is still alive
logger.critical() - complete downfall - database turned off
