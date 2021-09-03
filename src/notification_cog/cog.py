from logging import getLogger

import discord
from discord import Guild
from discord.ext import commands

logger = getLogger(__name__)


class NotificationCog(commands.Cog):
    """入退室を記録するCog"""

    ROLE_NAME = '入退室ログ'
    CHANNEL_NAME = '入退室ログ'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        for guild in self.bot.guilds:
            guild: Guild

            if discord.utils.get(guild.roles, name=self.ROLE_NAME) is None:
                logger.debug(f'{guild.name}に権限を作成しました')
                await guild.create_role(name=self.ROLE_NAME, reason='入退室ログで記録するユーザーを管理するため')

            if discord.utils.get(guild.channels, name=self.CHANNEL_NAME) is None:
                logger.debug(f'{guild.name}にチャンネルを作成しました')
                await guild.create_text_channel(name=self.CHANNEL_NAME, topic='入退室のログを記録するチャンネル', reason='入退室ログのために作成')

    @commands.Cog.listener('on_voice_state_update')
    async def on_voice_state_update(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        guild: Guild = member.guild
        before_vc_name = before.channel.name if before.channel is not None else None
        after_vc_name = after.channel.name if after.channel is not None else None
        logger.debug(f'{member.display_name} / {before_vc_name} -> {after_vc_name}')

        role = discord.utils.get(member.roles, name=self.ROLE_NAME)
        if role is None:
            logger.debug('対象のアカウントでないためスルー')
            return

        if before_vc_name == after_vc_name:
            logger.debug('入退室以外に反応したためスルー')
            return

        if after_vc_name is None:
            text = f'{member.display_name}が{before_vc_name}から退室しました'
        else:
            text = f'{member.display_name}が{after_vc_name}に入室しました'

        text_channel = discord.utils.get(guild.channels, name=self.CHANNEL_NAME)
        await text_channel.send(text)


def setup(bot):
    return bot.add_cog(NotificationCog(bot))
