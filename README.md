# 影刀可视化调度神器

RPA任务调度管理平台，提供美观的Web界面来管理和监控影刀机器人任务。

## 功能特性

### 🚀 核心功能
- **应用调度**: 启动、停止和监控RPA应用
- **任务调度**: 管理定时任务的执行
- **实时监控**: 实时查看任务执行状态和日志
- **参数配置**: 动态配置和管理流程参数
- **界面**: 响应式设计，支持移动端访问

### 🎨 界面特色
- 渐变色彩设计，视觉效果优美
- 动画效果和过渡，提升用户体验
- 响应式布局，适配各种屏幕尺寸
- 实时状态更新，无需手动刷新
- 控制台风格的日志显示

### 📱 技术栈
- **后端**: Flask (Python)
- **前端**: HTML5 + CSS3 + JavaScript
- **UI框架**: 自定义CSS + Font Awesome图标
- **API集成**: 影刀开放平台API

## 安装指南

### 环境要求
- Python 3.7+
- 浏览器 (Chrome, Firefox, Safari, Edge)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd trae_project
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   python app.py
   ```

4. **访问界面**
   打开浏览器访问: `http://localhost:5000`

## 使用说明

### 应用调度

1. **配置认证信息**
   - 填写机器人账号 (格式: xxx@xxx)
   - 输入Access Key ID和Secret (从影刀控制台获取)
   - 点击"获取令牌"按钮

2. **选择应用**
   - 点击"刷新应用"获取应用列表
   - 从下拉菜单中选择要执行的应用

3. **配置参数** (可选)
   - 勾选"使用流程参数"复选框
   - 点击"刷新参数"加载应用参数
   - 根据需要修改参数值

4. **执行任务**
   - 点击"启动应用"开始执行
   - 实时查看执行状态和日志
   - 可随时点击"停止应用"终止执行

### 任务调度

1. **配置任务信息**
   - 输入任务ID (从影刀控制台获取)
   - 填写Access Key ID和Secret

2. **执行定时任务**
   - 点击"启动任务"开始执行
   - 监控任务执行状态
   - 可随时停止任务

## 项目结构

```
trae_project/
├── app.py                 # Flask后端应用
├── api.py                 # API接口封装
├── main.py               # 原PyQt5界面 (已保留)
├── Qss.py                # PyQt5样式文件
├── requirements.txt      # Python依赖
├── README.md            # 项目说明
├── templates/           # HTML模板
│   └── index.html       # 主页面模板
└── static/              # 静态资源
    └── js/
        └── app.js       # 前端JavaScript
```

## API接口说明

### 认证相关
- `POST /api/get_token` - 获取访问令牌

### 应用管理
- `GET /api/get_applications` - 获取应用列表
- `POST /api/get_robot_params` - 获取机器人参数
- `POST /api/start_job` - 启动应用任务
- `POST /api/stop_job` - 停止应用任务
- `GET /api/job_status/<job_uuid>` - 获取任务状态

### 定时任务
- `POST /api/start_schedule` - 启动定时任务
- `POST /api/stop_schedule` - 停止定时任务

## 配置说明

### 影刀平台配置
1. 登录影刀控制台
2. 获取Access Key ID和Secret
3. 记录需要调度的应用UUID或任务ID

### 安全配置
- 修改`app.py`中的`secret_key`为安全的随机字符串
- 在生产环境中使用HTTPS
- 妥善保管API密钥，避免泄露

## 故障排除

### 常见问题

1. **令牌获取失败**
   - 检查Access Key ID和Secret是否正确
   - 确认网络连接正常
   - 验证影刀账号权限

2. **应用列表为空**
   - 确认已成功获取令牌
   - 检查账号下是否有可用应用
   - 验证API权限设置

3. **任务启动失败**
   - 检查机器人账号格式是否正确
   - 确认应用参数配置无误
   - 查看控制台错误信息

4. **页面无法访问**
   - 确认Flask应用已启动
   - 检查端口5000是否被占用
   - 验证防火墙设置

### 日志查看
- 后端日志: 查看终端输出
- 前端日志: 打开浏览器开发者工具

## 开发说明

### 扩展功能
1. 添加新的API接口到`app.py`
2. 在`static/js/app.js`中添加前端逻辑
3. 更新`templates/index.html`添加UI元素

### 自定义样式
- 修改`templates/index.html`中的CSS样式
- 调整颜色主题和布局
- 添加新的动画效果

## 版本历史

### v2.0.0 (当前版本)
- 全新Web界面设计
- 实时状态监控
- 响应式布局
- 改进的用户体验

### v1.0.0 (原版本)
- PyQt5桌面应用
- 基础功能实现

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进项目！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 请确保在使用前已正确配置影刀平台的API密钥，并遵守相关服务条款。
