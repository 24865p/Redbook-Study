# """
# 파이썬은 내장 딕셔너리 타입을 사용하면 객체의 생명 주기 동안 동적인 내부 상태를 잘 유지할 수 있음
# 동적: 어떤 값이 들어올지 미리 알 수 없는 식별자들을 유지
# """
# #
# # 아이템 37
# #

from collections import defaultdict

# class SimpleGradebook:
#     def __init__(self):
#         self._grades = {}

#     def add_student(self, name):
#         self._grades[name] = []

#     def report_grade(self, name, score):
#         self._grades[name].append(score)

#     def average_grade(self, name):
#         grades = self._grades[name]
#         return sum(grades) / len(grades)

# book = SimpleGradebook()
# book.add_student('아이작 뉴턴')
# book.report_grade('아이작 뉴턴', 90)
# book.report_grade('아이작 뉴턴', 95)
# book.report_grade('아이작 뉴턴', 85)

# print(book.average_grade('아이작 뉴턴'))


# """
# 딕셔너리와 관련 내장 타입은 사용하기 너무 쉬운만큼 과하게 확장하면서 깨지기 쉬움
# """
# #

# class BySubjectGradebook:
#     def __init__(self):
#         self._grades = {}  # 외부 dict

#     def add_student(self, name):
#         self._grades[name] = defaultdict(list)  # 내부 dict

#     def report_grade(self, name, subject, grade):
#         by_subject = self._grades[name]
#         grade_list = by_subject[subject]
#         grade_list.append(grade)

#     def average_grade(self, name):
#         by_subject = self._grades[name]
#         total, count = 0, 0
#         for grades in by_subject.values():
#             total += sum(grades)
#             count += len(grades)
#         return total / count

# book = BySubjectGradebook()
# book.add_student('알버트 아인슈타인')
# book.report_grade('알버트 아인슈타인', '수학', 70)
# book.report_grade('알버트 아인슈타인', '수학', 65)
# book.report_grade('알버트 아인슈타인', '체육', 90)
# book.report_grade('알버트 아인슈타인', '체육', 95)
# print(book.average_grade('알버트 아인슈타인'))

# #
# class WeightedGradebook:
#     def __init__(self):
#         self._grades = {}

#     def add_student(self, name):
#         self._grades[name] = defaultdict(list)

#     def report_grade(self, name, subject, score, weight):
#         by_subject = self._grades[name]
#         grade_list = by_subject[subject] # grade_list에 by_subject[subject]를 복사하는게 아님. "참조"로 같은 객체(self._grades)를 가리키고 있어서 grade_list에 append하면 self._grades가 영향을 받음
#         grade_list.append((score, weight))

#     def average_grade(self, name):
#         by_subject = self._grades[name]
#         score_sum, score_count = 0, 0

#         for subject, scores in by_subject.items():
#             subject_avg, total_weight = 0, 0

#             for score, weight in scores:
#                 subject_avg += score * weight
#                 total_weight += weight

#             score_sum += subject_avg / total_weight
#             score_count += 1

#         return score_sum / score_count


# book = WeightedGradebook()
# book.add_student('알버트 아인슈타인')
# book.add_student('남영')
# book.report_grade('남영', '수학', 95, 0.90)
# book.report_grade('알버트 아인슈타인', '수학', 75, 0.05)
# book.report_grade('알버트 아인슈타인', '수학', 65, 0.15)
# book.report_grade('알버트 아인슈타인', '수학', 70, 0.80)
# book.report_grade('알버트 아인슈타인', '체육', 100, 0.40)
# book.report_grade('알버트 아인슈타인', '체육', 85, 0.60)
# # print(book.average_grade('알버트 아인슈타인'))
# # print(book.average_grade('남영'))

# """
# 위와 같이 복잡도가 눈에 들어오면 더 이상 딕셔너리, 튜플, 집합, 리스트 등의 내장 타입을 사용하지 말고 클래스 계층 구조를 사용해야 한다. 
# 복잡도가 높은데 이중 이상으로 딕셔너리를 두면 유지 보수의 악몽 속으로 들어간다!!
# 코드에서 값을 관리하는 부분이 점점 복잡해지고 있음을 깨달은 즉시 해당 기능을 클래스로 분리해야 한다.
# """

# grades = []
# grades.append((95, 0.45))
# grades.append((85, 0.55))
# total = sum(score * weight for score, weight in grades)
# total_weight = sum(weight for _, weight in grades)
# average_grade = total / total_weight

# """
# 아래와 같이 튜플을 점점 더 길게 확장하는 패턴은 딕셔너리를 여러 단계로 내포시키는 경우와 유사함
# 원소가 세 개 이상인 튜플을 사용한다면 다른 접근 방법을 생각해봐야 한다.
# """

# grades = []
# grades.append((95, 0.45, '참 잘했어요'))
# grades.append((85, 0.55, '조금 만 더 열심히'))
# total = sum(score * weight for score, weight, _ in grades)
# total_weight = sum(weight for _, weight, _ in grades)
# average_grade = total / total_weight

#
"""
namedtuple을 사용하면 작은 불변 데이터 클래스를 쉽게 정의할 수 있다.
- namedtuple 클래스의 인스턴스를 만들 때는 위치 기반 인자&키워드 인자 사용 가능
- 필드에 접근시 애트리뷰트 이름 사용 가능
- 이름이 있는 애트리뷰트를 사용하면 요구사항이 바뀌는 경우에 namedtuple을 클래스로 변경하기 쉬움
- 가변성 지원 / 간단한 컨테이너 이상의 동작이 필요한 경우 namedtuple을 쉽게 클래스로 변경 가능

- 디폴트 인자 값을 지정할 수 없으므로 선택적인 property가 많은 데이터에 사용하기 어려움
- property가 4-5개 이상이면 dataclass 내장 모듈을 사용하는게 나음
"""
from collections import namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook: # 모든 학생을 저장하는 컨테이너, 이름을 사용해 동적으로 학생을 저장
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]

book = Gradebook()
albert = book.get_student('알버트 아인슈타인')
math = albert.get_subject('수학')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('체육')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())

"""
- 딕셔너리, 긴 튜플, 다른 내장 타입이 복잡하게 내포된 데이터를 값으로 사용하는 딕셔너리를 만들지 말자
- 유연성이 덜 필요하고 가벼운 불변 데이터 컨테이너가 필요하면 namedtuple을 사용하자
- 내부 상태를 표현하는 딕셔너리가 복잡해지면 데이터를 관리하는 코드를 여러 클래스로 나눠서 저장하자
"""