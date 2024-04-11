reserved_words = {
    'program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin',
    'end', 'if', 'then', 'else', 'while', 'do', 'not', 'true', 'false'
}


class AnalisadorLexico:

  def __init__(self):
    self.current_state = 'q0'
    self.word = ''
    self.line = 1
    self.tokens = []

    self.success = False

  def transition(self, char):
    if self.current_state == 'q0':
      if char in {' ', '\t', '\n'}:
        pass
      elif char == '{':
        self.current_state = 'q1'
      elif char.isalpha():
        self.word += char
        self.current_state = 'q2'
      elif char.isdigit():
        self.word += char
        self.current_state = 'q3'
      elif char in {';', '.', '(', ')', ','}:
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
      elif char in {'+', '-'}:
        self.word += char
        self.current_state = 'q11'
      elif char in {'*', '/'}:
        self.word += char
        self.current_state = 'q12'
      else:
        self.word += char
        self.current_state = 'invalid'
    elif self.current_state == 'q1':
      if char == '}':
        self.current_state = 'q0'
    elif self.current_state == 'q2':
      if char.isdigit() or char.isalpha() or char == '_':
        self.word += char
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
      elif char == '.':
        self.word += char
        self.current_state = 'q4'
      else:
        self.reset('NÚMERO_INTEIRO')
        self.transition(char)
    elif self.current_state == 'q4':
      if char.isdigit():
        self.word += char
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
      if char in {'=', '>'}:
        self.word += char
        self.current_state = 'q10'
      else:
        self.reset('OPERADORES_RELACIONAIS')
        self.transition(char)
    elif self.current_state == 'q9':
      if char == '=':
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

  def reset(self, classifier):
    self.tokens.append((self.word, classifier, self.line))
    self.word = ''
    self.current_state = 'q0'

  def check(self, input_file):
    input_file += '\n'

    for char in input_file:
      self.transition(char)

      if char == '\n':
        self.line += 1

      if self.current_state == 'invalid':
        break

    self.success = True
    
    if self.current_state == 'invalid':
      print(f'[ERRO] Erro léxico na linha {self.line}, caractere \'{self.word}\' inválido!')
      self.success = False
    elif self.current_state == 'q1':
      print(f'[ERRO] Erro léxico na linha {self.line}, comentário não fechado!')
      self.success = False
      
    
    ##self.exibir_tokens()

  def exibir_tokens(self):
    print("============================================")
    print("{:10} {:25} {:2}".format(*('Token', 'Classificador', 'Linha')))
    print("============================================")
    for token in self.tokens:
      print("{:10} {:25} {:2}".format(*token))
    print("============================================")