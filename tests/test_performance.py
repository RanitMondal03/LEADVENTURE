import time
from unittest import result

from utils.goal_coach import GoalCoach

coach = GoalCoach()


def test_response_time():

    start = time.time()

    result: object  =  coach.make_goal("Improve sales")


    end = time.time()

    assert end - start < 10
    print(result)


    print(f"SRART TIME IS {start}    ------     END TIME IS  {end}")
    print(f"TOTAL TIME IS {end-start}")

