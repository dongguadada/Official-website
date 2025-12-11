#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
from core import settings

def test_config():
    """测试配置是否正确读取"""
    print("=== 配置测试 ===")
    print(settings.bgm_api_key)

if __name__ == "__main__":
    test_config()