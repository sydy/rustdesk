# Custom Build 输出格式修复说明

## 问题描述

之前 **Custom Build with Preset Config** 工作流编译出来的是压缩包（zip），而 **Flutter Tag Build** 工作流编译出来的是完整的 exe 程序。

## 原因分析

### Flutter Tag Build 工作流的打包方式

Flutter Tag Build 使用了 `libs/portable/generate.py` 工具来生成**自解压可执行文件**（portable packer），这是一个完整的单文件 exe 程序，运行时会自动解压所需的所有文件。

关键步骤：
```bash
pushd ./libs/portable
pip3 install -r requirements.txt
python3 ./generate.py -f ../../rustdesk/ -o . -e ../../rustdesk/rustdesk.exe
popd
mv ./target/release/rustdesk-portable-packer.exe ./SignOutput/rustdesk-xxx.exe
```

### Custom Build 工作流的打包方式（修复前）

之前的 Custom Build 只是简单地使用 PowerShell 的 `Compress-Archive` 将所有文件压缩成 zip：
```powershell
Compress-Archive -Path release\* -DestinationPath rustdesk-windows-custom.zip -Force
```

## 解决方案

已修改 `.github/workflows/custom-build.yml`，添加了生成自解压可执行文件的步骤：

### 修改内容

1. **添加 manifest 处理步骤**
   ```powershell
   bash -c "sed -i '/dpiAware/d' res/manifest.xml"
   ```
   移除 dpiAware 配置，避免兼容性问题

2. **调用 portable packer 生成器**
   ```powershell
   bash -c "pushd ./libs/portable && pip3 install -r requirements.txt && python3 ./generate.py -f ../../release/ -o . -e ../../release/rustdesk.exe && popd"
   ```
   生成自解压可执行文件

3. **输出两种格式**
   - **rustdesk-custom.exe**：自解压可执行文件（主要输出）
   - **rustdesk-windows-custom.zip**：zip 压缩包（备份）

4. **分别上传两种格式**
   ```yaml
   - name: Upload Self-Extracted Executable
     uses: actions/upload-artifact@v4
     with:
       name: rustdesk-windows-custom-exe
       path: SignOutput/rustdesk-custom.exe
   
   - name: Upload Zip Backup
     uses: actions/upload-artifact@v4
     with:
       name: rustdesk-windows-custom-zip
       path: SignOutput/rustdesk-windows-custom.zip
   ```

## 使用说明

修复后，运行 **Custom Build with Preset Config** 工作流将生成：

1. **rustdesk-custom.exe**（推荐）
   - 单文件自解压可执行程序
   - 双击运行即可，无需解压
   - 自动解压所有必需文件到临时目录
   - 与 Flutter Tag Build 的输出格式一致

2. **rustdesk-windows-custom.zip**（备份）
   - 包含所有原始文件的压缩包
   - 如需自定义部署可使用此格式

## 优势

- ✅ **用户体验更好**：单文件 exe，无需手动解压
- ✅ **与官方版本一致**：输出格式与 Flutter Tag Build 相同
- ✅ **保持兼容性**：同时提供 zip 格式作为备份
- ✅ **便于分发**：单个 exe 文件更容易分享和部署

## 测试建议

下次运行 Custom Build 工作流时，请验证：
1. 生成的 `rustdesk-custom.exe` 可以正常运行
2. 双击 exe 后能自动解压并启动程序
3. 预设配置（服务器地址、密码）正常生效
4. Windows 服务功能正常（如果使用）

## 修改文件

- `.github/workflows/custom-build.yml`：第 101-191 行

## 修改日期

2025年11月19日
