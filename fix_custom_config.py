#!/usr/bin/env python3
"""
修复自定义配置文件的脚本
创建一个无需签名验证的配置方案
"""

import json
import base64

# 配置内容
config = {
    "default-settings": {
        "custom-rendezvous-server": "115.190.126.11",
        "key": "GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=",
        "access-mode": "full",
        "permanent-password": "lm8p2E5936",
        "verification-method": "use-permanent-password",
        "approve-mode": "password"
    }
}

def create_debug_config():
    """创建用于调试的配置文件"""
    # 转换为JSON
    json_data = json.dumps(config, separators=(',', ':'))
    print("Debug configuration JSON:")
    print(json_data)
    print()
    
    # Base64编码
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    print("Base64 encoded:")
    print(encoded_data)
    print()
    
    # 写入custom.txt文件
    with open('custom.txt', 'w') as f:
        f.write(encoded_data)
    
    # 也创建一个原始JSON文件用于调试
    with open('debug_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Files created:")
    print("- custom.txt (Base64 encoded)")
    print("- debug_config.json (human readable)")
    
    return json_data

def create_source_code_fix():
    """创建源代码修复方案"""
    
    fix_code = '''
// 在 src/main.rs 的开头添加以下代码
#[cfg(feature = "cli")]
fn main() {
    // Load custom client configuration first
    common::load_custom_client();
    
    if !common::global_init() {
        return;
    }
    // ... 其余代码保持不变
}

// 在 src/common.rs 的 global_init 函数中添加配置初始化
pub fn global_init() -> bool {
    #[cfg(target_os = "linux")]
    {
        if !crate::platform::linux::is_x11() {
            crate::server::wayland::init();
        }
    }
    
    // 强制设置Windows默认配置（无论是否有配置文件）
    #[cfg(target_os = "windows")]
    {
        use hbb_common::config::Config;
        // 强制设置默认值
        Config::set_option("custom-rendezvous-server".to_string(), "115.190.126.11".to_string());
        Config::set_option("key".to_string(), "GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=".to_string());
        Config::set_option("access-mode".to_string(), "full".to_string());
        Config::set_permanent_password("lm8p2E5936");
        Config::set_option("verification-method".to_string(), "use-permanent-password".to_string());
        Config::set_option("approve-mode".to_string(), "password".to_string());
        
        log::info!("Windows default configuration applied");
    }
    
    true
}
'''
    
    with open('source_code_fix.txt', 'w') as f:
        f.write(fix_code)
    
    print("Source code fix saved to: source_code_fix.txt")

if __name__ == "__main__":
    print("=== RustDesk 配置修复脚本 ===\n")
    
    # 创建调试配置
    json_data = create_debug_config()
    print()
    
    # 创建源代码修复方案
    create_source_code_fix()
    print()
    
    print("=== 解决方案 ===")
    print("1. 配置文件方案：将 custom.txt 放在 RustDesk 可执行文件同目录")
    print("2. 源代码修复：应用 source_code_fix.txt 中的代码修改")
    print("3. 强制配置：直接在代码中设置默认值（推荐）")
    print()
    print("推荐使用方案3，因为它不依赖外部文件且确保配置生效")