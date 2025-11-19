# Custom Build 无法安装服务问题分析

## 🔍 问题描述

使用 `Custom Build with Preset Config` 工作流编译的 RustDesk 程序**无法安装成 Windows 服务**。

---

## 🎯 根本原因

### 问题 1: 编译参数缺少 `--bins`

**当前编译命令**（custom-build.yml#81）:
```powershell
cargo build --release --features "inline,default_config"
```

**正确的编译命令**（参考 flutter-build.yml#366, #1813）:
```powershell
cargo build --release --features "inline,default_config" --bins
```

### 区别说明

| 参数 | 编译内容 | 问题 |
|------|---------|------|
| **不带 `--bins`** | 只编译默认二进制 `rustdesk.exe` | ⚠️ 可能缺少必要组件 |
| **带 `--bins`** | 编译所有二进制文件（rustdesk, naming, service） | ✅ 完整编译 |

---

## 📋 技术细节

### 1. Cargo.toml 定义的二进制文件

```@d:\wwwroot\rustdesk\Cargo.toml#1:21
[package]
name = "rustdesk"
version = "1.4.4"
authors = ["rustdesk <info@rustdesk.com>"]
edition = "2021"
build= "build.rs"
description = "RustDesk Remote Desktop"
default-run = "rustdesk"
rust-version = "1.75"

[lib]
name = "librustdesk"
crate-type = ["cdylib", "staticlib", "rlib"]

[[bin]]
name = "naming"
path = "src/naming.rs"

[[bin]]
name = "service"
path = "src/service.rs"
```

### 2. Windows 服务安装机制

当用户点击"安装服务"时，执行以下命令：

```@d:\wwwroot\rustdesk\src\platform\windows.rs#2907:2912
format!("
sc create {app_name} binpath= \"\\\"{exe}\\\" --service\" start= auto DisplayName= \"{app_name} Service\"
sc start {app_name}
",
    app_name = crate::get_app_name())
```

这会创建一个 Windows 服务，启动时带 `--service` 参数运行 `rustdesk.exe`。

### 3. --service 参数处理

程序支持 `--service` 参数启动服务模式：

```@d:\wwwroot\rustdesk\src\core_main.rs#339:342
} else if args[0] == "--service" {
    log::info!("start --service");
    crate::start_os_service();
    return None;
```

### 4. 为什么会失败

虽然主程序确实支持 `--service` 参数，但可能存在以下问题：

#### 问题 A: 缺少完整的二进制组件
不使用 `--bins` 可能导致：
- `naming` 二进制未编译
- `service` 二进制未编译
- 某些静态链接的组件未正确打包

#### 问题 B: 功能特性不完整
当前只启用了 `inline,default_config`，而标准构建还包括：
- `hwcodec`: 硬件编解码（服务模式可能需要）
- `vram`: 视频内存加速

#### 问题 C: 缺少运行时依赖
Custom Build 只下载了：
- `sciter.dll` - UI 引擎
- `usbmmidd_v2` - USB 驱动（可选）

但可能缺少服务运行所需的其他依赖。

---

## 🔧 解决方案

### 方案 1: 修改编译命令（推荐）

编辑 `.github/workflows/custom-build.yml`，修改编译步骤：

```yaml
- name: Build
  env:
    VCPKG_ROOT: C:\vcpkg
  run: |
    $env:VCPKG_ROOT = $env:VCPKG_INSTALLATION_ROOT
    # 添加 --bins 参数编译所有二进制文件
    cargo build --release --features "inline,default_config" --bins
  shell: powershell
```

### 方案 2: 添加服务支持特性

如果需要更完整的服务支持，建议添加硬件编码：

```yaml
- name: Build
  env:
    VCPKG_ROOT: C:\vcpkg
  run: |
    $env:VCPKG_ROOT = $env:VCPKG_INSTALLATION_ROOT
    cargo build --release --features "inline,default_config,hwcodec" --bins
  shell: powershell
```

**注意**: 启用 `hwcodec` 会显著增加编译时间（需要编译 FFmpeg）。

### 方案 3: 分别编译服务二进制

```yaml
- name: Build Main
  run: |
    cargo build --release --features "inline,default_config"

- name: Build Service Binary
  run: |
    cargo build --release --bin service --features "default_config"
```

### 方案 4: 完整打包（最保险）

参考官方 flutter-build.yml 的做法：

```yaml
- name: Build
  run: |
    $env:VCPKG_ROOT = $env:VCPKG_INSTALLATION_ROOT
    python res/inline-sciter.py
    cargo build --release --features "inline,default_config,hwcodec,vram" --bins
    
- name: Package
  run: |
    New-Item -ItemType Directory -Force -Path release
    
    # 复制所有二进制文件
    Copy-Item "target\release\rustdesk.exe" -Destination "release\rustdesk-custom.exe"
    Copy-Item "target\release\naming.exe" -Destination "release\naming.exe" -ErrorAction SilentlyContinue
    Copy-Item "target\release\service.exe" -Destination "release\service.exe" -ErrorAction SilentlyContinue
    
    # 复制 DLL
    Copy-Item "sciter.dll" -Destination "release\sciter.dll"
```

---

## 🧪 验证方法

修改工作流后，验证服务是否正常：

### 1. 编译完成后检查文件

```powershell
# 检查是否生成了所有二进制文件
ls target\release\*.exe

# 应该看到：
# rustdesk.exe
# naming.exe (可能)
# service.exe (可能)
```

### 2. 安装并测试服务

```powershell
# 1. 运行程序
.\rustdesk-custom.exe

# 2. 在界面中点击 "安装服务"
# 或使用命令行
.\rustdesk-custom.exe --install-service

# 3. 检查服务状态
sc query rustdesk

# 4. 查看服务是否运行
Get-Service rustdesk

# 5. 手动测试服务启动
sc start rustdesk

# 6. 查看事件日志
Get-EventLog -LogName Application -Source rustdesk -Newest 10
```

### 3. 测试服务模式

```powershell
# 直接测试 --service 参数
.\rustdesk-custom.exe --service

# 应该看到日志输出，程序进入服务模式
```

---

## 📊 其他可能的原因

### 原因 1: 权限不足

服务安装需要**管理员权限**。如果用户没有以管理员身份运行，会失败。

**解决方法**:
- 右键程序 → "以管理员身份运行"
- 或在代码中自动请求提升权限（已实现）

### 原因 2: 防火墙/安全软件阻止

某些安全软件可能阻止程序创建 Windows 服务。

**解决方法**:
- 将程序添加到白名单
- 临时禁用安全软件测试

### 原因 3: 服务已存在

如果之前安装过 RustDesk 服务，可能冲突。

**解决方法**:
```powershell
# 卸载旧服务
sc stop rustdesk
sc delete rustdesk

# 重新安装
.\rustdesk-custom.exe --install-service
```

### 原因 4: default_config 特性冲突

`default_config` 特性可能在服务启动时引入意外行为。

**调试方法**:
编辑 `src/default_config.rs`，在函数开头添加日志：

```rust
pub fn init_default_settings() {
    log::info!("🚀 开始初始化 default_config...");
    set_unattended_defaults();
    log::info!("✅ default_config 初始化完成");
}
```

然后查看日志文件 `rustdesk.log` 确认配置是否正确加载。

---

## 🔍 调试步骤

如果修改后仍然失败，按以下步骤调试：

### 1. 启用详细日志

```powershell
# 设置环境变量启用调试日志
$env:RUST_LOG = "debug"
.\rustdesk-custom.exe --install-service
```

### 2. 查看日志文件

```powershell
# Windows 日志位置
Get-Content "$env:TEMP\rustdesk\rustdesk.log" -Tail 50
Get-Content "$env:APPDATA\RustDesk\rustdesk.log" -Tail 50

# 或使用系统事件查看器
eventvwr.msc
# → Windows 日志 → 应用程序
# 筛选来源: rustdesk
```

### 3. 手动测试服务命令

```powershell
# 测试服务创建命令
$exe = "C:\Program Files\RustDesk\rustdesk.exe"
sc create rustdesk binpath= "`"$exe`" --service" start= auto DisplayName= "RustDesk Service"
sc start rustdesk
```

### 4. 检查进程

```powershell
# 查看 rustdesk 相关进程
Get-Process rustdesk* | Format-Table Name, Id, CommandLine -AutoSize

# 应该看到：
# rustdesk.exe --service  (服务进程)
# rustdesk.exe --tray     (托盘进程)
# rustdesk.exe            (主界面)
```

---

## 📚 参考对比

### Custom Build vs Flutter Build 编译对比

| 项目 | Custom Build | Flutter Build | 差异 |
|------|-------------|---------------|------|
| **编译命令** | `cargo build --release --features "inline,default_config"` | `cargo build --release --features "inline,hwcodec,vram" --bins` | ❌ 缺少 `--bins` |
| **Features** | inline, default_config | inline, hwcodec, vram | ❌ 缺少硬件加速 |
| **UI 资源** | ✅ 内嵌 | ✅ 内嵌 | ✅ 相同 |
| **vcpkg 依赖** | ✅ 完整 | ✅ 完整 | ✅ 相同 |
| **产物** | rustdesk.exe | rustdesk.exe + 其他 bins | ❌ 可能不完整 |

---

## ✅ 推荐配置

### 完整的 custom-build.yml 修复版

```yaml
- name: Build
  env:
    VCPKG_ROOT: C:\vcpkg
  run: |
    $env:VCPKG_ROOT = $env:VCPKG_INSTALLATION_ROOT
    
    # 编译完整的二进制文件
    # inline: UI 资源内嵌
    # default_config: 预设配置
    # hwcodec: 硬件编码（推荐，但编译时间长）
    cargo build --release --features "inline,default_config" --bins
    
    # 检查生成的文件
    Write-Host "Generated binaries:"
    Get-ChildItem target\release\*.exe | Select-Object Name, Length
  shell: powershell

- name: Package
  run: |
    New-Item -ItemType Directory -Force -Path release
    
    # 复制主程序（必需）
    Copy-Item "target\release\rustdesk.exe" -Destination "release\rustdesk-custom.exe"
    
    # 复制其他二进制文件（如果存在）
    if (Test-Path "target\release\naming.exe") {
        Copy-Item "target\release\naming.exe" -Destination "release\naming.exe"
    }
    if (Test-Path "target\release\service.exe") {
        Copy-Item "target\release\service.exe" -Destination "release\service.exe"
    }
    
    # 复制 Sciter UI 引擎（必需）
    Copy-Item "sciter.dll" -Destination "release\sciter.dll"
    
    # 其余打包步骤保持不变...
```

---

## 💡 总结

**问题根源**: Custom Build 工作流的编译命令缺少 `--bins` 参数，可能导致二进制文件不完整。

**立即修复**: 在编译命令后添加 `--bins`
```powershell
cargo build --release --features "inline,default_config" --bins
```

**最佳实践**: 参考官方 flutter-build.yml 的完整编译流程，确保所有组件正确编译和打包。

**验证方法**: 修改后运行工作流，下载产物，测试服务安装功能。

---

**文档创建时间**: 2024
**适用版本**: RustDesk 1.4.4+
**工作流**: Custom Build with Preset Config
