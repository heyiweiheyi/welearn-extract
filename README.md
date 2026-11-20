# welearn-extract

面向上海外语教育出版社 [WE Learn 随行课堂](https://welearn.sflep.com/) 的 Codex skill，帮助使用者提取自己可访问的课程附件、音频和视频，并按课程、单元和文件类型整理交付。

## 工作方式

Codex 读取 `SKILL.md` 后，通过可用的浏览器工具操作课程页面，核对资源标题和范围，再使用页面下载入口或可用的媒体保存方式取得文件。`scripts/package_media.py` 用于把已保存到本地的媒体打包。

提取过程需要具备浏览器操作能力的 Codex 环境。实际支持的资源类型和保存方式取决于课程页面、使用者权限以及环境提供的工具。

## 安装

将仓库内容放入 Codex 的 `skills/welearn-extract/` 目录，确保 `SKILL.md` 位于该目录的第一层。如果设置了 `CODEX_HOME`，使用其下的 `skills` 目录。

常见目录如下。

| 系统 | Skill 目录 |
| --- | --- |
| Windows | `%USERPROFILE%\.codex\skills\welearn-extract\` |
| macOS / Linux | `~/.codex/skills/welearn-extract/` |

安装后的结构应为下列形式。

```text
welearn-extract/
├── SKILL.md
├── references/
│   └── browser-extraction.md
└── scripts/
    └── package_media.py
```

在 Codex 中使用 `$welearn-extract` 调用，并提供课程页面或指定已经打开的课程标签页。

## 登录

使用者可以选择两种入口。

| 状态 | 操作 |
| --- | --- |
| 浏览器已经登录 WE Learn | 指定自己的课程标签页，Codex 检查课程和单元后继续提取。 |
| 浏览器尚未登录 | Codex 打开官方登录页，使用者在网页中亲自输入账号密码并完成验证，登录后继续。 |

使用者的账号和密码输入到 WE Learn 官方登录表单。登录会话保留在浏览器中，使用者可以选择需要使用的账号。

## 使用示例

### 提取指定单元的音视频

```text
使用 $welearn-extract。
我已经在浏览器登录 WE Learn 并打开课程。
请提取 Unit 2 的全部音频和视频，按音频、视频分类保存。
```

### 只提取指定部分

```text
使用 $welearn-extract。
提取当前课程 Unit 1 至 Unit 3 的 Part 1 和 Part 2。
把取得的音视频放在一个 ZIP 中，每个单元使用单独的目录。
```

### 使用账号密码登录后提取

```text
使用 $welearn-extract。
请打开 WE Learn 官方登录页，我会在网页中输入自己的账号密码。
登录后，提取我指定课程的音视频。
```

### 请求字幕或阅读稿

```text
使用 $welearn-extract。
提取当前单元的音视频，并查找平台已有的英文字幕。
如果需要自动转写，请说明并为每个文件生成对应的 SRT。
```

字幕转写、翻译和 PDF 排版需要运行环境提供相应能力。生成结果应说明是否采用自动转写，并核对文件配对和时间轴。

## 本地音视频打包

`package_media.py` 使用 Python 标准库，需要 Python 3.9 或更高版本。准备好仅包含目标课程资源的本地目录后，在仓库根目录运行以下命令。

```bash
python scripts/package_media.py "/path/to/media" "/path/to/welearn-media.zip"
```

Windows PowerShell 示例。

```powershell
python scripts/package_media.py "D:\Courses\Media" "D:\Courses\welearn-media.zip"
```

脚本保留媒体文件的相对目录，筛选支持的音视频扩展名，并在完成后校验 ZIP。输出路径已有 ZIP 时，脚本会在新压缩包校验通过后替换该文件。

支持的扩展名包括 `m4a`、`mp3`、`wav`、`ogg`、`opus`、`aac`、`flac`、`mp4`、`webm`、`mov`、`mkv` 和 `m4v`。

## 提取与核对

- 优先使用课程提供的下载或附件入口。
- 数字教材可能嵌入在课程页中，需要进入教材自己的目录或资源面板。
- 同一媒体可能在多道练习下重复出现，去重前应核实来源一致。
- 提取时核对标题、所属单元、媒体轨道和播放器时长。
- 对正在解析、无法播放或无法保存的资源，列出具体条目和页面提示。
- 如果用户限定了账号风险边界，应按该要求执行。出现验证码、限流、账号警告或访问拒绝时暂停相关提取。

## 账号与发布

在使用者有权访问的课程范围内操作，遵守课程平台的使用要求。遇到 DRM、下载限制或权限错误时停止相应提取路径。自动化提取的账号风险无法保证为零。

公开仓库中维护 skill 说明、流程参考和本地打包工具。个人课程链接、账号密码、Cookie、令牌、签名媒体地址、浏览器状态和提取的课程文件应保存在使用者自己的本地工作目录。

## 验证情况

已通过 skill 格式校验，并用本地样例验证音视频筛选、目录保留和 ZIP 完整性。平台页面或播放器更新可能需要调整提取流程。
