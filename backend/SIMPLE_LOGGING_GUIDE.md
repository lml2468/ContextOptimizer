# 简化日志系统使用指南

## 概述

新的日志系统采用极简设计，去除了复杂的层次结构和过度的emoji标识。

## 基本使用

### 1. 导入和初始化

```python
from app.utils.logger import get_logger

logger = get_logger()
```

### 2. 记录日志

```python
logger.debug("详细的调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

## 配置

### 环境变量

```bash
# 设置日志级别
LOG_LEVEL=DEBUG

# 设置日志文件路径
LOG_FILE=/path/to/app.log
```

### 默认配置

- 日志级别：INFO
- 日志文件：`logs/app.log`
- 格式：`%(asctime)s - %(levelname)s - %(message)s`

## 特性

1. **全局单例**：所有 `get_logger()` 调用返回同一个logger实例
2. **自动初始化**：首次调用时自动设置console和file handlers
3. **简洁格式**：去除了复杂的名称和emoji标识
4. **向后兼容**：保留了 `setup_logger` 别名

## 最佳实践

1. **统一使用**：所有模块都使用 `get_logger()` 获取logger
2. **适当级别**：
   - DEBUG：详细的调试信息
   - INFO：重要的业务流程信息
   - WARNING：需要注意的问题
   - ERROR：错误信息
3. **简洁描述**：日志信息清晰简洁，避免冗余

## 示例

```python
from app.utils.logger import get_logger

logger = get_logger()

def process_data(data):
    logger.info(f"Processing {len(data)} items")
    
    try:
        # 处理逻辑
        result = do_processing(data)
        logger.info("Processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
```

## 迁移指南

### 旧代码
```python
logger = get_logger(__name__)
logger.debug("🔧 Processing data...")
logger.info("✅ Data processed successfully")
```

### 新代码
```python
logger = get_logger()
logger.debug("Processing data")
logger.info("Data processed successfully")
```

## 故障排除

1. **日志不显示**：检查 `LOG_LEVEL` 环境变量
2. **日志文件为空**：确保 `logs/` 目录存在且有写权限
3. **重复日志**：新系统避免了重复handler问题

## 性能优化

- 生产环境建议使用 `INFO` 级别
- 日志文件会自动创建目录
- 无需手动清理handlers，系统自动管理 