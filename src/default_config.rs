// 默认配置模块 - 用于设置编译时的默认配置
// 这些配置将在程序首次启动时自动应用

use hbb_common::{config::Config, log};

/// 初始化默认配置
/// 在程序启动时调用，设置无人值守模式所需的默认值
pub fn init_default_settings() {
    set_unattended_defaults();
}

/// 设置无人值守模式的默认配置
fn set_unattended_defaults() {
    // 自建服务器配置
    set_custom_server();
    
    // 固定密码配置
    set_fixed_password();
    
    // 完全静默模式（无人值守）
    set_full_access_mode();
    
    // 性能和安全配置
    set_recommended_defaults();
    
    log::info!("✅ 无人值守模式配置完成");
}

/// 完全静默模式 - 自动接受所有连接（⚠️ 仅在信任环境使用）
#[allow(dead_code)]
fn set_full_access_mode() {
    // 设置访问模式为完全控制
    Config::set_option("access-mode".to_string(), "full".to_string());
    
    // 禁用连接确认提醒
    Config::set_option("approve-mode".to_string(), "password".to_string());
    
    log::info!("已启用完全静默模式 (无人值守)");
}

/// 密码验证模式 - 通过密码验证后自动连接
#[allow(dead_code)]
fn set_password_auth_mode() {
    // 设置通过密码验证
    Config::set_option("approve-mode".to_string(), "password".to_string());
    
    // 启用所有权限
    Config::set_option("enable-keyboard".to_string(), "Y".to_string());
    Config::set_option("enable-clipboard".to_string(), "Y".to_string());
    Config::set_option("enable-file-transfer".to_string(), "Y".to_string());
    
    log::info!("已启用密码验证模式");
}

/// 设置其他推荐的默认配置
#[allow(dead_code)]
pub fn set_recommended_defaults() {
    // 禁用自动更新（对于企业部署）
    Config::set_option("enable-check-update".to_string(), "N".to_string());
    
    // 启用硬件编码（提升性能）
    Config::set_option("enable-hwcodec".to_string(), "Y".to_string());
    
    // 设置默认图像质量
    Config::set_option("image-quality".to_string(), "balanced".to_string());
}

/// 一键设置企业无人值守模式（推荐配置组合）
#[allow(dead_code)]
pub fn set_enterprise_unattended_mode() {
    // 访问控制
    Config::set_option("access-mode".to_string(), "full".to_string());
    Config::set_option("approve-mode".to_string(), "password".to_string());
    
    // 启用所有功能
    Config::set_option("enable-keyboard".to_string(), "Y".to_string());
    Config::set_option("enable-clipboard".to_string(), "Y".to_string());
    Config::set_option("enable-file-transfer".to_string(), "Y".to_string());
    Config::set_option("enable-audio".to_string(), "Y".to_string());
    
    // 性能优化
    Config::set_option("enable-hwcodec".to_string(), "Y".to_string());
    
    // 安全设置
    Config::set_option("enable-check-update".to_string(), "N".to_string());
    
    log::info!("已启用企业无人值守模式");
}

/// 配置自建服务器
/// 服务器IP: 39.97.50.6
/// 秘钥: c77HeYQce1GVUCnx2YSyrYxJ1f5GYcyrvUufE8r0toU=
fn set_custom_server() {
    // 设置 ID 服务器
    Config::set_option("custom-rendezvous-server".to_string(), "39.97.50.6".to_string());
    
    // 设置服务器秘钥
    Config::set_option("key".to_string(), "c77HeYQce1GVUCnx2YSyrYxJ1f5GYcyrvUufE8r0toU=".to_string());
    
    // 设置 Relay 服务器（通常与 ID 服务器相同）
    Config::set_option("relay-server".to_string(), "39.97.50.6".to_string());
    
    // 设置 API 服务器（通常与 ID 服务器相同）
    Config::set_option("api-server".to_string(), "http://39.97.50.6".to_string());
    
    log::info!("✅ 已配置自建服务器: 39.97.50.6");
}

/// 设置固定的远程管理密码
/// 密码: 28b5hD8S26
fn set_fixed_password() {
    // 设置固定密码
    Config::set_permanent_password("28b5hD8S26");
    
    // 禁用临时密码
    Config::set_option("allow-temporary-password".to_string(), "N".to_string());
    
    // 设置密码验证模式
    Config::set_option("verification-method".to_string(), "use-permanent-password".to_string());
    
    log::info!("✅ 已设置固定密码");
}

/// 禁用不必要的功能（提升安全性和性能）
#[allow(dead_code)]
pub fn disable_unnecessary_features() {
    // 禁用自动更新
    Config::set_option("enable-check-update".to_string(), "N".to_string());
    
    // 禁用直接 IP 访问（强制使用服务器中继）
    Config::set_option("direct-server".to_string(), "N".to_string());
    
    // 禁用发现局域网
    Config::set_option("enable-lan-discovery".to_string(), "N".to_string());
    
    log::info!("已禁用不必要功能");
}
