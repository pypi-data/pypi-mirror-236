
import re

from cioseq.sequence import Sequence

AUTO_RX = re.compile(r"^auto[, :]+(\d+)$")
FML_RX = re.compile(r"^fml[, :]+(\d+)$")


def main_frame_sequence(**kwargs):
    """
    Generate a Sequence containing the current chosen frames.

    This function generates a sequence of frames based on the provided frame specification and chunk size.

    :param kwargs: A dictionary of keyword arguments that may include 'frame_spec' and 'chunk_size'.
    :return: A Sequence containing the chosen frames.
    """
    chunk_size = kwargs.get("chunk_size")
    spec = kwargs.get("frame_spec")
    if not spec:
        return Sequence.create(1, 1)
    else:
        return Sequence.create(spec, chunk_size=chunk_size, chunk_strategy="progressions")


def scout_frame_sequence(main_sequence, **kwargs):
    """
    Generate a Sequence containing scout frames.

    This function generates a sequence of scout frames, which can be generated from a specified pattern
    or by subsampling the main frame sequence.

    :param main_sequence: The main frame sequence.
    :param kwargs: A dictionary of keyword arguments that may include 'scout_frames' and 'use_scout_frames'.
    :return: A Sequence containing the scout frames or None.
    """
    if not kwargs.get("use_scout_frames"):
        return

    scout_spec = kwargs.get("scout_frames")

    match = AUTO_RX.match(scout_spec)
    if match:
        samples = int(match.group(1))
        return main_sequence.subsample(samples)
    else:
        match = FML_RX.match(scout_spec)
        if match:
            samples = int(match.group(1))
            return main_sequence.calc_fml(samples)

    try:
        return Sequence.create(scout_spec).intersection(main_sequence)

    except:
        pass


def resolve_payload(**kwargs):
    """
    Resolve the payload for scout frames.

    This function calculates and returns the scout frames if the 'use_scout_frames' option is enabled.

    :param kwargs: A dictionary of keyword arguments that may include 'use_scout_frames'.
    :return: A dictionary containing the scout frames or an empty dictionary.
    """
    use_scout_frames = kwargs.get("use_scout_frames")
    if not use_scout_frames:
        return {}

    main_seq = main_frame_sequence(**kwargs)
    scout_sequence = scout_frame_sequence(main_seq, **kwargs)
    if scout_sequence:
        return {"scout_frames": ",".join([str(f) for f in scout_sequence])}
    return {}
