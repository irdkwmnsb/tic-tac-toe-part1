import uuid

class GameException(Exception):
    pass

class Player():
    """Класс игрока"""
    def __init__(self, name, password):
        """
        Инициализация игрока.
        :param name: имя игрока
        :param password: пароль игрока
        """
        self.name = name
        self.password = password
        self.score = 0
        self.is_active = True
        self.is_admin = False

    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'Player({self.name}, {self.score})'
    
    def check_password(self, password):
        """
        Проверка пароля игрока.
        :param password: пароль игрока
        :return: True если пароль верный, иначе False
        """
        return self.password == password


class Game():
    """Класс игры"""

    WINNING_ROWS = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def __init__(self):
        """Инициализация игры."""
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.game_over = False
        self.started = False
        self.id = str(uuid.uuid4())
        self.player_x = None
        self.player_o = None
        self.current_player = None
    
    def join(self, player: Player):
        """
        Присоединение игрока к игре.
        :param player: игрок
        """
        if self.player_x is None:
            self.player_x = player
        elif self.player_o is None:
            self.player_o = player
        else:
            raise GameException("Game is full")

    def start(self):
        """
        Начать игру.
        :raises:
            GameException: если игра уже начата или игроков меньше 2
        """
        if self.started:
            raise GameException("Game has already started")
        self.current_player = self.player_x
        self.started = True
        if self.player_x is None or self.player_o is None:
            raise GameException("Not enough players")

    def __repr__(self):
        return f"Game({self.id} - {self.player_x} vs {self.player_o})"
    
    def move(self, player: Player, x, y):
        """
        Сделать ход.
        :param player: игрок
        :param x: координата x
        :param y: координата y
        :raises:
            GameException: если игра не начата, ходит не тот игрок, или клетка занята
        """
        if self.game_over:
            raise GameException("Game is over")
        if not self.started:
            raise GameException("Game has not started")
        if x < 0 or x > 2 or y < 0 or y > 2:
            raise GameException("Invalid move - out of bounds")
        if self.board[x][y] is not None:
            raise GameException("Invalid move - position already taken")
        if player != self.current_player:
            raise GameException("Invalid move - not your turn")
        self.board[x][y] = player
        self.check_winner()
        self.current_player = self.player_o if self.current_player == self.player_x else self.player_x
    
    def check_winner(self):
        """Проверка на выигрыш"""
        for row in self.WINNING_ROWS:
            if all(self.board[x][y] == self.current_player for x, y in row):
                self.winner = self.current_player
                self.game_over = True
                self.current_player.score += 1
                return
        if all(self.board[x][y] is not None for x in range(3) for y in range(3)):
            self.game_over = True
    
    def to_dict(self):
        """Преобразование игры в словарь"""
        return {
            "id": self.id,
            "board": self.board,
            "game_over": self.game_over,
            "winner": self.winner,
            "started": self.started,
            "current_player": self.current_player.name if self.current_player else None,
        }



class GameManager():
    def __init__(self) -> None:
        self.games = {}
        self.players = {}
    
    def create_game(self) -> Game:
        """Создание игры"""
        game = Game()
        self.games[game.id] = game
        return game
    
    def _assert_game_exists(self, game_id):
        """
        Проверка существования игры
        :param game_id: идентификатор игры
        :raises:
            GameException: если игра не найдена
        """
        if game_id not in self.games:
            raise GameException("Game not found")

    def get_game(self, game_id) -> Game:
        """
        Получение игры по идентификатору
        :param game_id: идентификатор игры
        """
        self._assert_game_exists(game_id)
        return self.games[game_id]

    def delete_game(self, game_id):
        """
        Удаление игры
        :param game_id: идентификатор игры
        """
        self._assert_game_exists(game_id)
        del self.games[game_id]
    
    def get_games(self):
        """Получение списка игр"""
        return self.games.values()
    
    def create_player(self, name, password) -> Player:
        """
        Создание игрока
        :param name: имя игрока
        :param password: пароль игрока
        :raises:
            GameException: если игрок с таким именем уже существует
        """
        if name in self.players:
            raise GameException("Player already exists")
        player = Player(name, password)
        self.players[name] = player
        return player
    
    def get_player(self, name, password) -> Player:
        """
        Получение игрока по имени и паролю
        :param name: имя игрока
        :param password: пароль игрока
        :raises:
            GameException: если игрок не найден
        """
        if name not in self.players:
            raise GameException("Player not found")
        player = self.players[name]
        if not player.check_password(password):
            raise GameException("Player not found")
        return player
