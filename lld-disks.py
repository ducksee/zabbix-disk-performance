#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys

def discover_disks():
    # 待过滤的设备关键词
    skippable = ("sr", "loop", "ram", "dm-", "nbd")
    
    devices = []
    try:
        # 遍历 /sys/class/block 目录
        for device in os.listdir("/sys/class/block"):
            # 过滤逻辑：
            # 1. 不在过滤名单中
            # 2. 排除分区（通常只监控整块磁盘 vda/sda，通过检查路径中是否存在 'device' 目录来判断）
            if not any(ignore in device for ignore in skippable):
                device_path = os.path.join("/sys/class/block", device)
                # 只有物理磁盘（非分区）在 sysfs 中通常才有 'device' 这个符号链接
                if os.path.exists(os.path.join(device_path, "device")):
                    devices.append({"{#DEVICENAME}": device})
    except Exception as e:
        # 如果出错，返回空列表，防止 Zabbix 解析 JSON 失败
        pass

    return {"data": devices}

if __name__ == "__main__":
    result = discover_disks()
    # 确保在 Python 2/3 下都能正确输出 JSON
    sys.stdout.write(json.dumps(result, indent=4) + '\n')
