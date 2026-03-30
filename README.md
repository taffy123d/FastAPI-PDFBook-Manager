# FastAPI 学习项目 - 图书管理系统
专为 FastAPI 入门打造的完整学习项目，覆盖**路由分发、接口文档、Request 对象、静态文件、模板渲染、SQLite 数据库**等核心知识点。
工程结构清晰、代码注释详尽、业务逻辑极简，专注让你快速掌握 FastAPI 开发全流程。

---

## 项目特性
- ✅ 标准工程化目录结构，适合学习与扩展
- ✅ 路由分发与模块化接口管理
- ✅ 自动生成交互式 API 文档（Swagger / ReDoc）
- ✅ Pydantic 数据校验与响应格式化
- ✅ SQLite + SQLAlchemy 异步 ORM 操作
- ✅ Jinja2 模板渲染 + 静态文件支持
- ✅ 完整图书 CRUD 增删改查接口
- ✅ 依赖注入、请求对象、异常处理实战

## 技术栈
- **框架**：FastAPI
- **服务器**：Uvicorn
- **数据库**：SQLite（文件数据库，无需额外安装）
- **ORM**：SQLAlchemy 2.0（异步）
- **模板**：Jinja2
- **包管理**：uv

## 项目结构
```
fastapi_learn_project/
├── app/
│   ├── main.py                 # 项目入口，创建 app、注册路由
│   ├── core/
│   │   └── config.py           # 全局配置（数据库、路径、项目信息）
│   ├── database/
│   │   └── db.py               # 数据库引擎、会话、建表函数
│   ├── models/
│   │   └── book.py             # ORM 模型（对应数据库表）
│   ├── schemas/
│   │   └── book.py             # Pydantic 模型（请求校验 + 响应格式）
│   ├── api/
│   │   ├── api_v1.py           # v1 版本路由汇总
│   │   └── endpoints/
│   │       ├── book.py         # 图书 CRUD 接口
│   │       └── common.py       # 通用接口（Request 演示）
│   ├── templates/              # HTML 模板文件
│   └── static/                 # 静态资源（CSS 等）
├── pyproject.toml              # uv 依赖管理
└── README.md
```

---

## 快速启动（uv 包管理）
### 1. 安装依赖
```bash
uv sync
```

### 2. 启动项目
```bash
uv run uvicorn app.main:app --reload
```

### 3. 访问地址
- 项目首页：http://127.0.0.1:8000
- 图书列表页面：http://127.0.0.1:8000/book-list
- **Swagger 接口文档**：http://127.0.0.1:8000/docs
- ReDoc 接口文档：http://127.0.0.1:8000/redoc

---

# 📖 接口文档详细使用说明（/docs）
打开 `http://127.0.0.1:8000/docs` 即可看到所有接口，支持**在线调试、参数填写、响应查看**。

## 一、通用操作步骤（所有接口一致）
1. 点击任意接口右侧 **「Try it out」**
2. 填写路径参数 / 请求体参数
3. 点击 **「Execute」** 发送请求
4. 查看 **Responses** 中的状态码与返回数据

---

## 二、图书管理接口（/api/v1/books）
### 1. 获取所有图书
- **方法**：GET
- **路径**：`/api/v1/books/`
- **作用**：查询数据库中所有图书
- **参数**：无
- **成功响应**：200
  ```json
  [
    {
      "title": "Python快速入门",
      "author": "张三",
      "price": 59.9,
      "description": "零基础入门",
      "id": 1
    }
  ]
  ```

---

### 2. 根据 ID 获取单本图书
- **方法**：GET
- **路径**：`/api/v1/books/{book_id}`
- **参数**：
  - `book_id`：路径参数，图书 ID（数字）
- **成功响应**：200 + 图书信息
- **失败响应**：404 图书不存在

---

### 3. 新增图书（重点）
- **方法**：POST
- **路径**：`/api/v1/books/`
- **请求体示例（直接复制使用）**
```json
{
  "title": "Python快速入门",
  "author": "张三",
  "price": 59.9,
  "description": "适合零基础学习Python"
}
```
- **必填字段**：`title`、`author`、`price`
- `price` 必须大于 0
- `title` 不能重复
- **成功响应**：201 Created
- **失败响应**：400 书名已存在

---

### 4. 更新图书信息
- **方法**：PUT
- **路径**：`/api/v1/books/{book_id}`
- **路径参数**：`book_id` 要修改的图书 ID
- **请求体示例（可只传需要修改的字段）**
```json
{
  "price": 69.9,
  "description": "更新后的简介"
}
```
- **成功响应**：200 + 更新后数据
- **失败响应**：404 图书不存在

---

### 5. 删除图书
- **方法**：DELETE
- **路径**：`/api/v1/books/{book_id}`
- **路径参数**：`book_id`
- **成功响应**：204 No Content
- **失败响应**：404 图书不存在

---

## 三、通用接口（/api/v1/common）
### 获取请求信息
- **方法**：GET
- **路径**：`/api/v1/common/request-info`
- **作用**：演示 Request 对象用法
- 返回内容包括：请求方法、URL、IP、请求头、Cookies、查询参数等

---

## 四、页面接口（非 API JSON 接口）
### 1. 首页
- GET `/`
- 返回 HTML 首页，展示项目功能

### 2. 图书列表页面
- GET `/book-list`
- 从数据库查询图书并渲染到 HTML 页面
- 无数据时会显示提示

---

## 五、常见状态码说明
- **200**：请求/查询/修改成功
- **201**：资源创建成功（新增图书）
- **204**：删除成功（无返回内容）
- **400**：参数错误/数据重复
- **404**：资源不存在
- **422**：请求体格式/类型校验失败

---

## 学习建议
1. 先启动项目，访问 `/docs` 熟悉所有接口
2. 先新增一本书，再查询、修改、删除，完整走一遍 CRUD
3. 对照代码理解：路由 → 校验模型 → ORM 模型 → 数据库操作
4. 观察模板页面如何从数据库读取并渲染数据
5. 尝试新增字段、新增接口，加深理解

---

## uv 常用命令
```bash
# 安装依赖
uv sync

# 新增依赖包
uv add 包名

# 启动项目
uv run uvicorn app.main:app --reload

# 查看已安装包
uv pip list
```