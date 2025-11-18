# 生成 custom.txt 配置文件说明

## 方法1: 使用官方签名（推荐）

如果你有 RustDesk 官方提供的签名密钥，使用官方签名工具。

公钥已在代码中硬编码：
```
5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM=
```

对应的私钥需要联系 RustDesk 官方获取或自己生成密钥对。

---

## 方法2: 开发/测试时绕过签名验证（仅限调试）

### 临时方案：调试模式读取

在 **debug 模式**下，RustDesk 会直接读取 `custom.txt` 而不验证签名。

#### 步骤：

1. 创建 `custom.txt`，直接放 base64 编码的 JSON：

```bash
# Linux/macOS
echo '{"default-settings":{"access-mode":"full"}}' | base64 > custom.txt

# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('{"default-settings":{"access-mode":"full"}}')) | Out-File -Encoding ASCII custom.txt
```

2. 将 `custom.txt` 放到项目根目录

3. 使用 debug 模式运行：
```bash
cargo run --features flutter
```

⚠️ **注意**: 这只在 `debug_assertions` 开启时有效，release 版本不可用。

---

## 方法3: 修改代码移除签名验证（不推荐）

### 仅用于内部测试版本

修改 `src/common.rs` 中的 `read_custom_client` 函数：

```rust
pub fn read_custom_client(config: &str) {
    // 注释掉签名验证部分
    /*
    let Ok(data) = decode64(config) else {
        log::error!("Failed to decode custom client config");
        return;
    };
    const KEY: &str = "5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM=";
    let Some(pk) = get_rs_pk(KEY) else {
        log::error!("Failed to parse public key of custom client");
        return;
    };
    let Ok(data) = sign::verify(&data, &pk) else {
        log::error!("Failed to dec custom client config");
        return;
    };
    */
    
    // 直接解码 base64
    let Ok(data) = decode64(config) else {
        log::error!("Failed to decode custom client config");
        return;
    };
    
    let Ok(mut data) =
        serde_json::from_slice::<std::collections::HashMap<String, serde_json::Value>>(&data)
    else {
        log::error!("Failed to parse custom client config");
        return;
    };
    
    // ... 其余代码保持不变
}
```

⚠️ **警告**: 此方法会降低安全性，仅用于内部测试！

---

## 方法4: 自己生成密钥对（推荐用于企业定制）

### 步骤1: 生成 Ed25519 密钥对

使用 Rust 代码生成：

```rust
use sodiumoxide::crypto::sign;

fn main() {
    sodiumoxide::init().unwrap();
    let (pk, sk) = sign::gen_keypair();
    
    println!("Public Key (base64): {}", 
        base64::encode(&pk.0));
    println!("Secret Key (base64): {}", 
        base64::encode(&sk.0));
}
```

### 步骤2: 替换代码中的公钥

修改 `src/common.rs` 中的 KEY：

```rust
const KEY: &str = "YOUR_NEW_PUBLIC_KEY_BASE64";
```

### 步骤3: 使用私钥签名配置

创建签名工具：

```rust
use sodiumoxide::crypto::sign;
use std::fs;

fn main() {
    sodiumoxide::init().unwrap();
    
    // 读取私钥
    let sk_bytes = base64::decode("YOUR_SECRET_KEY_BASE64").unwrap();
    let sk = sign::SecretKey::from_slice(&sk_bytes).unwrap();
    
    // 读取配置
    let config = fs::read_to_string("custom_config.json").unwrap();
    let config_bytes = config.as_bytes();
    
    // 签名
    let signed = sign::sign(config_bytes, &sk);
    
    // base64 编码
    let output = base64::encode(&signed);
    
    // 保存
    fs::write("custom.txt", output).unwrap();
    println!("Generated custom.txt");
}
```

---

## 快速实现脚本（PowerShell）

创建 `generate_custom.ps1`：

```powershell
# 读取 JSON 配置
$json = Get-Content "custom_config.json" -Raw

# Base64 编码（用于 debug 模式）
$bytes = [Text.Encoding]::UTF8.GetBytes($json)
$base64 = [Convert]::ToBase64String($bytes)

# 保存到 custom.txt
$base64 | Out-File -Encoding ASCII "custom.txt"

Write-Host "Generated custom.txt (debug mode only)" -ForegroundColor Green
Write-Host "For production, use signed version with private key" -ForegroundColor Yellow
```

使用：
```powershell
.\generate_custom.ps1
```

---

## 推荐流程

### 开发测试阶段
1. 使用 debug 模式 + 未签名的 base64 配置
2. 快速迭代测试

### 生产部署阶段
**选项A**: 联系 RustDesk 官方获取官方签名
**选项B**: 生成自己的密钥对，修改代码中的公钥
**选项C**: 使用方案2（代码硬编码），不使用 custom.txt

---

## 安全考虑

1. ✅ 官方签名：最安全，但需要官方支持
2. ✅ 自定义密钥对：安全，需要妥善保管私钥
3. ⚠️ 移除验证：不安全，仅限内部使用
4. ⚠️ Debug 模式：不安全，仅限开发测试

---

## 总结

**最佳实践：**
- 开发测试：debug 模式 + 简单 base64
- 内部部署：代码硬编码（方案2）
- 商业发布：自定义密钥对 + 签名验证
