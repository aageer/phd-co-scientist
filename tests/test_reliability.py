from swarm.reliability import hallucination_score, joint_score, plagiarism_score


def test_hallucination_clips_unlogged_number():
    paper = "We report accuracy of 99.7 and a score of 0.42"
    log = "score=0.42 calls=40"
    clip = hallucination_score(paper, log)
    assert clip.hallucination_score > 0
    assert any("99.7" in c for c in clip.clipped)
    assert any("0.42" in v for v in clip.verified)


def test_empty_log_is_total_hallucination():
    clip = hallucination_score("score of 1.0", "")
    assert clip.hallucination_score == 1.0


def test_plagiarism_detects_copied_ngrams():
    src = "the quick brown fox jumps over the lazy dog and then some extra tokens here"
    copy = src
    other = "completely different scientific prose about tournaments and logs"
    assert plagiarism_score(copy, [src]) > 0.5
    assert plagiarism_score(other, [src]) < 0.1


def test_joint_score_hallucination_dominates():
    # λ_hall=1 can wipe a 0.3 reviewer bump
    honest = joint_score(0.6, 0.0, 0.0)
    hacked = joint_score(0.9, 0.0, 1.0)
    assert honest > hacked
