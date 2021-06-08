# Cliente de testes - TP1

O cliente de testes realiza alguns dos testes básicos que serão executados durante a avaliação do seu trabalho. Observe que durante a avaliação, poderão ser executados testes adicionais.

A entrada e saída de cada caso de teste executado se encontram nos diretórios tests/in/ e tests/out/, respectivamente.

Cada caso de teste é executado usando tanto IPv4 quanto IPv6. Além disso, são avaliados três possíveis cenários:

* **single_msg_single_pkg**: cenário onde cada mensagem é, provavelmente, enviada em apenas um pacote (pode ser recebida pelo servidor em apenas um *recv*).
* **single_msg_multiple_pkg**: cenário onde cada mensagem será enviada em mais de um pacote (a mensagem deve ser recebida pelo servidor por mais de um *recv*).
* **multiple_msg_single_pkg**: cenário onde cada pacote carregará mais de uma mensagem (cada *recv* executado no servidor pode receber mais de uma mensagem).

## Execução
O programa de testes foi desenvolvido em Python3. Para executá-lo: 
> python3 run_tests.py \<server> \<port>

onde \<server> é o **caminho para o executável do seu servidor** e \<port> é a porta na qual ele deve ser executado.

Exemplo:
```
python3 run_tests.py /home/aluno/servidor 9999
```

## Saída
A saída do programa indica quais casos de teste foram executados com sucesso e quais falharam.
Exemplo de saída onde todos casos de teste foram executados com sucesso:

```
Testing IPv4 single_msg_single_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
Testing IPv4 single_msg_multiple_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
Testing IPv4 multiple_msg_single_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
Testing IPv6 single_msg_single_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
Testing IPv6 single_msg_multiple_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
Testing IPv6 multiple_msg_single_pkg
test_0	[OK]
test_1	[OK]
test_2	[OK]
test_3	[OK]
```


