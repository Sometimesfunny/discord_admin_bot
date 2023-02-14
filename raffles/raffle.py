from discord import Embed
import random
from datetime import datetime

def user_id_to_mention(user_id : int):
    return f'<@{user_id}>'

class Raffle:
    current_id = 0

    @staticmethod
    def get_new_id():
        Raffle.current_id += 1
        return Raffle.current_id

    @staticmethod
    def from_dict(data : dict):
        return Raffle(
            data['name'],
            data['description'],
            data['start_date'],
            data['end_date'],
            data['winner_count'],
            data['id'],
            data['winners'],
            data['participants'],
            data['message_id'],
            data['channel_id'],
            data.get('prize', '')
        )

    def __init__(self, name : str, description : str, start_date : int, end_date : int, winner_count : int, id : int = None, winners : list = [], participants : list = [], message_id : int = None, channel_id : int = None, prize : str = ''):
        if id is None:
            self.id : int = self.get_new_id()
        else:
            self.id = id
        self.name : str = name
        self.description : str = description
        self.start_date : int = start_date
        self.end_date : int = end_date
        self.winner_count : int = winner_count
        self.winners : list[int] = winners
        self.participants : list[int] = participants
        self.message_id : int = message_id
        self.channel_id : int = channel_id
        self.prize : str = prize

    def add_winner(self, winner):
        self.winners.append(winner)

    def get_winners(self):
        return self.winners

    def get_winner_count(self):
        return self.winner_count

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
    def add_participant(self, participant_id : int):
        self.participants.append(participant_id)
    
    def set_message_id(self, message_id : int):
        self.message_id = message_id
    
    def set_channel_id(self, channel_id : int):
        self.channel_id = channel_id
    
    def get_channel_id(self):
        return self.channel_id
    
    def get_message_id(self):
        return self.message_id
    
    def do_raffle(self):
        for i in range(min(self.winner_count, len(self.participants))):
            winner = self.participants.pop(random.randint(0, len(self.participants) - 1))
            self.add_winner(winner)
        return True
    
    def user_in_raffle(self, user_id : int):
        return user_id in self.participants
    
    def is_over(self):
        return self.end_date < datetime.now().timestamp()
    
    def to_embed(self):
        if len(self.winners) == 0:
            color = 0x0055e8
        else:
            color = 0xff0000
        embed = Embed(
            title=self.name, 
            description=self.description,
            color=color
            )
        embed.set_thumbnail(url='https://images.emojiterra.com/twitter/v14.0/512px/1f389.png')
        embed.add_field(name='Start Date', value=f'<t:{int(self.start_date)}:R>\n<t:{int(self.start_date)}:f>')
        embed.add_field(name='End Date', value=f'<t:{int(self.end_date)}:R>\n<t:{int(self.end_date)}:f>')
        embed.add_field(name='Winner Count', value=self.winner_count)
        embed.add_field(name='Prize', value=self.prize)
        embed.add_field(name='Participants', value=(len(self.participants)+len(self.winners)))
        if len(self.winners) > 0:
            for i in range(len(self.winners)//50+1):
                embed.add_field(name='Winners', value='\n'.join(user_id_to_mention(winner) for winner in self.winners[i*50:(i+1)*50]), inline=False)
        embed.set_footer(text=f'Raffle ID: {self.id}')
        return embed
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'winner_count': self.winner_count,
            'winners': self.winners,
            'participants': self.participants,
            'message_id': self.message_id,
            'channel_id': self.channel_id,
            'prize': self.prize
        }
    