#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :logging.py
# @Time      :2025/12/11 15:30
# @Author    :Dongguadada

import logging
import sys
import functools
from typing import Optional, Callable
from core import settings


class CustomLogger:
    """自定义日志记录器"""
    
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("bangumi")
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        # 创建格式化器
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器（如果配置了日志文件路径）
        log_file_path = getattr(settings, 'LOG_FILE_PATH', None)
        if log_file_path:
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def get_logger(self, module_name: Optional[str] = None) -> logging.Logger:
        """获取指定模块的日志记录器"""
        if module_name:
            return logging.getLogger(f"bangumi.{module_name}")
        return self.logger


# 全局日志记录器实例
custom_logger = CustomLogger()


def log_execution(
    log_level: str = "INFO",
    include_args: bool = True,
    include_result: bool = True,
    log_errors: bool = True
):
    """
    函数执行日志装饰器
    
    Args:
        log_level: 日志级别
        include_args: 是否记录函数参数
        include_result: 是否记录函数返回值
        log_errors: 是否记录异常信息
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger = custom_logger.get_logger(func.__module__)
            level = getattr(logging, log_level.upper(), logging.INFO)
            
            # 记录函数开始执行
            func_info = f"开始执行函数: {func.__name__}"
            if include_args:
                args_str = ", ".join([str(arg) for arg in args])
                kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                all_args = ", ".join(filter(None, [args_str, kwargs_str]))
                func_info += f" - 参数: [{all_args}]"
            
            logger.log(level, func_info)
            
            try:
                # 执行函数
                result = await func(*args, **kwargs)
                
                # 记录执行结果
                success_msg = f"函数 {func.__name__} 执行成功"
                if include_result:
                    success_msg += f" - 返回值: {result}"
                
                logger.log(level, success_msg)
                return result
                
            except Exception as e:
                if log_errors:
                    logger.error(f"函数 {func.__name__} 执行失败 - 错误: {str(e)}")
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger = custom_logger.get_logger(func.__module__)
            level = getattr(logging, log_level.upper(), logging.INFO)
            
            # 记录函数开始执行
            func_info = f"开始执行函数: {func.__name__}"
            if include_args:
                args_str = ", ".join([str(arg) for arg in args])
                kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                all_args = ", ".join(filter(None, [args_str, kwargs_str]))
                func_info += f" - 参数: [{all_args}]"
            
            logger.log(level, func_info)
            
            try:
                # 执行函数
                result = func(*args, **kwargs)
                
                # 记录执行结果
                success_msg = f"函数 {func.__name__} 执行成功"
                if include_result:
                    success_msg += f" - 返回值: {result}"
                
                logger.log(level, success_msg)
                return result
                
            except Exception as e:
                if log_errors:
                    logger.error(f"函数 {func.__name__} 执行失败 - 错误: {str(e)}")
                raise
        
        # 判断是否为异步函数
        if hasattr(func, '__code__') and hasattr(func.__code__, 'co_flags'):
            import inspect
            if inspect.iscoroutinefunction(func):
                return async_wrapper
        
        return sync_wrapper
    
    return decorator


def get_logger(module_name: Optional[str] = None) -> logging.Logger:
    """获取日志记录器的便捷函数"""
    return custom_logger.get_logger(module_name)