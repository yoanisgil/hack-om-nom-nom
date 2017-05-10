import random

class randomAi:
    def __init__(self):
        pass

    def init(self):
        pass
    
    def play(self, state):
        return random.randrange(6)

    def wasPlayed(self):
        pass

    def roundEnded(self):
        pass


def test():
    ai = randomAi()
    print ai.play(None)
    print ai.play(None)

if __name__ == "__main__":
    test()
