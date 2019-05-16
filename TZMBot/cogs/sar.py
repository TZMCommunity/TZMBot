import logging

import discord
from discord.ext import commands

from TZMBot import settings, utils

logger = logging.getLogger("__main__")


class SelfAssignableRoles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = settings.SAR_CONFIG

        self.dict = {
            emoji: role_id
            for message_id in self.config.keys()
            for category in self.config[message_id]["categories"].values()
            for emoji, role_id in category.items()
        }

        self.channel = None
        self.message = None
        self.active = False
        self.messages = {}
        self.client.loop.create_task(self.async_call_setup())

    async def async_call_setup(self):
        await self.client.wait_until_ready()

        try:
            await self.async_setup()
        except Exception as e:
            logger.error("SelfAssignableRoles ERROR " + str(e))
    
    async def async_setup(self):
        self.channel = self.client.get_channel(settings.SAR_CHANNEL_ID)
        if not isinstance(self.channel, discord.TextChannel):
            raise ValueError(
                "SAR_CHANNEL_ID config variable must correspond to a TextChannel " + str(settings.SAR_CHANNEL_ID)
            )

        for message_id in self.config:
            logger.info("SelfAssignableRoles setup message_id " + str(message_id))
            
            message = await self.channel.fetch_message(message_id)
            self.messages[message_id] = message
            
            await message.edit(embed=self.make_embed(message_id), content=None)
            await message.clear_reactions()
            await utils.add_many_reactions(message, *self.dict.keys())
        
        self.active = True

        logger.info("SelfAssignableRoles cog async_setup complete")

    def make_embed(self, message_id) -> discord.Embed:
        embed = discord.Embed(
            title="Self-Assignable Roles",
            description="Click a reaction below to obtain a role, click it again to remove it.",
        )
        for name, category in self.config[message_id]["categories"].items():
            value = ""
            for emoji, role_id in category.items():
                role = self.channel.guild.get_role(role_id)
                value += f"\n{emoji}: {role.mention}"
            embed.add_field(name=name, value=value)
        return embed

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if (
            self.active
            and payload.message_id in self.messages
            and payload.channel_id == self.channel.id
            and payload.emoji.name in self.dict.keys()
        ):
            role = self.channel.guild.get_role(self.dict[payload.emoji.name])
            member = self.channel.guild.get_member(payload.user_id)

            if role.id in [r.id for r in member.roles]:
                await member.remove_roles(role, reason="Removed via the SAR system.")
                message = f'{member.mention}, I removed your "{role}" role!'
            else:
                await member.add_roles(role, reason="Added via the SAR system.")
                message = f'{member.mention}, I gave you a "{role}" role!'

            await self.messages[payload.message_id].remove_reaction(payload.emoji.name, member)
            await self.channel.send(message, delete_after=8)


def setup(client):
    client.add_cog(SelfAssignableRoles(client))
