from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.load_extension('notification_cog')  # <1>
bot.run('<bot token>')  # <2>
