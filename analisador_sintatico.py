import analisador_semantico
  
class AnalisadorSintatico:

  def __init__(self, tokens):
    self.semantico = analisador_semantico.AnalisadorSemantico()
    
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
          f'Erro sintático na linha {self.tokens[self.stack_pos][2]}, {e}, encontrado: \'{self.tokens[self.stack_pos][0]}\''
      )
    except analisador_semantico.SemanticError as e:
      print(f'Erro semântico na linha {self.tokens[self.stack_pos-1][2]}, {e}')

  def next(self):
    self.stack_pos += 1
    self.current_token = self.tokens[self.stack_pos] if self.stack_pos < len(
        self.tokens) else (None, None, None)

  def parser(self):
    if self.current_token[0] != 'program':
      raise SyntaxError('esperado \'program\'')

    self.semantico.declared_ids.append('$')
    self.next()

    if self.current_token[1] != 'IDENTIFICADOR':
      raise SyntaxError('esperado IDENTIFICADOR')

    self.semantico.add_declared_id([self.current_token[0], 'program'])
    self.next()

    if self.current_token[0] != ';':
      raise SyntaxError('esperado \';\'')

    self.next()

    try:
      self.declarações_variáveis()
    except SyntaxError as e:
      raise SyntaxError(f'em declarações de variáveis, {e}')
    except analisador_semantico.SemanticError as e:
      raise analisador_semantico.SemanticError(e)

    try:
      self.declarações_de_subprogramas()
    except SyntaxError as e:
      raise SyntaxError(f'em declarações de subprogramas, {e}')
    except analisador_semantico.SemanticError as e:
      raise analisador_semantico.SemanticError(e)

    try:
      self.comando_composto()
    except SyntaxError as e:
      raise SyntaxError(f'em comando composto, {e}')
    except analisador_semantico.SemanticError as e:
      raise analisador_semantico.SemanticError(e)

    if self.current_token[0] != '.':
      raise SyntaxError('esperado \'.\'')

    self.accepted = True
    print('Semântico aceito!')

  def declarações_variáveis(self):
    if self.current_token[0] == 'var':
      self.next()
      self.lista_declarações_variáveis()

  def lista_declarações_variáveis(self):
    if self.current_token[1] != 'IDENTIFICADOR':
      raise SyntaxError('esperado lista de declaração de variáveis')

    self.semantico.add_declared_id([self.current_token[0], None])
    self.next()
    self.lista_de_identificadores()

    if self.current_token[0] != ':':
      raise SyntaxError('esperado \':\'')

    self.next()
    self.tipo()

    if self.current_token[0] != ';':
      raise SyntaxError('esperado \';\'')

    self.next()
    
    try:
      self.lista_declarações_variáveis()
    except SyntaxError as e:
      if str(e) == 'esperado lista de declaração de variáveis':
        pass
      else:
        raise SyntaxError(e)

  def lista_de_identificadores(self):
    if self.current_token[0] == ',':
      self.next()
      
      if self.current_token[1] != 'IDENTIFICADOR':
        raise SyntaxError('esperado IDENTIFICADOR')

      self.semantico.add_declared_id([self.current_token[0], None])
      if self.semantico.parametros > 0:
        self.semantico.parametros += 1
      self.next()
      self.lista_de_identificadores()     

  def tipo(self):
    if self.current_token[0] not in ('integer', 'real', 'boolean'):
      raise SyntaxError('esperado tipo')

    self.semantico.add_type(self.current_token[0])
    self.next()
      
  def declarações_de_subprogramas(self):
    self.declaração_de_subprograma()

  def declaração_de_subprograma(self):
    if self.current_token[0] == 'procedure':
      self.next()

      if self.current_token[1] != 'IDENTIFICADOR':
        raise SyntaxError('esperado IDENTIFICADOR')

      self.semantico.add_declared_id([self.current_token[0], 'procedure', []])
      self.semantico.procedure_pos = len(self.semantico.declared_ids) - 1
      self.semantico.declared_ids.append('$')
      self.next()
      self.argumentos()
      self.semantico.procedure_pos = -1

      if self.current_token[0] != ';':
        raise SyntaxError('esperado \';\'')
      
      self.next()

      self.declarações_variáveis()
      self.declarações_de_subprogramas()
      self.comando_composto()

      if self.current_token[0] != ';':
        raise SyntaxError('esperado \';\'')

      self.next()
      self.declarações_de_subprogramas()
        
  def argumentos(self):
    if self.current_token[0] == '(':
      self.next()
      self.lista_de_parametros()
      
      if self.current_token[0] != ')':
        raise SyntaxError('esperado \')\'')

      self.semantico.update_arguments()
      self.next()
      
  def lista_de_parametros(self):
    if self.current_token[1] != 'IDENTIFICADOR':
      raise SyntaxError('esperado lista de parâmetros')

    self.semantico.add_declared_id([self.current_token[0], None])
    self.semantico.parametros += 1
    self.next()
    self.lista_de_identificadores()

    if self.current_token[0] != ':':
      raise SyntaxError('esperado \':\'')

    self.next()
    self.tipo()

    if self.current_token[0] == ';':
      self.next()
      self.lista_de_parametros()

  def comando_composto(self):
    if self.current_token[0] != 'begin':
      raise SyntaxError('esperado \'begin\'')

    self.semantico.scope += 1
    ##self.semantico.print_declared_ids()
    self.next()
    self.comandos_opcionais()
    
    if self.current_token[0] != 'end':
      raise SyntaxError('esperado \'end\'')

    self.semantico.scope -= 1
    self.semantico.close_scope()
    self.next()

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
      self.semantico.check_used_id(self.current_token[0])
      pos = self.semantico.seek(self.current_token[0])
      self.next()
      
      if self.current_token[1] == 'ATRIBUIÇÃO':
        self.semantico.result_type = self.semantico.declared_ids[pos][1]
        self.next()
        self.expressão()
        self.semantico.check_result()
      else:
        self.semantico.procedure_pos = pos
        self.ativação_de_procedimento()
        self.semantico.check_parameters_absence()
        self.semantico.parametros = 0
        self.semantico.procedure_pos = -1
    elif self.current_token[0] == 'if':
      self.semantico.result_type = 'boolean'
      self.next()
      self.expressão()
      self.semantico.check_result()

      if self.current_token[0] != 'then':
        raise SyntaxError('esperado then')

      self.next()

      try:
        self.comando()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado comando')
        else:
          raise SyntaxError(e)

      self.parte_else()   
    elif self.current_token[0] == 'while':
      self.semantico.result_type = 'boolean'
      self.next()
      self.expressão()
      self.semantico.check_result()

      if self.current_token[0] != 'do':
        raise SyntaxError('esperado \'do\'')
      
      self.next()
      
      try:
        self.comando()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado comando')
        else:
          raise SyntaxError(e)
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
      
      try:
        self.comando()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado comando')
        else:
          raise SyntaxError(e)
        

  def ativação_de_procedimento(self):
    if self.current_token[0] == '(':
      if self.semantico.declared_ids[self.semantico.procedure_pos][1] != 'procedure':
        raise analisador_semantico.SemanticError(f'{self.semantico.declared_ids[self.semantico.procedure_pos][0]} não é um procedimento')
        
      self.next()
      
      try:
        self.lista_de_expressoes()
      except SyntaxError:
        raise SyntaxError('esperado lista de expressões')
      except analisador_semantico.SemanticError as e:
        raise analisador_semantico.SemanticError(e)

      if self.current_token[0] != ')':
        raise SyntaxError('esperado \')\'')

      self.next()

  def lista_de_expressoes(self):
    self.semantico.check_parameters_excession()
    self.semantico.result_type = self.semantico.declared_ids[self.semantico.procedure_pos][2][self.semantico.parametros]
    self.expressão()
    self.semantico.check_result()
    self.semantico.parametros += 1
    
    if self.current_token[0] == ',':
      self.next()
      self.lista_de_expressoes()

  def expressão(self):
    try:
      self.expressão_simples()
    except SyntaxError as e:
      if str(e) == '':
        raise SyntaxError('esperado expressão')
      else:
        raise SyntaxError(e)
    
    if self.current_token[1] == 'OPERADORES_RELACIONAIS':
      operation = self.current_token[0]
      self.next()

      try:
        self.expressão_simples()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado expressão simples')
        else:
          raise SyntaxError(e)

      self.semantico.check_types(operation)

  def expressão_simples(self):
    if self.current_token[0] == '+' or self.current_token[0] == '-':
      self.next()
    self.termo()
    
    if self.current_token[1] == 'OPERADORES_ADITIVOS':
      operation = self.current_token[0]
      self.next()
      
      try:
        self.expressão_simples()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado expressão simples')
        else:
          raise SyntaxError(e)

      self.semantico.check_types(operation)

  def termo(self):
    self.fator()
    
    if self.current_token[1] == 'OPERADORES_MULTIPLICATIVOS':
      operation = self.current_token[0]
      self.next()

      try:
        self.termo()
      except SyntaxError as e:
        if str(e) == '':
          raise SyntaxError('esperado fator')
        else:
          raise SyntaxError(e)

      self.semantico.check_types(operation)
          
  def fator(self):
    if self.current_token[1] == 'IDENTIFICADOR':
      self.semantico.check_used_id(self.current_token[0])
      self.semantico.procedure_pos = self.semantico.seek(self.current_token[0])
      ##print(self.semantico.type_stack)
      self.next()

      if self.current_token[0] == '(':
        self.next()
        _result = self.semantico.result_type
        _stack = self.semantico.type_stack
        self.semantico.type_stack = []
        self.lista_de_expressoes()
        self.semantico.result_type = _result
        self.semantico.type_stack = _stack
        self.semantico.check_parameters_absence()
        self.semantico.parametros = 0
        if self.current_token[0] != ')':
          raise SyntaxError('esperado \')\'')
          
        self.next()
      self.semantico.procedure_pos = -1
    elif self.current_token[1] == 'NÚMERO_INTEIRO':
      self.semantico.type_stack.append('integer')
      #print(self.semantico.type_stack)
      self.next()
    elif self.current_token[1] == 'NÚMERO_REAL':
      self.semantico.type_stack.append('real')
      #print(self.semantico.type_stack)
      self.next()
    elif self.current_token[0] in ('true', 'false'):
      self.semantico.type_stack.append('boolean')
      #print(self.semantico.type_stack)
      self.next()
    elif self.current_token[0] == '(':
      self.next()
      self.expressão()
      
      if self.current_token[0] != ')':
        raise SyntaxError('esperado \')\'')
        
      self.next()
    elif self.current_token[0] == 'not':
      operation = self.current_token[0]
      self.next()
      self.fator()
      self.semantico.check_types(operation)
    else:
      raise SyntaxError('')
