## 必应聊天机器人

> 本项目作为[`wechat-gptbot`](https://github.com/iuiaoin/wechat-gptbot)插件，可以使用必应作为聊天机器人。

### 安装

> ⚠️ 需要先部署[`bingo`](https://github.com/weaigc/bingo)

添加以下配置到插件源配置文件`plugins/source.json`:
```yaml
  "bingo": {
    "repo": "https://github.com/al-one/wechat-bingo.git",
    "desc": "必应聊天机器人"
  }
```

### 配置

添加以下配置到配置文件`config.json`:
```yaml
  "plugins": [
    {
      "name": "bingo",
      "command": ["必应", "Bing"],
      "api_base": "http://bingo.your.server:7860/api/v1",
      "start_with_command": true, # 消息需要以命令开头才会触发，bool或dict
      "without_at": {             # 无需@机器人也会触发，bool或dict
        "wx_userid": true,        # 私聊
        "xxxx@chatroom": true,    # 群聊
        "*": false
      }
    }
  ]
```

### 鸣谢

- https://github.com/weaigc/bingo
