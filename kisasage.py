from enum import Enum, auto
from time import sleep
import re
from collections import deque
import sys
from datetime import datetime

class TokenType(Enum):
  VAL = auto()
  OPER = auto()
  VAR = auto()
  STRING = auto()
  PRINT = auto()
class Token:
  def __init__(self, enum_type, value, proc):
    self.type = enum_type
    self.value = value
    self.proc = proc

class Operator():
  def __init__(self):
    self.oper_dict = {
      '+': self.add_oper,
      '-': self.sub_oper,
      '*': self.mul_oper,
      '/': self.div_oper,
      '**': self.pow_oper,
      '%': self.mod_oper,
      '|': self.bit_or_oper,
      '&': self.bit_and_oper,
      '^': self.bit_xor_oper,
      '>>': self.rshift_oper,
      '<<': self.lshift_oper,
      '~': self.bit_inv_oper,
      '?': self.input_oper,
      '==': self.comp_eq_oper,
      '!=': self.comp_ne_oper,
      '<': self.comp_gt_oper,
      '<=': self.comp_ge_oper,
      '>': self.comp_lt_oper,
      '>=': self.comp_le_oper,
      '!': self.log_not_oper,
      '||': self.log_or_oper,
      '&&': self.log_and_oper,
      '^^': self.log_xor_oper,
      '(': self.if_start_oper,
      ')': self.if_end_oper,
      '{': self.loop_start_oper,
      '}': self.loop_end_oper,
      '[': self.jump_start_oper,
      ']': self.jump_end_oper,
      '_': self.dup_oper,
      '$': self.def_var_oper,
      '$=': self.set_var_oper,
      ':': self.set_rt_oper,
      '::': self.set_lambda_rt_oper,
      ';': self.return_rt_oper,
      '@': self.def_ary_oper,
      '@g': self.get_ary_oper,
      '@s': self.set_ary_oper,
      '@l': self.len_ary_oper,
      '&*': self.get_ptr_oper,
      '&>': self.set_ptr_oper,

      '\\time': self.time_oper,
      '\\depth': self.stack_depth_oper,
      '\\pause': self.pause_oper,
      '\\sleep': self.sleep_oper,
      # '\\?': self.status_oper,
      # '\\out': self.output_oper,
      # '\\in': self.input_oper,
    }
  def __contains__(self, item):
    return item in self.oper_dict
  def __getitem__(self, key):
    if not isinstance(key, str):
      raise Exception('Operator Error')
    return self.oper_dict.get(key)
  
  def _exe_bin_value_oper(self, oper):
    a, b = data.pop_data_stack(), data.pop_data_stack()
    if a.val_type == ValueType.VALUE and b.val_type == ValueType.VALUE:
      data.push_data_stack(getattr(b.val, oper)(a.val))
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)

  def add_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__add__')
    return idx + 1
  def sub_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__sub__')
    return idx + 1
  def mul_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__mul__')
    return idx + 1
  def div_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__floordiv__')
    return idx + 1
  def pow_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__pow__')
    return idx + 1
  def mod_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__mod__')
    return idx + 1
  def bit_or_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__or__')
    return idx + 1
  def bit_and_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__and__')
    return idx + 1
  def bit_xor_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__xor__')
    return idx + 1
  def rshift_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__rshift__')
    return idx + 1
  def lshift_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__lshift__')
    return idx + 1
  def bit_inv_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    if a.val_type == ValueType.VALUE:
      data.push_data_stack(~a.val)
      return idx + 1
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
  def input_oper(self, value, idx, words, data):
    data.push_data_stack(input())
    return idx + 1
  def comp_eq_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__eq__')
    return idx + 1
  def comp_ne_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__ne__')
    return idx + 1
  def comp_gt_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__lt__')
    return idx + 1
  def comp_ge_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__le__')
    return idx + 1
  def comp_lt_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__gt__')
    return idx + 1
  def comp_le_oper(self, value, idx, words, data):
    self._exe_bin_value_oper('__ge__')
    return idx + 1

  def log_not_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    if a.val_type == ValueType.VALUE:
      data.push_data_stack(1 if a.val == 0 else 0)
      return idx + 1
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
  def log_or_oper(self, value, idx, words, data):
    a, b = data.pop_data_stack(), data.pop_data_stack()
    if a.val_type == ValueType.VALUE and b.val_type == ValueType.VALUE:
      data.push_data_stack(1 if bool(b.val) or bool(a.val) else 0)
      return idx + 1
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
  def log_and_oper(self, value, idx, words, data):
    a, b = data.pop_data_stack(), data.pop_data_stack()
    if a.val_type == ValueType.VALUE and b.val_type == ValueType.VALUE:
      data.push_data_stack(1 if bool(b.val) and bool(a.val) else 0)
      return idx + 1
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
  def log_xor_oper(self, value, idx, words, data):
    a, b = data.pop_data_stack(), data.pop_data_stack()
    if a.val_type == ValueType.VALUE and b.val_type == ValueType.VALUE:
      data.push_data_stack(1 if bool(b.val) ^ bool(a.val) else 0)
      return idx + 1
    else:
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
  def if_start_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    if (a.val_type != ValueType.VALUE):
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
    if not bool(a.val):
      pare_match_count = 0
      for i in range(idx + 1, len(words)):
        if (words[i].value == ')'):
          if (pare_match_count == 0):
            return i
          else:
            pare_match_count -= 1
        elif(words[i].value == '('):
          pare_match_count += 1
      else:
        print_error('Operator', 'Match Parentheses Not Found', True)
    else:
      return idx + 1
  def if_end_oper(self, value, idx, words, data):
    return idx + 1
  def loop_start_oper(self, value, idx, words, data):
    return idx + 1
  def loop_end_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    if (a.val_type != ValueType.VALUE):
      print_error('Operator', f'Unexpected Type {a} {b}, Expected VALUE', True)
    if bool(a.val):
      pare_match_count = 0
      for i in range(idx - 1, -1, -1):
        if (words[i].value == '{'):
          if (pare_match_count == 0):
            return i
          else:
            pare_match_count -= 1
        elif(words[i].value == '}'):
          pare_match_count += 1
      else:
        print_error('Operator', 'Match Curly Brackets Not Found', True)
    else:
      return idx + 1
  def jump_start_oper(self, value, idx, words, data):
    pare_match_count = 0
    for i in range(idx + 1, len(words)):
      if (words[i].value == ']'):
        if (pare_match_count == 0):
          return i
        else:
          pare_match_count -= 1
      elif(words[i].value == '['):
        pare_match_count += 1
    else:
      print_error('Operator', 'Match Square Not Found', True)
  def jump_end_oper(self, value, idx, words, data):
    return idx + 1
  def dup_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    data.push_data_stack(a.val)
    data.push_data_stack(a.val)
    return idx + 1
  def def_var_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    data.def_var_value(words[idx + 1].value, a)
    return idx + 2
  def set_var_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    data.set_var_value(words[idx + 1].value, a)
    return idx + 2
  def set_rt_oper(self, value, idx, words, data):
    data.def_var_value(words[idx + 1].value, Value(idx + 2, ValueType.ROUTINE))
    pare_match_count = 0
    for i in range(idx + 1, len(words)):
      if (words[i].value == ';'):
        if (pare_match_count == 0):
          return i + 1
        else:
          pare_match_count -= 1
      elif(words[i].value == ':' or words[i].value == '::'):
        pare_match_count += 1
    else:
      print_error('Operator', 'Routine Return Not Found', True)
  def set_lambda_rt_oper(self, value, idx, words, data):
    lambda_rt_name = data.get_lambda_name('~')
    data.def_var_value(lambda_rt_name, Value(idx + 1, ValueType.ROUTINE))
    addr, _, _ = data.get_var_value(lambda_rt_name)
    data.push_data_stack(addr)
    pare_match_count = 0
    for i in range(idx + 1, len(words)):
      if (words[i].value == ';'):
        if (pare_match_count == 0):
          return i + 1
        else:
          pare_match_count -= 1
      elif(words[i].value == ':' or words[i].value == '::'):
        pare_match_count += 1
    else:
      print_error('Operator', 'Routine Return Not Found', True)
  def return_rt_oper(self, value, idx, words, data):
    data.pop_variable_scope()
    return data.pop_routine_addr()
  def def_ary_oper(self, value, idx, words, data):
    a = data.pop_data_stack()
    if (a.val_type != ValueType.VALUE):
      print_error('Operator', 'Not Value', True)
    data.def_var_value(words[idx + 1].value, Value([0 for i in range(a.val)], ValueType.ARRAY))
    addr, val_type, val = data.get_var_value(words[idx + 1].value)
    for i in range(a.val, 0, -1):
      b = data.pop_data_stack()
      data.set_value_by_raw_addr(addr + i, b.val)
    return idx + 2
  def get_ary_oper(self, value, idx, words, data):
    addr, val_type, val = data.get_var_value(words[idx + 1].value)
    if (not(val_type == ValueType.ARRAY or val_type == ValueType.STRING)):
      print_error('Operator', 'Not Array', True)
    if (val_type == ValueType.STRING):
      val = list(map(lambda c: ord(c), val))
    a = data.pop_data_stack()
    if (a.val_type != ValueType.VALUE):
      print_error('Operator', 'Not Value', True)
    if (not(0 <= a.val < len(val))):
      print_error('Operator', 'Index Not In Range', True)
    data.push_data_stack(val[a.val])
    return idx + 2
  def set_ary_oper(self, value, idx, words, data):
    addr, val_type, val = data.get_var_value(words[idx + 1].value)
    a, b = data.pop_data_stack(), data.pop_data_stack()
    if (not(val_type == ValueType.ARRAY or val_type == ValueType.STRING)):
      print_error('Operator', 'Not Array', True)
    elif (not(a.val_type == ValueType.VALUE and b.val_type == ValueType.VALUE)):
      print_error('Operator', 'Not Value', True)
    elif (not(0 <= a.val < len(val))):
      print_error('Operator', 'Not Value', True)
    data.memory.set_value_by_raw_addr(addr + 1 + a.val, b.val)
    return idx + 2
  def len_ary_oper(self, value, idx, words, data):
    addr, val_type, val = data.get_var_value(words[idx + 1].value)
    if (not(val_type == ValueType.ARRAY or val_type == ValueType.STRING)):
      print_error('Operator', 'Not Array', True)
    data.push_data_stack(len(val))
    return idx + 2
  def time_oper(self, value, idx, words, data):
    now_time = datetime.now()
    a = data.pop_data_stack()
    if a.val_type != ValueType.VALUE:
      print_error('Operator', '\\time expect VALUE', True)
    time_bit = {
      'microsecond': 64,
      'second': 32,
      'minute': 16,
      'hour': 8,
      'day': 4,
      'month': 2,
      'year': 1,
    }
    for k in time_bit.keys():
      if time_bit[k] & a.val:
        data.push_data_stack(getattr(now_time, k))
    return idx + 1
  def stack_depth_oper(self, value, idx, words, data):
    depth = len(data.data_stack)
    data.push_data_stack(depth)
    return idx + 1
  def pause_oper(self, value, idx, words, data):
    try:
      input()
    except KeyboardInterrupt:
      sys.exit(0)
    return idx + 1
  def sleep_oper(self, value, idx, words, data):
    time = data.pop_data_stack()
    if time.val_type != ValueType.VALUE:
      print_error('Operator', '\\sleep expect VALUE')
    try:
      sleep(time.val / 1000)
    except KeyboardInterrupt:
      sys.exit(0)
    return idx + 1
  def get_ptr_oper(self, value, idx, words, data):
    addr, _, _ = data.get_var_value(words[idx + 1].value)
    data.push_data_stack(addr)
    return idx + 2
  def set_ptr_oper(self, value, idx, words, data):
    ptr = data.pop_data_stack()
    if ptr.val_type != ValueType.VALUE:
      print_error('Operator', 'Unexpected Ptr', True)
    data.set_var_ptr(f"*{words[idx + 1].value}", ptr.val)
    return idx + 2

  @staticmethod
  def print_oper(value, idx, words, data):
    reversed_value = value[::-1]
    while (chr(26) in reversed_value):
      v = str(data.pop_data_stack().val)[::-1]
      reversed_value = reversed_value.replace(chr(26), v, 1)
    write_stdout(reversed_value[::-1], end='')
    return idx + 1

  @staticmethod
  def string_oper(value, idx, words, data):
    reversed_value = value[::-1]
    while (chr(26) in reversed_value):
      v = str(data.pop_data_stack().val)[::-1]
      reversed_value = reversed_value.replace(chr(26), v, 1)
    data.push_data_stack(reversed_value[::-1])
    return idx + 1

  @staticmethod
  def value_oper(value, idx, words, data):
    data.push_data_stack(value)
    return idx + 1
  
  @staticmethod
  def variable_oper(value, idx, words, data):
    addr, val_type, val = data.get_var_value(value)
    if val_type == ValueType.VALUE:
      data.push_data_stack(val)
      return idx + 1
    elif val_type == ValueType.STRING:
      data.push_data_stack(val)
      return idx + 1
    elif val_type == ValueType.ARRAY:
      data.push_data_stack(addr)
      return idx + 1
    elif val_type == ValueType.ROUTINE:
      data.push_routine_addr(idx + 1)
      data.push_variable_scope()
      return val
    else:
      print_error('Data', 'Unexpected Variable Type', True)
    

def write_stdout(out_str, end="\n"):
  sys.stdout.write(str(out_str) + end)
  sys.stdout.flush()

def write_stderr(out_str, end="\n"):
  sys.stderr.write(str(out_str) + end)
  sys.stdout.flush()

class ValueType(Enum):
  VALUE = auto()
  STRING = auto()
  ARRAY = auto()
  ROUTINE = auto()

class Value():
  def __init__(self, val, val_type):
    self.val = val
    self.val_type = val_type

def get_bit_limit(m, b=32):
    bit = b
    if(m == "top"):
        return (2 ** bit) // 2 - 1
    elif(m == "under"):
        return -(2 ** bit // 2)
    elif(m == "logi"):
        return (2 ** bit) - 1

def round_overflow(arth, b=32):
    _max = get_bit_limit("top", b)
    _min = get_bit_limit("under", b)
    _lmax = get_bit_limit("logi", b)
    if(_min <= arth <= _max):
        return arth
    elif(arth % _lmax <= _max):
        return arth % _lmax
    else:
        arth %= _lmax
        return arth - _max + _min - 1

class Memory:
  def __init__(self):
    self._memory = []
    self.LENGTH = 0x0000_FFFF
    self.INT = 0x0001_0000
    self.CHAR = 0x0002_0000
    self.ROUTINE = 0x004_0000
    self.VALUE = 0x0010_0000
    self.ARRAY = 0x0020_0000

  def alloc(self, val_type, value):
    head = None
    body = None
    if val_type == ValueType.VALUE:
      head = self.INT | self.VALUE
      body = [value]
    elif val_type == ValueType.STRING:
      head = self.CHAR | self.ARRAY | (len(value) & self.LENGTH)
      body = map(lambda c: ord(c), value)
    elif val_type == ValueType.ARRAY:
      head = self.INT | self.ARRAY | (len(value) & self.LENGTH)
      body = value
    elif val_type == ValueType.ROUTINE:
      head = self.ROUTINE | self.VALUE
      body = [value]
    else:
      print_error('Memory', f'Allocate Error {val_type} {body}')
    addr = len(self._memory)
    self._memory.append(head)
    self._memory.extend(body)
    return addr

  def free(self, head_addr):
    head = self._memory[head_addr]
    if (head & self.VALUE):
      del self._memory[head_addr:head_addr + 2]
    elif(head & self.ARRAY):
      length = head & self.LENGTH
      del self._memory[head_addr:head_addr + length + 1]

  def get_data_by_addr(self, head_addr):
    if (not(0 <= head_addr < len(self._memory))):
      print_error('Memory', f'Invalid Address: {head_addr}', True)
    head = self._memory[head_addr]
    addr = head_addr
    val_type = None
    value = None
    if (head & self.INT) and (head & self.VALUE):
      val_type = ValueType.VALUE
      value = self._memory[head_addr + 1]
    elif (head & self.CHAR) and (head & self.ARRAY):
      val_type = ValueType.STRING
      length = head & self.LENGTH
      value = "".join(map(lambda i: chr(i), self._memory[head_addr+1:head_addr + 1 + length])) 
    elif (head & self.INT) and (head & self.ARRAY):
      val_type = ValueType.ARRAY
      length = head & self.LENGTH
      value = self._memory[head_addr+1:head_addr + 1 + length]
    elif (head & self.ROUTINE):
      val_type = ValueType.ROUTINE
      value = self._memory[head_addr + 1]
    else:
      print_error('Memory', f'Invalid Head Address {head_addr}', True)
    return addr, val_type, value

  
  def set_data_by_head_addr(self, head_addr, value):
    head = self._memory[head_addr]
    if (head & self.INT) and (head & self.VALUE):
      self._memory[head_addr + 1] = value.val
    elif (head & self.CHAR) and (head & self.ARRAY):
      for i in range(head_addr + 1, head_addr + 1 + len(value.val)):
        self._memory[i] = ord(value.val[i])
    elif (head & self.INT) and (head & self.ARRAY):
      for i in range(head_addr + 1, head_addr + 1 + len(value.val)):
        self._memory[i] = value.val[i]
    elif (head & self.ROUTINE):
      self._memory[head_addr + 1] = value.val
    else:
      print_error('Memory', f'Invalid Head Address {head_addr}', True)
  
  def set_value_by_raw_addr(self, addr, value):
    self._memory[addr] = int(value)

class Data:
  def __init__(self):
    self.data_stack = deque([])
    self.routine_stack = deque([])
    self.variable_scope = deque([{}])
    self.variable_scope_depth = 0
    self.memory = Memory()
    self.lambda_name_serial = -1

  def push_data_stack(self, value):
    if type(value) == int:
      self.data_stack.append(Value(round_overflow(value), ValueType.VALUE))
    elif type(value) == bool:
      self.data_stack.append(Value(1 if value else 0, ValueType.VALUE))
    elif type(value) == str:
      self.data_stack.append(Value(value, ValueType.STRING))
    else:
      print_error('Data', 'Unexpected Push Data', True)
  def pop_data_stack(self):
    if (len(self.data_stack) == 0):
      print_error('Data', 'Stack Empry', True)
    return self.data_stack.pop()

  def push_routine_addr(self, addr):
    self.push_variable_scope()
    self.routine_stack.append(addr)
  def pop_routine_addr(self):
    self.pop_variable_scope()
    return self.routine_stack.pop()

  def push_variable_scope(self):
    self.variable_scope.append({})
    self.variable_scope_depth += 1
  def pop_variable_scope(self):
    cur_scope = self.variable_scope[self.variable_scope_depth]
    cur_var_names = filter(lambda name: name[0] != '*', cur_scope.keys())
    addrs = sorted(map(lambda name: cur_scope[name], cur_var_names), reverse=True)
    for head_addr in addrs:
      self.memory.free(head_addr)
    self.variable_scope.pop()
    self.variable_scope_depth -= 1
  
  def get_var_value(self, var):
    for i in range(len(self.variable_scope) - 1, -1, -1):
      scope = self.variable_scope[i]
      if var in scope:
        return self.memory.get_data_by_addr(scope[var])
      elif f"*{var}" in scope:
        return self.memory.get_data_by_addr(scope[f"*{var}"])
    else:
      print_error('Data', f'Not Found Variable {var}', True)
  
  def def_var_value(self, var, val):
    scope = self.variable_scope[self.variable_scope_depth]
    scope[var] = self.memory.alloc(val.val_type, val.val)

  def set_var_value(self, var, val):
    for i in range(len(self.variable_scope) - 1, -1, -1):
      scope = self.variable_scope[i]
      if var in scope:
        self.memory.set_data_by_head_addr(scope[var], val)
        break
      elif f"*{var}" in scope:
        return self.memory.set_data_by_head_addr(scope[var], val)
    else:
      print_error('Data', f'Not Found Variable {var}', True)
  def set_var_ptr(self, var, ptr):
    scope = self.variable_scope[self.variable_scope_depth]
    scope[var] = ptr

  def set_value_by_raw_addr(self, addr, value):
    self.memory.set_value_by_raw_addr(addr, value)

  def get_lambda_name(self, prefix):
    self.lambda_name_serial += 1
    return f"{prefix}{self.lambda_name_serial:08}"

def print_error(source, msg, is_exist):
  write_stderr(f"{source} {msg}")
  if (is_exist):
    sys.exit(0)

def open_file(file_name):
  src_code = ''
  with open(file_name, mode="r") as f:
    src_code = f.read()
  return src_code

class MacroDict:
  def __init__(self):
    self.DYNAMIC_MACRO = 0
    self.macro_dict = {}
  def is_dyn_macro_token(self, token):
    try:
      int(token[1:], 10)
      return token[0] == '#'
    except:
      return False
  def get_macro_tokens(self, macro_token):
    if (self.is_dyn_macro_token(macro_token)):
      return [self.DYNAMIC_MACRO, [macro_token]]
    elif (macro_token in self.macro_dict):
      return self.macro_dict[macro_token]
    else:
      print_error('Macro', f'Unexpected format macro {macro_token}', True)
  def cnv_dyn_macro_to_token(self, macro_tokens, token_array):
    result_tokens = []
    for t in macro_tokens:
      if self.is_dyn_macro_token(t) and int(t[1:]) <= len(token_array):
        result_tokens.append(token_array[-int(t[1:])])
      else:
        result_tokens.append(t)
    return result_tokens
  def set_macro_tokens(self, macro_token, expanded_tokens):
    self.macro_dict[macro_token] = expanded_tokens

macro_dict = MacroDict()

def convert_escape_char(c):
  dict_esc_chars = {
    '%': chr(26),
    "\\":"\\", "\"":"\"", "\'":"\'",
    "a":"\a", "b":"\b", "f":"\f",
    "n":"\n", "r":"\r", "t":"\t",
    "v":"\v", "e":'\x1b', "0":"\0"
  }
  if c in dict_esc_chars:
    return dict_esc_chars[c]
  else:
    print_error('Parser', f'Unexpected Escape Character: {c}', True)

def parse_src_code(src_code, recurse_lim, cur_file_name):
  if (recurse_lim == 0):
    print_error('Parse', f'RecursionError {cur_file_name}', True)
  class ParseMode(Enum):
    NORMAL = auto()
    STRING = auto()
    PRINT = auto()
    LINE_COMMENT = auto()
    AREA_COMMENT = auto()
    MACRO = auto()
    INCLUDE = auto()
  
  src_code += '\n'
  cur_token = ''
  token_array = []
  is_esq_str = False
  DELIMIT_CHAR = [' ', '\n']
  parse_mode = ParseMode.NORMAL
  for c in src_code:
    if (parse_mode == ParseMode.NORMAL):
      if c == '\'':
        cur_token += c
        parse_mode = ParseMode.STRING
      elif c == '\"':
        cur_token += c
        parse_mode = ParseMode.PRINT
      elif cur_token == '//':
        parse_mode = ParseMode.LINE_COMMENT
      elif cur_token == '/*':
        parse_mode = ParseMode.AREA_COMMENT
      elif cur_token == '###':
        cur_token += c
        parse_mode = ParseMode.MACRO
      elif cur_token == '##<':
        cur_token += c
        parse_mode = ParseMode.INCLUDE
      elif c not in DELIMIT_CHAR:
        cur_token += c
      else:
        if (cur_token == ''):
          continue
        if (cur_token[0] == '#'):
          macro_tokens = macro_dict.get_macro_tokens(cur_token)
          if (macro_tokens[0] == macro_dict.DYNAMIC_MACRO):
            token_array.extend(macro_tokens[1])
          else:
            token_array.extend(macro_dict.cnv_dyn_macro_to_token(macro_tokens, token_array))
          cur_token = ''
        else:
          token_array.append(cur_token)
          cur_token = ''
    elif (parse_mode == ParseMode.STRING):
      if (is_esq_str):
        cur_token += convert_escape_char(c)
        is_esq_str = False
      elif c == '\\':
        is_esq_str = True
      elif c == '\'':
        token_array.append(cur_token + '\'')
        cur_token = ''
        parse_mode = ParseMode.NORMAL
      else:
        cur_token += c
    elif (parse_mode == ParseMode.PRINT):
      if (is_esq_str):
        cur_token += convert_escape_char(c)
        is_esq_str = False
      elif c == '\\':
        is_esq_str = True
      elif c == '\"':
        token_array.append(cur_token + '\"')
        cur_token = ''
        parse_mode = ParseMode.NORMAL
      else:
        cur_token += c
    elif (parse_mode == ParseMode.LINE_COMMENT):
      cur_token += c
      if (c == '\n'):
        parse_mode = ParseMode.NORMAL
        cur_token = ''
    elif (parse_mode == ParseMode.AREA_COMMENT):
      cur_token += c
      if (cur_token[-2:] == '*/'):
        parse_mode = ParseMode.NORMAL
        cur_token = ''
    elif (parse_mode == ParseMode.MACRO):
      cur_token += c
      if (c == '\n'):
        macro_token_name = f"#{cur_token[3:].strip().split(' ')[0]}"
        macro_tokens = parse_src_code(cur_token[3:], recurse_lim - 1, f"{cur_file_name}/{macro_token_name}")
        macro_dict.set_macro_tokens(macro_token_name, macro_tokens[1:])
        parse_mode = ParseMode.NORMAL
        cur_token = ''
    elif (parse_mode == ParseMode.INCLUDE):
      cur_token += c
      if (c == '>'):
        file_name = cur_token[3:-1].strip()
        include_tokens = parse_src_code(open_file(file_name), recurse_lim - 1, f"{cur_file_name}/{file_name}")
        token_array.extend(include_tokens)
        parse_mode = ParseMode.NORMAL
        cur_token = ''
  return token_array

def convert_tokens_words(token_array, operator):
  def parse_token(token):
    def toValue(token):
      try:
        if (token[:2] == '0b' and len(token) < 35):
          t = f"{token[2:]:>032}"
          i_val = int(t, 2)
          if (t[0] == '1'):
            i_val -= 2 ** 32
          return i_val
        elif(token[:2] == '0x' and len(token) < 11):
          t = f"{token[2:]:>08}"
          i_val = int(t, 16)
          if (i_val >= 2 ** 31):
            i_val -= 2 ** 32
          return i_val
        elif(token[:2] == '0c' and len(token) < 4):
          return ord(token[2])
        else:
          return int(token, 10)
      except:
        return None

    def toOperator(token):
      if (token in operator):
        return token
    def toString(token):
      if token[0] == '\'' and token[-1] == '\'':
        return token[1:-1]
    def toPrintStr(token):
      if token[0] == '\"' and token[-1] == '\"':
        return token[1:-1]

    def toName(token):
      pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
      if (bool(re.match(pattern, token))):
        return token
    
    parsed_token = toValue(token)
    if parsed_token is not None:
      return Token(TokenType.VAL, parsed_token, operator.value_oper)
    
    parsed_token = toOperator(token)
    if parsed_token is not None:
      return Token(TokenType.OPER, parsed_token, operator[token])

    parsed_token = toString(token)
    if parsed_token is not None:
      return Token(TokenType.STRING, parsed_token, operator.string_oper)
  
    parsed_token = toPrintStr(token)
    if parsed_token is not None:
      return Token(TokenType.PRINT, parsed_token, operator.print_oper)

    parsed_token = toName(token)
    if parsed_token is not None:
      return Token(TokenType.VAR, parsed_token, operator.variable_oper)

    print_error('Parser', f'Unexpected token: {token}', True)

  return list(map(lambda t: parse_token(t), token_array))


def execute(words, data, option):
  def print_trace_word(idx, word, option):
    if option[:7] != '--trace':
      return
    s = f"S={list(map(lambda e: e.val, data.data_stack))}" if 's' in option[7:] else ''
    v = f"V={list(data.variable_scope)}" if 'v' in option[7:] else ''
    r = f"R={list(data.routine_stack)}" if 'r' in option[7:] else ''
    m = f"M={list(data.memory._memory)}" if 'm' in option[7:] else ''
    replace_newline_char = lambda w: str(w).replace('\n', '\\n')
    write_stdout(f"[{idx}]({replace_newline_char(word):>6}) {s} {v} {r} {m}")

  idx = 0
  while (0 <= idx < len(words)):
    print_trace_word(idx, words[idx].value, option)
    idx = words[idx].proc(words[idx].value, idx, words, data)
  else:
    print_trace_word(' ', '######', option)

def print_dry_words(words):
  write_stdout("[ 0]  ", end="")
  for i, w in enumerate(words):
    if (i != 0 and i % 10 == 0):
      write_stdout(f"\n[{i}]  ", end="")
    write_stdout(f"{w.value:^8} ".replace("\n", "\\n"), end="")

if __name__ == "__main__":
  file_name = sys.argv[1]
  src_code = input() if file_name == '--pipe' else open_file(file_name)
  recurce_lim = 5
  token_array = parse_src_code(src_code, recurce_lim, '_')
  words = convert_tokens_words(token_array, Operator())
  data = Data()
  option = sys.argv[2] if len(sys.argv) >= 3 else ''
  if (option == '--dry'):
    print_dry_words(words)
  else:
    execute(words, data, option)
