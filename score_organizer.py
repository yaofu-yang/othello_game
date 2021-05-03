# Creates an instance to sort score content


class ScoreOrganizer:
    """
    Updates the score file for the Othello game.

    Attributes
    ----------
    filename = str
        Name of score file to be updated.
    name = str
        Name of user
    score = int
        User's score at end-game

    Methods
    -------
    update_score
        Create or read from a score file for the Othello game. After adding in
        the name and score for the current round, updates file accordingly.
    add_scores
        Given a list of string (contents), store each string within a list of
        tuples (score_list). Returns a list of tuples.
    """
    def __init__(self, name, score, filename):
        """
        Parameters
        ----------
        name : str
            The player's name.
        score : int
            The player's score this round.
        filename : str
            The name of the score file.
        ----------
        """
        self.filename = filename
        self.name = name.lower().capitalize()
        self.score = score

    def update_score(self):
        """
        Create or read from a score file for the Othello game. After adding in
        the name and score for the current round, updates file accordingly.
        """
        try:
            with open(self.filename, "r+") as f:
                contents = f.readlines()
        except:
            with open(self.filename, "w") as fn:
                fn.write("" + self.name + " " + str(self.score) + "\n")
                return

        # Store scores in dictionary for sorting.
        score_list = []
        separator = contents[0].rfind(' ')
        top_score = contents[0][separator + 1:]
        if self.score > int(top_score):
            score_list.append((self.name, self.score))
            score_list = self.add_scores(score_list, contents)
        else:
            score_list = self.add_scores(score_list, contents)
            score_list.append((self.name, self.score))

        # Writing scores back to the text file.
        new_scores = ""
        for scores in score_list:
            new_scores += scores[0] + " " + str(scores[1]) + "\n"
        with open(self.filename, "w") as fn:
            fn.write(new_scores)

    def add_scores(self, score_list, contents):
        """
        Given a list of string (contents), store each string within a list of
        tuples (score_list). Returns a list of tuples.
        """
        for line in contents:
            separator = line.rfind(' ')
            name, score = line[: separator], line[separator + 1:]
            score_list.append((name, int(score)))
        return score_list
