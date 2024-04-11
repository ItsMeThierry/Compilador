import analisador_lexico
import analisador_sintatico

arquivos = ('exemplos/lexico/teste1.txt', 'exemplos/sintatico/Test1.pas',
            'exemplos/sintatico/Test2.pas', 'exemplos/sintatico/Test3.pas',
            'exemplos/sintatico/Test4.pas', 'exemplos/sintatico/Test5.pas',
            'exemplos/teste.txt', 'exemplos/semantico/Teste1.pas')

lexico = analisador_lexico.AnalisadorLexico()
sintatico = analisador_sintatico.AnalisadorSintatico()

print('Abrindo arquivo...')

try:
  with open(arquivos[0], 'r') as file:

    lexico.check(file.read())

    if lexico.success:
      print('[LÉXICO] Analise feita com sucesso!')

      sintatico.check(lexico.tokens)

      if sintatico.success:
        print('[SINTATICO] Analise feita com sucesso!')
        print('[SEMANTICO] Analise feita com sucesso!')

except FileNotFoundError:
  print('[ERRO] Arquivo não encontrado.')
