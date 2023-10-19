from random import randint


def get_expo_jitter(
    base: int,
    attempts: int = 0,
    cap: int = 100_000_000,
    jitter: bool = True,
    jitter_min: int = 1,
):
    """
    Returns a backoff value https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

    :param base: The time to sleep in the first attempt.
    :param attempts: The number of attempts that have already been made.
    :param cap: The maximum value that can be returned.
    :param jitter: Whether or not to apply jitter to the returned value.
    :param jitter_min: The minimum value that can be returned if jitter is applied.
    """
    # Full jitter formula
    # https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    if jitter:
        return randint(jitter_min, min(cap, base * 2**attempts))
    else:
        return min(cap, base * 2**attempts)
