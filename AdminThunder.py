import discord
import os
import configparser
import time
import asyncio
from discord.ext import commands
# os.environ variables for bot token, mod_channel
try:
    TOKEN = os.environ['TOKEN']
    MOD_CHANNEL = os.environ['MOD_CHANNEL']
    USER_COUNT = int(os.environ['USER_COUNT'])
    IGNORE_CHANNELS = os.environ['IGNORE_CHANNELS'].split(',')
    MODS = os.environ['MODS'].split(',')
    STAN_CHANNEL = os.environ['STAN_CHANNEL']
    guild = [os.environ['GUILD']]

except:
    config = configparser.ConfigParser()
    config.read('config.cfg')
    TOKEN = config['INDEV']['TOKEN']
    MOD_CHANNEL = config['INDEV']['MOD_CHANNEL']
    USER_COUNT = 1
    IGNORE_CHANNELS = [715969933980467263]
    MODS = [96084847696560128]
    STAN_CHANNEL = 867024768745078785
    guild = 715969933980467260

# Create a new interactions Discord client
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = discord.Bot()

async def is_mod(ctx):
    if ctx.author.id in MODS:
        return True
    else:
        return False

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')

@bot.event
async def on_raw_reaction_add(payload):
    #check if the reaction is the one we want
    if payload.emoji.name.lower() == 'pleasestop':
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.author.id == bot.user.id:
            return

        if payload.channel_id in IGNORE_CHANNELS:
            return
        
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

        if reaction.count >= USER_COUNT:
            log_channel = bot.get_channel(int(MOD_CHANNEL))
            user = bot.get_user(message.author.id)
            if message.author.id != 304870344924200972:
                await log_channel.send(f"Offending User: {user.display_name} \nChannel: {f'<#{channel.id}>'}\nTime: <t:{int(time.time())}:F> \nOffended Users: {', '.join(member.name for member in users)}\nMessage:\n\n {message.content}", files=files)
                
                await channel.send(f'{user.mention}, your post has been deleted and is under further review.')

            await message.delete()

@commands.check(is_mod)
@bot.message_command(name="Yeet to Stan", guild_ids=guild)
async def yeet(ctx: discord.ApplicationContext, message: discord.Message):
    await ctx.defer(ephemeral =True)
    stan = bot.get_channel(int(STAN_CHANNEL))
    mod_channel = bot.get_channel(int(MOD_CHANNEL))
    files = []
    try:
        for index, attachment in enumerate(message.attachments):
            #save attachment as file in /tmp/
            await attachment.save(f'tmp/{index}_' + attachment.filename)
            files.append(discord.File(f"tmp/{index}_{attachment.filename}"))
    except:
            files = None

    try:    
        new_message = await stan.send(f"{message.author.mention} (from {message.channel.mention}): {message.content}", files=files)
    except Exception as e:
        await mod_channel.send(f"{ctx.author.mention} tried to yeet to Stan's channel, but failed to send a message to {stan.mention}.")
        print(e)

    embed = discord.Embed(title="Yeeted to Stan's", description = f"Your message/images were sent to Stan's channel, as they were deemed inappropriate for {message.channel}.", color=0x00ff00)
    if message.content != "":
        embed.add_field(name = "Message", value = message.content)
    embed.add_field(name = "Moved By", value = ctx.author)
    embed.add_field(name="Moved To", value = new_message.jump_url)

    await message.author.send(embed=embed)
    #await message.author.send(files=files)

    

#    try:
        
#    except:
#        await mod_channel.send(f"{ctx.author.mention} tried to yeet images to Stan's channel, but failed to send a message to {stan.mention}.")
    
    await message.delete()

    await mod_channel.send(f"Message from {message.author.mention} in {message.channel.mention} was yeeted to Stan's channel.")
    
#@yeet.error
#async def info_error(ctx: discord.ApplicationContext, error):
#    if isinstance(error, commands.CheckFailure):
#        await ctx.send("You are not a mod.")
        
@bot.event
async def on_message(message):

    if message.author.id == bot.user.id:
        #delete all files in /tmp/
        await asyncio.sleep(10)
        for file in os.listdir(r'./tmp/'):
            try:
                os.remove('tmp/'+ file)
            except:
                pass
        return

    else:
        pass
        

bot.run(TOKEN)
