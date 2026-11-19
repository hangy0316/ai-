import pytest
from load_scores import load_scores


def 쓰기(path, 점수):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(f"name,score\n홍길동,{점수}\n")


# 정상 ① 평범한 파일
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


# 정상 ② 빈 줄이 섞였을 때
def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "blank_lines.csv"
    csv_file.write_text("name,score\n김하나,88\n\n\n이두리,92\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == [("김하나", 88), ("이두리", 92)]
    assert skipped == []


# 정상 ③ 이름에 쉼표가 있을 때
def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


# 예외 ① 없는 파일을 주면
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


# 예외 ② 헤더만 있는 파일을 주면
def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


# 경계 ①~③ 점수 경계값 (parametrize로 한 번에)
@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    쓰기("임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가


# 기록표 ② 커버리지 측정 후 안 지나간 줄(55-56행: 이름이 비어 있음)을 지나가게 만든 추가 테스트
def test_이름이_비어있으면_건너뛰고_기록한다(tmp_path):
    csv_file = tmp_path / "empty_name.csv"
    csv_file.write_text("name,score\n,90\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == []
    assert skipped == [(2, ",90", "이름이 비어 있음")]
