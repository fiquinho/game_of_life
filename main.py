from game import Engine, GameConfig


def main():
    board_width = 40
    board_height = 30
    cell_side = 20
    fps = 60

    game_config = GameConfig(board_width=board_width, board_height=board_height,
                             cell_side=cell_side, fps=fps)

    engine = Engine(game_config=game_config)

    engine.run_game(render=True)


if __name__ == '__main__':
    main()
