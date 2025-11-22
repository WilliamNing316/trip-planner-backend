"""JSON解析和修复工具"""

import json
import re
from typing import Optional, Dict, Any
from loguru import logger


def extract_json_from_text(text: str) -> Optional[str]:
    """
    从文本中提取JSON字符串
    
    Args:
        text: 包含JSON的文本
        
    Returns:
        提取的JSON字符串，如果未找到则返回None
    """
    # 方法1: 查找 ```json 代码块
    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()
    
    # 方法2: 查找 ``` 代码块
    code_match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if code_match:
        content = code_match.group(1).strip()
        # 检查是否是JSON格式
        if content.strip().startswith('{') or content.strip().startswith('['):
            return content
    
    # 方法3: 查找第一个 { 到最后一个 } 之间的内容
    first_brace = text.find('{')
    if first_brace != -1:
        # 从第一个 { 开始，找到匹配的最后一个 }
        brace_count = 0
        for i in range(first_brace, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[first_brace:i+1]
    
    return None


def fix_json_string(json_str: str) -> Optional[str]:
    """
    尝试修复常见的JSON格式错误
    
    Args:
        json_str: 可能有错误的JSON字符串
        
    Returns:
        修复后的JSON字符串，如果无法修复则返回None
    """
    try:
        # 先尝试直接解析
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        pass
    
    # 尝试修复常见问题
    fixes = [
        # 修复单引号
        (r"'([^']*)':", r'"\1":'),
        # 修复尾随逗号
        (r',(\s*[}\]])', r'\1'),
        # 修复注释
        (r'//.*?$', '', re.MULTILINE),
        (r'/\*.*?\*/', '', re.DOTALL),
        # 修复未转义的控制字符
        (r'\n', '\\n'),
        (r'\r', '\\r'),
        (r'\t', '\\t'),
    ]
    
    fixed = json_str
    for pattern, replacement, *flags in fixes:
        flags = flags[0] if flags else 0
        fixed = re.sub(pattern, replacement, fixed, flags=flags)
    
    try:
        json.loads(fixed)
        logger.info("成功修复JSON格式错误")
        return fixed
    except json.JSONDecodeError as e:
        logger.warning(f"无法修复JSON格式错误: {e}")
        return None


def parse_json_safely(text: str, use_fix: bool = True) -> Optional[Dict[str, Any]]:
    """
    安全地解析JSON，包含自动修复功能
    
    Args:
        text: 包含JSON的文本
        use_fix: 是否尝试修复JSON
        
    Returns:
        解析后的字典，如果解析失败则返回None
    """
    # 提取JSON字符串
    json_str = extract_json_from_text(text)
    
    if json_str is None:
        logger.error("无法从文本中提取JSON")
        return None
    
    # 尝试解析
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON解析失败: {e}")
        
        if use_fix:
            # 尝试修复
            fixed_json = fix_json_string(json_str)
            if fixed_json:
                try:
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    pass
        
        logger.error("JSON解析和修复都失败")
        return None

