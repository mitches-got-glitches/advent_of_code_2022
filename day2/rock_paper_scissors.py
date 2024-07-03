from enum import IntEnum

from aoc_helpers import get_input_path


class ScoreEnum(IntEnum):
    @property
    def score(self):
        return self.value


class HandShape(ScoreEnum):
    """The points for each hand shape in the game."""

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class GameResult(ScoreEnum):
    """The points for each game result."""

    L = 0
    D = 3
    W = 6


RPS_MAPPER: dict[str, HandShape] = {
    "A": HandShape.ROCK,
    "B": HandShape.PAPER,
    "C": HandShape.SCISSORS,
    "X": HandShape.ROCK,
    "Y": HandShape.PAPER,
    "Z": HandShape.SCISSORS,
}


if __name__ == "__main__":
    with open(get_input_path()) as f:
        games: list[str] = [line.strip() for line in f]

    ## Challenge: Part 1
    p1_score, p2_score = 0, 0

    for game in games:
        p1: HandShape
        p2: HandShape
        p1, p2 = map(RPS_MAPPER.get, game.split(" "))
        if (
            (p1 == HandShape.ROCK and p2 == HandShape.SCISSORS)
            or (p1 == HandShape.PAPER and p2 == HandShape.ROCK)
            or (p1 == HandShape.SCISSORS and p2 == HandShape.PAPER)
        ):
            p1_score += GameResult["W"].score + p1.score
            p2_score += GameResult["L"].score + p2.score
        elif p1.name == p2.name:
            p1_score += GameResult["D"].score + p1.score
            p2_score += GameResult["D"].score + p2.score
        else:
            p1_score += GameResult["L"].score + p1.score
            p2_score += GameResult["W"].score + p2.score

    print(f"Opponent score: {p1_score}")
    print(f"My score: {p2_score}")

    RESULT_MAPPER: dict[str, GameResult] = {
        "X": GameResult["L"],
        "Y": GameResult["D"],
        "Z": GameResult["W"],
    }

    ## Challenge: Part 2
    p1_score, p2_score = 0, 0

    def get_winning_play(shape: HandShape):
        if shape == HandShape.ROCK:
            return HandShape.PAPER

    for game in games:
        char1, char2 = game.split(" ")
        p1: HandShape = RPS_MAPPER.get(char1)
        result: GameResult = RESULT_MAPPER.get(char2)

        if result == GameResult["W"]:
            if p1 == HandShape.ROCK:
                p2 = HandShape.PAPER
            elif p1 == HandShape.PAPER:
                p2 = HandShape.SCISSORS
            else:
                p2 = HandShape.ROCK

            p1_score += GameResult["L"].score + p1.score
            p2_score += result.score + p2.score

        elif result == GameResult["D"]:
            p2 = p1
            p1_score += result.score + p1.score
            p2_score += result.score + p2.score

        else:
            if p1 == HandShape.ROCK:
                p2 = HandShape.SCISSORS
            elif p1 == HandShape.PAPER:
                p2 = HandShape.ROCK
            else:
                p2 = HandShape.PAPER

            p1_score += GameResult["W"].score + p1.score
            p2_score += GameResult["L"].score + p2.score

    print(f"Opponent score: {p1_score}")
    print(f"My score: {p2_score}")
