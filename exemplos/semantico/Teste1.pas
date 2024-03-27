program Test4;
var X: real;
Y, Z: integer;

procedure teste (A:integer; B:boolean);
var S, X: real;
begin
   S := A + A * X
end; {verifique se é necessário um ";" no fechamento de um procedimento}

begin
   while (X >= 5) do
   begin
      Y := 5 + 2;
      Z := Z-1;
      X := Y + Z;
      X := X + 1;

      teste(5, Y >= 12);

      X := teste(5-10, true)
   end
end.

{retirar algumas palavras reservadas para gerar erros sintáticos}