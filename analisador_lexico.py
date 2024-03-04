reserved_words = [
    'program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin',
    'end', 'if', 'then', 'else', 'while', 'do', 'not'
]
delimiters = [';', '.', '(', ')', ',']


class AnalisadorLexico:

  def __init__(self):
    self.current_state = 'q0'
    self.word = ""
    self.line = 0
    self.tokens = []

  def transition(self, char):
    if self.current_state == 'q0':
      if char == ' ' or char == '\t' or char == '\n':
        self.current_state = 'q0'
      elif char == '{':
        self.current_state = 'q1'
      elif char.isalpha():
        self.word += char
        self.current_state = 'q2'
      elif char.isdigit():
        self.word += char
        self.current_state = 'q3'
      elif char in delimiters:
        self.word += char
        self.current_state = 'q5'
      elif char == ':':
        self.word += char
        self.current_state = 'q6'
      elif char == '<':
        self.word += char
        self.current_state = 'q8'
      elif char == '>':
        self.word += char
        self.current_state = 'q9'
      elif char == '=':
        self.word += char
        self.current_state = 'q10'
      elif char == '+' or char == '-':
        self.word += char
        self.current_state = 'q11'
      elif char == '*' or char == '/':
        self.word += char
        self.current_state = 'q12'
      else:
        self.word += char
        self.current_state = 'invalid'
    elif self.current_state == 'q1':
      if char == '}':
        self.current_state = 'q0'
      else:
        self.current_state = 'q1'
    elif self.current_state == 'q2':
      if char.isdigit() or char.isalpha() or char == '_':
        self.word += char
        self.current_state = 'q2'
      else:
        if self.word in reserved_words:
          self.reset('PALAVRA_RESERVADA')
          self.transition(char)
        elif self.word == 'and':
          self.reset('OPERADORES_MULTIPLICATIVOS')
          self.transition(char)
        elif self.word == 'or':
          self.reset('OPERADORES_ADITIVOS')
          self.transition(char)
        else:
          self.reset('IDENTIFICADOR')
          self.transition(char)
    elif self.current_state == 'q3':
      if char.isdigit():
        self.word += char
        self.current_state = 'q3'
      elif char == '.':
        self.word += char
        self.current_state = 'q4'
      else:
        self.reset('NÚMERO_INTEIRO')
        self.transition(char)
    elif self.current_state == 'q4':
      if char.isdigit():
        self.word += char
        self.current_state = 'q4'
      else:
        self.reset('NÚMERO_REAL')
        self.transition(char)
    elif self.current_state == 'q5':
      self.reset('DELIMITADOR')
      self.transition(char)
    elif self.current_state == 'q6':
      if char == '=':
        self.word += char
        self.current_state = 'q7'
      else:
        self.reset('DELIMITADOR')
        self.transition(char)
    elif self.current_state == 'q7':
      self.reset('ATRIBUIÇÃO')
      self.transition(char)
    elif self.current_state == 'q8':
      if char == '=':
        self.word += char
        self.current_state = 'q10'
      else:
        self.reset('OPERADORES_RELACIONAIS')
        self.transition(char)
    elif self.current_state == 'q9':
      if char == '=' or char == '>':
        self.word += char
        self.current_state = 'q10'
      else:
        self.reset('OPERADORES_RELACIONAIS')
        self.transition(char)
    elif self.current_state == 'q10':
      self.reset('OPERADORES_RELACIONAIS')
      self.transition(char)
    elif self.current_state == 'q11':
      self.reset('OPERADORES_ADITIVOS')
      self.transition(char)
    elif self.current_state == 'q12':
      self.reset('OPERADORES_MULTIPLICATIVOS')
      self.transition(char)

  def stop(self):
    if self.current_state == 'q2':
      if self.word in reserved_words:
        self.tokens.append((self.word, 'PALAVRA_RESERVADA', self.line))
      elif self.word == 'and':
        self.tokens.append(
            (self.word, 'OPERADORES_MULTIPLICATIVOS', self.line))
      elif self.word == 'or':
        self.tokens.append((self.word, 'OPERADORES_ADITIVOS', self.line))
      else:
        self.tokens.append((self.word, 'IDENTIFICADOR', self.line))
    elif self.current_state == 'q3':
      self.tokens.append((self.word, 'NÚMERO_INTEIRO', self.line))
    elif self.current_state == 'q4':
      self.tokens.append((self.word, 'NÚMERO_REAL', self.line))
    elif self.current_state == 'q5':
      self.tokens.append((self.word, 'DELIMITADOR', self.line))
    elif self.current_state == 'q6':
      self.tokens.append((self.word, 'DELIMITADOR', self.line))
    elif self.current_state == 'q7':
      self.tokens.append((self.word, 'ATRIBUIÇÃO', self.line))
    elif self.current_state == 'q8' or self.current_state == 'q9' or self.current_state == 'q10':
      self.tokens.append((self.word, 'OPERADORES_RELACIONAIS', self.line))
    elif self.current_state == 'q11':
      self.tokens.append((self.word, 'OPERADORES_ADITIVOS', self.line))
    elif self.current_state == 'q12':
      self.tokens.append((self.word, 'OPERADORES_MULTIPLICATIVOS', self.line))

  def reset(self, classifier):
    self.tokens.append((self.word, classifier, self.line))
    self.word = ""
    self.current_state = 'q0'

  def check_line(self, input_string):
    self.line += 1

    for char in input_string:
      self.transition(char)

      if self.current_state == 'invalid':
        break
