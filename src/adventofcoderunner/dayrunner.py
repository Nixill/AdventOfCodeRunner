from abc import abstractmethod
from dataclasses import dataclass
from io import StringIO
from typing import Iterable
from pathlib import Path

class DayCode():
  input: InputFile
  result: RunResult

  def __init__(self, input: InputFile):
    self.input = input

    try:
      self.result = self.run()
    except Exception as e:
      self.result = RunResult(exception=e)

    input.stream.close()

  @abstractmethod
  def run(self) -> RunResult:
    ...

class InputFile():
  filepath: Path
  data: str
  stream: StringIO

  process_p1: bool = True
  process_p2: bool = True

  def __init__(self, filepath: Path,
      process_p1: bool = True,
      process_p2: bool = True,):
    self.filepath = filepath
    self.data = filepath.read_text()
    self.stream = StringIO(self.data)
    self.process_p1 = process_p1
    self.process_p2 = process_p2

  def next_line(self) -> str:
    return self.stream.readline().rstrip('\r\n')

  def lines_until_empty(self) -> Iterable[str]:
    while True:
      line = self.stream.readline().rstrip('\r\n')
      if line:
        yield line
      else:
        return

  def all_lines(self) -> Iterable[str]:
    while True:
      line = self.stream.readline()
      if line:
        yield line.rstrip('\r\n')
      else:
        return

  def content_until_empty(self) -> str:
    output = ''
    while True:
      line = self.stream.readline()
      if line.rstrip('\r\n'):
        output += line
      else:
        return output.rstrip('\r\n')

  def all_remaining_content(self) -> str:
    return self.stream.read()

  def __hash__(self): return self.filepath.__hash__()
  def __eq__(self, other): return self.filepath.__eq__(other)

class ExampleFile(InputFile):
  expected_answer_p1: int | str | None = None
  expected_answer_p2: int | str | None = None

  def __init__(
      self,
      filepath: Path,
  ):
    super().__init__(filepath)
    answer_1 = self.next_line()
    if answer_1:
      if answer_1 == '\\SKIP':
        self.process_p1 = False
      else:
        try:
          self.expected_answer_p1 = int(answer_1)
        except ValueError:
          self.expected_answer_p1 = answer_1

    answer_2 = self.next_line()
    if answer_2:
      if answer_2 == '\\SKIP':
        self.process_p2 = False
      else:
        try:
          self.expected_answer_p2 = int(answer_2)
        except ValueError:
          self.expected_answer_p2 = answer_2

@dataclass(frozen=True)
class RunResult:
  part_1_answer: int | str | None = None
  part_2_answer: int | str | None = None
  exception: Exception | None = None

def get_examples_for_day(day_index: int) -> Iterable[ExampleFile]:
  return [ExampleFile(f) for f in Path(f'data/day{day_index}').iterdir() if f.name.startswith('example')]

def get_input_for_day(day_index: int) -> InputFile:
  return InputFile(Path(f'data/day{day_index}/input.txt'))

def run_code_for_day[T : DayCode](day_code: type[T], day_index: int) -> None:
  print()

  examples = get_examples_for_day(day_index)
  passed = 0
  failed = 0
  errored = 0

  for example in examples:
    passing = True
    print(f'For example file {example.filepath.stem}:')
    example_output = day_code(example)
    daycode = example_output.result

    if daycode.exception:
      print(f'Exception occurred: {daycode.exception}')
      errored += 1
      continue

    if daycode.part_1_answer is not None:
      if example.expected_answer_p1 is not None:
        matches = daycode.part_1_answer == example.expected_answer_p1
        passing &= matches
        print(f'Part 1 answer: {daycode.part_1_answer} / Expected: {example.expected_answer_p1} / Pass: {matches}')
      else:
        print(f'Part 1 answer: {daycode.part_1_answer} / (No expected answer)')

    if daycode.part_2_answer is not None:
      if example.expected_answer_p2 is not None:
        matches = daycode.part_2_answer == example.expected_answer_p2
        passing &= matches
        print(f'Part 2 answer: {daycode.part_2_answer} / Expected: {example.expected_answer_p2} / Pass: {matches}')
      else:
        print(f'Part 2 answer: {daycode.part_2_answer} / (No expected answer)')

    print()
    if passing:
      passed += 1
    else:
      failed += 1

  print()
  print(f'Passed: {passed} / Failed: {failed} / Errored: {errored}')
  print()

  if (failed + errored) > 0:
    print('Failures detected, ending execution.')
    print()
    return

  input = get_input_for_day(day_index)
  daycode = day_code(input)

  if daycode.result.exception:
    print(f'Exception: {daycode.result.exception}')
  if daycode.result.part_1_answer:
    print(f'Part 1 answer: {daycode.result.part_1_answer}')
  if daycode.result.part_2_answer:
    print(f'Part 2 answer: {daycode.result.part_2_answer}')

  print()