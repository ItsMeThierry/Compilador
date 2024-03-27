import analisador_lexico
import analisador_sintatico


def exibir_tokens(tokens):
  for token in tokens:
    print("{:10} {:19} {:2}".format(*token))


arquivos = [
    'exemplos/lexico/teste1.txt', 'exemplos/sintatico/Test1.pas',
    'exemplos/sintatico/Test2.pas', 'exemplos/sintatico/Test3.pas',
    'exemplos/sintatico/Test4.pas', 'exemplos/sintatico/Test5.pas',
    'exemplos/teste.txt', 'exemplos/semantico/Teste1.pas'
]

lexico = analisador_lexico.AnalisadorLexico()

with open(arquivos[7], 'r') as f:

  for line in f:
    lexico.check_line(line)

  lexico.stop()

  if lexico.current_state == 'invalid':

    print(f'Erro léxico na linha {lexico.line}, caractere {lexico.word} inválido!')

  elif lexico.current_state == 'q1':

    print(f'Erro léxico na linha {lexico.line}, comentário não fechado!')

  elif lexico.current_state != 'invalid' and lexico.current_state != 'q1':

    ##exibir_tokens(lexico.tokens)

    sintatico = analisador_sintatico.AnalisadorSintatico(lexico.tokens)

    ##if sintatico.accepted:
      ##print('Sintaxe aceito!')
    