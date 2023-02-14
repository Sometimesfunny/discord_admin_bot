from datetime import datetime, timedelta
import discord
from discord.ext import tasks
from discord import app_commands
from discord import RawReactionActionEvent
import configparser
import json
from raffles.raffle_processor import RaffleProcessor
from raffles.raffle_modal import CreateRaffleModal
import random
from captcha_lib.captcha import NewCaptcha
import copy

# save data
def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# load data
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# load raffles.json
try:
    raffles = load_data('raffles.json')
except FileNotFoundError:
    raffles = {
        'ongoing_raffles_list': [],
        'completed_raffles_list': [],
        'current_id': 0
    }
    save_data(raffles, 'raffles.json')

# load calls_timetable.json
def load_calls_timetable():
    try:
        loaded_data : dict = load_data('calls_timetable.json')
        # convert dict keys to int
        loaded_data_copy = copy.deepcopy(loaded_data)
        output_data = {}
        try:
            for week in loaded_data_copy.items():
                output_data[int(week[0])] = {}
                for time in week[1].items():
                    output_data[int(week[0])][time[0]] = {}
                    for week_number in time[1].items():
                        output_data[int(week[0])][time[0]][int(week_number[0])] = loaded_data[week[0]][time[0]][week_number[0]]
            return output_data
        except:
            return None
    except FileNotFoundError:
        calls_timetable = {}
        for weekday in range(1, 8):
            calls_timetable[weekday] = {}
        return calls_timetable
    except json.decoder.JSONDecodeError:
        return None


# calculate next call time
def calculate_next_calls_time():
    now = datetime.now()
    calls_timetable = load_calls_timetable()
    if calls_timetable is None:
        return None
    output_timetable = {}
    for week in calls_timetable.items():
        for time in week[1].items():
            for week_number in time[1].items():
                call_date : datetime = datetime.fromisocalendar(year=now.year, week=now.isocalendar()[1], day=week[0])
                call_time = time[0].split(':')
                call_date = call_date.replace(hour=int(call_time[0]), minute=int(call_time[1]))
                if week_number[0] == (now.isocalendar()[1] % 2 + 1):
                    if call_date.replace(hour=int(call_time[0])+1) < now:
                        call_date = call_date + timedelta(days=14)
                else:
                    call_date = call_date + timedelta(days=7)
                output_timetable[week_number[1]] = [f'<t:{int(call_date.timestamp())}>', f'<t:{int(call_date.timestamp())}:R>', f'<t:{int((call_date + timedelta(days=14)).timestamp())}>']
    return output_timetable
            


raffle_processor = RaffleProcessor(raffles)

class ButtonForRaffle(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Participate', style=discord.ButtonStyle.primary, custom_id='participate')
    async def participate(self, interaction : discord.Interaction, button : discord.ui.Button):
        raffle = raffle_processor.get_raffle_by_message_id(interaction.message.id)
        if raffle.user_in_raffle(interaction.user.id):
            await interaction.response.send_message(f'{interaction.user.mention} you are already in the raffle!', ephemeral=True)
        else:
            # embed as image
            await interaction.response.defer(thinking=True, ephemeral=True)
            captcha = NewCaptcha()
            embed = discord.Embed(title='Captcha', description='Please solve the captcha to participate in the raffle')
            embed.set_image(url=captcha.picture_url)
            await interaction.followup.send(embed=embed, view=captcha.view, ephemeral=True)
            await captcha.view.wait()
            if captcha.is_right:
                raffle.participants.append(interaction.user.id)
                await interaction.followup.send(f'{interaction.user.mention} you are now participating in the raffle!', ephemeral=True)

def check_role(user : discord.Member, command_name : str, server_data : dict):
    if user.guild_permissions.administrator:
        return True
    if command_name in server_data['allowed_roles'].keys():
        if server_data['allowed_roles'][command_name] == []:
            return False
        roles_hierarchy = [role.id for role in user.guild.roles]
        command_role_index = roles_hierarchy.index(server_data['allowed_roles'][command_name][0])
        user_role_index = roles_hierarchy.index(user.top_role.id)
        if user_role_index >= command_role_index:
            return True
    else:
        print(f'{command_name} is not a valid command, added to allowed_roles')
        server_data['allowed_roles'][command_name] = []
        save_data(data, 'data.json')
        return True
    return False

def community_calls_timetable_embed():
    calls_timetable = calculate_next_calls_time()
    if calls_timetable is None:
        return discord.Embed(title='DBS DAO Community Calls Timetable', description='No timetable found')
    embed = discord.Embed(title='DBS DAO Community Calls Timetable', description='Upcoming community calls', color=0x0055e8, timestamp=datetime.now())
    # sort timetable by date
    sorted_timetable = sorted(calculate_next_calls_time().items(), key=lambda x: x[1][0])
    for call in sorted_timetable:
        embed.add_field(name=call[0], value=f'Closest call: {call[1][0]}\nTime until closest call starts : {call[1][1]}\nNext call in 14 days: {call[1][2]}', inline=False)
    embed.set_footer(text='DBS DAO is a way to be in the black')
    return embed

# create discord bot class
class DiscordBot(discord.Client):
    # constructor
    def __init__(self, data : dict, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents ,*args, **kwargs)
        self.synced = False
        self.data = data
        self.view_added = False
    # on ready function
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        if not self.synced:
            await tree.sync()
            self.synced = True
        if not self.view_added:
            self.add_view(ButtonForRaffle())
            self.view_added = True
        raffles_check_loop.start()
        community_calls_timetable_loop.start()
    # on message function
    async def on_message(self, message : discord.Message):
        if message.author.bot:
            return
        if message.guild.id != GUILD_ID:
            return
    # on reaction add function
    async def on_raw_reaction_add(self, payload : RawReactionActionEvent):
        if payload.guild_id != GUILD_ID:
            return
        if payload.user_id == self.user.id:
            return
        if self.data == {}:
            return
        if payload.message_id == self.data['verification_message']['message_id']:
            if payload.emoji.name == self.data['verification_message']['emoji']:
                # get_guild
                guild = self.get_guild(payload.guild_id)
                await payload.member.add_roles(guild.get_role(self.data['verification_message']['role_id']), reason='Verified')
                await payload.member.add_roles(guild.get_role(1010588528767418470), reason='Verified')
                return

config = configparser.ConfigParser()
config.read('admin_bot_config.ini')
token = config['AUTH']['bot_token']

# try to load data
try:
    data = load_data('data.json')
except FileNotFoundError:
    data = {}

# run bot
bot = DiscordBot(data=data, command_prefix='!')

tree = app_commands.CommandTree(bot)

GUILD_ID = 1006200270176407582
GUILD = bot.get_guild(GUILD_ID)

# create command to add verification message to data
@tree.command(name='add_verification_message', description='Add a verification message to the data', guild=GUILD)
async def add_verification_message(interaction : discord.Interaction, message : str, emoji : str, giving_role : discord.Role):
    if not interaction.user.guild_permissions.administrator:
        return
    # create embed
    embed = discord.Embed(
        title='VERIFICATION MESSAGE',
        description=message,
        color=0x0055e8
    )
    await interaction.response.send_message(embed=embed)
    original_response = await interaction.original_response()
    await original_response.add_reaction(emoji)
    # add message to data
    data['verification_message'] = {
        'message_id': original_response.id,
        'emoji': emoji,
        'role_id': giving_role.id
    }
    print('Verification message created')
    # save data
    save_data(data, 'data.json')

# create command to create raffle
@tree.command(name='create_raffle', description='Create a raffle', guild=GUILD)
async def create_raffle(interaction : discord.Interaction):
    if not check_role(interaction.user, 'create_raffle', data):
        return
    new_raffle_modal = CreateRaffleModal()
    await interaction.response.send_modal(new_raffle_modal)
    if await new_raffle_modal.wait():
        await interaction.followup.send('Timeout', ephemeral=True)
        return
    name = new_raffle_modal.raffle_name.value
    description = new_raffle_modal.raffle_description.value
    duration = new_raffle_modal.raffle_duration.value
    try:
        duration = duration.split(':')
        duration = int(duration[0])*3600 + int(duration[1])*60 + int(duration[2])
    except Exception as e:
        print('[!] Error in create_raffle: ', e)
        await interaction.followup.send('Invalid duration', ephemeral=True)
        return
    winners_count = new_raffle_modal.raffle_winner_count.value
    try:
        winners_count = int(winners_count)
        if winners_count < 1:
            raise ValueError('Winners count must be greater than 0')
    except Exception as e:
        print('[!] Error in create_raffle: ', e)
        await interaction.followup.send('Invalid winners count', ephemeral=True)
        return
    prize = new_raffle_modal.raffle_prize.value
    new_raffle = raffle_processor.create_raffle(name, description, datetime.now().timestamp()+duration, winners_count, start_date=datetime.now().timestamp(), prize=prize)
    raffle_message = await interaction.followup.send(embed=new_raffle.to_embed(), view=ButtonForRaffle())
    print(f'Raffle id {new_raffle.id} created')
    # original_response = await interaction.original_response()
    new_raffle.set_message_id(raffle_message.id)
    new_raffle.set_channel_id(raffle_message.channel.id)
    save_data(raffle_processor.to_dict(), 'raffles.json')
    if not raffles_check_loop.is_running():
        raffles_check_loop.start()
    
# create command to delete raffle
@tree.command(name='delete_raffle', description='Delete a raffle without chosing a winner', guild=GUILD)
async def delete_raffle(interaction : discord.Interaction, raffle_id : int):
    if not check_role(interaction.user, 'delete_raffle', data):
        return
    raffle = raffle_processor.end_raffle_without_winner(raffle_id)
    if raffle is None:
        await interaction.response.send_message(content='Raffle not found', ephemeral=True)
        print('Raffle not found')
        return
    else:
        raffle_message = await bot.get_guild(GUILD_ID).get_channel(raffle.get_channel_id()).fetch_message(raffle.get_message_id())
        await raffle_message.delete()
        await interaction.response.send_message(content=f'Raffle with id {raffle_id} deleted', ephemeral=True)
        print(f'Raffle with id {raffle_id} deleted')
        save_data(raffle_processor.to_dict(), 'raffles.json')

# create command to reroll raffle
@tree.command(name='reroll_raffle', description='Reroll a raffle', guild=GUILD)
async def reroll_raffle(interaction : discord.Interaction, raffle_id : int):
    if not check_role(interaction.user, 'reroll_raffle', data):
        return
    raffle = raffle_processor.choose_winners_by_id(raffle_id)
    raffle_message = await bot.get_guild(GUILD_ID).get_channel(raffle.get_channel_id()).fetch_message(raffle.get_message_id())
    await raffle_message.edit(embed=raffle.to_embed(), view=None)
    winners_string = ''
    for winner in raffle.get_winners():
        winners_string += f'<@{winner}>\n'
    await raffle_message.reply(f'Raffle "{raffle.name}" rerolling is over!\n\nWinners:\n{winners_string}')
    await interaction.response.send_message('Rerolled', ephemeral=True)
    print(f'Rerolled id {raffle_id}')
    save_data(raffle_processor.to_dict(), 'raffles.json')

# create command to add allowed roles
@tree.command(name='add_allowed_role', description='Add a role to the allowed roles', guild=GUILD)
async def add_allowed_role(interaction : discord.Interaction, command_name : str, role : discord.Role):
    if not interaction.user.guild_permissions.administrator:
        return
    if 'allowed_roles' not in data:
        data['allowed_roles'] = {}
    if command_name not in data['allowed_roles']:
        data['allowed_roles'][command_name] = []
    data['allowed_roles'][command_name].append(role.id)
    await interaction.response.send_message(content=f'Added role {role.name} to allowed roles for command {command_name}', ephemeral=True)
    print(f'Added role {role.name} to allowed roles for command {command_name}')
    save_data(data, 'data.json')

# create command to remove allowed roles
@tree.command(name='remove_allowed_role', description='Remove a role from the allowed roles', guild=GUILD)
async def remove_allowed_role(interaction : discord.Interaction, command_name : str, role : discord.Role):
    if not interaction.user.guild_permissions.administrator:
        return
    if 'allowed_roles' not in data:
        data['allowed_roles'] = {}
    if command_name not in data['allowed_roles']:
        data['allowed_roles'][command_name] = []
    data['allowed_roles'][command_name].remove(role.id)
    await interaction.response.send_message(content=f'Removed role {role.name} from allowed roles for command {command_name}', ephemeral=True)
    print(f'Removed role {role.name} from allowed roles for command {command_name}')
    save_data(data, 'data.json')

# create command to add participants with random id to raffle
@tree.command(name='add_participants', description='Add a participants to the raffle', guild=GUILD)
async def add_participant(interaction : discord.Interaction, raffle_id : int, participant_amount : int = 1):
    if not check_role(interaction.user, 'add_participant', data):
        return
    raffle = raffle_processor.get_raffle_by_id(raffle_id)
    if raffle is None:
        await interaction.response.send_message(content='Raffle not found', ephemeral=True)
        return
    else:
        for i in range(participant_amount):
            raffle.add_participant(random.randint(1, 100000000))
        await interaction.response.send_message(content=f'{participant_amount} participant(-s) added to raffle with id {raffle_id}', ephemeral=True)
        save_data(raffle_processor.to_dict(), 'raffles.json')

# create command to create embed with community calls timetable
@tree.command(name='community_calls', description='Create embed with community calls timetable', guild=GUILD)
async def community_calls(interaction : discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return
    delete_message_id = data.get('community_calls_message_id')
    if delete_message_id is not None:
        try:
            delete_message = await interaction.guild.get_channel(data.get('community_calls_channel_id')).fetch_message(delete_message_id)
            await delete_message.delete()
        except discord.errors.NotFound:
            pass
    await interaction.response.send_message(content='Creating embed...', ephemeral=True)
    message = await interaction.channel.send('Creating embed...')
    data['community_calls_message_id'] = message.id
    data['community_calls_channel_id'] = interaction.channel.id
    save_data(data, 'data.json')
    community_calls_timetable_loop.restart()

@tasks.loop(minutes=10)
async def community_calls_timetable_loop():
    community_calls_timetable_message_id = data.get('community_calls_message_id')
    if community_calls_timetable_message_id is None:
        community_calls_timetable_loop.stop()
    try:
        message = await bot.get_guild(GUILD_ID).get_channel(data['community_calls_channel_id']).fetch_message(community_calls_timetable_message_id)
        await message.edit(embed=community_calls_timetable_embed(), content='')
        next_calls = calculate_next_calls_time()
        if next_calls is None:
            return
        # if scheduled event for next call is not created create it
        for call in next_calls.items():
            call_time = int(call[1][0].replace('<', '').replace('>', '').replace(':', '').replace('t', ''))
            if call_time < int(datetime.now().timestamp()):
                continue
            # if call time not in scheduled events create it
            print(call_time)
            print([int(x.start_time.timestamp()) for x in await bot.get_guild(GUILD_ID).fetch_scheduled_events(with_counts=False)])
            if call_time not in [int(x.start_time.timestamp()) for x in await bot.get_guild(GUILD_ID).fetch_scheduled_events(with_counts=False)]:
                start_time = datetime.fromtimestamp(call_time).astimezone()
                end_time = start_time + timedelta(hours=1)
                channel = bot.get_guild(GUILD_ID).get_channel(1009805503376916480)
                new_scheduled_event = await bot.get_guild(GUILD_ID).create_scheduled_event(
                    name=call[0], 
                    start_time=start_time,
                    end_time=end_time,
                    channel=channel,
                    privacy_level=discord.PrivacyLevel.guild_only,
                    reason='Automatically created community call'
                    )
    except discord.errors.NotFound:
        community_calls_timetable_loop.stop()
    except discord.errors.DiscordServerError:
        print('Discord Server Error')

@tasks.loop(seconds=5)
async def raffles_check_loop():
    if raffle_processor.ongoing_raffles_list == []:
        raffles_check_loop.stop()
        return
    for raffle in raffle_processor.ongoing_raffles_list:
        if raffle.is_over():
            raffle_processor.choose_winners(raffle)
        raffle_message = await bot.get_guild(GUILD_ID).get_channel(raffle.get_channel_id()).fetch_message(raffle.get_message_id())
        if raffle.is_over():
            await raffle_message.edit(embed=raffle.to_embed(), view=None)
            winners_string = ''
            for winner in raffle.get_winners():
                winners_string += f'<@{winner}>\n'
            await raffle_message.reply(f'*Raffle "{raffle.name}" is over!*\n\nWinners:\n{winners_string}')
        else:
            await raffle_message.edit(embed=raffle.to_embed(), view=ButtonForRaffle())
    save_data(raffle_processor.to_dict(), 'raffles.json')

bot.run(token)
save_data(data, 'data.json')
save_data(raffle_processor.to_dict(), 'raffles.json')