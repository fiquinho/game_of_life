from game import Engine


def main():
    """Runs the game in a pygame window with default configurations"""
    engine = Engine()
    engine.run_game(render=True)


if __name__ == '__main__':
    main()
