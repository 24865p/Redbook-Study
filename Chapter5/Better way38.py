#
# 아이템 38 간단한 인터페이스의 경우 클래스 대신 함수를 받아라
#

"""
- hook 함수: API가 실행되는 과정에서 내가 전달한 "함수"를 실행하는 경우
- 인자와 반환 값이 잘 정의된, 상태가 없는 함수를 훅으로 사용하는 경우가 많음
- 파이썬은 함수나 메서드를 "일급 시민 객체" 취급하므로 함수를 훅으로 사용할 수 있다.
    -> 일반적인 값과 마찬가지로 다른 함수(메서드)에 넘기거나 변수로 참조할 수 있음
"""
from collections import defaultdict

names = ['소크라테스', '아르키메데스', '플라톤', '아리스토텔레스']
names.sort(key=len) # key훅으로 len 내장 함수를 전달
print(names)

def log_missing(): # 정해진 동작과 side effect를 분리할 수 있어 API를 쉽게 만들 수 있음
    print('키 추가됨')
    return 0

current = {'초록': 12, '파랑': 3}
increments = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9),
]
result = defaultdict(log_missing, current)
print('이전:', dict(result))
for key, amount in increments:
    result[key] += amount
print('이후:', dict(result))

"""
defaultdict에 전달하는 디폴트 값 훅이 존재하지 않는 키에 접근한 총 횟수 세기
-> 상태가 있는 클로저를 사용하면 됨
-> 아래 코드는 클로저가 있는 도우미 함수를 디폴트 값 훅으로 사용함
"""
def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # 상태가 있는 클로저
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2 # defaultdict은 missing훅이 상태를 관리하는 것을 모르지만 함수를 실행하면 원하는 결과(2)를 볼 수 있음
# 인터페이스에서 간단한 함수를 인자로 받으면 클로저 안에 상태를 감추는 기능 계층을 쉽게 추가할 수 있음 (하지만 이해하기 어려움)

#
class CountMissing:
    """상태를 저장하는 작은 클래스 정의"""
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current) # 메서드 참조
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

"""
더 깔끔하지만 CountMissing 클래스의 목적을 알기 어렵다
- 명확한 표현을 위해 클래스에 __call__ 특별 메서드를 정의할 수 있음
- __call__을 사용하면 객체를 함수처럼 사용할 수 있음
- __call__이 정의된 클래스의 인스턴스에 대해 callable 내장 함수를 호출하면 다른 일반 함수나 메서드처럼 True가 반환됨
- 이런 방식으로 호출되어 호출될 수 있는 모든 객체를 "callable" 객체라고 함
"""

#
class BetterCountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)

# BetterCountMissing 인스턴스를 defaultdict의 디폴트 값 훅으로 사용해서 존재하지 않는 키에 접근한 횟수를 추적
counter = BetterCountMissing()
result = defaultdict(counter, current) # __call__에 의존함
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
"""
- __call__메서드는 API훅처럼 함수가 인자로 쓰일 수 있는 부분에 이 클래스의 인스턴스를 사용할수 있다는 사실을 나타냄
- __call__부터 보고 이 클래스의 목적이 상태를 저장하는 클로저 역할이라는 것을 알 수 있음
- defaultdict이 __call__ 내부에서 어떤 일이 벌어지는지 전혀 알 필요가 없음
- defaultdict에게 필요한건 키가 없는 경우를 처리하기 위한 디폴트 값 훅 뿐임
"""

"""
- 여러 컴포넌트 사이에 간단한 인터페이스가 필요할 때는 클래스를 정의하고 인스턴스화하는 대신 간단히 함수를 사용할 수 있음
- 파이썬 함수나 메서드는 일급 시민이다.
    -> 다른 타입의 값과 마찬가지로 함수나 함수 참조에 식을 사용할 수 있음
- __call__ 특별 메서드를 사용하면 클래스의 인스턴스인 객체를 일반 파이썬 함수처럼 호출할 수 있다.
- 상태를 유지하기 위한 함수가 필요한 경우 상태가 있는 클로저 정의 대신 __call__메서드가 있는 클래스를 정의할 지 고려해보자
"""