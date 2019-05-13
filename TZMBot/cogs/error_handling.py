import asyncio
import logging
import sys
import traceback

from discord.ext import commands

from TZMBot import settings, utils

logger = logging.getLogger("__main__")


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.error_channel = None
        self.client.loop.create_task(self.async_setup())

    async def async_setup(self):
        await self.client.wait_until_ready()
        self.error_channel = self.client.get_channel(settings.ERROR_CHANNEL_ID)

        logger.info("ErrorHandling cog async_setup complete")

    async def err_reporting(self, ctx, err):
        report_confirmation = await ctx.send(
            "An unexpected error occurred, would you like to report it? "
            "You must decide within 30 seconds"
        )
        await report_confirmation.add_reaction(
            "\U0001f1fe"
        )  # regional_indicator_y emoji
        await report_confirmation.add_reaction(
            "\U0001f1f3"
        )  # regional_indicator_n emoji

        try:
            response, user = await self.client.wait_for(
                "reaction_add",
                check=lambda r, u: u.id == ctx.author.id
                and r.emoji in ["\U0001f1fe", "\U0001f1f3"],
                timeout=30,
            )

        except asyncio.TimeoutError:  # 30 seconds passes without response
            await utils.strikethrough(report_confirmation, "Time's up!")
            return

        if response.emoji == "\U0001f1fe":  # response is yes
            report = "".join(
                traceback.format_exception(type(err), err, err.__traceback__)
            )
            await self.error_channel.send(
                f"Exception raised in command {ctx.command} in cog {ctx.command.cog_name} "
                f"by user {ctx.author}: ```py\n{report}\n```"
            )

        else:  # response is no
            await utils.strikethrough(
                report_confirmation, "You chose not to report the error"
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandInvokeError):
            if ctx.author.id in settings.DEV_IDS:
                print(
                    f"Ignoring exception in command {ctx.command} in cog {ctx.command.cog_name}:",
                    file=sys.stderr,
                )
                traceback.print_exception(
                    type(exc), exc, exc.__traceback__, file=sys.stderr
                )

                return await ctx.send("Unexpected error, traceback printed to console")

            return await self.err_reporting(ctx, exc)

        if (
            isinstance(exc, commands.CheckFailure)
            or isinstance(exc, commands.CommandNotFound)
            or isinstance(exc, commands.DisabledCommand)
        ):
            return

        await ctx.send(exc)


def setup(client):
    client.add_cog(ErrorHandling(client))
