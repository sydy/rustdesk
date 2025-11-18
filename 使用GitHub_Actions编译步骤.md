# 使用 GitHub Actions 编译 RustDesk - 详细步骤

## 📋 前置要求

- ✅ GitHub 账号
- ✅ Git 已安装
- ✅ 已完成代码修改（default_config.rs 等）

---

## 第一部分：准备 GitHub 仓库

### 选项1：创建新仓库（推荐）

#### 1.1 在 GitHub 上创建仓库

1. 登录 GitHub
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Repository name**: `rustdesk-custom`
   - **Description**: `RustDesk 定制版本`
   - **Private**: ✅ 建议选择私有（保护配置信息）
4. ❌ 不要勾选 "Initialize with README"
5. 点击 **Create repository**

#### 1.2 推送本地代码到 GitHub

```powershell
# 在项目目录打开 PowerShell
cd d:\wwwroot\rustdesk

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交修改
git commit -m "初始提交：添加自定义配置"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/rustdesk-custom.git

# 推送到 GitHub
git push -u origin master
```

### 选项2：Fork 原仓库后修改

如果你是 fork 的 RustDesk 官方仓库：

```powershell
cd d:\wwwroot\rustdesk

# 添加你的修改
git add src/default_config.rs
git add src/lib.rs
git add src/core_main.rs
git add Cargo.toml
git add .github/workflows/custom-build.yml

# 提交
git commit -m "添加自定义配置支持"

# 推送（如果是 fork，直接 push 到你的仓库）
git push origin master
```

---

## 第二部分：触发 GitHub Actions 编译

### 方法1：手动触发编译（最简单）

#### 步骤1：进入 Actions 页面

1. 打开你的 GitHub 仓库页面
2. 点击顶部导航栏的 **Actions** 标签

#### 步骤2：选择工作流

1. 在左侧列表找到 **Custom Build with Preset Config**
2. 点击它

#### 步骤3：运行工作流

1. 在右侧点击 **Run workflow** 按钮（绿色）
2. 会弹出一个对话框，选择：
   - **Build target**: 选择 `windows`（或 `linux`, `all`）
3. 点击绿色的 **Run workflow** 按钮确认

#### 步骤4：查看编译进度

1. 页面会刷新，显示一个新的工作流运行
2. 点击进入查看详情
3. 可以实时查看编译日志

---

### 方法2：通过推送自动触发

如果你想每次推送代码自动编译：

#### 步骤1：创建专用分支

```powershell
# 创建并切换到 custom-config 分支
git checkout -b custom-config

# 推送到 GitHub
git push origin custom-config
```

#### 步骤2：修改触发条件

编辑 `.github/workflows/custom-build.yml`，添加：

```yaml
on:
  push:
    branches:
      - custom-config
  workflow_dispatch:
    # ... 保留手动触发
```

#### 步骤3：推送代码自动编译

```powershell
# 以后每次修改代码
git add .
git commit -m "更新配置"
git push origin custom-config

# 会自动触发编译
```

---

## 第三部分：下载编译结果

### 步骤1：等待编译完成

- **Windows**: 大约 20-30 分钟
- **Linux**: 大约 15-20 分钟

编译状态：
- 🟡 黄点 = 正在编译
- ✅ 绿勾 = 编译成功
- ❌ 红叉 = 编译失败

### 步骤2：下载产物

编译成功后：

1. 在 Actions 页面，点击你的工作流运行
2. 进入详情页面
3. 向下滚动到 **Artifacts** 区域
4. 下载对应的文件：
   - `rustdesk-windows-custom.zip` - Windows 版本
   - `rustdesk-linux-custom.tar.gz` - Linux 版本

### 步骤3：解压和使用

**Windows:**
```powershell
# 解压
Expand-Archive rustdesk-windows-custom.zip -DestinationPath RustDesk

# 查看配置
type RustDesk\config.txt

# 运行
.\RustDesk\rustdesk-custom.exe
```

**Linux:**
```bash
# 解压
tar xzf rustdesk-linux-custom.tar.gz

# 查看配置
cat config.txt

# 运行
chmod +x rustdesk-custom
./rustdesk-custom
```

---

## 第四部分：验证配置

### 1. 检查服务器连接

启动程序后，查看日志应该显示：
```
✅ 已配置自建服务器: 39.97.50.6
✅ 已设置固定密码
✅ 已启用完全静默模式 (无人值守)
```

### 2. 测试连接

1. 在被控端运行编译的程序
2. 记下显示的 ID
3. 在主控端输入 ID
4. 输入密码：`28b5hD8S26`
5. 应该无需确认直接连接成功

---

## 第五部分：进阶技巧

### 技巧1：使用 GitHub Secrets 保护敏感信息

如果不想在代码中明文保存密码：

#### 步骤1：设置 Secrets

1. 在仓库页面点击 **Settings**
2. 左侧菜单找到 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加：
   - Name: `CUSTOM_PASSWORD`
   - Value: `28b5hD8S26`

#### 步骤2：修改代码

在 `src/default_config.rs` 中：

```rust
fn set_fixed_password() {
    // 从环境变量读取密码
    let password = std::env::var("CUSTOM_PASSWORD")
        .unwrap_or_else(|_| "28b5hD8S26".to_string());
    
    Config::set_password(&password);
    log::info!("✅ 已设置固定密码");
}
```

#### 步骤3：在 Actions 中使用

修改 `.github/workflows/custom-build.yml`：

```yaml
- name: Build
  env:
    CUSTOM_PASSWORD: ${{ secrets.CUSTOM_PASSWORD }}
  run: cargo build --release --features default_config
```

---

### 技巧2：自动发布到 Release

#### 步骤1：创建 Tag

```powershell
git tag v1.0.0
git push origin v1.0.0
```

#### 步骤2：修改工作流

在 `.github/workflows/custom-build.yml` 添加：

```yaml
- name: Create Release
  if: startsWith(github.ref, 'refs/tags/')
  uses: softprops/action-gh-release@v1
  with:
    files: |
      rustdesk-windows-custom.zip
      rustdesk-linux-custom.tar.gz
    body: |
      ## 定制版本发布
      
      **预设配置:**
      - 服务器: 39.97.50.6
      - 密码: 28b5hD8S26
      - 模式: 无人值守
```

---

### 技巧3：定时自动编译

每周自动编译最新版本：

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨2点 (UTC)
  workflow_dispatch:
```

---

## 常见问题

### Q1: 编译失败怎么办？

**A:** 
1. 点击失败的工作流查看日志
2. 找到红色的错误信息
3. 常见错误：
   - **语法错误**: 检查 Rust 代码是否正确
   - **依赖缺失**: 确认 Cargo.toml 正确
   - **权限问题**: 检查 GitHub Actions 权限设置

### Q2: 下载的文件在哪里？

**A:** 
- Artifacts 在工作流详情页底部
- 需要登录 GitHub 才能下载
- 保留期为 30 天

### Q3: 可以私有仓库吗？

**A:** 
可以！私有仓库也能用 GitHub Actions。
- 免费账户: 2000 分钟/月
- Pro 账户: 3000 分钟/月

### Q4: 如何加快编译速度？

**A:**
1. 使用缓存（已在工作流中配置）
2. 只编译需要的目标
3. 使用 GitHub Actions 的更快 runner（付费）

### Q5: 编译的文件安全吗？

**A:**
- ✅ GitHub Actions 环境是隔离的
- ✅ 私有仓库的代码和产物不会公开
- ⚠️ 注意不要在公开日志中显示密码
- ⚠️ Artifacts 只有仓库成员能下载（私有仓库）

---

## 总结

### 最简单的使用流程：

1. **推送代码** → GitHub 仓库
2. **点击 Actions** → 选择工作流
3. **Run workflow** → 选择 windows
4. **等待编译** → 20-30 分钟
5. **下载 Artifacts** → 解压使用

### 优势：

✅ 无需配置本地环境
✅ 云端自动编译
✅ 可重复构建
✅ 版本管理方便
✅ 支持多平台编译

---

需要帮助？查看 GitHub Actions 日志或参考官方文档。
