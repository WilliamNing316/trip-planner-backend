# 智能旅行规划多智能体系统

基于 HelloAgents 框架的多智能体系统，通过 4 个专业化 Agent 协作实现智能旅行规划。

## 功能特性

- 🎯 **多智能体协作**: 4 个专业化 Agent（景点搜索、天气查询、酒店推荐、行程规划）异步协作
- ⚡ **性能优化**: 异步并行执行，提升响应速度
- 🔄 **高可用设计**: 指数退避重试机制，提升系统稳定性
- 🛡️ **容错机制**: 智能 JSON 解析与自修复，多级降级策略
- 📊 **可观测性**: 结构化日志系统，完整的执行流程追踪

## 技术栈

- **框架**: HelloAgents
- **语言**: Python 3.x
- **协议**: Model Context Protocol (MCP)
- **服务**: 高德地图 API
- **日志**: Loguru

## 项目结构

```
backend/
├── app/
│   ├── agents/          # Agent 实现
│   │   └── trip_planner_agent.py
│   ├── api/             # API 路由
│   │   └── routes/
│   ├── models/          # 数据模型
│   ├── services/        # 服务层
│   └── utils/           # 工具模块
│       ├── retry.py     # 重试机制
│       ├── json_parser.py  # JSON 解析
│       └── logger.py    # 日志配置
├── requirements.txt
└── run.py
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# 高德地图 API Key
AMAP_API_KEY=your_amap_api_key

# LLM 配置
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=your_llm_base_url
LLM_MODEL_ID=your_model_id
```

### 3. 运行服务

```bash
python run.py
```

## 核心优化

### 异步并行执行
- 使用 `asyncio.gather` 并行执行多个 Agent
- 通过线程池执行同步 Agent 调用
- 有效降低 I/O 等待时间

### 重试机制
- 指数退避算法（exponential_base=2.0）
- 支持随机抖动
- 自动重试网络异常和 API 调用失败

### JSON 解析与修复
- 支持多种格式提取（代码块、直接 JSON 等）
- 自动修复常见格式错误
- 提升解析成功率

### 容错与降级
- 异常隔离机制
- 自动触发 fallback 方案
- 保障系统可用性

## 开发

### 代码规范
- 使用类型提示
- 遵循 PEP 8 规范
- 使用结构化日志

### 测试
```bash
# 运行测试（如果有）
pytest
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

