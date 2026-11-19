# test_ai_A.py — 프롬프트 A (load_scores.py 코드를 주고 생성한 테스트)
import pytest
from load_scores import load_scores


def test_normal_scores(tmp_path):
    p = tmp_path / "normal.csv"
    p.write_text("name,score\n김하나,88\n이두리,95\n김하나,91\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == [("김하나", 88), ("이두리", 95), ("김하나", 91)]
    assert skipped == []


def test_blank_lines_ignored(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("name,score\n\n김하나,88\n\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == [("김하나", 88)]
    assert skipped == []


def test_comma_in_name(tmp_path):
    p = tmp_path / "comma.csv"
    p.write_text('name,score\n"최,네번",77\n', encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("non_existent_file.csv")


def test_header_only(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("name,score\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == []
    assert skipped == []


def test_invalid_rows_skipped(tmp_path):
    p = tmp_path / "invalid.csv"
    p.write_text(
        "name,score\n"
        "장미르,72,비고없음\n"
        ",90\n"
        "박세찬,\n"
        "한겨울,결석\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(p))
    assert kept == []
    assert skipped == [
        (2, "장미르,72,비고없음", "열 개수가 2가 아님"),
        (3, ",90", "이름이 비어 있음"),
        (4, "박세찬,", "점수가 비어 있음"),
        (5, "한겨울,결석", "점수가 정수가 아님"),
    ]


@pytest.mark.parametrize(
    "score,is_valid",
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_score_boundaries(tmp_path, score, is_valid):
    p = tmp_path / "boundary.csv"
    p.write_text(f"name,score\n홍길동,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    if is_valid:
        assert kept == [("홍길동", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1
        assert skipped[0][2] == "점수가 0~100 밖"
