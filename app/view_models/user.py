class UserViewModel:
    def __init__(self, user):
        self.nickname = user.nickname
        self.coins = user.coins
        self.email = user.email
        self.send_receive = '{}/{}'.format(user.send_count, user.receive_count)