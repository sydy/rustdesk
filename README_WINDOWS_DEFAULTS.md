# RustDesk Windows 版本默认设置配置

本文档说明如何修改 RustDesk Windows 版本的默认设置，包括：

## 配置要求

- **ID 服务器**：115.190.126.11
- **密钥**：GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=
- **安全权限**：完全访问
- **固定密码**：lm8p2E5936

## 方法一：使用自定义客户端配置 (推荐)

### 1. 使用生成的配置文件

已生成的配置文件 `custom.txt` 包含了所有必需的默认设置。

### 2. 部署配置

将 `custom.txt` 文件放置在以下位置之一：

- **开发环境**：项目根目录下的 `custom.txt`
- **生产环境**：RustDesk 可执行文件同目录下的 `custom.txt`
- **macOS**：应用程序包内的 `Resources/custom.txt`

### 3. 配置内容

生成的配置包含以下设置：

```json
{
  "default-settings": {
    "custom-rendezvous-server": "115.190.126.11",
    "key": "GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=",
    "access-mode": "full",
    "permanent-password": "lm8p2E5936",
    "verification-method": "use-permanent-password",
    "approve-mode": "password"
  }
}
```

## 方法二：修改源代码 (高级用户)

### 1. 修改默认配置值

如果需要在编译时硬编码这些设置，可以修改以下文件：

#### 修改 `src/common.rs`

在 `read_custom_client` 函数中添加默认配置逻辑，或者在程序初始化时设置这些值。

#### 创建编译时配置

可以在 `build.rs` 中添加编译时配置：

```rust
// 在 build.rs 中添加
fn set_default_config() {
    println!("cargo:rustc-env=DEFAULT_RENDEZVOUS_SERVER=115.190.126.11");
    println!("cargo:rustc-env=DEFAULT_KEY=GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=");
    println!("cargo:rustc-env=DEFAULT_ACCESS_MODE=full");
    println!("cargo:rustc-env=DEFAULT_PASSWORD=lm8p2E5936");
}
```

### 2. 修改初始化代码

在 `src/main.rs` 或相关初始化代码中添加：

```rust
// 设置默认配置
if Config::get_option("custom-rendezvous-server").is_empty() {
    Config::set_option("custom-rendezvous-server".to_string(), 
                      "115.190.126.11".to_string());
}
if Config::get_option("key").is_empty() {
    Config::set_option("key".to_string(), 
                      "GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=".to_string());
}
if Config::get_option("access-mode").is_empty() {
    Config::set_option("access-mode".to_string(), "full".to_string());
}
if Config::get_permanent_password().is_empty() {
    Config::set_permanent_password("lm8p2E5936");
}
```

## 验证配置

启动 RustDesk 后，可以通过以下方式验证配置是否生效：

1. **ID 服务器**：检查设置中的 "ID/中继服务器" 是否显示为 115.190.126.11
2. **访问权限**：检查 "安全" -> "权限" 是否设置为 "完全访问"
3. **固定密码**：检查是否已设置固定密码 lm8p2E5936

## 构建说明

### 使用自定义配置构建

1. 确保 `custom.txt` 在正确位置
2. 正常编译 RustDesk：
   ```bash
   cargo build --release
   ```

### Windows 特定构建

对于 Windows 版本，确保：

1. 配置文件与可执行文件在同一目录
2. 如果创建安装包，确保 `custom.txt` 包含在安装包中
3. 考虑在 MSI 安装程序中包含配置文件

## 安全注意事项

1. **配置文件保护**：`custom.txt` 包含敏感信息，应妥善保护
2. **密码安全**：固定密码应定期更换
3. **签名验证**：生产环境建议使用签名的配置文件

## 故障排除

如果配置未生效：

1. 检查 `custom.txt` 文件位置是否正确
2. 验证 JSON 格式是否正确
3. 查看 RustDesk 日志文件中的相关错误信息
4. 确认配置键名是否正确（参考源代码中的键名定义）

## 文件清单

- `custom.txt` - 自定义配置文件（Base64 编码）
- `custom_config.json` - 原始 JSON 配置
- `create_custom_config.py` - 配置生成脚本
- `README_WINDOWS_DEFAULTS.md` - 本说明文档