import json
import requests
import logging

from Colya.bot import config


POST = 'post'
GET = 'get'
platform = ""
self_id = ""


class Call:
    def __init__(self, method, url, platform, self_id, data) -> None:
        self.method = method
        self.url = url
        self.data = data
        self.platform = platform
        self.self_id = self_id

    def run(self):
        # API endpoint
        # 替换为实际API endpoint
        endpoint = f'http://{config.getHost()}:{config.getPort()}/v1{self.url}'
        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.getToken()}',
            'X-Platform': self.platform,
            'X-Self-ID': self.self_id
        }
        response = requests.post(
            endpoint, json=self.data, headers=headers, verify=True)
        
        # 检查响应
        if response.status_code == 200:
            logging.info(f'[操作成功:{self.url}]({response.status_code}){str(self.data)}')
            return response.text
        else:
            logging.info(f'[操作失败:{self.url}]({response.status_code}){str(self.data)}')
            return None


class _Base:
    def __init__(self, method, url, platform, self_id, data) -> None:
        self.method = method
        self.url = url
        self.data = data
        self.platform = platform
        self.self_id = self_id

    def do(self):
        Call(self.method, self.url, self.platform,
             self.self_id, self.data).run()


class Dictionary:
    '''
    字典类

    包含所有操作的实现方法

    :param p string	平台(默认chronocat)
    :param sid string	机器人id
。
    '''
    def __init__(self, sid, p='chronocat') -> None:
        global platform, self_id
        platform = p
        self_id = sid

    class Channel(_Base):
        '''
        频道 (Channel) 
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/channel'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeChannel:
        '''
        Channel
        :param id	        string	        频道 ID
        :param type	        Channel.Type	频道类型
        :param name	        string?	        频道名称
        :param parent_id	string?	        父频道 ID

        Channel.Type
        :param TEXT	0	文本频道
        :param VOICE	1	语音频道
        :param CATEGORY	2	分类频道
        :param DIRECT	3	私聊频道
        '''
        id = ""
        type = 0,
        name = "",
        parent_id = ""

    class ChannelGet(Channel):
        '''
        获取群组频道
        :param channel_id	string	频道 ID

        根据 ID 获取频道。返回一个 Channel 对象。
        '''

        def __init__(self, channel_id) -> None:
            super().__init__(POST, 'get', {
                "channel_id": channel_id
            })

    class ChannelList(Channel):
        '''
        获取群组频道列表
        :param guild_id	string	群组 ID
        :param next	string	分页令牌

        获取群组中的全部频道。返回一个 Channel 的 分页列表。
        '''

        def __init__(self, guild_id, _next="") -> None:
            super().__init__(POST, 'list', {
                "guild_id": guild_id,
                "next": _next
            })

    class ChannelCreate(Channel):
        '''
        创建群组频道
        :param guild_id	string	群组 ID
        :param data	Channel	频道数据

        创建群组频道。返回一个 Channel 对象。
        '''

        def __init__(self, guild_id, data) -> None:
            super().__init__(POST, 'create', {
                "guild_id": guild_id,
                "data": data
            })

    class ChannelUpdate(Channel):
        '''
        修改群组频道
        :param channel_id	string	频道 ID
        :param data	Channel	频道数据

        修改群组频道。
        '''

        def __init__(self, channel_id, data) -> None:
            super().__init__(POST, 'update', {
                "channel_id": channel_id,
                "data": data
            })

    class ChannelDelete(Channel):
        '''
        删除群组频道
        :param channel_id	string	频道 ID

        删除群组频道。
        '''

        def __init__(self, channel_id) -> None:
            super().__init__(POST, 'delete', {
                "channel_id": channel_id
            })

    class UserChannelCreate(Channel):
        '''
        创建私聊频道
        :param user_id	string	用户 ID

        创建一个私聊频道。返回一个 Channel 对象。
        '''

        def __init__(self, user_id) -> None:
            super().__init__(POST, 'create', {
                "user_id": user_id
            })
            self.url = self.url.replace('/', '/user.')

    class Guild(_Base):
        '''
        群组 (Guild) 

        事件列表

        guild-added

        加入群组时触发。必需资源：guild。

        guild-updated

        群组被修改时触发。必需资源：guild。

        guild-removed

        退出群组时触发。必需资源：guild。

        guild-request

        接收到新的入群邀请时触发。必需资源：guild。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/guild'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeGuild:
        '''
        Guild 
        :param id	string	群组 ID
        :param name	string?	群组名称
        :param avatar	string?	群组头像
        '''
        id = ""
        name = ""
        avatar = ""

    class GuildGet(Guild):
        '''
        获取群组
        :param guild_id	string	群组 ID

        根据 ID 获取。返回一个 Guild 对象。
        '''

        def __init__(self, guild_id) -> None:
            super().__init__(POST, 'get', {
                "guild_id": guild_id
            })

    class GuildList(Guild):
        '''
        获取群组列表

        :param next	string	分页令牌

        获取当前用户加入的全部群组。返回一个 Guild 的 分页列表。
        '''

        def __init__(self, _next="") -> None:
            super().__init__(POST, 'list', {
                "next": _next
            })

    class GuildApprove(Guild):
        '''
        处理群组邀请 

        :param message_id	string	请求 ID
        :param approve	boolean	是否通过请求
        :param comment	string	备注信息
        处理来自群组的邀请。
        '''

        def __init__(self, message_id, approve, comment) -> None:
            super().__init__(POST, 'approve', {
                "message_id": message_id,
                "approve": approve,
                "comment": comment
            })

    class GuildMember(_Base):
        '''
        群组成员 (GuildMember) 

        事件
        guild-member-added

        群组成员增加时触发。必需资源：guild，member，user。

        guild-member-updated

        群组成员信息更新时触发。必需资源：guild，member，user。

        guild-member-removed

        群组成员移除时触发。必需资源：guild，member，user。

        guild-member-request

        接收到新的加群请求时触发。必需资源：guild，member，user。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/guild.member'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeGuildMember:
        '''
        :param user	TypeUser?	用户对象
        :param name	string?	用户在群组中的名称
        :param avatar	string?	用户在群组中的头像
        :param joined_at	number?	加入时间
        '''
        user = {}
        name = ""
        avatar = ""
        joined_at = ""

    class GuildMemberGet(GuildMember):
        '''
        获取群组成员

        :param guild_id	string	群组 ID
        :param user_id	string	用户 ID

        获取群成员信息。返回一个 GuildMember 对象。
        '''

        def __init__(self, guild_id, user_id) -> None:
            super().__init__(POST, 'get', {
                "guild_id": guild_id,
                "user_id": user_id
            })

    class GuildMemberList(GuildMember):
        '''
        获取群组成员列表

        :param guild_id	string	群组 ID
        :param next	string	分页令牌

        获取群成员列表。返回一个 GuildMember 的 分页列表。
        '''

        def __init__(self, guild_id, _next="") -> None:
            super().__init__(POST, 'list', {
                "guild_id": guild_id,
                "next": _next
            })

    class GuildMemberKick(GuildMember):
        '''
        踢出群组成员

        :param guild_id	string	群组 ID
        :param user_id	string	用户 ID
        :param permanent	boolean?	是否永久踢出 (无法再次加入群组)
        '''

        def __init__(self, guild_id, user_id, permanent) -> None:
            super().__init__(POST, 'kick', {
                "guild_id": guild_id,
                "user_id": user_id,
                "permanent": permanent
            })

    class GuildMemberApprove(GuildMember):
        '''
         通过群组成员申请

         :param message_id	string	请求 ID
         :param approve	boolean	是否通过请求
         :param comment	string?	备注信息

         处理加群请求。
        '''

        def __init__(self, message_id, approve, comment) -> None:
            super().__init__(POST, 'approve', {
                "message_id": message_id,
                "approve": approve,
                "comment": comment
            })

    class GuildRole(_Base):
        '''
        群组角色 (GuildRole) 

        事件

        guild-role-created

        群组角色被创建时触发。必需资源：guild，role。

        guild-role-updated

        群组角色被修改时触发。必需资源：guild，role。

        guild-role-deleted

        群组角色被删除时触发。必需资源：guild，role。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/guild.member.role'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeGuildRole:
        '''
        :param id	string	角色 ID
        :param name	string?	角色名称
        '''

    class GuildMemberRoleSet(GuildRole):
        '''
        设置群组成员角色

        :param guild_id	string	群组 ID
        :param user_id	string	用户 ID
        :param role_id	string	角色 ID

        设置群组内用户的角色。
        '''

        def __init__(self, guild_id, user_id, role_id) -> None:
            super().__init__(POST, 'set', {
                "guild_id": guild_id,
                "user_id": user_id,
                "role_id": role_id
            })

    class GuildMemberRoleUnset(GuildRole):
        '''
        取消群组成员角色

        :param guild_id	string	群组 ID
        :param user_id	string	用户 ID
        :param role_id	string	角色 ID

        取消群组内用户的角色。
        '''

        def __init__(self, guild_id, user_id, role_id) -> None:
            super().__init__(POST, 'unset', {
                "guild_id": guild_id,
                "user_id": user_id,
                "role_id": role_id
            })

    class GuildRoleList(GuildRole):
        '''
        获取群组角色列表

        :param guild_id	string	群组 ID
        :param next	string?	分页令牌

        获取群组角色列表。返回一个 GuildRole 的 分页列表。
        '''

        def __init__(self, guild_id, _next="") -> None:
            super().__init__(POST, 'list', {
                "guild_id": guild_id,
                "next": _next
            })
            self.url.replace('.member', '')

    class GuildRoleCreate(GuildRole):
        '''
        创建群组角色

        :param guild_id	string	群组 ID
        :param role	GuildRole	角色数据

        创建群组角色。返回一个 GuildRole 对象。
        '''

        def __init__(self, guild_id, role) -> None:
            super().__init__(POST, 'create', {
                "guild_id": guild_id,
                "role": role
            })
            self.url.replace('.member', '')

    class GuildRoleUpdate(GuildRole):
        '''
        修改群组角色

        :param rguild_id	string	群组 ID
        :param rrole_id	string	角色 ID
        :param rrole	GuildRole	角色数据

        修改群组角色。
        '''

        def __init__(self, rguild_id, rrole_id, rrole) -> None:
            super().__init__(POST, 'update', {
                "rguild_id": rguild_id,
                "rrole_id": rrole_id,
                "rrole": rrole
            })
            self.url.replace('.member', '')

    class GuildRoleDelete(GuildRole):
        '''
        删除群组角色

        :param guild_id	string	群组 ID
        :param role_id	string	角色 ID

        删除群组角色。
        '''

        def __init__(self, guild_id, role_id) -> None:
            super().__init__(POST, 'delete', {
                "guild_id": guild_id,
                "role_id": role_id
            })
            self.url.replace('.member', '')

    class Login(_Base):
        '''
        登录信息 (Login) 

        事件 

        login-added

        登录被创建时触发。必需资源：login。

        login-removed

        登录被删除时触发。必需资源：login。

        login-updated

        登录信息更新时触发。必需资源：login。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/login'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeLogin:
        '''
        类型定义

        Login

        :param user	TypeUser?	用户对象
        :param self_id	string?	平台账号
        :param platform	string?	平台名称
        :param status	Status	登录状态

        Login.Status

        :param OFFLINE	0	离线
        :param ONLINE	1	在线
        :param CONNECT	2	连接中
        :param DISCONNECT	3	断开连接
        :param RECONNECT	4	重新连接
        '''
        user = {}
        self_id = ""
        platform = ""
        status = 0

    class LoginGet(Login):
        '''
        获取登录信息

        获取登录信息。返回一个 Login 对象。
        '''

        def __init__(self) -> None:
            super().__init__(POST, 'get', {})

    class Message(_Base):
        '''
        消息 (Message) 

        message-created

        当消息被创建时触发。必需资源：channel，message，user。

        message-updated

        当消息被编辑时触发。必需资源：channel，message，user。

        message-deleted

        当消息被删除时触发。必需资源：channel，message，user。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/message'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeMessage:
        '''
        Message

        :param id	string	消息 ID
        :param content	string	消息内容
        :param channel	TypeChannel?	频道对象
        :param guild	TypeGuild?	群组对象
        :param member	TypeGuildMember?	成员对象
        :param user	TypeUser?	用户对象
        :param created_at	number?	消息发送的时间戳
        :param updated_at	number?	消息修改的时间戳
        '''
        id = ""
        content = ""
        channel = {}
        guild = {}
        member = {}
        user = {}
        created_at = 0
        updated_at = 0

    class MessageCreate(Message):
        '''
        发送消息

        :param channel_id	string	频道 ID
        :param content	string	消息内容

        发送消息。返回一个 Message 对象构成的数组。
        '''

        def __init__(self, channel_id,content) -> None:
            super().__init__(POST, 'create', {
                "channel_id": channel_id,
                "content":content
            })

    class MessageGet(Message):
        '''
        获取消息

        :param channel_id	string	频道 ID
        :param message_id	string	消息 ID

        获取特定消息。返回一个 Message 对象。
        '''

        def __init__(self, channel_id, message_id) -> None:
            super().__init__(POST, 'get', {
                "channel_id": channel_id,
                "message_id": message_id
            })

    class MessageDelete(Message):
        '''
        撤回消息

        :param channel_id	string	频道 ID
        :param message_id	string	消息 ID

        撤回特定消息。
        '''

        def __init__(self, channel_id, message_id) -> None:
            super().__init__(POST, 'delete', {
                "channel_id": channel_id,
                "message_id": message_id
            })

    class MessageUpdate(Message):
        '''
        编辑消息

        :param channel_id	string	频道 ID
        :param message_id	string	消息 ID
        :param content	string	消息内容

        编辑特定消息。
        '''

        def __init__(self, channel_id, message_id, content) -> None:
            super().__init__(POST, 'update', {
                "channel_id": channel_id,
                "message_id": message_id,
                "content": content
            })

    class MessageList(Message):
        '''
        获取消息列表

        :param channel_id	string	频道 ID
        :param next	string	分页令牌

        获取频道消息列表。返回一个 Message 的 分页列表。
        '''

        def __init__(self, channel_id, _next="") -> None:
            super().__init__(POST, 'list', {
                "channel_id": channel_id,
                "next": _next
            })

    class User(_Base):
        '''
        用户 (User) 

        事件

        friend-request

        接收到新的好友申请时触发。必需资源：user。
        '''

        def __init__(self, method, url, data) -> None:
            self.baseUrl = '/user'
            super().__init__(
                method, f'{self.baseUrl}.{url}', platform, self_id, data)

    class TypeUser:
        '''
        :param id	string	用户 ID
        :param name	string?	用户名称
        :param avatar	string?	用户头像
        :param is_bot	boolean?	是否为机器人
        '''
        id = ""
        name = ""
        avatar = ""
        is_bot = False

    class UserGet(User):
        '''
        获取用户信息

        :param user_id	string	用户 ID

        获取用户信息。返回一个 User 对象。
        '''
        def __init__(self, user_id) -> None:
            super().__init__(POST, 'get', {
                "user_id": user_id
            })

    class FriendList(User):
        '''
        获取好友列表

        :param next	string?	分页令牌

        获取好友列表。返回一个 User 的 分页列表。
        '''
        def __init__(self, _next="") -> None:
            super().__init__(POST, 'list', {
                "next": _next
            })
            self.url.replace('/user','/friend')
    
    class FriendApprove(User):
        '''
        处理好友申请

        :param message_id	string	请求 ID
        :param approve	boolean	是否通过请求
        :param comment	string?	备注信息

        处理好友申请。
        '''
        def __init__(self, message_id,approve,comment) -> None:
            super().__init__(POST, 'approve', {
                "message_id":message_id,
                "approve":approve,
                "comment":comment
            })
            self.url.replace('/user','/friend')

