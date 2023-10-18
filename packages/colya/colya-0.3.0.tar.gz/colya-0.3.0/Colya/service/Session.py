class Session:
    def __init__(self, body):
        self.id = body.get('id')
        self.type = body.get('type')
        self.platform = body.get('platform')
        self.self_id = body.get('self_id')
        self.timestamp = body.get('timestamp')
        self.channel = Channel(body.get('channel', {}))
        self.guild = Guild(body.get('guild', {}))
        self.member = body.get('member', {})
        self.message = Message(body.get('message', {}))
        self.user = User(body.get('user', {}))
        self.isGroupMsg = self.guild.id != None

class User:
    def __init__(self, user_info):
        self.id = user_info.get('id')
        self.name = user_info.get('name')
        self.avatar = user_info.get('avatar')


class Channel:
    def __init__(self, channel_info):
        self.type = channel_info.get('type')
        self.id = channel_info.get('id')
        self.name = channel_info.get('name')


class Guild:
    def __init__(self, guild_info):
        self.id = guild_info.get('id')
        self.name = guild_info.get('name')
        self.avatar = guild_info.get('avatar')


class Member:
    def __init__(self, guild_info):
        self.name = guild_info.get('name')


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id')
        self.content = message_info.get('content')