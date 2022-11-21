from manager import GameManager, Game, Player, GameException
from flask import Flask, jsonify

manager = GameManager()
app = Flask(__name__)

@app.errorhandler(GameException)
def handle_game_exception(error: GameException):
    response = jsonify(error.args[0])
    response.status_code = 400
    return response

# Ваша задача реализовать API которое позволит игрокам играть в крестики-нолики.

# Класс Game имеет метод to_dict который возвращает словарь с информацией о текущем состоянии игры.

# Вам необходимо реализовать следующие методы:
# POST /register - регистрация игрока
# Пример запроса:
# {
#     "name": "player1",
#     "password": "123"
# }
# GET /games - возвращает список всех игр
# Пример ответа:
# [
#     {
#         "id": "e3b0c442-98fc-11e8-8eb2-f2801f1b9fd1",
#         "player_x": "player1",
#         "player_o": "player2",
#         "winner": "player1",
#         "game_over": true,
#         "started": true,
#         "board": [
#             ["X", "O", "X"],
#             ["O", "X", "O"],
#             ["X", "O", "X"]
#         ]
#     },
#     {
#         "id": "e3b0c442-98fc-11e8-8eb2-f2801f1b9fd2",
#         "player_x": "player3",
#         "player_o": null,
#         "winner": null,
#         "game_over": false,
#         "started": false,
#         "board": [
#             [null, null, null],
#             [null, null, null],
#             [null, null, null]
#         ]
#     }
# ]

@app.route("/games", methods=["GET"])
def get_games():
    return jsonify([game.to_dict() for game in manager.get_games()])

# PUT /game - создает новую игру и возвращает ее id
# Пример ответа:
# {
#     "id": "e3b0c442-98fc-11e8-8eb2-f2801f1b9fd1"
# }

# GET /game/<id> - возвращает информацию о игре
# Пример ответа:
# {
#     "id": "e3b0c442-98fc-11e8-8eb2-f2801f1b9fd1",
#     "player_x": "player1",
#     "player_o": "player2",
#     "winner": "player1",
#     "game_over": true,
#     "started": true,
#     "board": [
#         ["X", "O", "X"],
#         ["O", "X", "O"],
#         ["X", "O", "X"]
#     ]
# }

# PUT /game/<id>/join - присоединяет игрока к игре
# В теле запроса необходимо передать имя и пароль игрока
# Пример запроса:
# {
#     "name": "player1",
#     "password": "123",
# }
# Возвращает информацию о игре
# Пример ответа:
# {
#     "id": "e3b0c442-98fc-11e8-8eb2-f2801f1b9fd1",
#     "player_x": "player1",
#     "player_o": null,
#     "winner": "player1",
#     "game_over": false,
#     "started": false,
#     "board": [
#         [null, null, null],
#         [null, null, null],
#         [null, null, null]
#     ]
# }
# PUT /game/<id>/start - начинает игру
# POST /game/<id>/start - начинает игру
# В теле запроса необходимо передать имя и пароль игрока. 
# Начать игру может только игрок X
# Пример запроса:
# {
#     "name": "player1",
#     "password": "123",
# }
# Возвращает информацию о игре
# POST /game/<id>/move - делает ход
# В теле запроса необходимо передать имя и пароль игрока, а также координаты хода
# Пример запроса:
# {
#     "name": "player1",
#     "password": "123",
#     "x": 0,
#     "y": 0
# }
# Возвращает информацию о игре

# Все методы, кроме /register и /games, должны возвращать 401, если имя или пароль игрока не верны




if __name__ == '__main__':
    app.run(debug=True, port=8000)