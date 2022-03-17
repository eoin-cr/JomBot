# error.py
import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot: commands.Bot):
        print("Error initialised")
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """A global error handler cog."""
        print(error)
        print(type(error))
        match type(error):
            case commands.CommandNotFound:
                return  # Return because we don't want to show an error for every command not found
            case commands.CommandOnCooldown:
                message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
            case commands.MissingPermissions:
                message = "You are missing the required permissions to run this command!"
            case commands.UserInputError:
                message = "Something about your input was wrong, please check your input and try again!"
            case commands.MissingRequiredArgument:
                message = "You are missing a required argument for this command!"
            case commands.BadArgument:
                message = "There was an error in parsing one of your arguments, please check your input and try again!"
            case commands.PrivateMessageOnly:
                message = "This command only works in DMs!"
            case commands.NoPrivateMessage:
                message = "This command doesn't works in DMs!"
            case commands.TooManyArguments:
                message = "Too many arguments provided!"
            case commands.ChannelNotReadable:
                message = "JomBot cannot read this channel!  Please fix the perms!"
            case commands.BotMissingPermissions:
                message = "JomBot is missing the perms to run this command.  Please fix the permissions!"
            case commands.CommandInvokeError:
                message = "There was an invoke error.  There is probably a mistake in one of your arguments."
            case commands.CheckFailure:
                return
            case _:
                message = "Oh no! Something went wrong while running the command!"

        error_str = str(type(error)).replace("<class 'discord.ext.commands.errors.", "")
        error_str = error_str.replace("'>", "")
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name=error_str, value=message, inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
