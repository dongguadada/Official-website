#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :config.py
# @Time      :2025/12/11 13:39
# @Author    :Dongguadada

import os
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # HTTP客户端配置
    http_timeout: float = Field(default=15.0, description="HTTP请求超时时间(秒)")
    http_connect_timeout: float = Field(default=5.0, description="HTTP连接超时时间(秒)")
    http_max_connections: int = Field(default=200, description="最大连接数")
    http2_enabled: bool = Field(default=True, description="是否启用HTTP/2")

    # API配置
    bgm_api_base_url: str = Field(default="https://api.bgm.tv/v0", description="Bangumi API基础URL")
    bgm_api_key: Optional[str] = Field(default="test_api_key_123", description="Bangumi API密钥")
    bgm_username: Optional[str] = Field(default="", description="Bangumi 用户名")

    # 应用配置
    app_name: str = Field(default="Bangumi", description="应用名称")
    debug: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")

    # 日志配置
    log_file_path: str = Field(default="logs/bangumi.log", description="日志文件路径")
    log_include_args: bool = Field(default=True, description="日志是否包含参数")
    log_include_result: bool = Field(default=True, description="日志是否包含结果")

    class Config:
        env_file = ".env"  # 指定.env文件路径
        env_file_encoding = 'utf-8'  # 指定编码格式
        case_sensitive = False  # 环境变量不区分大小写

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# 创建全局配置实例
settings = Settings()


def get_http_client_config() -> dict:
    """获取HTTP客户端配置"""
    return {
        "http_timeout": settings.http_timeout,
        "http_connect_timeout": settings.http_connect_timeout,
        "http_max_connections": settings.http_max_connections,
        "http2_enabled": settings.http2_enabled,
    }


def get_api_config() -> dict:
    """获取API配置"""
    return {
        "base_url": settings.bgm_api_base_url,
        "api_key": settings.bgm_api_key,
        "username": settings.bgm_username,
    }