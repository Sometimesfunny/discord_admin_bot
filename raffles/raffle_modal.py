from discord.ui import Modal, TextInput
from discord import TextStyle, Interaction

class CreateRaffleModal(Modal, title='New Raffle'):
    def __init__(self):
        super().__init__(timeout=600)
    
    raffle_name = TextInput(
        label='Raffle Name',
        placeholder='Input Raffle Name Here',
        style=TextStyle.short,
        required=True
    )

    raffle_description = TextInput(
        label='Raffle Description',
        placeholder='Description',
        style=TextStyle.long,
        required=False,
        default=''
    )

    raffle_prize = TextInput(
        label='Raffle Prize',
        placeholder='Prize',
        style=TextStyle.long,
        required=True
    )

    raffle_duration = TextInput(
        label='Raffle Duration (hh:mm:ss)',
        placeholder='hh:mm:ss',
        style=TextStyle.short,
        required=True
    )

    raffle_winner_count = TextInput(
        label='Raffle Winner Count (>1)',
        placeholder='1',
        style=TextStyle.short,
        required=True,
        default='1'
    )

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.send_message('Raffle Created!', ephemeral=True)
