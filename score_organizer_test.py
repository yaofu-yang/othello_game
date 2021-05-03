# Test the score_organizer function.
from score_organizer import ScoreOrganizer


def test_constructor():
    """Test the constructor"""
    scorg = ScoreOrganizer("andy", 30, "test_scores.txt")
    assert scorg.filename == "test_scores.txt"
    assert scorg.name == "Andy"
    assert scorg.score == 30


def test_update_score():
    """Test the update_score method when the file does not exist."""
    scorg = ScoreOrganizer("happy", 10, "test_scores.txt")
    scorg2 = ScoreOrganizer("lucky go", 30, "test_scores.txt")
    scorg3 = ScoreOrganizer("kimi", 32, "test_scores.txt")
    scorg.update_score()
    scorg2.update_score()
    scorg3.update_score()

    with open("test_scores.txt", "r") as fn:
        contents = fn.readlines()
        player1, sep1 = contents[0], contents[0].rfind(' ')
        p1_name, p1_score = player1[: sep1], player1[sep1 + 1:].rstrip()

        player2, sep2 = contents[1], contents[1].rfind(' ')
        p2_name, p2_score = player2[: sep2], player2[sep2 + 1:].rstrip()

        player3, sep3 = contents[2], contents[2].rfind(' ')
        p3_name, p3_score = player3[: sep3], player3[sep3 + 1:].rstrip()

        assert (p1_name, p1_score) == ("Kimi", "32")
        assert (p2_name, p2_score) == ("Lucky go", "30")
        assert (p3_name, p3_score) == ("Happy", "10")


def test_add_scores():
    """Test the add_scores method."""
    scorg = ScoreOrganizer("happy", 10, "test_scores2.txt")
    contents = ["Kimi 32", "Happy 10", "Lucky 30"]
    new_contents = scorg.add_scores([], contents)
    assert new_contents == [("Kimi", 32), ("Happy", 10), ("Lucky", 30)]
