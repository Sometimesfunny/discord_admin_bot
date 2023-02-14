import discord
import random

selector_pool = [
    {
        'option' : discord.SelectOption(label='CAT', value='cat', emoji='🐈'),
        'value' : 'cat',
        'label' : 'Option 1',
        'emoji' : '🐈'
    },
    {
        'option' : discord.SelectOption(label='DOG', value='dog', emoji='🐕'),
        'value' : 'dog',
        'label' : 'Option 2',
        'emoji' : '🐕'
    },
    {
        'option' : discord.SelectOption(label='TURTLE', value='turtle', emoji='🐢'),
        'value' : 'turtle',
        'label' : 'Option 3',
        'emoji' : '🐢'
    },
    {
        'option' : discord.SelectOption(label='BIRD', value='bird', emoji='🐦'),
        'value' : 'bird',
        'label' : 'Option 4',
        'emoji' : '🐦'
    },
    {
        'option' : discord.SelectOption(label='FISH', value='fish', emoji='🐟'),
        'value' : 'fish',
        'label' : 'Option 5',
        'emoji' : '🐟'
    },
    {
        'option' : discord.SelectOption(label='FOX', value='fox', emoji='🦊'),
        'value' : 'fox',
        'label' : 'Option 6',
        'emoji' : '🦊'
    },
    {
        'option' : discord.SelectOption(label='BEAR', value='bear', emoji='🐻'),
        'value' : 'bear',
        'label' : 'Option 7',
        'emoji' : '🐻'
    },
    {
        'option' : discord.SelectOption(label='PANDA', value='panda', emoji='🐼'),
        'value' : 'panda',
        'label' : 'Option 8',
        'emoji' : '🐼'
    },
]

pictures = {
                'cat': [
                    'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/617278/pexels-photo-617278.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'dog': [
                    'https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1851164/pexels-photo-1851164.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/58997/pexels-photo-58997.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1254140/pexels-photo-1254140.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/220938/pexels-photo-220938.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'turtle': [
                    'https://images.pexels.com/photos/1618606/pexels-photo-1618606.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/847393/pexels-photo-847393.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/162307/giant-tortoise-reptile-shell-walking-162307.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/10467/pexels-photo-10467.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/2397653/pexels-photo-2397653.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'bird': [
                    'https://images.pexels.com/photos/73825/osprey-adler-bird-of-prey-raptor-73825.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/2662434/pexels-photo-2662434.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/75973/pexels-photo-75973.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/45851/bird-blue-cristata-cyanocitta-45851.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/2629372/pexels-photo-2629372.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'fish': [
                    'https://images.pexels.com/photos/128756/pexels-photo-128756.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/45910/goldfish-carassius-fish-golden-45910.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1145274/pexels-photo-1145274.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/40021/fish-aquarium-speed-scale-40021.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/2053815/pexels-photo-2053815.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'fox': [
                    'https://images.pexels.com/photos/247399/pexels-photo-247399.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/134058/pexels-photo-134058.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/2121799/pexels-photo-2121799.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/271932/pexels-photo-271932.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/162291/fuchs-wild-animal-predator-animal-world-162291.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'bear': [
                    'https://images.pexels.com/photos/158109/kodiak-brown-bear-adult-portrait-wildlife-158109.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/35435/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1068554/pexels-photo-1068554.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/162340/bear-bavarian-bear-wild-brown-bear-162340.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/1466592/pexels-photo-1466592.jpeg?auto=compress&cs=tinysrgb&w=800'
                ],
                'panda': [
                    'https://images.pexels.com/photos/3608263/pexels-photo-3608263.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/7506265/pexels-photo-7506265.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/4062907/pexels-photo-4062907.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/11909034/pexels-photo-11909034.jpeg?auto=compress&cs=tinysrgb&w=800',
                    'https://images.pexels.com/photos/7619819/pexels-photo-7619819.jpeg?auto=compress&cs=tinysrgb&w=800'
                ]
            }

all_names = list(pictures.keys())

class NewCaptcha():

    def __init__(self):
        pool = selector_pool.copy()
        answer = random.choice(pool)
        pool.remove(answer)
        self.right_answer = answer['value']
        self.options = []
        for i in range(3):
            self.options.append(pool.pop(random.randint(0, len(pool) - 1))['option'])
        self.options.append(answer['option'])
        random.shuffle(self.options)
        self.view = self.get_new_selector_view()
        self.picture_url = self.get_picture_url()
        self.is_right = False
    
    def get_new_selector_view(self):
        view = discord.ui.View(timeout=30)
        select = discord.ui.Select(
            placeholder='Select an animal',
            options=self.options
        )

        async def on_selection(interaction : discord.Interaction):
            if self.right_answer == select.values[0]:
                await interaction.response.edit_message(content="You're right!", view=None, embed=None)
                self.is_right = True
            else:
                await interaction.response.edit_message(content="You're wrong! Try again!", view=None, embed=None)
            view.stop()

        select.callback = on_selection
        view.add_item(select)
        return view
    
    def get_picture_url(self):
        return pictures[self.right_answer][random.randint(0, len(pictures[self.right_answer])-1)]