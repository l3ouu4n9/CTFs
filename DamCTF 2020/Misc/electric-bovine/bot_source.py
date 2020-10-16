import discord
import bot_token
import os
import random

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def authenticate(author, authorizer, role):

    # Derive a variant to make auth requests resolve uniquely
    variant = author.discriminator
    variant = int(variant * 4)

    # Add author's name to their credential set
    author_credentials = [author.nick]
    # Add perms
    author_credentials.extend([str(int(y.id) + variant) for y in author.roles])
    author_credentials.extend([y.name.lower() for y in author.roles])

    # Add authorizer's name
    authorizer_credentials = [authorizer.name]
    # Add perms
    authorizer_credentials.extend([str(int(y.id) + variant) for y in authorizer.roles])
    authorizer_credentials.extend([y.name.lower() for y in authorizer.roles])

    # Add role name
    role_information = [role.name, str(int(role.id) + variant)]

    permset = list(
        (set(author_credentials) & set(authorizer_credentials)) & set(role_information)
    )

    if len(permset) >= 1:
        return True
    else:
        return False


@client.event
async def on_ready():
    print("+ We have logged in as {0.user}".format(client))


@client.event
async def on_member_join(member):
    # Assign new member the `user` role
    role = client.guilds[0].get_role(763128055429595156)
    await member.add_roles(role)

    # Dm the help command to the user.
    await member.send(f"Welcome! You may run `!help` here to find out about me.",)


@client.event
async def on_message(message):

    # print(f"+ Captured Message [{ message.content }] :: { message }")

    # Forbid bot from replying if in guild and channel is not botspam.
    if message.guild and message.channel.name != "botspam":
        return

    # Hello
    if message.content.startswith("!ping"):
        if message.guild:
            await message.channel.send("> Server Pong")
        else:
            await message.author.send("> DM Pong")

    # Help
    if message.content.startswith("!help"):
        await message.channel.send(
            "".join(
                (
                    "**Help Menu**\n",
                    "-------------\n",
                    " - `!help`\tDisplays this message.\n",
                    " - `!ping`\tPong??\n",
                    " - `!about`\tDisplays information about this bot.\n",
                    " - `!resource`\tLinks you to a random resource.\n",
                    " - `!cowsay <text>`\tDisplays your text in cowsay format. Requires greater permissions than `user` in the guild to use.\n",
                    " - `!list_users`\t Lists all users in channel.\n",
                    " - `!send_msg <text>`\t(when used from DMs) sends a message in the #botspam channel in the guild.\n",
                    " - `!role_add <user> <role>`\tAttempt to add role to user. May only be used from within guild.\n",
                )
            )
        )

    # About
    if message.content.startswith("!about"):
        await message.channel.send(
            "".join(
                (
                    "**About Me**\n",
                    "----------\n",
                    "I'm a bot. On the weekends, I'm a huge fan.\n",
                    f"My name is `{client.user}`\n",
                    "You may find my source code here:<https://beav.es/o7y>\n",
                    "You may find my bot token here <https://beav.es/o7r>\n",
                    "License: None.",
                )
            )
        )

    # Resource
    if message.content.startswith("!resource"):
        if message.guild:
            return
        else:

            resources = [
                "https://youtu.be/Ik_EN0fivxY",
                "https://youtu.be/rRPQs_kM_nw",
                "https://youtu.be/r-5KzHDPCTM",
                "https://youtu.be/QajlEuPMVjg",
                "https://youtu.be/QhLMlA3Wb8w",
            ]

            await message.author.send(random.choice(resources))

    # Send Msg
    if message.content.startswith("!send_msg"):
        try:
            message_to_send = message.content.split("!send_msg ")[1]
        except:
            return

        if message.guild:
            await message.author.send(
                f"**The following was sent from {message.author.name} in {message.guild.name}**"
            )
            await message.author.send(message_to_send)
        else:
            await client.guilds[0].text_channels[1].send(
                f"**The following message was sent from {message.author.name} in DMs**"
            )
            await client.guilds[0].text_channels[1].send(message_to_send)

    # List Users
    if message.content.startswith("!list_users"):
        if message.guild:
            await message.channel.send(
                " - `"
                + "`\n- `".join(
                    [member.display_name for member in message.guild.members]
                )
                + "`"
            )
        else:
            await message.author.send("Here, it's just us two.")

    # Cowsay
    if message.content.startswith("!cowsay"):
        if message.guild:
            await message.channel.send(
                "Sorry, but `!cowsay` is only available for use in dm channels."
            )
            return

        else:
            if message.author == client.user:
                return
            elif (
                client.guilds[0].get_member(message.author.id).guild_permissions
                >= client.guilds[0].get_role(763128087226351638).permissions
            ):
                # accept, do cowsay.
                try:
                    arg = message.content.split("!cowsay ")[1]
                except:
                    message.author.send("Bad arguments to !cowsay")
                    return

                for char in arg:
                    if char in " `1234567890-=~!@#$%^&*()_+[]\\{}|;':\",./?":
                        await message.author.send("Invalid character sent. Quitting.")
                        return

                cow = "```\n" + os.popen("cowsay " + arg).read() + "\n```"

                await message.author.send(cow)

            else:
                await message.author.send(
                    "You do not have the requisite roles to use !cowsay. Sorry."
                )

    # Add A Role
    if message.content.startswith("!role_add"):
        if message.guild:
            content = message.content

            try:
                args = content.split("!role_add ")[1].split(" ")
            except:
                await message.channel.send(f"Too few values to !role_add")
                return

            if len(args) != 2:
                return

            try:
                member = message.guild.get_member(int(args[0][3:-1]))
                user = client.get_user(int(args[0][3:-1]))
                role = message.guild.get_role(int(args[1][3:-1]))
            except:
                await message.channel.send(
                    f"You passed a bad user or role to !role_add"
                )
                return

            await message.channel.send(
                f"Hmmm... { member.name } wants to add role { role.name }. Interesting. . . "
            )
            await user.send(
                f"Hmmm... { member.name } wants to add role { role.name }. Interesting. . . ",
            )

            auth = authenticate(member, message.guild.get_member(client.user.id), role,)

            if auth and role.name != "bot":
                await member.add_roles(role)
                await message.channel.send(
                    f"Granted role {role.name} to member {member.name}. Well Done!"
                )
                await user.send(
                    f"Granted role {role.name} to member {member.name}. Well Done!"
                )
            else:
                await message.channel.send(
                    f"Denied role {role.name} to member {member.name}. Gotta hack harder than that!"
                )
                await user.send(
                    f"Denied role {role.name} to member {member.name}. Gotta hack harder than that!",
                )
        else:
            await message.author.send("You are forbidden from invoking that here.")


client.run(bot_token.token)
