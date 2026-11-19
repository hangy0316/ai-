# test_ai_B.py — 프롬프트 B (10주차 명세서 6칸만 주고 생성한 테스트)
import pytest
from load_scores import load_scores


def test_spec_normal_read(tmp_path):
    csv_file = tmp_path / "scores_normal.csv"
    csv_file.write_text(
        'name,score\n김하나,88\n"최,네번",77\n김하나,91\n',
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91)]
    assert skipped == []


def test_spec_skip_empty_lines(tmp_path):
    csv_file = tmp_path / "scores_blank.csv"
    csv_file.write_text("name,score\n\n윤보람,64\n\n서한별,95\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == [("윤보람", 64), ("서한별", 95)]
    assert skipped == []


def test_spec_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_scores("does_not_exist_12345.csv")


def test_spec_header_only_returns_empty(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == []
    assert skipped == []


def test_spec_malformed_rows_recorded(tmp_path):
    csv_file = tmp_path / "malformed.csv"
    csv_file.write_text(
        "name,score\n"
        "장미르,72,추가열\n"
        ",85\n"
        "박세찬,\n"
        "한겨울,abc\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert kept == []
    assert len(skipped) == 4
    assert [row[0] for row in skipped] == [2, 3, 4, 5]


@pytest.mark.parametrize(
    "score,expected_kept",
    [
        (-1, 0),
        (0, 1),
        (1, 1),
        (99, 1),
        (100, 1),
        (101, 0),
    ],
)
def test_spec_boundary_scores(tmp_path, score, expected_kept):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n테스터,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == expected_kept
    assert len(skipped) == (1 - expected_kept)
