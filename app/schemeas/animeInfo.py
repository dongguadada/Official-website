#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :animeInfo.py
# @Time      :2025/12/11 13:47
# @Author    :Dongguadada

from enum import Enum
from pydantic import BaseModel

class AnimeStatus(Enum):
    WATCHING = "watching"      # 在看
    COMPLETED = "completed"    # 已看完
    PAUSED = "paused"          # 暂停
    PLANNED = "planned"        # 计划看
    DROPPED = "dropped"        # 弃坑


class AnimeInfo(BaseModel):
    title: str                  # 标题
    score: int                  # 个人评分
    status: AnimeStatus         # 状态