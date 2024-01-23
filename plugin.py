import re
import openai
from plugins import register, Plugin, Event, logger, Reply, ReplyType

@register
class App(Plugin):
    name = 'bingo'

    def __init__(self, config: dict):
        super().__init__(config)

    def help(self, **kwargs):
        return '必应聊天机器人'

    @property
    def commands(self):
        cmds = self.config.get('command', '必应')
        if not isinstance(cmds, list):
            cmds = [cmds]
        return cmds

    def config_for(self, event: Event, key, default=None):
        val = self.config.get(key, {})
        if isinstance(val, dict):
            msg = event.message
            dfl = val.get('*', default)
            val = val.get(msg.room_id or msg.sender_id, dfl)
        return val

    def did_receive_message(self, event: Event):
        if self.config_for(event, 'without_at'):
            self.reply(event)

    def will_generate_reply(self, event: Event):
        if not self.config_for(event, 'without_at'):
            self.reply(event)

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def reply(self, event: Event):
        query = event.message.content
        start_with_command = self.config_for(event, 'start_with_command')
        for cmd in self.commands:
            if start_with_command and not query.startswith(cmd):
                continue
            if cmd not in query:
                continue
            if not (reply := self.generate_reply(event)):
                continue
            event.reply = reply
            event.bypass()
            return

    def generate_reply(self, event: Event) -> Reply:
        msg = event.message
        try:
            res = openai.ChatCompletion.create(
                messages=[{
                    'role': 'user',
                    'content': msg.content,
                }],
                api_base=self.config.get('api_base'),
                api_type=self.config.get('api_type', 'open_ai'),
                model=self.config_for(event, 'model', 'gpt-4'),
            )
            txt = res.choices[0]['message']['content']
            logger.info('Bing reply: %s', txt or res)
        except Exception as exc:
            return Reply(ReplyType.TEXT, f'Bingo: {exc}')

        refs = re.findall(f'\[\d+].*?""\s+', txt)
        txt = re.sub(f'\[\d+].*?""\s+', '', txt)
        txt = re.sub(r'[你您]好，[这我]是必应。', '', txt)
        txt = re.sub(r'\[\^\d+\^]', '', txt)
        txt += '\n'
        maxlen = self.config_for(event, 'quotations', 5)
        for i, ref in enumerate(refs):
            if i >= maxlen:
                break
            txt += '\n' + re.sub(r'\s""\s*$', '', ref)
        reply = Reply(ReplyType.TEXT, txt)
        return reply
