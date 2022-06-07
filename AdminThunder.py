import discord
import os
import configparser

# os.environ variables for bot token, mod_channel
try:
    TOKEN = os.environ['TOKEN']
    MOD_CHANNEL = os.environ['MOD_CHANNEL']
    USER_COUNT = int(os.environ['USER_COUNT'])
except:
    config = configparser.ConfigParser()
    config.read('config.cfg')
    TOKEN = config['INDEV']['TOKEN']
    MOD_CHANNEL = config['INDEV']['MOD_CHANNEL']
    USER_COUNT = 1

# Create a new interactions Discord client
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents, command_prefix='.', case_insensitive=True)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------------')

@client.event
async def on_raw_reaction_add(payload):
    #check if the reaction is the one we want
    if payload.emoji.name.lower() == 'pleasestop':
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
        users = set()
        async for member in reaction.users():
            users.add(member)
        files = []
        try:
            for index, attachment in enumerate(message.attachments):
                #save attachment as file in /tmp/
                await attachment.save(f'tmp/{index}_' + attachment.filename)
                files.append(discord.File(f"tmp/{index}_{attachment.filename}"))
        except:
            files = None

        if reaction.count > USER_COUNT:
            log_channel = client.get_channel(MOD_CHANNEL)
            user = client.get_user(message.author.id)

            await log_channel.send(f"{user.display_name} sent the following message in {f'<#{channel.id}>'}, which was deemed inappropriate by at least three users: {', '.join(member.name for member in users)}\n\n {message.content}", files=files)
            
            await channel.send(f'{user.mention}, your post has been deleted and is under further review.')

            await message.delete()

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        #delete all files in /tmp/
        for file in os.listdir(r'./tmp/'):
            try:
                os.remove('tmp/'+ file)
            except:
                pass
        return

    else:
        message.process_commands()
        

client.run(TOKEN)
