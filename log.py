import logging
import logging.config as log_config
from logging.handlers import TimedRotatingFileHandler

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s %(levelname)s %(message)s',
            # Windows下可能需要指定编码
            # '()': 'logging.Formatter',  # 显式指定Formatter类
            # 'style': '%',  # 默认格式风格
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',  # 明确指定输出到stdout
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'when': "d",
            'interval': 1,
            'backupCount': 30,
            'filename': "log.log",  # 添加文件扩展名
            'encoding': 'utf-8',  # 关键：指定文件编码为UTF-8
        }
    },
    'loggers': {
        'StreamLogger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'FileLogger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }
}
# 加载配置
# log_config.dictConfig(logging_config)
log_config.dictConfig(logging_config)
# 实例化logger 加载loggers的配置
logger = logging.getLogger('FileLogger')