#pyLuaScanner

Scanner da lingaugem [Lua](http://www.lua.org/manual/5.1/pt/manual.html) feito em **python 3.0** usando a biblioteca **re** do python

###Como usar

```sh
python pyLuaScanner.py <script.lua>
```
Analiza o script e verifica se possui erros ou não, dando a linha e coluna do erro se houver

```sh
python pyLuaScanner.py <script.lua> -v
```

Analiza e, se tudo estiver bem, mostra todos os Tokens registrados no script

```sh
python pyLuaScanner.py <script.lua> -V
```
Analiza e mostra todos os Tokens registrados no script, mesmo havendo erro Léxico. Caso haja um erro mostra-se os Token identificados ate então.
