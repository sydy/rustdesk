# GitHub Actions 自动编译指南

## 快速开始

### 1. 推送代码到 GitHub

```bash
cd d:\wwwroot\rustdesk
git init
git add .
git commit -m "添加自定义配置"
git remote add origin https://github.com/你的用户名/rustdesk.git
git push -u origin master
```

### 2. 在 GitHub 上触发编译

1. 打开仓库页面
2. 点击 **Actions** 标签
3. 选择 **Custom Build with Preset Config**
4. 点击 **Run workflow**
5. 选择编译目标（windows/linux/all）
6. 点击绿色的 **Run workflow** 按钮

### 3. 等待编译完成

- Windows: 约 20-30 分钟
- Linux: 约 15-20 分钟
- 可以实时查看编译日志

### 4. 下载编译结果

编译完成后：
1. 在 Actions 页面找到你的工作流运行
2. 点击进入详情页
3. 在底部 **Artifacts** 区域下载
   - `rustdesk-windows-custom.zip` (Windows 版本)
   - `rustdesk-linux-custom.tar.gz` (Linux 版本)

## 已配置的内容

编译产物已包含以下预设：
- 服务器: 39.97.50.6
- 密码: 28b5hD8S26
- 完全控制权限
- 无人值守模式

## 优势

✅ 无需本地配置开发环境
✅ 云端自动编译
✅ 支持 Windows 和 Linux
✅ 自动打包和上传
✅ 可重复构建

## 注意事项

1. 需要有 GitHub 账号
2. 仓库可以是私有的
3. 编译日志可能包含配置信息
4. Actions 有使用时长限制（免费账户：2000分钟/月）

## 高级配置

### 自动编译特定分支

修改 `.github/workflows/custom-build.yml`：

```yaml
on:
  push:
    branches:
      - custom-config  # 推送到此分支自动编译
```

### 定时自动编译

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨2点编译
```

### 发布到 Release

添加以下步骤到 workflow：

```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: |
      rustdesk-windows-custom.zip
      rustdesk-linux-custom.tar.gz
```

## 故障排除

### 编译失败

1. 查看 Actions 日志找到具体错误
2. 检查代码是否有语法错误
3. 确认依赖是否正确

### 下载不了

1. 确认编译已完成（绿色对勾）
2. Artifacts 保留期为 30 天
3. 需要登录 GitHub 才能下载

## 相关链接

- GitHub Actions 文档: https://docs.github.com/actions
- Rust 工具链: https://rustup.rs/
