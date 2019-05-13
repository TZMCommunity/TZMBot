import logging

from discord.ext import commands

from TZMBot import settings

WELCOME_MESASGE = "{member.mention} just joined. welcome!"
GOODBYE_MESSAGE = "{member.mention} ({member}) just left. goodbye!"

logger = logging.getLogger("__main__")


class Welcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.welcome_channel = None
        self.client.loop.create_task(self.async_setup())

    async def async_setup(self):
        await self.client.wait_until_ready()
        self.welcome_channel = self.client.get_channel(settings.WELCOME_CHANNEL_ID)

        logger.info("Welcoming cog async_setup complete")

    async def welcome_goodbye(self, member, message):
        if member.guild.id == self.welcome_channel.guild.id:
            await self.welcome_channel.send(message.format(member=member))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.welcome_goodbye(member, WELCOME_MESASGE)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.welcome_goodbye(member, GOODBYE_MESSAGE)


def setup(client):
    client.add_cog(Welcoming(client))
