# 이제 모듈을 임포트할 수 있습니다
from doxg.app import imp, pic, who

# 나머지 테스트 코드
def test_pic():
    pic()
    assert True

def test_who():
    who()
    assert True

def test_imp():
    imp()
    assert True