# RustDesk 隐身修改指南

## 1. 进程名称伪装

### 修改 Cargo.toml
```toml
[package]
name = "windows-service-helper"  # 改为看似系统工具的名称
```

### 修改 src/common.rs
```rust
// 在 hbb_common::config::APP_NAME 初始化时设置为伪装名称
// 或者修改 get_app_name() 函数
```

## 2. 窗口隐藏和伪装

### 修改 src/privacy_mode/win_topmost_window.rs
```rust
// 修改隐私窗口名称
pub(super) const PRIVACY_WINDOW_NAME: &'static str = "SystemWindow";

// 修改注入进程名称
pub const WIN_TOPMOST_INJECTED_PROCESS_EXE: &'static str = "dwm.exe";
```

## 3. 会话检测绕过

### 修改 src/platform/windows.cc
```cpp
DWORD get_current_session(BOOL include_rdp) {
    // 始终返回控制台会话，避免RDP检测
    return WTSGetActiveConsoleSessionId();
}

BOOL inputDesktopSelected() {
    // 始终返回TRUE，假装在正确的桌面
    return TRUE;
}
```

## 4. 启用默认隐私模式

### 修改 src/privacy_mode.rs
```rust
lazy_static::lazy_static! {
    pub static ref DEFAULT_PRIVACY_MODE_IMPL: String = {
        #[cfg(windows)]
        {
            // 默认启用 exclude_from_capture 模式
            PRIVACY_MODE_IMPL_WIN_EXCLUDE_FROM_CAPTURE.to_owned()
        }
        #[cfg(not(windows))]
        {
            "".to_owned()
        }
    };
}
```

## 5. 网络流量伪装

### 修改连接参数
- 使用非标准端口
- 修改协议标识符
- 启用加密传输

## 6. 运行时反检测

### 进程注入技术
利用现有的 DLL 注入机制，将 RustDesk 注入到合法系统进程中运行。

### 内存中运行
避免在磁盘上留下可检测的文件痕迹。

## 7. 编译选项

```bash
# 使用发布模式编译以减少可检测特征
cargo build --release --target x86_64-pc-windows-msvc

# 可选：使用 UPX 压缩以改变文件特征
upx --best target/release/windows-service-helper.exe
```

## 重要提醒

⚠️ **法律和道德警告**：
1. 这些修改仅用于技术研究和学习目的
2. 在考试环境中使用可能违反考试规则和法律法规
3. 建议仅在授权的测试环境中使用
4. 请遵守当地法律法规和考试规则

## 检测规避策略

1. **时间延迟启动**：避免在考试开始时立即启动
2. **进程迁移**：启动后迁移到其他进程空间
3. **API Hook**：Hook 系统检测API并返回正常值
4. **虚拟化绕过**：在虚拟机中运行考试软件
