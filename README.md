# Servidor UDP

### 1.Tenha o Python 3 instalado.
### 2. Tenha o PostgreSQL instalado em sua maquina.
### 3. Instale os pacotes necessarios para a execução.

<pre>
pip install psycopg2 python-dotenv socket
</pre>
### 4. Renomeie o arquivo .env_Example para .env e preencha as variaveis de ambiente com os dados do seu banco PostgreSQL.
### 5. Execute o script python

<pre>
python socket_udp.py
</pre>

# Enviar dados de teste.

## 1. Execute o script em outro terminal.

<pre>
python simulate.py
</pre>


## 2. Para encerrar aperte CTRL+C.
