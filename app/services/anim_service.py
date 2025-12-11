#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :anim_service.py
# @Time      :2025/12/11 14:49
# @Author    :Dongguadada

from typing import List, Optional
from core import settings
from core import http_client, get_api_config
from schemeas import AnimeInfo, AnimeStatus
from utils import log_execution


class AnimeService:
    
    @staticmethod
    @log_execution(log_level=settings.LOG_LEVEL, 
                   include_args=settings.LOG_INCLUDE_ARGS,
                   include_result=settings.LOG_INCLUDE_RESULT)
    async def search_anime_by_title(title: str) -> List[AnimeInfo]:
        """
        根据标题搜索动漫
        
        Args:
            title: 动漫标题
            
        Returns:
            List[AnimeInfo]: 动漫信息列表
            
        Raises:
            Exception: API调用失败时抛出异常
        """
        try:
            api_config = get_api_config()
            url = f"{api_config['base_url']}/anime?q={title}"
            response = await http_client.get(url)
            data = response.json()
            
            anime_list = []
            if data.get("data") and isinstance(data["data"], list):
                for item in data["data"]:
                    anime_info = AnimeService._convert_to_anime_info(item)
                    anime_list.append(anime_info)
            
            return anime_list
            
        except Exception as e:
            raise Exception(f"搜索动漫失败: {str(e)}")
    
    @staticmethod
    @log_execution(log_level=settings.LOG_LEVEL,
                   include_args=settings.LOG_INCLUDE_ARGS,
                   include_result=settings.LOG_INCLUDE_RESULT)
    async def get_anime_by_id(anime_id: int) -> Optional[AnimeInfo]:
        """
        根据ID获取动漫详情
        
        Args:
            anime_id: 动漫ID
            
        Returns:
            Optional[AnimeInfo]: 动漫信息，如果未找到返回None
            
        Raises:
            Exception: API调用失败时抛出异常
        """
        try:
            api_config = get_api_config()
            url = f"{api_config['base_url']}/anime/{anime_id}"
            response = await http_client.get(url)
            data = response.json()
            
            if data.get("data"):
                return AnimeService._convert_to_anime_info(data["data"])
            
            return None
            
        except Exception as e:
            raise Exception(f"获取动漫详情失败: {str(e)}")
    
    @staticmethod
    def _convert_to_anime_info(api_data: dict) -> AnimeInfo:
        """
        将API返回的数据转换为AnimeInfo对象
        
        Args:
            api_data: API返回的动漫数据
            
        Returns:
            AnimeInfo: 转换后的动漫信息对象
        """
        title = api_data.get("titles", [{}])[0].get("title") or api_data.get("title", "未知标题")
        score = int(api_data.get("score", 0)) or 0
        status = AnimeStatus.PLANNED  # 默认状态为"计划看"
        
        return AnimeInfo(
            title=title,
            score=score,
            status=status
        )


anime_service = AnimeService()

