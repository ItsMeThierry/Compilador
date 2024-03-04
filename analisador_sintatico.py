class AnalisadorSintatico:

  def __init__(self, tokens):
    self.tokens = tokens
    self.current_token = self.tokens[0]
    self.stack_pos = 0
    self.accepted = False

    try:
      self.parser()
    except SyntaxError as e:
      if self.stack_pos == len(self.tokens):
        self.stack_pos -= 1
      print(
          f'Erro sintático na linha {self.tokens[self.stack_pos][2]}, {e}, encontrado: {self.tokens[self.stack_pos][0]}'
      )

  def next(self):
    self.stack_pos += 1
    self.current_token = self.tokens[self.stack_pos] if self.stack_pos < len(
        self.tokens) else (None, None, None)

  def parser(self):
    if self.current_token[0] == 'program':
      self.next()
      if self.current_token[1] == 'IDENTIFICADOR':
        self.next()
        if self.current_token[0] == ';':
          self.next()
          try:
            self.declarações_variáveis()
          except SyntaxError as e:
            raise SyntaxError(f'em declarações de variáveis, {e}')
          try:
            self.declarações_de_subprogramas()
          except SyntaxError as e:
            raise SyntaxError(f'em declarações de subprogramas, {e}')
          try:
            self.comando_composto()
          except SyntaxError as e:
            raise SyntaxError(f'em comando composto, {e}')
          if self.current_token[0] == '.':
            self.accepted = True
          else:
            raise SyntaxError('esperado \'.\'')
        else:
          raise SyntaxError('esperado \';\'')
      else:
        raise SyntaxError('esperado IDENTIFICADOR')
    else:
      raise SyntaxError('esperado \'program\'')

  def declarações_variáveis(self):
    if self.current_token[0] == 'var':
      self.next()
      self.lista_declarações_variáveis()

  def lista_declarações_variáveis(self):
    if self.current_token[1] == 'IDENTIFICADOR':
      self.next()
      self.lista_de_identificadores()
      if self.current_token[0] == ':':
        self.next()
        if self.current_token[0] == 'integer' or self.current_token[
            0] == 'real' or self.current_token[0] == 'boolean':
          self.next()
          if self.current_token[0] == ';':
            self.next()
            try:
              self.lista_declarações_variáveis()
            except SyntaxError as e:
              if str(e) == 'esperado lista de declaração de variáveis':
                pass
              else:
                raise SyntaxError(e)
          else:
            raise SyntaxError('esperado \';\'')
        else:
          raise SyntaxError('esperado tipo')
      else:
        raise SyntaxError('esperado \':\'')
    else:
      raise SyntaxError('esperado lista de declaração de variáveis')

  def lista_de_identificadores(self):
    if self.current_token[0] == ',':
      self.next()
      if self.current_token[1] == 'IDENTIFICADOR':
        self.next()
        self.lista_de_identificadores()
      else:
        raise SyntaxError('esperado IDENTIFICADOR')

  def declarações_de_subprogramas(self):
    self.declaração_de_subprograma()

  def declaração_de_subprograma(self):
    if self.current_token[0] == 'procedure':
      self.next()
      if self.current_token[1] == 'IDENTIFICADOR':
        self.next()
        self.argumentos()
        if self.current_token[0] == ';':
          self.next()
          try:
            self.declarações_variáveis()
          except SyntaxError as e:
            raise SyntaxError(e)
          try:
            self.declarações_de_subprogramas()
          except SyntaxError as e:
            raise SyntaxError(e)
          try:
            self.comando_composto()
          except SyntaxError as e:
            raise SyntaxError(e)
          if self.current_token[0] == ';':
            self.next()
            self.declarações_de_subprogramas()
          else:
            raise SyntaxError('esperado \';\'')
        else:
          raise SyntaxError('esperado \';\'')
      else:
        raise SyntaxError('esperado IDENTIFICADOR')

  def argumentos(self):
    if self.current_token[0] == '(':
      self.next()
      self.lista_de_parametros()
      if self.current_token[0] == ')':
        self.next()
      else:
        raise SyntaxError('esperado \')\'')

  def lista_de_parametros(self):
    if self.current_token[1] == 'IDENTIFICADOR':
      self.next()
      self.lista_de_identificadores()
      if self.current_token[0] == ':':
        self.next()
        if self.current_token[0] == 'integer' or self.current_token[
            0] == 'real' or self.current_token[0] == 'boolean':
          self.next()
          if self.current_token[0] == ';':
            self.next()
            self.lista_de_parametros()
        else:
          raise SyntaxError('esperado tipo')
      else:
        raise SyntaxError('esperado \':\'')
    else:
      raise SyntaxError('esperado lista de parâmetros')

  def comando_composto(self):
    if self.current_token[0] == 'begin':
      self.next()
      self.comandos_opcionais()
      if self.current_token[0] == 'end':
        self.next()
      else:
        raise SyntaxError('esperado \'end\'')
    else:
      raise SyntaxError('esperado \'begin\'')

  def comandos_opcionais(self):
    try:
      self.lista_de_comandos()
    except SyntaxError as e:
      if str(e) == '':
        pass
      else:
        raise SyntaxError(e)

  def lista_de_comandos(self):
    self.comando()
    if self.current_token[0] == ';':
      self.next()
      try:
        self.lista_de_comandos()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado lista de comandos')
        else:
          raise SyntaxError(e)

  def comando(self):
    if self.current_token[1] == 'IDENTIFICADOR':
      self.next()
      if self.current_token[1] == 'ATRIBUIÇÃO':
        self.next()
        try:
          self.expressão()
        except SyntaxError as e:
          if str(e) != 'esperado termo':
            raise SyntaxError('esperado expressão')
          else:
            raise SyntaxError(e)
      else:
        try:
          self.ativação_de_procedimento()
        except SyntaxError as e:
          if str(e) == '':
            pass
          else:
            raise SyntaxError(e)
    else:
      if self.current_token[0] == 'if':
        self.next()
        try:
          self.expressão()
        except:
          raise SyntaxError('esperado expressão')
        if self.current_token[0] == 'then':
          self.next()
          try:
            self.comando()
          except SyntaxError as e:
            if str(e) == '':
              raise SyntaxError('esperado comando')
            else:
              raise SyntaxError(e)
          self.parte_else()
        else:
          raise SyntaxError('esperado then')
      elif self.current_token[0] == 'while':
        self.next()
        try:
          self.expressão()
        except:
          raise SyntaxError('esperado expressão')
        if self.current_token[0] == 'do':
          self.next()
          try:
            self.comando()
          except SyntaxError as e:
            if str(e) == '':
              raise SyntaxError('esperado comando')
            else:
              raise SyntaxError(e)
        else:
          raise SyntaxError('esperado \'do\'')
      else:
        try:
          self.comando_composto()
        except SyntaxError as e:
          if str(e) == 'esperado \'begin\'':
            raise SyntaxError('')
          else:
            raise SyntaxError(e)

  def parte_else(self):
    if self.current_token[0] == 'else':
      self.next()
      self.comando()

  def ativação_de_procedimento(self):
    if self.current_token[0] == '(':
      self.next()
      try:
        self.lista_de_expressoes()
      except:
        raise SyntaxError('esperado lista de expressões')
      if self.current_token[0] == ')':
        self.next()
      else:
        raise SyntaxError('esperado \')\'')
    else:
      raise SyntaxError('')

  def lista_de_expressoes(self):
    try:
      self.expressão()
    except:
      raise SyntaxError('esperado expressão')
    if self.current_token[0] == ',':
      self.next()
      self.lista_de_expressoes()

  def expressão(self):
    self.expressão_simples()
    if self.current_token[1] == 'OPERADORES_RELACIONAIS':
      self.next()
      self.expressão_simples()

  def expressão_simples(self):
    if self.current_token[0] == '+' or self.current_token[0] == '-':
      self.next()
    self.termo()
    if self.current_token[1] == 'OPERADORES_ADITIVOS':
      self.next()
      self.expressão_simples()

  def termo(self):
    self.fator()
    if self.current_token[1] == 'OPERADORES_MULTIPLICATIVOS':
      self.next()
      try:
        self.termo()
      except:
        raise SyntaxError('esperado termo')

  def fator(self):
    if self.current_token[1] == 'IDENTIFICADOR':
      self.next()
      if self.current_token[0] == '(':
        self.next()
        self.lista_de_expressoes()
        if self.current_token[0] == ')':
          self.next()
    elif self.current_token[1] == 'NÚMERO_INTEIRO' or self.current_token[
        1] == 'NÚMERO_REAL':
      self.next()
    else:
      if self.current_token[0] == 'true' or self.current_token[0] == 'false':
        self.next()
      elif self.current_token[0] == '(':
        self.next()
        self.expressão()
        if self.current_token[0] == ')':
          self.next()
      elif self.current_token[0] == 'not':
        self.next()
        self.fator()
      else:
        raise SyntaxError()
