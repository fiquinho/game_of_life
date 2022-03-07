from game import Engine


import pygame


def main():
    """Runs the game in a pygame window with default configurations"""
    pygame.init()

    engine = Engine()
    engine.run_game(render=True)

    pygame.quit()


if __name__ == '__main__':
    main()
