from Colya.dictionary import Dictionary
class PluginBase():
    def __init__(self,context) -> None:
        self.session = context.session
        self.session_guild_id = self.session.guild.id
        self.session_user_id = self.session.user.id
        self.session_content = self.session.message.content
        self.session_type = self.session.type
        self.plugin = context.plugin
        self.memberHistor = context.getMember(self.session.user.id)
        self.groupHistory = context.getGroupMember(self.session.guild.id,self.session.user.id)
        self.dictionary = Dictionary(self.session.self_id,self.session.platform)