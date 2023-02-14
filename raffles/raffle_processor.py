from raffles import raffle
from datetime import datetime
class RaffleProcessor:

    def __init__(self, raffle_dict : dict = {}):
        if raffle_dict != {}:
            self.ongoing_raffles_list : list[raffle.Raffle] = [raffle.Raffle.from_dict(one_raffle) for one_raffle in raffle_dict['ongoing_raffles_list']]
            self.completed_raffles_list : list[raffle.Raffle] = [raffle.Raffle.from_dict(one_raffle) for one_raffle in raffle_dict['completed_raffles_list']]
            raffle.Raffle.current_id = raffle_dict['current_id']
        else:
            self.ongoing_raffles_list : list[raffle.Raffle] = []
            self.completed_raffles_list : list[raffle.Raffle] = []
            raffle.Raffle.current_id = 0
        
    def to_dict(self):
        return {
            'ongoing_raffles_list': [one_raffle.to_dict() for one_raffle in self.ongoing_raffles_list],
            'completed_raffles_list': [one_raffle.to_dict() for one_raffle in self.completed_raffles_list],
            'current_id' : raffle.Raffle.current_id
        }
    
    def create_raffle(self, raffle_name : str, raffle_description : str, end_date : int, raffle_winner_count : int, start_date : int = datetime.now().timestamp(), prize : str = ''):
        new_raffle = raffle.Raffle(raffle_name, raffle_description, start_date, end_date, raffle_winner_count, winners=[], participants=[], message_id=None, channel_id=None, prize=prize)
        self.ongoing_raffles_list.append(new_raffle)
        return new_raffle
    
    def get_raffle_by_id(self, raffle_id : int):
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.id == raffle_id:
                return one_raffle
        for one_raffle in self.completed_raffles_list:
            if one_raffle.id == raffle_id:
                return one_raffle
        return None
    
    def get_raffle_by_name(self, raffle_name : str):
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.name == raffle_name:
                return one_raffle
        for one_raffle in self.completed_raffles_list:
            if one_raffle.name == raffle_name:
                return one_raffle
        return None
    
    def get_raffle_by_message_id(self, message_id : int):
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.message_id == message_id:
                return one_raffle
        for one_raffle in self.completed_raffles_list:
            if one_raffle.message_id == message_id:
                return one_raffle
        return None
    
    def user_in_raffle(self, user_id : int, raffle : raffle.Raffle):
        return user_id in raffle.participants
    
    def get_ongoing_raffles(self):
        return self.ongoing_raffles_list
    
    def get_completed_raffles(self):
        return self.completed_raffles_list
    
    def choose_winners_by_id(self, raffle_id : int):
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.id == raffle_id:
                one_raffle.do_raffle()
                self.ongoing_raffles_list.remove(one_raffle)
                self.completed_raffles_list.append(one_raffle)
                return one_raffle
        for one_raffle in self.completed_raffles_list:
            if one_raffle.id == raffle_id:
                winners = one_raffle.get_winners()
                one_raffle.participants.extend(winners)
                one_raffle.winners = []
                one_raffle.do_raffle()
                return one_raffle
        return None
    
    def choose_winners(self, raffle : raffle.Raffle):
        raffle.do_raffle()
        self.ongoing_raffles_list.remove(raffle)
        self.completed_raffles_list.append(raffle)
        return raffle
    
    def end_raffle_without_winner(self, raffle_id : int):
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.id == raffle_id:
                self.ongoing_raffles_list.remove(one_raffle)
                self.completed_raffles_list.append(one_raffle)
                return one_raffle
        return None
    
    def finish_outdated_raffles(self):
        completed_raffles = []
        for one_raffle in self.ongoing_raffles_list:
            if one_raffle.end_date < datetime.now().timestamp():
                one_raffle.do_raffle()
                self.ongoing_raffles_list.remove(one_raffle)
                self.completed_raffles_list.append(one_raffle)
                completed_raffles.append(one_raffle)
        return completed_raffles
