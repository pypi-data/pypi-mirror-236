"""This module contains a tic tac toe environment that can be used for
reference purposes.
"""
from copy import deepcopy

import numpy as np
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import Box, Discrete
from palaestrai.types.multi_binary import MultiBinary
from palaestrai.types.simtime import SimTime
from palaestrai.util import seeding
from typing import List

from . import LOG


class TicTacToeEnvironment(Environment):
    """The tic tac toe environment.

    The goal is to place symbols on the board and form a three symbol
    row of the own symbol.

    There are three possible states per tile:

        [0,0] = unassigned
        [1,0] = assigned to player 1 (the environment)
        [0,1] = assigned to player 2 (the agent)

    """

    def __init__(
        self,
        uid,
        broker_uri,
        seed,
        randomness: float = 0.5,
        invalid_turn_limit: int = 5,
    ):
        super().__init__(uid, broker_uri, seed)
        self.rng = seeding.np_random(seed)[0]
        self.randomness: float = randomness
        self.invalid_turn_limit: int = invalid_turn_limit
        self.board: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.reward_space: Box = Box(-100, 10, (1,))
        self.invalid_turn_counter: int = 0
        self.turn_counter: int = 0

        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) Parameter loaded: randomness=%f, invalid_turn_limit=%x",
            self.__class__,
            id(self),
            self.uid,
            self.randomness,
            self.invalid_turn_limit,
        )

    def start_environment(self):
        """Start the tic tac toe environment.

        The function sets up the sensors and the actuator used by the
        agent to make turns.

        """
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.turn_counter: int = 0
        self.sensors = [
            SensorInformation([0, 0], MultiBinary(2), "Tile 1-1"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 1-2"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 1-3"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 2-1"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 2-2"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 2-3"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 3-1"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 3-2"),
            SensorInformation([0, 0], MultiBinary(2), "Tile 3-3"),
        ]
        self.actuators = [
            ActuatorInformation(0, Discrete(len(self.board)), "Field selector")
        ]
        if np.random.uniform(0, 1) > 0.5:
            # optimal tic tac toe algorithm starts
            self.board[self._compute_oponent_turn(self.board)] = 1
            self._map_board_to_sensors()

        return EnvironmentBaseline(
            sensors_available=self.sensors,
            actuators_available=self.actuators,
            simtime=SimTime(self.turn_counter, None),
        )

    def update(self, actuators):
        """Creates new sensor information

        This method creates new sensor readings. The actuator value
        marks the desired tile of the agent player. Only one actuator
        is allowed.

        Parameters
        ----------
        actuators : List[ActuatorInformation]
            List of actuators, in this case only one actuator is
            allowed.

        Returns
        -------
        Tuple[List[SensorInformation], List[RewardInformation], bool]
            Tuple of List of SensorInformation with new values, reward(s)
            and a flag that sigals if the current state is a terminal
            state.

        """
        assert len(actuators) == 1, "Can only handle 1 actuator"
        actuator = actuators[0]
        self.turn_counter += 1

        # terminate environment if self.invalid_turn_limit is reached
        if self.invalid_turn_counter >= self.invalid_turn_limit:
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Agent made too many invalid turns! Environment terminates now!",
                self.__class__,
                id(self),
                self.uid,
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        -100, self.reward_space, "Tic-Tac-Toe-Reward"
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # Agent makes invalid turn
        # high penalty, no change in the env. The agent can try again until self.invalid_turn_limit
        # is reached
        if not (self._is_valid_move(self.board, actuator.value)):
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Agent made invalid turn: %x",
                self.__class__,
                id(self),
                self.uid,
                actuator.value,
            )
            self.invalid_turn_counter = self.invalid_turn_counter + 1
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        -100, self.reward_space, "Tic-Tac-Toe-Reward"
                    )
                ],
                done=False,
                simtime=SimTime(self.turn_counter, None),
            )

        else:
            self.invalid_turn_counter = 0

        # execute turn of agent
        self.board[actuator.value] = -1
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) Board after agent's turn: %s",
            self.__class__,
            id(self),
            self.uid,
            str(self.board),
        )
        self._map_board_to_sensors()

        # check if the agent won
        if self._has_player_won(self.board, -1):
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        10, self.reward_space, "Tic-Tac-Toe-Reward"
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # check if the game is a draw because of agent move
        if self._is_draw(self.board):
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[RewardInformation(0, self.reward_space, "Reward")],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # turn of algorithm within environment
        # in order to spice things up, the algorithm can make random,
        # not optimal turns with a specified probability
        if np.random.uniform(0, 1) > self.randomness:
            # optimal tic tac toe algorithm makes turn
            self.board[self._compute_oponent_turn(self.board)] = 1
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Board after environments "
                "optimal turn: %s",
                self.__class__,
                id(self),
                self.uid,
                str(self.board),
            )
        else:
            # random turn
            # sampling from actuator space is currently not possible
            # -> gives same "random" number all the time
            # within one experiment run
            random_move = np.random.randint(0, 9)
            while not self._is_valid_move(self.board, random_move):
                random_move = np.random.randint(0, 9)
            self.board[random_move] = 1
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Board after environments "
                "random turn: %s.",
                self.__class__,
                id(self),
                self.uid,
                str(self.board),
            )

        self._map_board_to_sensors()

        # check if algorithm won
        if self._has_player_won(self.board, 1):
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        -10, self.reward_space, "Tic-Tac-Toe-Reward"
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # check if the game is a draw because of algorithm move
        if self._is_draw(self.board):
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        0, self.reward_space, "Tic-Tac-Toe-Reward"
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )
        return EnvironmentState(
            sensor_information=self.sensors,
            rewards=[
                RewardInformation(1, self.reward_space, "Tic-Tac-Toe-Reward")
            ],
            done=False,
            simtime=SimTime(self.turn_counter, None),
        )

    def _has_player_won(self, board, player):
        if self._is_game_won(board, player):
            if player == 1:
                LOG.info(
                    "Environment %s(id=0x%x, uid=%s) Game ended: "
                    "Environment won!",
                    self.__class__,
                    id(self),
                    self.uid,
                )
            else:
                LOG.info(
                    "Environment %s(id=0x%x, uid=%s) Game ended: "
                    "Agent won!",
                    self.__class__,
                    id(self),
                    self.uid,
                )
            return True
        else:
            return False

    def _is_draw(self, board):
        if self._is_board_full(self.board):
            LOG.info(
                "Environment %s(id=0x%x, uid=%s) Game ended: Draw!",
                self.__class__,
                id(self),
                self.uid,
            )
            return True
        else:
            return False

    def _is_board_full(self, board):
        for tile in board:
            if tile == 0:
                return False
        return True

    def _is_valid_move(self, board, tile_index):
        return board[tile_index] == 0

    def _switch_players(self, player):
        return player * -1

    def _is_game_won(self, board, player):
        # horizontal lines
        if board[0] == player and board[1] == player and board[2] == player:
            return True
        elif board[3] == player and board[4] == player and board[5] == player:
            return True
        elif board[6] == player and board[7] == player and board[8] == player:
            return True

        # vertical lines
        elif board[0] == player and board[3] == player and board[6] == player:
            return True
        elif board[1] == player and board[4] == player and board[7] == player:
            return True
        elif board[2] == player and board[5] == player and board[8] == player:
            return True

        # diagonal lines
        elif board[0] == player and board[4] == player and board[8] == player:
            return True
        elif board[2] == player and board[4] == player and board[6] == player:
            return True
        else:
            return False

    def _map_board_to_sensors(self):
        for i in range(len(self.board)):
            # sensor range is 0...2, but the agent player is marked
            # as -1 internally
            if self.board[i] == -1:
                self.sensors[i].value = [0, 1]
            elif self.board[i] == 0:
                self.sensors[i].value = [0, 0]
            else:
                self.sensors[i].value = [1, 0]

    def _compute_oponent_turn(self, board):
        best_score = -123
        best_move = None
        for move in range(len(board)):
            if self._is_valid_move(board, move):
                board_copy = deepcopy(board)
                board_copy[move] = 1
                score = self._minimax(board_copy, self._switch_players(1))
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move

    def _print_board(self, board):
        print("-----------")
        print(str(board[0]) + str(board[1]) + str(board[2]))
        print(str(board[3]) + str(board[4]) + str(board[5]))
        print(str(board[6]) + str(board[7]) + str(board[8]))
        print("-----------")

    def _minimax(self, board, player):
        if self._is_board_full(board):
            return 0
        # check if previous turn was a winning turn (for the other player)
        if self._is_game_won(board, self._switch_players(player)):
            return self._switch_players(player)
        scores = []
        for move in range(len(board)):
            if self._is_valid_move(board, move):
                board_copy = deepcopy(board)
                board_copy[move] = player
                score = self._minimax(board_copy, self._switch_players(player))
                scores.append(score)
        # maximize from the perspective of the current player
        if player == -1:
            return min(scores)
        else:
            return max(scores)
