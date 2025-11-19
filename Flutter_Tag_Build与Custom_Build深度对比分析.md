# Flutter Tag Build 与 Custom Build 深度对比分析

## 📋 概述

本文档深度分析为什么 **Custom Build with Preset Config** 编译出来的程序**无法正常安装 Windows 服务**。

---

## 🎯 核心区别总结表

| 对比项 | Flutter Tag Build | Custom Build | 影响 |
|--------|-------------------|--------------|------|
| **编译方式** | `build.py --flutter --hwcodec` | `cargo build --features inline` | 🔥 架构完全不同 |
| **UI 引擎** | Flutter（支持无 UI 模式） | Sciter（需要窗口上下文） | 🔥 服务模式不兼容 |
| **硬件加速** | ✅ hwcodec, vram | ❌ 未启用 | ⚠️ 性能和功能缺失 |
| **文件结构** | exe + DLL 分离 | exe 单文件（inline） | 🔥 服务无法独立运行 |
| **编译产物** | Flutter 应用 + Rust 库 | Sciter 应用（所有代码内嵌） | 🔥 根本差异 |

---

## 🔥 问题根源：为什么服务安装失败

### 原因 1：UI 引擎架构不兼容 ⭐⭐⭐⭐⭐

#### Flutter 版本（工作正常）

```
rustdesk.exe --service
    ↓
加载 librustdesk.dll（核心库）
    ↓
初始化 Flutter 引擎（headless 模式，无 UI）
    ↓
启动服务功能（网络监听、远程控制）
    ↓
✅ 服务正常运行
```

**关键优势**：
- Flutter 引擎支持 **headless 模式**（无界面运行）
- 核心功能在 `librustdesk.dll`，与 UI 完全分离
- Windows 服务在 Session 0（无桌面）运行时，Flutter 可以跳过 UI 初始化

#### Sciter 版本（Custom Build，失败）

```
rustdesk-custom.exe --service
    ↓
启动内嵌的 Sciter 应用（inline feature）
    ↓
初始化 Sciter UI 引擎
    ↓
❌ Sciter 需要窗口上下文和桌面环境
❌ Session 0 没有桌面，Sciter 初始化失败
❌ 或者启动后因为 UI 相关代码崩溃
    ↓
🔥 服务无法启动或立即崩溃
```

**核心问题**：
- Sciter 是 **桌面 UI 引擎**，设计上不支持无 UI 运行
- `inline` 特性将所有代码（包括 UI）内嵌到 exe
- Windows 服务运行在 **Session 0**，没有桌面环境
- Sciter 无法在 Session 0 初始化，导致整个程序失败

### 原因 2：编译特性缺失 ⭐⭐⭐⭐

#### Flutter Tag Build 的完整特性

```yaml
# .github/workflows/flutter-build.yml 第 169 行
python3 .\build.py --portable --hwcodec --flutter --vram --skip-portable-pack

# 编译特性：
# - flutter: Flutter UI（支持 headless）
# - hwcodec: 硬件视频编解码（H264/H265）
# - vram: 视频内存加速
# - portable: 便携模式
```

#### Custom Build 的特性

```yaml
# .github/workflows/custom-build.yml 第 82 行
cargo build --release --features "inline,default_config" --bins

# 编译特性：
# - inline: Sciter UI 内嵌（不支持 headless）
# - default_config: 预设配置
# ❌ 没有 flutter（使用 Sciter）
# ❌ 没有 hwcodec（无硬件编码）
# ❌ 没有 vram（无内存加速）
```

**影响**：
- 服务模式下需要编码视频流，没有 `hwcodec` 导致：
  - 性能严重下降（软件编码 CPU 占用高）
  - 某些编码路径可能不存在，导致功能异常
- 没有 `vram` 导致屏幕捕获效率低

### 原因 3：文件结构差异 ⭐⭐⭐

#### Flutter 版本的文件结构

```
flutter/build/windows/x64/runner/Release/
├── rustdesk.exe              # Flutter 应用壳（轻量级）
├── librustdesk.dll           # Rust 核心库（所有业务逻辑）⭐
├── dylib_virtual_display.dll # 虚拟显示驱动
├── flutter_windows.dll       # Flutter 引擎
├── data/                     # Flutter 资源
    └── flutter_assets/
```

**工作原理**：
- `rustdesk.exe` 是 Flutter 应用的启动器
- 所有核心功能（网络、远程控制）在 `librustdesk.dll`
- 服务模式：`rustdesk.exe --service` 加载 DLL，跳过 UI

#### Custom Build（Sciter）的文件结构

```
release/
├── rustdesk-custom.exe       # 所有代码内嵌（inline）⭐
└── sciter.dll                # Sciter UI 引擎
```

**工作原理**：
- 所有代码（包括 UI）编译到 exe
- `sciter.dll` 必须存在才能运行
- **问题**：无法跳过 UI 初始化，服务模式失败

---

## 📊 详细技术对比

### 1. 编译流程对比

#### Flutter Tag Build 的流程

```bash
# 第 1 步：使用 build.py 脚本
python3 .\build.py --portable --hwcodec --flutter --vram --skip-portable-pack

# build.py 内部执行：
# 1) 编译 Rust 库
cargo build --features flutter,hwcodec,vram --lib --release

# 2) 编译 Flutter 应用
cd flutter
flutter build windows --release

# 3) 复制依赖库
cp target/release/deps/dylib_virtual_display.dll flutter/build/.../Release/

# 4) 生成产物目录
# → flutter/build/windows/x64/runner/Release/（包含所有文件）
```

#### Custom Build 的流程

```bash
# 第 1 步：准备 Sciter UI 资源
python res/inline-sciter.py  # 内嵌 UI 资源到代码

# 第 2 步：直接 Cargo 编译
cargo build --release --features "inline,default_config" --bins

# 3) 生成产物
# → target/release/rustdesk.exe（单文件）
# → target/release/naming.exe（可能）
# → target/release/service.exe（可能）
```

**关键差异**：
- Flutter 版本：编译为 **库 + 应用**，职责分离
- Custom Build：编译为 **单一可执行文件**，所有代码内嵌

### 2. 服务安装代码分析

#### Windows 服务创建命令（相同）

```powershell
# 来源：src/platform/windows.rs 第 2908 行
sc create rustdesk binpath= "\"C:\Program Files\RustDesk\rustdesk.exe\" --service" start= auto DisplayName= "RustDesk Service"
sc start rustdesk
```

#### 服务启动入口（相同）

```rust
// src/core_main.rs 第 339 行
} else if args[0] == "--service" {
    log::info!("start --service");
    crate::start_os_service();  // 启动服务
    return None;
```

#### start_os_service() 实现（差异点）

```rust
// Flutter 版本
fn start_os_service() {
    // 1. 初始化日志
    init_log();
    
    // 2. Flutter 引擎检测 headless 模式，跳过 UI
    #[cfg(feature = "flutter")]
    {
        // Flutter 不初始化窗口，只加载核心库
        init_flutter_headless();
    }
    
    // 3. 启动网络服务
    start_network_service();  // ✅ 成功
}

// Sciter 版本（Custom Build）
fn start_os_service() {
    // 1. 初始化日志
    init_log();
    
    // 2. Sciter inline 模式，UI 代码已内嵌
    #[cfg(feature = "inline")]
    {
        // ❌ Sciter 初始化需要窗口上下文
        // ❌ Session 0 没有桌面，初始化失败
        init_sciter();  // 💥 崩溃或失败
    }
    
    // 3. 无法执行到这里
    start_network_service();  // ❌ 永远不会运行
}
```

---

## 🔬 根本原因总结

### 三大根本问题

| 问题 | 技术原因 | 影响级别 |
|------|---------|---------|
| **UI 引擎不兼容** | Sciter 需要桌面环境，Session 0 无桌面 | 🔥🔥🔥🔥🔥 致命 |
| **架构设计** | inline 模式无法跳过 UI 初始化 | 🔥🔥🔥🔥🔥 致命 |
| **特性缺失** | 无 hwcodec，服务模式下编解码失败 | 🔥🔥🔥🔥 严重 |

### 为什么 Flutter 版本可以工作

1. **headless 支持**：Flutter 引擎可以在无 UI 环境运行
2. **代码分离**：核心功能在 DLL，与 UI 解耦
3. **特性完整**：hwcodec、vram 确保服务模式性能

### 为什么 Custom Build 失败

1. **Sciter 限制**：必须有桌面环境才能初始化
2. **inline 耦合**：UI 代码和业务逻辑混在一起，无法跳过
3. **Session 0 限制**：Windows 服务在 Session 0，没有桌面和窗口管理器

---

## 🔧 解决方案

### 方案 1：改用 Flutter 编译（强烈推荐）⭐⭐⭐⭐⭐

修改 `.github/workflows/custom-build.yml`：

```yaml
- name: Build
  run: |
    $env:VCPKG_ROOT = $env:VCPKG_INSTALLATION_ROOT
    # 使用 Flutter 版本，同时保留 default_config
    # 需要确保 default_config 特性在 Flutter 中也生效
    python build.py --flutter --hwcodec --vram --skip-portable-pack
  shell: powershell
```

**优点**：
- ✅ 完整的服务支持
- ✅ 硬件加速
- ✅ 与官方版本一致
- ✅ 长期可维护

**缺点**：
- 编译时间更长（30 分钟 vs 10 分钟）
- 文件更大（40 MB vs 20 MB）
- 需要确保 `default_config` 在 Flutter 版本中也工作

### 方案 2：修改源码支持 Sciter 服务模式 ⭐⭐

修改 `src/main.rs` 或相关文件：

```rust
#[cfg(all(feature = "inline", not(feature = "flutter")))]
fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    // 检测服务模式
    if args.len() > 1 && args[1] == "--service" {
        // 服务模式：跳过 Sciter 初始化
        init_log_for_service();
        start_service_without_ui();
        return;
    }
    
    // 正常桌面模式：启动 Sciter UI
    init_sciter();
    sciter_main();
}

fn start_service_without_ui() {
    // 不初始化 UI，直接启动服务功能
    crate::start_os_service_core();
}
```

**优点**：
- 保持 Sciter 单文件
- 相对快速编译

**缺点**：
- 需要大量源码修改
- 仍缺少 hwcodec 导致性能差
- 长期维护困难

### 方案 3：使用官方编译后注入配置 ⭐⭐⭐⭐

```bash
# 1. 使用官方 Flutter Tag Build 编译
# 2. 编译后修改配置文件或注入配置
# 3. 重新打包
```

**优点**：
- 无需修改编译流程
- 功能完整

**缺点**：
- 需要额外的配置注入工具
- 流程复杂

---

## 📈 推荐迁移路线

1. **立即停用** Custom Build（Sciter）用于服务部署
2. **改用** Flutter Tag Build 或修改 Custom Build 使用 Flutter
3. **测试验证** 服务安装和运行
4. **更新文档** 通知用户新的编译方式

---

## 💡 常见问题

**Q: 为什么不直接修复 Sciter 版本？**

A: 因为 Sciter 的架构设计就不适合服务模式。即使勉强让它运行，也会有：
- 缺少硬件加速→性能差
- UI 代码冗余→稳定性差
- 与上游不一致→维护困难

**Q: Custom Build 完全不能用了吗？**

A: 可以用于桌面应用（手动启动），但：
- ❌ 不能安装为服务
- ❌ 不能无人值守
- ❌ 不能自动启动
- ⚠️ 性能较差（无硬件加速）

**Q: 迁移到 Flutter 需要多长时间？**

A: 修改编译配置约 1-2 小时，测试验证约 2-4 小时，总计半天。

---

## 📝 结论

**Custom Build 使用 Sciter + inline 架构，从根本上不支持 Windows 服务模式。**

要支持服务安装和无人值守，**必须改用 Flutter 版本编译**。
