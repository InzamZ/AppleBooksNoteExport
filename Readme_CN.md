# Apple Books Note Export Tools

## 简介

Apple Books 在中国市场虽然没有办法使用，但是作为（iPad、iPhone）本地电子书阅读器还是非常好用的。本工具用来批量导出阅读笔记。仅需将笔记发送到个人邮箱，每日定期触发检查新邮件并且解析笔记。

## 使用方法

接收邮件的程序需要提供邮箱账号，邮箱口令，邮件 `IMAP` 服务器，以及 `Atlas` 的连接链接。目前只支持储存到 `Atlas` 的 `MongoDB` 中，可以自行重写 `DataBaseConnect.py` 实现不同数据库的储存。

```bash
python main.py -u <username> -p <password> -s <server> -a <atlasuri>
```

不需要储存到数据库可以使用解析后返回的数组，以 `python Dictionary` 形式储存，目前解析完成后的格式为：

- `from` : 书名
- `author` : 作者
- `content` : 选中内容
- `chapter` : 所在章节
- `date` : 添加日期
- `note` : 笔记内容
- `type` : 笔记类型(按照高亮颜色区分，目前只区分是否为下划线)

## 下一步

- [ ] 按照选中内容进行Hash并且索引，相同内容进行更新
- [ ] 在笔记中添加特殊标识字段，例如`[[speaker]]`来解析选中文本的讲话人
- [ ] `type`字段的完善
- [ ] `Readme.md` in English
- [ ] `CI`相关