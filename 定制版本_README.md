# RustDesk 定制版本 - 完整指南

## 🎯 项目概述

本项目是 RustDesk 的定制版本，已预配置：
- ✅ 自建服务器：39.97.50.6
- ✅ 固定密码：28b5hD8S26
- ✅ 无人值守模式
- ✅ Windows 无弹窗
- ✅ 完全控制权限

---

## 📚 文档导航

### 🚀 快速开始（推荐）

1. **[编译方式对比.md](./编译方式对比.md)** - 选择最适合你的编译方式
2. **[使用GitHub_Actions编译步骤.md](./使用GitHub_Actions编译步骤.md)** - 详细的 GitHub Actions 使用教程

### ⚙️ 配置说明

3. **[配置说明.md](./配置说明.md)** - 三种配置方案对比
4. **[预设配置清单.md](./预设配置清单.md)** - 所有配置选项详解
5. **[编译和部署说明.md](./编译和部署说明.md)** - 本地编译方法

### 🔧 技术文档

6. **[GitHub_Actions使用指南.md](./GitHub_Actions使用指南.md)** - GitHub Actions 快速参考
7. **[生成custom.txt说明.md](./生成custom.txt说明.md)** - custom.txt 方案说明

---

## ⚡ 快速开始（3 步）

### 使用 GitHub Actions（推荐）

```bash
# 1. 推送代码到 GitHub
git init
git add .
git commit -m "初始提交"
git remote add origin https://github.com/你的用户名/rustdesk-custom.git
git push -u origin master

# 2. 在 GitHub 网页上
#    Actions → Custom Build → Run workflow → 选择 windows

# 3. 等待完成后下载编译产物
#    下载 rustdesk-windows-custom.zip
```

**详细步骤：** 查看 `使用GitHub_Actions编译步骤.md`

---

### 或本地编译

```powershell
# 编译
cargo build --release --features default_config

# 运行
.\target\release\rustdesk.exe
```

**详细步骤：** 查看 `编译和部署说明.md`

---

## 📦 已配置的内容

### 服务器配置
```
ID 服务器: 39.97.50.6
Relay 服务器: 39.97.50.6
API 服务器: http://39.97.50.6
服务器秘钥: c77HeYQce1GVUCnx2YSyrYxJ1f5GYcyrvUufE8r0toU=
```

### 访问控制
```
固定密码: 28b5hD8S26
访问模式: 完全控制
授权模式: 密码验证后自动授权
```

### 功能权限
```
✅ 键盘控制
✅ 鼠标控制
✅ 剪贴板同步
✅ 文件传输
✅ 音频传输
```

### 性能优化
```
✅ 硬件编码
✅ 图像质量：balanced
❌ 禁用自动更新
```

### Windows 特性
```
✅ 无 UI 模式（--cm-no-ui）
✅ 不弹出 Connection Manager 窗口
✅ 完全静默运行
```

---

## 🔄 修改的文件

### 核心文件
- `src/default_config.rs` - **新增** 预设配置模块
- `src/lib.rs` - 添加 default_config 模块声明
- `src/core_main.rs` - 初始化配置调用
- `Cargo.toml` - 添加 default_config feature
- `src/server/connection.rs` - Windows 无 UI 支持

### GitHub Actions
- `.github/workflows/custom-build.yml` - **新增** 自定义编译工作流

### 文档
- 多个说明文档（见文档导航）

---

## 🎯 下一步操作

### 方案A：使用 GitHub Actions（推荐）

**适合：** 不想配置本地环境的用户

1. ✅ **确认代码已修改完成**
2. ⬜ **推送到 GitHub**（见上方快速开始）
3. ⬜ **触发 Actions 编译**
4. ⬜ **下载编译产物**
5. ⬜ **部署测试**

**详细步骤：** `使用GitHub_Actions编译步骤.md`

---

### 方案B：本地编译

**适合：** 有 Rust 环境或需要调试的开发者

1. ✅ **确认代码已修改完成**
2. ⬜ **安装编译依赖**
3. ⬜ **执行编译命令**
4. ⬜ **测试运行**

**详细步骤：** `编译和部署说明.md`

---

## ✅ 验证清单

编译完成后，验证以下功能：

### 启动验证
- [ ] 程序能正常启动
- [ ] 日志显示：✅ 已配置自建服务器: 39.97.50.6
- [ ] 日志显示：✅ 已设置固定密码
- [ ] 日志显示：✅ 无人值守模式配置完成

### 连接验证
- [ ] 能从服务器获取 ID
- [ ] 主控端可以连接被控端
- [ ] 输入密码 28b5hD8S26 成功连接
- [ ] **无弹窗、无确认提示**

### 功能验证
- [ ] 键盘和鼠标控制正常
- [ ] 剪贴板同步工作
- [ ] 文件传输功能可用
- [ ] 音频传输正常（如需要）

---

## 🔒 安全建议

### ⚠️ 当前配置安全级别

**适用场景：**
- ✅ 企业内网环境
- ✅ VPN 保护的网络
- ✅ 可信任的管理员

**不适用：**
- ❌ 直接暴露公网
- ❌ 不受控的环境

### 提升安全性

可选的额外配置（在 `预设配置清单.md` 中查看详情）：

1. **会话录制** - 审计所有连接
2. **连接时长限制** - 防止长期占用
3. **IP 白名单** - 限制访问来源
4. **强制中继** - 统一流量管理

---

## 📊 GitHub Actions 使用情况

### 免费额度
| 账户类型 | 每月时长 | 本项目可编译次数 |
|---------|---------|----------------|
| 个人免费 | 2000分钟 | ~66 次 Windows |
| GitHub Pro | 3000分钟 | ~100 次 Windows |

### 编译时间
| 平台 | 首次 | 增量 |
|------|------|------|
| Windows | 25-30分钟 | 5-10分钟 |
| Linux | 15-20分钟 | 5-8分钟 |

---

## 🛠️ 故障排除

### GitHub Actions 编译失败

1. 查看 Actions 日志找到错误
2. 检查代码语法
3. 确认依赖正确
4. 参考 `GitHub_Actions使用指南.md`

### 本地编译失败

1. 检查 Rust 版本（需要 1.75+）
2. 确认依赖已安装
3. 清理缓存：`cargo clean`
4. 参考 `编译和部署说明.md`

### 运行时问题

1. 检查服务器 39.97.50.6 是否可访问
2. 确认防火墙允许连接
3. 查看程序日志文件
4. 验证配置是否生效

---

## 📞 技术支持

### 文档资源
- RustDesk 官方文档：https://rustdesk.com/docs/
- GitHub Actions 文档：https://docs.github.com/actions
- Rust 编程指南：https://doc.rust-lang.org/

### 常见问题
查看各文档中的"常见问题"章节

---

## 📋 项目结构

```
rustdesk/
├── src/
│   ├── default_config.rs          # 新增：预设配置
│   ├── lib.rs                     # 修改：添加模块
│   ├── core_main.rs               # 修改：初始化调用
│   └── server/connection.rs       # 修改：Windows 无 UI
├── .github/
│   └── workflows/
│       └── custom-build.yml       # 新增：自定义工作流
├── Cargo.toml                     # 修改：添加 feature
├── 配置说明.md                    # 新增：配置方案
├── 预设配置清单.md                # 新增：配置详解
├── 编译和部署说明.md              # 新增：本地编译
├── GitHub_Actions使用指南.md      # 新增：Actions 指南
├── 使用GitHub_Actions编译步骤.md  # 新增：详细步骤
├── 编译方式对比.md                # 新增：方案对比
└── 定制版本_README.md             # 本文件
```

---

## 🎓 学习路径

### 新手用户
1. 阅读 `编译方式对比.md`
2. 跟随 `使用GitHub_Actions编译步骤.md`
3. 下载并测试

### 进阶用户
1. 了解 `预设配置清单.md`
2. 自定义 `src/default_config.rs`
3. 本地编译测试

### 开发者
1. 研究 `src/default_config.rs` 实现
2. 修改 `.github/workflows/custom-build.yml`
3. 添加自定义功能

---

## 🌟 特性亮点

1. **真正的无人值守** - 密码验证后自动连接，无需确认
2. **完全无弹窗** - Windows 平台不显示任何管理窗口
3. **即插即用** - 编译后直接运行，自动配置
4. **云端编译** - GitHub Actions 自动化编译，无需本地环境
5. **企业级** - 固定服务器和密码，便于统一管理

---

## ✨ 开始使用

**推荐路径：**

```
1. 阅读本文件（当前） 
     ↓
2. 选择编译方式（GitHub Actions 或本地）
     ↓
3. 查看对应的详细步骤文档
     ↓
4. 执行编译
     ↓
5. 测试验证
     ↓
6. 部署使用
```

**立即开始：**
- GitHub Actions：查看 `使用GitHub_Actions编译步骤.md`
- 本地编译：查看 `编译和部署说明.md`

---

## 🎉 完成！

所有配置已就绪，文档已完善。
选择你喜欢的方式开始编译吧！

**祝编译成功！** 🚀
