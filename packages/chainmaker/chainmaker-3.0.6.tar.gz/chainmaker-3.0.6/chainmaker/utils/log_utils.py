#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   logger.py
# @Function     :   SDK日志配置

import logging


def get_logger(name, level, format, datefmt='%Y-%m-%s %H:%M:%S', log_file=None):
    logger = logging.getLogger(name)
    format = logging.Formatter(fmt=format, datefmt=datefmt)  # 日志格式
    logger.setLevel(level)
    
    cli_handler = logging.StreamHandler()  # 输出到屏幕的日志处理器
    cli_handler.setFormatter(format)  # 设置屏幕日志格式
    cli_handler.setLevel(level)  # 设置屏幕日志等级, 可以大于日志记录器设置的总日志等级
    
    logger.handlers.clear()  # 清空已有处理器, 避免继承了其他logger的已有处理器
    logger.addHandler(cli_handler)  # 将屏幕日志处理器添加到logger
    
    if log_file is not None:
        file_handler = logging.FileHandler(filename='sdk.log', mode='a', encoding='utf-8')  # 输出到文件的日志处理器
        file_handler.setLevel(level)  # 不设置默认使用logger的等级
        file_handler.setFormatter(format)  # 设置文件日志格式
        logger.addHandler(file_handler)  # 将文件日志处理器添加到logger
    return logger


