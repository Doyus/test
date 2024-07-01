from datetime import datetime
import os
from loguru import logger as logging

# log_path = './log/runtime.log'
# logging.add(log_path, rotation="2048 MB", retention=3, level='DEBUG', format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>', backtrace=True, diagnose=True, enqueue=False, catch=True)

# 创建日志文件夹
log_dir = '../logs'
os.makedirs(log_dir, exist_ok=True)

# 设置日志文件名,包含日期
log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_path = os.path.join(log_dir, log_filename)

# 设置日志格式
log_format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'

# 添加日志句柄
logging.add(log_path, rotation="00:00", retention=30, level='DEBUG', format=log_format, backtrace=True, diagnose=True, enqueue=False, catch=True)