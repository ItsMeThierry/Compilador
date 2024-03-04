tipos = ['integer', 'real', 'boolean']

class AnalisadorSintatico:

  def __init__(self):
    self.current_state = 'q0'
    self.stack = ['$']

  def transition(self, token):
    if self.current_state == 'q0':
      if token[0] == 'program' and self.stack[len(self.stack) - 1] == '$':
        self.stack.append(token[0])
        print(self.stack)
      elif token[1] == 'IDENTIFICADOR' and self.stack[len(self.stack) -
                                                      1] == 'program':
        self.stack.append(token[1])
        print(self.stack)
      elif token[0] == ';' and self.stack[len(self.stack) -
                                          1] == 'IDENTIFICADOR':
        self.current_state = 'q1'
        self.stack.append(token[0])
        print(self.stack)
    elif self.current_state == 'q1':
      if token[0] == 'var' and self.stack[len(self.stack) - 1] == ';':
        self.current_state = 'q3'
        self.stack.append(token[0])
        print(self.stack)
      elif self.stack[len(self.stack) - 1] == 'lista_declarações_variáveis' or self.stack[len(self.stack) - 1] == ';':
        self.current_state = 'q4'
        self.reduce_to_declarações_variáveis()
        print(self.stack)
        self.transition(token)
    elif self.current_state == 'q2':
      if token[0] == ',' and self.stack[len(self.stack) - 1] == 'lista_de_identificadores':
        self.current_state = 'q3'
        self.stack.append(token[0])
        print(self.stack)
      elif token[0] == ':' and self.stack[len(self.stack) - 1] == 'lista_de_identificadores':
        self.stack.append(token[0])
        print(self.stack)
      elif token[0] in tipos and self.stack[len(self.stack) - 1] == ':':
        self.stack.append('tipo')
        print(self.stack)
      elif token[0] == ';' and self.stack[len(self.stack) - 1] == 'tipo':
        self.stack.append(token[0])
        print(self.stack)
      elif token[1] == 'IDENTIFICADOR' and self.stack[len(self.stack) - 1] == ';':
        self.reduce_to_lista_declarações_variáveis()
        self.stack.append('lista_de_identificadores')
        print(self.stack)
      elif self.stack[len(self.stack) - 1] == ';':
        self.current_state = 'q1'
        self.reduce_to_lista_declarações_variáveis()
        print(self.stack)
        self.transition(token)
        
    elif self.current_state == 'q3':
      if token[1] == 'IDENTIFICADOR' and self.stack[len(self.stack) - 1] == 'var':
        self.current_state = 'q2'
        self.stack.append('lista_de_identificadores')
        print(self.stack)
      elif token[1] == 'IDENTIFICADOR' and self.stack[len(self.stack) - 1] == ',':
        self.current_state = 'q2'
        self.stack.pop()
        print(self.stack)
    elif self.current_state == 'q4':
      if token[0] == 'procedure' and self.stack[len(self.stack) - 1] == 'declarações_variáveis':
        self.current_state = 'q5'
        self.stack.append(token[0])
        print(self.stack)
        print('hey')

  def reduce_to_lista_declarações_variáveis(self):
    for i in range(4):
      self.stack.pop()

    if self.stack[len(self.stack) - 1] != 'lista_declarações_variáveis':
      self.stack.append('lista_declarações_variáveis')

  def reduce_to_declarações_variáveis(self):
    for i in range(2):
      self.stack.pop()

    self.stack.append('declarações_variáveis')
