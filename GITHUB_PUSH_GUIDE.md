# GitHub 推送完整流程指南

## 前提条件

1. 已安装 Git
2. 已注册 GitHub 账号
3. 已配置 Git 用户信息（如果未配置，见步骤1）

---

## 完整流程

### 步骤 1: 配置 Git 用户信息（首次使用需要）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

### 步骤 2: 初始化 Git 仓库

在项目根目录（backend文件夹）执行：

```bash
# 初始化git仓库
git init

# 查看当前状态
git status
```

### 步骤 3: 添加 .gitignore（已存在，检查是否完整）

检查 `.gitignore` 文件是否包含以下内容（你的文件已经包含了）：

- Python 相关文件（`__pycache__/`, `*.pyc` 等）
- 虚拟环境（`venv/`, `.venv` 等）
- 环境变量文件（`.env`）
- IDE 配置（`.vscode/`, `.idea/` 等）
- 日志文件（`*.log`）
- 操作系统文件（`.DS_Store` 等）

如果需要添加日志目录，可以添加：
```
logs/
```

### 步骤 4: 添加所有文件到暂存区

```bash
# 添加所有文件（.gitignore 中排除的文件不会添加）
git add .

# 或者只添加特定文件
git add app/ requirements.txt run.py
```

### 步骤 5: 创建初始提交

```bash
git commit -m "初始提交: 智能旅行规划多智能体系统

- 实现基于 HelloAgents 的多智能体系统
- 集成 MCP 协议对接高德地图服务
- 实现异步并行执行和重试机制
- 添加 JSON 解析与修复功能
- 实现结构化日志系统"
```

### 步骤 6: 在 GitHub 上创建新仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `helloagents-trip-planner`（或你喜欢的名字）
   - **Description**: `基于 HelloAgents 框架的智能旅行规划多智能体系统`
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为本地已有代码）
4. 点击 "Create repository"

### 步骤 7: 添加远程仓库并推送

GitHub 创建仓库后会显示推送命令，通常有两种方式：

#### 方式 A: HTTPS（推荐，简单）

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/helloagents-trip-planner.git

# 查看远程仓库
git remote -v

# 推送到 GitHub（首次推送）
git push -u origin main
```

如果默认分支是 `master` 而不是 `main`：

```bash
# 重命名本地分支为 main（如果需要）
git branch -M main

# 推送到 GitHub
git push -u origin main
```

#### 方式 B: SSH（需要配置 SSH 密钥）

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin git@github.com:YOUR_USERNAME/helloagents-trip-planner.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 8: 验证推送成功

1. 在浏览器中打开你的 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查文件结构是否正确

---

## 后续更新代码流程

当你修改代码后，使用以下命令更新 GitHub：

```bash
# 1. 查看修改的文件
git status

# 2. 添加修改的文件
git add .

# 或者添加特定文件
git add app/agents/trip_planner_agent.py

# 3. 提交更改
git commit -m "优化: 实现 Agent 并行执行和重试机制"

# 4. 推送到 GitHub
git push
```

---

## 常见问题解决

### 问题 1: 推送时要求输入用户名密码

**解决方案**: 使用 Personal Access Token (PAT)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 选择权限：至少勾选 `repo`
4. 生成后复制 token
5. 推送时密码输入框输入 token（不是 GitHub 密码）

或者配置 SSH 密钥（更安全，推荐）

### 问题 2: 分支名称不匹配

如果本地是 `master` 而远程是 `main`：

```bash
# 重命名本地分支
git branch -M main

# 推送
git push -u origin main
```

### 问题 3: 远程仓库已存在文件

如果 GitHub 仓库初始化时创建了 README：

```bash
# 先拉取远程内容
git pull origin main --allow-unrelated-histories

# 解决可能的冲突后
git push -u origin main
```

### 问题 4: 忘记添加 .env 文件到 .gitignore

如果误提交了敏感文件：

```bash
# 从 git 历史中移除（但保留本地文件）
git rm --cached .env

# 提交更改
git commit -m "移除敏感文件"

# 推送到 GitHub
git push
```

---

## 推荐的仓库结构

推送后，你的 GitHub 仓库应该包含：

```
helloagents-trip-planner/
├── app/
│   ├── agents/
│   │   └── trip_planner_agent.py
│   ├── api/
│   │   └── routes/
│   ├── models/
│   ├── services/
│   └── utils/
│       ├── retry.py
│       ├── json_parser.py
│       └── logger.py
├── .gitignore
├── requirements.txt
└── run.py
```

---

## 快速命令参考

```bash
# 初始化仓库
git init

# 添加文件
git add .

# 提交
git commit -m "提交信息"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 推送
git push -u origin main

# 查看状态
git status

# 查看提交历史
git log
```

---

## 安全提示

⚠️ **重要**: 确保以下文件在 `.gitignore` 中：

- `.env` - 包含 API 密钥等敏感信息
- `*.log` - 日志文件可能包含敏感信息
- `venv/` 或 `.venv/` - 虚拟环境不需要上传

推送前检查：

```bash
# 查看将要提交的文件
git status

# 确认没有敏感文件
git diff --cached
```

