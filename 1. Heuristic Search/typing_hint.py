# 3월 25일 실습 1.1: python typing module 이해하기
# 학번: 2017320123
# 이름: 김장영

# module: 간단히 말하면 파이썬 코드로 구성된 파일. 한 모듈은 함수, 클래스, 변수, 실행가능한 코드를 정의함
# typing module: 파이썬 코드에 type annotation을 추가하게 해주는 모듈

# 1. 동적인 타이핑 언어인 파이썬
# TODO
a = 10
a = 'ten'

# 2. 문제가 되는 상황
# TODO
def make_double(a, b):
  return (2.5 * a) + b

# print(make_double(10, 2))
# print(make_double('ten', 'two'))

# 3. Python typing hint
# 정의: variable_name: type = value

# TODO: 정수형
some_value: int = 10

# TODO: 문자열
some_text: str = 'Python'

# TODO: 함수에서의 사용
def greeting(name: str) -> str:
  return name + ", good day!"

# TODO: List
from typing import List
nums: List[int] = [4, 7, 5, 9]

# TODO: Dict
from typing import Dict
fruits: Dict[str, int] = {'apple': 3, 'Orange': 5}

# TODO: tuple
from typing import Tuple
user: Tuple[int, str, bool] = (3, 'bob', True)

# TODO: Generic
# 데이터 형식에 의존하지 않고 인자, 변수 또는 반환값 등이 여러 다른 데이터 타입들을 가질 수 있는 방식
from typing import TypeVar

T = TypeVar('T')

def first_index(l: List[T]) -> T:
  return l[0]

print(first_index([(4,5,1), (4,1,9), (0,4,5)]))