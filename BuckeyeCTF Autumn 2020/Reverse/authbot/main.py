import discord
import random
import logging
import hashlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_fh = logging.FileHandler("bot.log")
logger_sh = logging.StreamHandler()

formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger_fh.setFormatter(formatter)

logger.addHandler(logger_fh)
logger.addHandler(logger_sh)

with open('secret/token.txt', 'r') as f:
    token = f.read().strip()

with open('secret/password.txt', 'r') as f:
    password_cipher = f.read().strip()


def escape_code(src):
    x = "\N{ZERO WIDTH SPACE}"
    return src.replace('```', '`{}`{}`'.format(x, x))


def split_cmd(args):
    result = []
    arg = ''
    inside_quotes = False
    for c in args:
        if c == '"':
            if inside_quotes:
                # Stop recording token
                inside_quotes = False
                result.append(arg)
                arg = ''
            else:
                # Start recording token
                inside_quotes = True
        else:
            if inside_quotes:
                arg += c
            else:
                if c == ' ':
                    if arg != '':
                        result.append(arg)

                    arg = ''
                else:
                    arg += c

    if arg != '':
        result.append(arg)

    return result


def file_tail(filename, n):
    """Print last `n` lines of file"""
    result = ''
    with open(filename, 'r') as f:
        for line in (f.readlines()[-n:]):
            result += line

    return result


class MyClient(discord.Client):
    message_caches = {}

    async def on_ready(self):
        logger.info('Logged in as {0.user}'.format(client))

    async def cmd_info(self, message, args):
        response = """
I'm a super cool authentication bot
Source code: https://github.com/qxxxb/auth_bot
        """

        await message.channel.send(response)

    async def cmd_ping(self, message, args):
        response = "{:.0f} ms".format(self.latency * 1000)
        await message.channel.send(response)

    async def cmd_debug_log(self, message, args):
        prefix = '```log\n'
        suffix = '```'
        response = file_tail('bot.log', 10)
        await message.channel.send(prefix + response + suffix)

    async def cmd_coinflip(self, message, args):
        result = random.randrange(2)
        if result:
            response = 'Heads'
        else:
            response = 'Tails'
        await message.channel.send(response)

    async def cmd_unknown(_, self, message, args):
        await message.channel.send('Unknown command')

    async def cmd_auth(self, message, args):
        if len(args) != 1:
            response = 'Expected 1 argument'
        else:
            plaintext = args[0]
            plaintext_bytes = str.encode(plaintext)

            m = hashlib.sha256()
            m.update(plaintext_bytes)
            cipher = m.hexdigest()

            if cipher == password_cipher:
                logger.debug(
                    'User {} authed as admin with password hash {}'
                    .format(message.author, cipher)
                )

                guild = discord.utils.get(self.guilds, name="Rubberduck")
                admin_role = discord.utils.get(guild.roles, name="admin")
                member = guild.get_member(message.author.id)
                await member.add_roles(admin_role)

                response = 'Successfully authenticated as admin on Rubberduck'
            else:
                response = 'Incorrect password'

        await message.channel.send(response)

    async def cmd_help(self, message, args):
        response = """
```
$ping
$coinflip
$auth
$help
$info
```
        """

        await message.channel.send(response)

    cmd_prefix = '$'

    cmd_switch = {
        'ping': cmd_ping,
        'coinflip': cmd_coinflip,
        'auth': cmd_auth,
        'help': cmd_help,
        'info': cmd_info,
        'debug_log': cmd_debug_log,
    }

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith(self.cmd_prefix):
            cmd = message.content[1:]
            cmd_array = split_cmd(cmd)

            cmd = cmd_array[0]
            args = cmd_array[1:]

            cmd_func = self.cmd_switch.get(cmd, self.cmd_unknown)
            await cmd_func(self, message, args)


client = MyClient()
client.run(token)
