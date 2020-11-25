
"""
@ Author Hyun Kim, shi5857@dgist.ac.kr
@ Date 04 / 11 / 20
@ Environment Python 3.6.10
"""
import numpy as np
import copy
import random
#from . import ReversiGame

class Predictor:
    class Node:
        def __init__(self, player, loc, game, score, reverse):
            self.player = player
            self.loc = loc
            self.game = game
            self.score = score
            self.final_score = score
            self.reverse = reverse
            self.childs = []
            
        def _freedom(
            game,
            player: int
            ) -> int:

            return len(game.GetPossiblePositions(player))

        def _opposite(
            player: int
            ) -> int: #return opposite player no.

            if player == 1:
                return 2
            elif player == 2:
                return 1
            else:
            #Damn something wrong
            #IDK what to do
                return random.randrange(1, 3)
        def _apply(
            game,
            loc,
            player: int = -1
            ) : #
    
            if player is -1:
                player = game.gamestate

            try:
                game.PlacePiece(player, loc)
            except:
                #print("APply DaMGAE")
                return None
            return game
        
        def _score(
            value: int,
            freedom: int,
            anti_freedom: int
            ) -> float:
            return value + freedom - anti_freedom
            
        def score_propagate(self):
            if len(self.childs) == 0:
                return self.score
            else:
                for i in self.childs:
                    i.score_propagate()

                self.final_score = self.score - max(self.childs, key = lambda i : i.final_score).final_score
                return self.final_score

        def predict_propagate(self):
            if len(self.childs) == 0:
                self._predict()

                #if self.reverse:
                    #self.predict_propagate()
            else:
                for i in self.childs:
                    i.predict_propagate()

        def _predict(self):
            player = self.player if not self.reverse else Predictor.Node._opposite(self.player)
            choices = self.game.GetPossiblePositions(player)
            values = [self.game.GetReversiblePiecesCount(player, loc) for loc in choices]
            results = [Predictor.Node._apply(copy.deepcopy(self.game), loc, player) for loc in choices]
            freedoms = [Predictor.Node._freedom(game, player) for game in results]
            anti_freedoms = [Predictor.Node._freedom(game, Predictor.Node._opposite(player)) for game in results]

            nones = []
            for i , g in enumerate(results):
                if g is None:
                    nones.append(i)

            for i in sorted(nones, reverse=True):
                choices.pop(i)
                values.pop(i)
                results.pop(i)
                freedoms.pop(i)
                anti_freedoms.pop(i)

            scores = [Predictor.Node._score(values[i], freedoms[i], anti_freedoms[i]) for i in range(len(choices))]
            self.childs = [Predictor.Node(self.player, c,r,s, not self.reverse) for c,r,s in zip(choices, results, scores)]
            return self.childs

        def get_max(self):
            return max(self.childs, key = lambda x : x.final_score)
    
    def __init__(
        self
        ): #It require game argument?
        self.depth = 1

    def Initialize(
        self,
        game,
        player: int
        ) -> None:
        
        self.player = player
        #self.depth = depth if depth > 0 else 1
        

    def Finish(
        self,
        game,
        player: int
        ) -> None:

        pass
        
    def NextMove(
        self,
        game,
        player: int
        ) -> tuple:

        current = self.Node(player, None, game, 0, False)
        for i in range(self.depth):
            current.predict_propagate()
        current.score_propagate()
            
        return current.get_max().loc
    
