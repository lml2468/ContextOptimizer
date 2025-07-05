### **ContextOptimizer 系统概要设计文档**

**版本: 1.0**

---

### **1. 引言 (Introduction)**

#### **1.1 项目背景**
多智能体系统（Multi-Agent System, MAS）是实现复杂任务自动化的前沿技术，其潜力巨大但工程化挑战严峻。系统的稳定性、效率和可靠性在很大程度上取决于两个关键要素：各个Agent的**System Prompt**设计质量，以及**工具返回信息**的结构化程度。当前，这两个核心要素的优化类似于一门"玄学"，严重依赖开发者的个人经验和大量的手动试错，缺乏数据驱动的、可复现的优化方法。

#### **1.2 问题陈述**
当一个MAS任务执行失败或表现不佳时，问题往往源于两个层面：
1. **System Prompt层面**: 指令不够明确、逻辑不够清晰、约束不够严格
2. **工具信息层面**: 工具返回的信息结构混乱、关键信息缺失、冗余信息干扰

这些微观问题会导致宏观的**上下文逻辑断裂**，使得整个MAS的协作链路变得混乱和低效。开发者迫切需要一个工具来回答："**如何同时优化System Prompt和工具返回信息，让整个MAS的上下文逻辑变得清晰、通畅、连贯？**"

#### **1.3 项目愿景与目标**
`ContextOptimizer`旨在成为MAS开发者的**智能上下文工程助手 (Intelligent Context Engineering Assistant)**，专注于**System Prompt + 工具返回信息**的协同优化，确保MAS的上下文逻辑清晰连贯。

*   **核心愿景**: 通过协同优化System Prompt和工具返回信息，让MAS的上下文流转变得像精心编排的交响乐一样和谐流畅。
*   **主要目标**:
    1.  **上下文逻辑诊断 (Context Logic Diagnosis)**: 自动识别System Prompt和工具返回信息中导致**上下文断裂**的设计缺陷
    2.  **协同优化生成 (Coordinated Optimization)**: 同时优化System Prompt和工具返回信息结构，确保两者协同效果最佳
    3.  **可用方案输出 (Actionable Solutions)**: 生成可直接使用的优化配置和实施指南
    4.  **最佳实践沉淀 (Best Practices Accumulation)**: 积累经过验证的设计模式和标准

#### **1.4 范围 (Scope)**
*   **范围内 (In-Scope)**:
    *   System Prompt的逻辑结构诊断和优化建议
    *   工具返回信息的结构化分析和改进方案
    *   上下文信息传递逻辑的问题识别和修复
    *   协同优化方案的生成和效果预测
*   **范围外 (Out-of-Scope)**:
    *   工具本身的功能实现和性能优化
    *   Agent推理能力的底层算法改进
    *   实时性能监控和成本分析

---

### **2. 系统架构 (System Architecture)**

系统采用"极简LLM驱动"架构，基于大模型能力进行智能诊断和优化，去除所有不必要的复杂性。

#### **2.1 整体架构图**

```
+-------------------------------------------------------------------------+
|                              Web Interface                              |
|                   (Upload, Analysis Report, Optimization)              |
+-------------------------------------------------------------------------+
       ^                                                 |
       | Sync API Calls (Get Results)                    | Sync API Calls (Upload Data)
       v                                                 v
+-------------------------------------------------------------------------+
|                             Backend API Server                          |
|               (FastAPI: Sync Processing, File Management)              |
+------------------------------------+------------------------------------+
       |                             |
       | (Direct LLM Calls)          | (Direct File I/O)
       v                             v
+--------------------------------+----------------------------------------+
|   LLM-Driven Analysis Engine  |      File-Based Storage                |
|                                |   +--------------------------------+   |
| +----------------------------+ |   |  Local File System             |   |
| | Context Evaluation Module  | |   |  - Session Directories         |   |
| | (LLM + Evaluation Prompts) | |   |  - JSON Files                  |   |
| +----------------------------+ |   |  - Temporary Storage            |   |
| | Coordinated Optimization   | |   +--------------------------------+   |
| | (LLM + Optimization Prompts)| |   |  In-Memory Cache               |   |
| +----------------------------+ |   |  - Python Dict                 |   |
|                                |   |  - Simple Variables             |   |
+--------------------------------+   +--------------------------------+   |
```

#### **2.2 架构特点**
- **零外部依赖**: 无需数据库、Redis、消息队列等外部服务
- **同步处理**: 直接的请求-响应模式，用户等待分析完成
- **文件存储**: 基于本地文件系统的临时存储
- **LLM驱动**: 核心逻辑完全基于精心设计的提示词
- **单一部署**: 一个容器包含所有功能

#### **2.3 数据流向**
```
用户上传文件 → 创建会话目录 → 保存输入数据 → 调用LLM分析 → 
保存分析结果 → 调用LLM优化 → 保存优化方案 → 返回完整结果
```

---

### **3. 核心工作流程 (User Workflow)**

开发者的使用路径专注于"快速诊断、获得方案"的高效闭环。

#### **3.1 用户旅程图**
```
步骤1: 数据准备        步骤2: 上传分析        步骤3: 查看报告        步骤4: 获取方案        步骤5: 应用优化
    ↓                     ↓                    ↓                    ↓                    ↓
导出配置文件           拖拽上传到网页         查看评分和问题        复制优化配置          应用到MAS系统
导出对话数据           选择分析选项           了解根因分析          下载实施指南          验证改进效果
                     等待分析完成           按优先级查看问题      预览改进效果
```

#### **3.2 详细步骤**

**步骤1: 数据准备 (Data Preparation)**
- 从MAS系统导出Agent配置文件 (agents_config.json)
- 导出完整的对话数据 (messages_dataset.json)
- 确保数据包含失败或问题案例

**步骤2: 上传分析 (Upload & Analysis)**
- 通过Web界面拖拽上传两个JSON文件
- 选择分析深度（快速/深度诊断）
- 点击开始分析，等待2-3分钟获得结果

**步骤3: 查看报告 (Report Review)**
- 查看5个维度的量化评分
- 按优先级查看问题清单（高/中/低）
- 了解根因分析和影响评估

**步骤4: 获取方案 (Solution Acquisition)**
- 查看优化后的System Prompt
- 获得工具信息结构建议
- 了解预期的改进效果

**步骤5: 应用优化 (Implementation)**
- 一键复制优化后的配置
- 下载完整的实施指南
- 应用到实际MAS系统并验证效果

---

### **4. 数据模式定义 (Data Schema Definition)**

#### **4.1 输入数据格式**

**Agent配置文件 (agents_config.json)**
- 包含所有Agent的基本信息、系统提示词和工具配置
- 支持多种Agent类型：Supervisor、Worker、Specialist等
- 清晰定义每个Agent的职责范围和工具权限

**agents_config.json 示例**:
```json
[
  {
    "agent_id": "supervisor",
    "agent_name": "Supervisor Agent",
    "version": "1.0",
    "system_prompt": "You are a supervisor agent responsible for coordinating multi-agent workflows. When receiving user requests, you should: 1) Analyze the task requirements using the think tool, 2) Create structured plans with the planning tool, 3) Delegate tasks to appropriate workers with clear context and goals.",
    "tools": [
      {
        "name": "think", 
        "description": "Internal reasoning and planning tool"
      },
      {
        "name": "planning",
        "description": "Create and manage execution plans"
      },
      {
        "name": "transfer_to_browser_use_worker",
        "description": "Delegate web browsing and data extraction tasks"
      },
      {
        "name": "transfer_to_coder_worker", 
        "description": "Delegate coding and development tasks"
      }
    ]
  },
  {
    "agent_id": "browser_use_worker",
    "agent_name": "Browser Use Worker",
    "version": "1.0", 
    "system_prompt": "You are a browser use worker responsible for web browsing and data extraction. When delegated tasks, you should: 1) Access specified websites, 2) Extract required information comprehensively, 3) Provide structured analysis results, 4) Transfer back to supervisor with complete findings.",
    "tools": [
      {
        "name": "transfer_to_supervisor",
        "description": "Transfer completed task back to supervisor"
      }
    ]
  },
  {
    "agent_id": "coder_worker",
    "agent_name": "Coder Worker", 
    "version": "1.0",
    "system_prompt": "You are a coder worker responsible for development tasks. When delegated tasks, you should: 1) Use think tool to analyze requirements, 2) Implement code solutions using file_editor, 3) Ensure code quality and functionality, 4) Transfer completed work back to supervisor.",
    "tools": [
      {
        "name": "think",
        "description": "Internal reasoning for development planning"
      },
      {
        "name": "file_editor", 
        "description": "Create and edit files"
      },
      {
        "name": "transfer_to_supervisor",
        "description": "Transfer completed task back to supervisor"
      }
    ]
  }
]
```

**对话数据文件 (messages_dataset.json)**
- 包含完整的多Agent协作对话流程
- 记录所有的工具调用和响应
- 保留Agent间的信息传递链路

**messages_dataset.json 示例**:
```json
{
  "messages": [
    {
      "content": "请使用web_search和crawl功能对喵啊网站进行深入分析，并基于提取的关键元素完成UI重新设计。",
      "type": "human",
      "name": null,
      "id": "362b1caa-5744-4409-ad3b-caad1b03f0c6",
      "example": false
    },
    {
      "content": "",
      "type": "ai",
      "name": "supervisor",
      "id": "run--ec043387-8db5-4656-ace2-a0100f808dc5",
      "example": false,
      "tool_calls": [
        {
          "name": "think",
          "args": {
            "thought": "用户要求对喵啊网站进行深入分析并完成UI重新设计。这是一个复杂的多步骤任务，需要：\n\n1. 网站内容抓取与分析\n2. 基于分析结果进行UI重新设计\n3. 提供完整的设计交付成果"
          },
          "id": "toolu_vrtx_01FTBerNUSnPNcoaPQUeNPvV",
          "type": "tool_call"
        }
      ],
      "invalid_tool_calls": [],
      "usage_metadata": null
    },
    {
      "content": "",
      "type": "tool",
      "name": "think",
      "id": "ddd2033d-0360-4149-9751-db840c21e21b",
      "tool_call_id": "toolu_vrtx_01FTBerNUSnPNcoaPQUeNPvV",
      "artifact": {
        "attachments": [
          {
            "type": "text",
            "data": "用户要求对喵啊网站进行深入分析并完成UI重新设计。这是一个复杂的多步骤任务。",
            "mime_type": "text/plain"
          }
        ]
      },
      "status": "success"
    },
    {
      "content": "",
      "type": "ai",
      "name": "supervisor",
      "id": "run--2de418b4-0987-4800-8fa2-08eff9b80103",
      "example": false,
      "tool_calls": [
        {
          "name": "transfer_to_browser_use_worker",
          "args": {
            "task_goal": "对喵啊网站进行深入分析并重新设计为简约大气的专业SaaS官网风格，最终交付完整可运行的HTML官网",
            "current_step_goal": "访问喵啊网站并抓取关键页面内容，提取品牌信息、配色方案、核心业务、内容架构等关键元素。"
          },
          "id": "toolu_vrtx_015YGx7wEEeoZUEjdWssHsL5",
          "type": "tool_call"
        }
      ],
      "invalid_tool_calls": [],
      "usage_metadata": null
    },
    {
      "content": "Workflow Delegation: supervisor has delegated the task to browser_use_worker.",
      "type": "tool",
      "name": "transfer_to_browser_use_worker",
      "id": "766c3fba-d1c0-40d3-aab6-3c872c465e03",
      "tool_call_id": "toolu_vrtx_015YGx7wEEeoZUEjdWssHsL5",
      "artifact": null,
      "status": "success"
    }
  ]
}
```

#### **4.2 输出数据格式**

**评估报告 (evaluation_report.json)**
- 5个维度的量化评分 (1-10分)
- 按优先级分类的问题清单
- 详细的根因分析和改进建议

**优化方案 (optimization_result.json)**
- 优化后的完整Agent配置
- 工具返回信息的标准化格式
- 修改说明和预期改进效果

#### **4.3 会话管理结构**
```
/tmp/context-optimizer/
├── sessions/
│   ├── {session_id}/
│   │   ├── input/
│   │   │   ├── agents_config.json
│   │   │   └── messages_dataset.json
│   │   ├── analysis/
│   │   │   ├── evaluation_report.json
│   │   │   └── optimization_result.json
│   │   └── metadata.json
│   └── ...
└── cache/
    └── llm_responses/
```

---

### **5. 核心组件详解 (Detailed Component Breakdown)**

#### **5.1 上下文评估模块 (Context Evaluation Module)**

**功能职责**
- 基于精心设计的评估提示词，驱动大模型进行全面分析
- 评估Agent角色职责一致性、工作流程规范性、工具调用合规性
- 识别协作质量问题和系统设计缺陷
- 生成量化评分和详细问题清单

**核心评估维度**
1. **角色职责一致性**: 检查各Agent是否在其定义职责范围内行动
2. **工作流程规范性**: 验证是否遵循标准的协作流程
3. **工具调用合规性**: 确保工具使用符合配置和权限要求
4. **协作质量**: 评估任务分解、信息传递、协作效率
5. **系统设计质量**: 发现配置缺失、职责模糊等设计问题

**输出格式**
- 整体评分矩阵（1-10分制）
- 分优先级的问题清单
- 根因分析报告
- 具体的改进方向建议

#### **5.2 协同优化模块 (Coordinated Optimization Module)**

**功能职责**
- 基于评估结果，使用优化提示词驱动大模型生成改进方案
- 同时优化System Prompt和工具信息结构
- 确保所有优化组件在逻辑上保持一致
- 提供可直接使用的配置和实施指南

**核心优化策略**
1. **System Prompt重构**: 指令清晰化、约束强化、流程标准化
2. **工具信息标准化**: 返回结构统一、关键信息突出、错误处理规范
3. **协作流程优化**: 任务分解改进、信息传递增强、效率提升
4. **质量保证**: 一致性检查、完整性验证、兼容性保证

**输出格式**
- 优化后的完整Agent配置
- 工具返回信息规范和格式建议
- 详细的修改说明和理由
- 量化的预期改进效果

---

### **6. 用户界面设计 (User Interface Design)**

#### **6.1 设计理念**

**开发者工具化体验**
- 界面简洁专业，类似IDE和开发工具的审美
- 功能导向，每个页面都有明确的任务目标
- 效率优先，最短路径完成核心工作流程
- 结果导向，突出显示最重要的信息和行动建议

#### **6.2 主要页面设计**

**数据上传页面**
- 大面积的拖拽上传区域，支持多文件同时上传
- 清晰的文件格式说明和示例
- 上传进度指示和文件验证反馈
- 分析选项配置（快速/深度模式）
- 一键开始分析的主要行动按钮

**分析报告页面**
- 顶部展示5个维度的评分仪表板
- 按优先级分组的问题清单（红/黄/绿色标识）
- 折叠式的详细问题描述和影响分析
- 简洁的根因分析总结
- 明确的"查看优化方案"行动指引

**优化方案页面**
- 左右分栏对比优化前后的配置
- 每个Agent的优化内容独立展示
- 一键复制优化后配置的功能
- 工具信息格式规范的代码块展示
- 预期改进效果的量化指标
- 完整配置文件的下载功能

#### **6.3 交互设计原则**

**无学习成本**
- 界面布局符合开发者的使用习惯
- 功能图标和按钮使用业界标准
- 重要操作提供明确的视觉反馈

**效率优先**
- 关键信息在一屏内完整展示
- 支持键盘快捷键操作
- 提供批量复制和下载功能

**结果导向**
- 突出显示最重要的问题和解决方案
- 每个问题都有明确的修复建议
- 清晰展示优化后的预期效果

#### **6.4 响应式设计**

**桌面端优先**
- 主要针对开发者的桌面工作环境
- 充分利用大屏幕空间展示详细信息
- 支持多窗口并行工作

**移动端适配**
- 简化的移动端界面，主要用于查看报告
- 关键信息的垂直布局
- 核心功能的触摸友好设计

---

### **7. 技术选型 (Technology Stack)**

#### **7.1 极简技术栈**

| 类别 | 技术选型 | 选择理由 |
| :--- | :--- | :--- |
| **后端框架** | Python + FastAPI | 轻量级、同步处理、快速开发、零配置 |
| **前端框架** | React + Next.js | 成熟生态、开发者友好、静态部署 |
| **UI组件库** | Tailwind CSS + Headless UI | 灵活定制、现代审美、无额外依赖 |
| **数据存储** | 本地文件系统 + JSON | 零配置、直接可用、透明存储 |
| **缓存系统** | Python内存字典 | 进程内缓存、无外部依赖 |
| **会话管理** | 文件系统目录结构 | 天然隔离、简单可靠 |
| **任务处理** | 同步HTTP请求 | 简单直接、用户体验清晰 |
| **LLM服务** | OpenAI API / Anthropic API | 强大的推理能力、稳定的服务 |
| **部署方式** | 单一Docker容器 | 最简部署、零配置启动 |

#### **7.2 技术选型原则**

**简单优于复杂**
- 优先选择零配置的技术方案
- 避免引入不必要的中间件和服务
- 减少系统的组件数量和依赖关系

**可靠优于先进**
- 选择经过验证的成熟技术
- 避免使用实验性或过于新颖的工具
- 确保技术栈的长期稳定性

**实用优于完美**
- 满足核心功能需求即可
- 避免过度工程和功能冗余
- 专注于解决实际问题

---

### **8. 项目代码目录结构设计 (Project Structure Design)**

#### **8.1 整体目录结构**

```
context-optimizer/
├── README.md                           # 项目说明文档
├── LICENSE                             # 开源协议
├── .gitignore                          # Git忽略文件
├── .env.example                        # 环境变量示例
├── docker-compose.yml                  # Docker编排文件
├── Dockerfile                          # 单一容器构建文件
├── requirements.txt                    # Python依赖清单
├── pyproject.toml                      # Python项目配置
│
├── backend/                            # 后端服务
│   ├── app/                           # 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI应用入口
│   │   ├── config.py                  # 应用配置
│   │   │
│   │   ├── api/                       # API路由层
│   │   │   ├── __init__.py
│   │   │   ├── v1/                    # API版本目录
│   │   │   │   ├── __init__.py
│   │   │   │   ├── upload.py          # 文件上传API
│   │   │   │   ├── analysis.py        # 分析任务API
│   │   │   │   ├── sessions.py        # 会话管理API
│   │   │   │   └── health.py          # 健康检查API
│   │   │   └── deps.py                # API依赖注入
│   │   │
│   │   ├── core/                      # 核心业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── evaluator.py           # 上下文评估器
│   │   │   ├── optimizer.py           # 协同优化器
│   │   │   └── prompts.py             # LLM提示词模板
│   │   │
│   │   ├── services/                  # 业务服务层
│   │   │   ├── __init__.py
│   │   │   ├── session_service.py     # 会话管理服务
│   │   │   ├── file_service.py        # 文件处理服务
│   │   │   └── llm_service.py         # LLM调用服务
│   │   │
│   │   ├── models/                    # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py             # Pydantic数据模型
│   │   │   ├── agent.py               # Agent相关模型
│   │   │   ├── message.py             # 消息相关模型
│   │   │   └── session.py             # 会话相关模型
│   │   │
│   │   ├── utils/                     # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── file_utils.py          # 文件操作工具
│   │   │   ├── validation.py          # 数据验证工具
│   │   │   ├── cache.py               # 缓存工具
│   │   │   ├── logger.py              # 日志工具
│   │   │   └── exceptions.py          # 自定义异常
│   │   │
│   │   └── middleware/                # 中间件
│   │       ├── __init__.py
│   │       ├── cors.py                # 跨域处理
│   │       ├── error_handler.py       # 错误处理
│   │       └── logging.py             # 请求日志
│   │
│   ├── tests/                         # 测试文件
│   │   ├── __init__.py
│   │   ├── conftest.py                # pytest配置
│   │   ├── test_api/                  # API测试
│   │   │   ├── __init__.py
│   │   │   ├── test_upload.py
│   │   │   └── test_sessions.py
│   │   ├── test_core/                 # 核心逻辑测试
│   │   │   ├── __init__.py
│   │   │   ├── test_evaluator.py
│   │   │   └── test_optimizer.py
│   │   ├── test_services/             # 服务层测试
│   │   │   ├── __init__.py
│   │   │   ├── test_session_service.py
│   │   │   └── test_llm_service.py
│   │   └── fixtures/                  # 测试数据
│   │       ├── sample_agents_config.json
│   │       └── sample_messages_dataset.json
│   │
│   └── scripts/                       # 脚本文件
│       ├── setup.py                   # 环境设置脚本
│       ├── cleanup.py                 # 数据清理脚本
│       └── health_check.py            # 健康检查脚本
│
├── frontend/                          # 前端应用
│   ├── package.json                   # Node.js依赖配置
│   ├── next.config.js                 # Next.js配置
│   ├── tailwind.config.js             # Tailwind CSS配置
│   ├── tsconfig.json                  # TypeScript配置
│   ├── .eslintrc.json                 # ESLint配置
│   │
│   ├── public/                        # 静态资源
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   └── images/
│   │       ├── upload-icon.svg
│   │       └── analysis-bg.jpg
│   │
│   ├── src/                           # 源代码
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── layout.tsx             # 根布局组件
│   │   │   ├── page.tsx               # 首页
│   │   │   ├── upload/
│   │   │   │   └── page.tsx           # 上传页面
│   │   │   ├── analysis/
│   │   │   │   └── [sessionId]/
│   │   │   │       └── page.tsx       # 分析报告页面
│   │   │   ├── optimization/
│   │   │   │   └── [sessionId]/
│   │   │   │       └── page.tsx       # 优化方案页面
│   │   │   ├── globals.css            # 全局样式
│   │   │   └── not-found.tsx          # 404页面
│   │   │
│   │   ├── components/                # 可复用组件
│   │   │   ├── ui/                    # 基础UI组件
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── progress.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   └── dialog.tsx
│   │   │   │
│   │   │   ├── layout/                # 布局组件
│   │   │   │   ├── header.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   ├── sidebar.tsx
│   │   │   │   └── main-layout.tsx
│   │   │   │
│   │   │   ├── upload/                # 上传相关组件
│   │   │   │   ├── file-uploader.tsx
│   │   │   │   ├── upload-zone.tsx
│   │   │   │   ├── file-list.tsx
│   │   │   │   └── analysis-options.tsx
│   │   │   │
│   │   │   ├── analysis/              # 分析相关组件
│   │   │   │   ├── score-dashboard.tsx
│   │   │   │   ├── problem-list.tsx
│   │   │   │   ├── problem-item.tsx
│   │   │   │   ├── root-cause-summary.tsx
│   │   │   │   └── loading-spinner.tsx
│   │   │   │
│   │   │   ├── optimization/          # 优化相关组件
│   │   │   │   ├── config-comparison.tsx
│   │   │   │   ├── agent-optimization.tsx
│   │   │   │   ├── tool-format-spec.tsx
│   │   │   │   ├── improvement-metrics.tsx
│   │   │   │   └── download-button.tsx
│   │   │   │
│   │   │   └── common/                # 通用组件
│   │   │       ├── loading.tsx
│   │   │       ├── error-boundary.tsx
│   │   │       ├── copy-button.tsx
│   │   │       └── status-indicator.tsx
│   │   │
│   │   ├── lib/                       # 工具库
│   │   │   ├── api.ts                 # API客户端
│   │   │   ├── utils.ts               # 通用工具函数
│   │   │   ├── validations.ts         # 前端验证
│   │   │   ├── constants.ts           # 常量定义
│   │   │   └── formatters.ts          # 数据格式化
│   │   │
│   │   ├── hooks/                     # 自定义Hooks
│   │   │   ├── useApi.ts              # API调用Hook
│   │   │   ├── useUpload.ts           # 文件上传Hook
│   │   │   ├── useAnalysis.ts         # 分析状态Hook
│   │   │   ├── useSession.ts          # 会话管理Hook
│   │   │   └── useLocalStorage.ts     # 本地存储Hook
│   │   │
│   │   ├── types/                     # TypeScript类型定义
│   │   │   ├── api.ts                 # API响应类型
│   │   │   ├── agent.ts               # Agent相关类型
│   │   │   ├── message.ts             # 消息相关类型
│   │   │   ├── analysis.ts            # 分析结果类型
│   │   │   ├── session.ts             # 会话相关类型
│   │   │   └── common.ts              # 通用类型
│   │   │
│   │   ├── styles/                    # 样式文件
│   │   │   ├── globals.css            # 全局样式
│   │   │   ├── components.css         # 组件样式
│   │   │   └── themes.css             # 主题样式
│   │   │
│   │   └── contexts/                  # React Context
│   │       ├── session-context.tsx    # 会话上下文
│   │       ├── theme-context.tsx      # 主题上下文
│   │       └── error-context.tsx      # 错误处理上下文
│   │
│   └── __tests__/                     # 前端测试
│       ├── components/                # 组件测试
│       ├── hooks/                     # Hook测试
│       ├── pages/                     # 页面测试
│       └── utils/                     # 工具函数测试
│
├── docs/                              # 项目文档
│   ├── README.md                      # 文档首页
│   ├── CONTRIBUTING.md                # 贡献指南
│   ├── CHANGELOG.md                   # 更新日志
│   │
│   ├── api/                           # API文档
│   │   ├── overview.md                # API概览
│   │   ├── authentication.md          # 认证说明
│   │   ├── upload.md                  # 上传接口
│   │   ├── analysis.md                # 分析接口
│   │   └── sessions.md                # 会话接口
│   │
│   ├── user-guide/                    # 用户指南
│   │   ├── getting-started.md         # 快速开始
│   │   ├── data-preparation.md        # 数据准备
│   │   ├── analysis-guide.md          # 分析指南
│   │   ├── optimization-guide.md      # 优化指南
│   │   └── troubleshooting.md         # 故障排除
│   │
│   ├── development/                   # 开发文档
│   │   ├── setup.md                   # 开发环境设置
│   │   ├── architecture.md            # 架构说明
│   │   ├── coding-standards.md        # 编码规范
│   │   └── testing.md                 # 测试指南
│   │
│   └── deployment/                    # 部署文档
│       ├── docker.md                  # Docker部署
│       ├── production.md              # 生产环境部署
│       ├── configuration.md           # 配置说明
│       └── monitoring.md              # 监控指南
│
├── scripts/                           # 项目脚本
│   ├── setup.sh                      # 项目初始化脚本
│   ├── build.sh                      # 构建脚本
│   ├── test.sh                       # 测试脚本
│   ├── deploy.sh                     # 部署脚本
│   ├── cleanup.sh                    # 清理脚本
│   └── health-check.sh               # 健康检查脚本
│
├── examples/                          # 示例文件
│   ├── sample-data/                   # 示例数据
│   │   ├── simple-workflow/
│   │   │   ├── agents_config.json
│   │   │   └── messages_dataset.json
│   │   ├── complex-workflow/
│   │   │   ├── agents_config.json
│   │   │   └── messages_dataset.json
│   │   └── error-cases/
│   │       ├── agents_config.json
│   │       └── messages_dataset.json
│   │
│   └── integration/                   # 集成示例
│       ├── python-client.py           # Python客户端示例
│       ├── curl-examples.sh           # cURL使用示例
│       └── postman-collection.json    # Postman集合
│
└── .github/                           # GitHub配置
    ├── workflows/                     # GitHub Actions
    │   ├── ci.yml                     # 持续集成
    │   ├── cd.yml                     # 持续部署
    │   └── release.yml                # 发布流程
    ├── ISSUE_TEMPLATE/                # Issue模板
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── question.md
    └── pull_request_template.md       # PR模板
```

#### **8.2 目录组织原则**

**模块化设计**
- 每个功能模块都有独立的目录
- 相关文件集中管理，便于维护
- 清晰的依赖关系和接口定义

**职责分离**
- API层、服务层、核心逻辑层分离
- 前端组件按功能和层级组织
- 配置、文档、测试独立管理

**开发友好**
- 目录结构直观易懂
- 文件命名规范统一
- 便于新开发者快速上手

**扩展性考虑**
- 预留了功能扩展的空间
- 支持插件化的组件开发
- 便于后续的重构和优化

#### **8.3 核心文件说明**

**后端关键文件**
- `main.py`: FastAPI应用的启动入口
- `config.py`: 统一的配置管理
- `evaluator.py`: 核心的上下文评估逻辑
- `optimizer.py`: 协同优化算法实现
- `prompts.py`: LLM提示词模板管理

**前端关键文件**
- `layout.tsx`: 应用的根布局组件
- `file-uploader.tsx`: 文件上传核心组件
- `score-dashboard.tsx`: 评分展示仪表板
- `config-comparison.tsx`: 配置对比组件
- `api.ts`: 统一的API调用客户端

**配置文件**
- `docker-compose.yml`: 简化的容器编排
- `requirements.txt`: Python依赖管理
- `package.json`: Node.js依赖管理
- `tailwind.config.js`: UI样式配置

---

### **9. 核心创新点 (Core Innovations)**

#### **9.1 LLM驱动的智能分析**
**创新点**: 完全基于大模型能力进行上下文分析，无需复杂的传统算法
**技术价值**: 具备强大的理解和推理能力，能处理各种复杂的上下文问题
**商业价值**: 快速迭代，易于优化，能适应不同的MAS架构和需求

#### **9.2 双轨协同优化**
**创新点**: 首次将System Prompt和工具返回信息作为一个协同系统进行优化
**技术价值**: 避免单点优化导致的系统性问题，确保整体上下文逻辑的一致性
**商业价值**: 解决了行业中普遍存在的"头痛医头，脚痛医脚"的优化问题

#### **9.3 提示词工程驱动**
**创新点**: 核心逻辑完全通过精心设计的提示词实现，而非传统编程
**技术价值**: 高度灵活，易于迭代优化，能快速适应新的分析需求
**商业价值**: 降低了技术门槛，非专业开发者也能参与优化和改进

#### **9.4 极简部署架构**
**创新点**: 零外部依赖的极简架构，一键部署即可使用
**技术价值**: 降低了部署复杂度，提高了系统稳定性
**商业价值**: 大幅降低了用户的使用成本和学习成本

#### **9.5 开发者工具化体验**
**创新点**: 将复杂的AI分析包装成简洁直观的开发者工具
**技术价值**: 提供了专业、高效的工作界面
**商业价值**: 符合目标用户的使用习惯，提升了产品的接受度

---

这份设计文档为ContextOptimizer项目提供了全面而详细的指导，确保项目能够作为一个真正有效的**智能上下文工程助手**，通过极简的架构设计和强大的LLM驱动分析能力，帮助MAS开发者快速发现问题、获得优化方案，并显著提升多智能体系统的质量和效率。