class SemanticError(Exception):

  def __init__(self, message):
    self.message = message


class AnalisadorSemantico:

  def __init__(self):
    self.type_stack = []
    self.declared_ids = []
    self.result_type = None

    self.scope = 0
    self.procedure_pos = -1
    self.parametros = 0

  def add_declared_id(self, id):
    has_found = self.seek(id[0])
    
    if has_found != -1:
      raise SemanticError(f'identificador \'{id[0]}\' já foi declarado.')
    else:
      self.declared_ids.append(id)
    
  def check_used_id(self, id):
    has_found = self.seek(id)

    if has_found != -1:
      if self.result_type != None:
        self.type_stack.append(self.declared_ids[has_found][1])
    else:
      raise SemanticError(f'identificador \'{id}\' não foi declarado.')

  def seek(self, id):
    i = len(self.declared_ids) - 1
    
    while self.declared_ids[i] != '$':
      if self.declared_ids[i][0] == id:
        return i

      i -= 1

    return -1
  
  def close_scope(self):
    if self.scope == 0:
      while self.declared_ids[-1] != '$':
        self.declared_ids.pop()
      self.declared_ids.pop()
    
  def add_type(self, type):
    i = len(self.declared_ids) - 1

    while self.declared_ids[i] != '$' and self.declared_ids[i][1] is None:
        self.declared_ids[i][1] = type
        i -= 1

  def check_types(self, operation):
    last_id = len(self.type_stack) - 1
    
    if operation in ('*', '+', '-'):
      types = {self.type_stack[last_id], self.type_stack[last_id - 1]}
      
      if {'integer', 'integer'} == types:
        self.update_types('integer')
      elif {'integer', 'real'} == types or {'real', 'real'} == types:
        self.update_types('real')
      else:
        raise SemanticError(f'operação \'{operation}\' não pode ser realizada entre {self.type_stack[last_id - 1]} e {self.type_stack[last_id]}')
    elif operation == '/':
      types = (self.type_stack[last_id], self.type_stack[last_id - 1])

      if 'boolean' in types or 'procedure' in types:
        raise SemanticError(f'operação \'{operation}\' não pode ser realizada entre {self.type_stack[last_id - 1]} e {self.type_stack[last_id]}')
      else:
        self.update_types('real')
    elif operation in ('or', 'and'):
      types = (self.type_stack[last_id], self.type_stack[last_id - 1])

      if types == ('boolean', 'boolean'):
        self.update_types('boolean')
      else:
        raise SemanticError(f'operação \'{operation}\' não pode ser realizada entre {self.type_stack[last_id - 1]} e {self.type_stack[last_id]}')
    elif operation in ('=', '<', '>', '<=', '>=', '<>'):
      types = {self.type_stack[last_id], self.type_stack[last_id - 1]}

      if types == {'integer', 'integer'} or types == {'real', 'integer'} or types == {'boolean', 'boolean'}:
        self.update_types('boolean')
      else:
        raise SemanticError(f'operação \'{operation}\' não pode ser realizada entre {self.type_stack[last_id - 1]} e {self.type_stack[last_id]}')
    elif operation == 'not':
      if self.type_stack[last_id] in ('integer', 'real'):
        raise SemanticError(f'operação \'{operation}\' não pode ser realizada com {self.type_stack[last_id]}')

  def update_types(self, type):
    self.type_stack.pop()
    self.type_stack.pop()
    self.type_stack.append(type)
    ##print(self.type_stack)

  def check_result(self):
    if self.result_type == self.type_stack[0] or (self.result_type == 'real' and self.type_stack[0] == 'integer'):
      self.type_stack.pop()
      self.result_type = None
    else:
      raise SemanticError(f'operação inválida, o tipo esperado é {self.result_type}, encontrado {self.type_stack[0]}')

  def check_parameters_absence(self):
    size = len(self.declared_ids[self.procedure_pos][2])

    if self.parametros != size:
      raise SemanticError(f'procedimento \'{self.declared_ids[self.procedure_pos][0]}\' necessita de {size} parametro(s)')

  def check_parameters_excession(self):
    size = len(self.declared_ids[self.procedure_pos][2]) - 1

    if self.parametros > size:
      if size == -1:
        raise SemanticError(f'procedimento \'{self.declared_ids[self.procedure_pos][0]}\' precisa de nenhum parametro')
        
      raise SemanticError(f'procedimento \'{self.declared_ids[self.procedure_pos][0]}\' necessita de apenas {size+1} parametros')

  def has_arguments(self):
    if len(self.declared_ids[self.procedure_pos][2]) > 0:
      raise SemanticError(f'procedimento {self.declared_ids[self.procedure_pos][0]} necessita dos parametros {self.declared_ids[self.procedure_pos][2]}')
      
  def update_arguments(self):
    i = 1
    
    while self.parametros != 0:
      self.declared_ids[self.procedure_pos][2].append(self.declared_ids[self.procedure_pos+1+i][1])
      self.parametros -= 1
      i += 1

  def print_declared_ids(self):
    print('=====DECLARAÇÕES=====')
    for item in self.declared_ids:
      print(item)
    print('=====================\n')