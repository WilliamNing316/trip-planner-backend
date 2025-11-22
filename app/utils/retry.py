"""重试机制工具"""

import asyncio
import time
from typing import Callable, TypeVar, Optional, List
from functools import wraps
from loguru import logger

T = TypeVar('T')


class RetryError(Exception):
    """重试失败错误"""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[tuple] = None
):
    """
    带指数退避的重试装饰器
    
    Args:
        max_retries: 最大重试次数
        initial_delay: 初始延迟(秒)
        max_delay: 最大延迟(秒)
        exponential_base: 指数基数
        jitter: 是否添加随机抖动
        retryable_exceptions: 可重试的异常类型
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        # 计算延迟时间
                        delay = min(
                            initial_delay * (exponential_base ** attempt),
                            max_delay
                        )
                        
                        # 添加抖动
                        if jitter:
                            import random
                            delay = delay * (0.5 + random.random() * 0.5)
                        
                        logger.warning(
                            f"函数 {func.__name__} 执行失败 (尝试 {attempt + 1}/{max_retries + 1}): {str(e)}. "
                            f"{delay:.2f}秒后重试..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"函数 {func.__name__} 在 {max_retries + 1} 次尝试后仍然失败"
                        )
            
            raise RetryError(f"函数 {func.__name__} 重试失败") from last_exception
        
        return wrapper
    return decorator


async def async_retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[tuple] = None
):
    """
    异步版本的带指数退避的重试装饰器
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        delay = min(
                            initial_delay * (exponential_base ** attempt),
                            max_delay
                        )
                        
                        if jitter:
                            import random
                            delay = delay * (0.5 + random.random() * 0.5)
                        
                        logger.warning(
                            f"异步函数 {func.__name__} 执行失败 (尝试 {attempt + 1}/{max_retries + 1}): {str(e)}. "
                            f"{delay:.2f}秒后重试..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"异步函数 {func.__name__} 在 {max_retries + 1} 次尝试后仍然失败"
                        )
            
            raise RetryError(f"异步函数 {func.__name__} 重试失败") from last_exception
        
        return wrapper
    return decorator

