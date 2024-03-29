import asyncio
import dataset
import discord

DATABASE = dataset.connect('sqlite:///data/bot/higgsbot.db')

class Token:
    def __init__(self):
        self.table = DATABASE['balance']
    
    async def start(self, bot):
        for member in bot.get_all_members():
            id = member.id
            if self.table.find_one(user=id) is None:
                self.table.insert(dict(user=id, coins=3))    

    def check_balance(self, usr):
        id = usr.id
        if self.table.find_one(user=id) is not None:
            user = self.table.find_one(user=id)
            return user['coins']
        else:
            self.table.insert(dict(user=id, coins=3))
            return 3
    
    def set_balance(self, usr, b):
        if b >= 0:
            id = usr.id
            if self.table.find_one(user=id) is not None:
                self.table.update(dict(user=id, coins=b), ['user'])
                return
            else:
                self.table.insert(dict(user=id, coins=b))
                return
        else:
            raise Exception("Balance cannot be less than 0") 
    
    def remove_balance(self, usr, c):
        id = usr.id
        if self.table.find_one(user=id) is not None:
            user = self.table.find_one(user=id)
            if (user['coins'] - c) >= 0:
                new_coins = user['coins'] - c
                self.table.update(dict(user=id, coins=new_coins), ['user'])
                return
            else:
                raise Exception("Balance insufficient") 
        else:
            self.table.insert(dict(user=id, coins=c))
            user = self.table.find_one(user=id)
            if (user['coins'] - c) >= 0:
                new_coins = user['coins'] - c
                self.table.update(dict(user=id, coins=new_coins), ['user'])
                return
            else:
                raise Exception("Balance insufficient")

    def join(self, usr): # On joining of user add him to the table if he's not already there.
        id = usr.id
        if self.table.find_one(user=id) is None:
                self.table.insert(dict(user=id, coins=3))    

    async def payment(self):
        while True: # 10 minute loop to add CodeTokens.
            await asyncio.sleep(600)
            for user in self.table:
                if user['coins'] < 10:
                    user['coins'] = user['coins'] + 1
                    self.table.update(dict(user=user['user'], coins=user['coins']), ['user'])