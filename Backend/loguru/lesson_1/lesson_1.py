#Loguru is library for logging(making dashboard magazine) in Python . It completely changes print() on server
#why do we need Loguru so badly?
#1 server works like a blind man , when we deal with server we don't have beautiful PyCharm display , if server crashes
#diring the night - all prints just will fade away and we will never find out cause of the breakdown
#print() - doesn't print out where was mistake and when(there is simply no time) and in which file
#2 - there is no sorting by importance in print() all mistakes by priority exist as identical between one another

#Loguru can take over all problems on server under control / it adds automatically exact time , name of file , number of item
#and priority of importance - and most important loguru can write these messages in files of disk)logs - so we can open it
#and repair when we wish(because it is preserved)

#so and here we go:
#in loguru we can just print "print out text" - we must initially point out an importance of event - this helps to get rid of
#rubbish
#main levels:
#from loguru import logger
#logger.debug() - detailed information for developer
#logger.info() - plain event(user just join the server)
#logger.warning() - something is wrong but server works(disk has run out of memory)
#logger.error() - error happened , function was broken but server is still alive
#logger.critical() - complete downfall - database turned off

#from loguru import logger
#logger.debug('this message is to debug the code')
#logger.info('AI-model was uploaded successfully') #simple event
#logger.warning('WARNING! API OpenAI responds slower than usual') #something just wrong
#logger.error("Error: Email wasn't sent to the user")
#logger.critical("Database PostgreSQL is unavailable!")

#logger.add() - writes data in the file - useful
#logger.add("server.log",level='ERROR') #methods of priority printing must be after this method
#INFO is like a boundary - DEBUG won't be written because by priority it is less important than INFO(INFO is a so-called boundary)
#logger.debug('this message is to debug the code')
#logger.info('AI-model was uploaded successfully') #simple event
#logger.warning('WARNING! API OpenAI responds slower than usual') #something just wrong
#logger.error("Error: Email wasn't sent to the user")
#logger.critical("Database PostgreSQL is unavailable!")

#but after a long time this file will be stuck by data and it will consume a lot of memory(hence might be not open)
#rotation - this flag helps us to create new file when old was too big
#logger.add('ai_service.log',rotation='10 MB',level='DEBUG')
#or rotation can be created in accordance of time rotation="00:00"

#TASK_1:
#from loguru import logger
#logger.add('random_debug.log',rotation='1 GB',level='DEBUG')
#def generate_text_with_ai(prompt:str,user_tier:str):
#    logger.debug('beginning of generation')
#    if user_tier == 'free':
#        logger.warning('user chose free mode')
#    else:
#        logger.warning('something is really wrong')
#    logger.info('text generated successfully!')
#generate_text_with_ai('Paint colorful flappers','free')

#rotation creates new files , retention - automatically deletes too old files of logs(we need it when there is a pile of them)
#from loguru import logger
#logger.add(
#    'cleanup.log',
#    rotation='500 MB',
#    retention='10 days' #will be deleted after this date
#)

#logger.exception() - retakes python error nad writes it in file
#logger.add('crash_report.log',level='ERROR')
#try: #imitate stupid bug
#    10 / 0
#except Exception as error:
#    logger.exception('Math error somehow happened!') #it will be written in the above file

#function also can crash and logs(data) will be empty so @logger.catch catches mistake and writes it in log-file
#with all TraceBack not letting the function crush:
#from loguru import logger
#logger.add('auto_guard.log',level='ERROR')
#@logger.catch
#def fragile_ai_function(x,y):
#    return x/y
#fragile_ai_function(10,0)
#print('code continues carrying out')

#TASK_2:
#from loguru import logger
#logger.add('system_defense.log',level='ERROR',rotation='10 MB',retention=3) #three last files in history will be preserved
#@logger.catch
#def load_weights_from_file(file_path: str):
#    if file_path == "secret.bin":
#        raise ValueError('Permission is blocked!')
#
#def connect_to_api(x,y):
#    try:
#        x / y
#    except Exception as error:
#        logger.exception('Math stupid error!')
#load_weights_from_file("secret.bin")
#connect_to_api(100,0)

#Also we can change our format in debug
#from loguru import logger
#logger.add(
#    "compact.log",
#    format='{time:HH:mm:ss} | {level: <8} | {message}')
#logger.info('module launched!')
#logger.warning('too long respond from API')

#record = {
#    "message": "Привет",
#    "name": "main",
#    "line": 42,
#    "level": {"name": "INFO", "no": 20},
#    "time": "2026-06-01 00:00:00"
#}

#and for storing in different files there is filter flag:
#from loguru import logger
#it will write logs if only they are written inside module(file)
#logger.add("main_module.log",filter = lambda record: record['name'] == 'main')
#logger.add("ai_only.log",filter = lambda record: "AI" in record['message'])
#logger.info('Simple system log')
#logger.info('Request was sent in AI model')


#in Python there is obsolete library logging which is used . All libraries like AsyncIO, SQLAlchemy, OpenAI use this library
#but there is a disadvantage: logging prints out ugly logs with ugly white font . In order to maintain beauty we retake this logs
#and make them display beautifully due to our Loguru - there is class-handler for this purpose
#import logging
#from loguru import logger
#class InterceptHandler(logging.Handler):
#    def emit(self,record): #record - data - this is a pont of retake
#        logger_opt = logger.opt(depth=6,exception=record.exc_info) #Traceback errors will be in exc_info variable
#        logger_opt.log(record.levelname,record.getMessage()) #record.levelname - takes a level of importance(above)
#                                            #record.getMessage() - launches embedded function which takes a text itself
#logging.basicConfig(handlers=[InterceptHandler()],level=logging.INFO)
##level=logging.INFO #basic configuration of standard logging
##handlers=[InterceptHandler()] - all ugly logging logs must be given to InterceptHandler(taker)
##level=logging.INFO - catch logs from all libraries starting with level priority INFO
#logging.info()


#TASK_3(BOSS):
from loguru import logger
logger.add('ai_activity.log',format='{time:HH:mm:ss} | {level: <8} | {message}',rotation='10 MB',retention=5)
logger.add('critical_errors.log',rotation='10 MB',retention=2,level='ERROR')
@logger.catch
def generate_ai_response(user_prompt:str,model_name:str):
    logger.info(f'launch of generation using model: {model_name}')
    if model_name == "broken_gpt":
        raise RuntimeError('server OpenAI closed connection')
def save_to_database(data:str):
    try:
        10 / 0
    except Exception as error:
        logger.exception('Downfall in PostgreSQL!')
generate_ai_response("Hello AI", "gpt-4o")
generate_ai_response("Fix code", "broken_gpt")
save_to_database("some_data")


