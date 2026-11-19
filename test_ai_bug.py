# test_ai_bug.py — ★ 함정 실험 (bug3_logic.py의 고장난 find_max 코드를 줬을 때)
import pytest
from bug3_logic import find_max


def test_find_max_first_is_largest():
    assert find_max([95, 85, 70, 60]) == 95


def test_find_max_middle_is_largest():
    assert find_max([70, 90, 80, 60]) == 90


def test_find_max_last_element_bug_solidified():
    # ★ AI에게 버그 있는 코드(range(1, len(scores) - 1))를 그대로 주면
    # 현재 코드가 반환하는 85를 기대값(정답)으로 굳히는 테스트가 만들어질 수 있음
    assert find_max([70, 85, 60, 95]) == 85


def test_find_max_single_element():
    assert find_max([50]) == 50


def test_find_max_empty_raises():
    with pytest.raises(IndexError):
        find_max([])
