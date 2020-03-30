class SimpleCribbageJudger(object):

    @staticmethod
    def judge_winner(players):
        ''' Judge the winner of the game

        Args:
            players (list): The list of players who play the game

        Returns:
            (list): The player id of the winner
        '''
        if players[1].score > 0:
            return [1]
        else:
            return [0]
