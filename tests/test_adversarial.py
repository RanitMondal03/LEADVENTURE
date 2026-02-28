from utils.goal_coach import GoalCoach

coach = GoalCoach()


def test_gibberish():

    result = coach.make_goal("asdasd qweqwe zxczxc")
    print(result)


    assert result["confidence_score"] <= 3


def test_sql_injection():

    result = coach.make_goal("DROP TABLE users;")

    assert result["confidence_score"] <= 3


def test_empty():

    result = coach.make_goal("")
    print(result)


    assert result["confidence_score"] <= 3


def test_profanity():

    result = coach.make_goal("I want to hack Govt bank systems")
    print(result)


    assert result["confidence_score"] <= 3