from socket import *
import os, sys, time, threading
from random import randint


lista_de_ips = ["127.0.0.1","192.168.0.148"]
porta = 12000

###########################PESQUISA###########################

def pesquisa(url_pagina,palavra):
	return ("Nome da pagina",randint(0,20))

###########################SERVIDOR###########################
def cria_servidor(ip, porta, num_clientes):

	"""
	Use porta = 50007
	Use ip = localhost

	Cria um objeto socket. As duas constantes referem-se a:
	família do endereço (padrão é socket.AF_INET)
	Se é stream(socket.SOCK_STREAM, o padrão) ou datagram(socket.SOCK_DATAGRAM)
	E o protocolo (padrão é 0)
	Significado:
	AF_INET == Protocolo de endereço IP
	SOCK_STREAM == Protocolo de transferência TCP
	Combinação = Server TCP/IP
	"""
	ip = str(ip)
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sockobj.bind((ip, porta))
	#O socket começa a esperar por clientes limitando a 5 conexões por vez
	sockobj.listen(num_clientes)
	print("\n\nSERVIDOR: \n","Servidor iniciado em ",ip, " na porta ",porta, ", esperando por no máximo ", num_clientes, " clientes")
	return sockobj

def recebe_cliente(sockobj):
	"""
	Aceita uma conexão quando encontrada e devolve a um novo socket conexão e o endereço do cliente conectado
	"""
	conexao, endereco = sockobj.accept()
	#print("SERVIDOR \n",'Server conectado por ', endereco)
	return (conexao, endereco)

def recebe_tarefa():
	"""
	Recebe de um cliente socket, a palavra desejada para pesquisa
	e a lista de sites para pesquisar, retorna [("nome_da_pagina",numero_de_ocorrencias), ...].
	"""
	lista_urls = ["g1.globo.com","uol.com","site1","site2","site3"]
	lista_resultados = []
	sock = cria_servidor('localhost', 12000, 5)
	while True:
		sockserv, endereco = recebe_cliente(sock) #fica esperando o cliente aparecer
		requisicao = sockserv.recv(1024)
		palavra = requisicao.decode("utf8")

		#Cria lista de tuplas(nome_da_pagina, numero_de_ocorrencias) ordenada.
		for url in lista_urls:
			nome_da_pagina, numero_de_ocorrencias = pesquisa(url,palavra)
			lista_resultados.append((nome_da_pagina,numero_de_ocorrencias))
		lista_resultados_ordenada = sorted(lista_resultados, key=lambda x: x[1], reverse=True)
		resultado = str(lista_resultados_ordenada)

		sockserv.send(resultado.encode())
		lista_resultados = []
		#sockserv.close()

###########################Cliente###########################
def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor
	"""
	try:
		ip = str(ip)
		sockobj = socket(AF_INET, SOCK_STREAM)
		sockobj.settimeout(1.0)
		sockobj.connect((ip, porta))
		sockobj.settimeout(None)

	except:
		sockobj = None
	return sockobj

def atribui_tarefa(lista_de_ips):
	"""
	Essa é a função que atribui a tarefa de pesquisa
	para todas as maquinas da rede através da
	thread Cliente.
	"""

	#espera servidor iniciar
	time.sleep(0.5)
	#GUI - go_start = True
	go_start = input("\nClique ENTER para iniciar a pesquisa: \n")
	while True:
		# Dicionario = {'ip':[sockobj,resposta]}
		dicionario_ip_resposta = {}

		#palavra = input("Informe a string para pesquisa: ")

		#Cria conexão com todos os servidores disponíveis
		print("Conectando com servidores...\n")
		for ip in lista_de_ips: # Pra cada ip tenta criar um cliente e preencher o dict de ip-objeto_socket
			sockobj = cria_cliente(ip, porta)
			if sockobj:
				dicionario_ip_resposta[ip] = [sockobj, None]
				print(" - Conectado ao servidor!", ip)
			else:
				print(" - O IP: ",ip," não estádisponível no momento!\n")

		#Palavra a ser pesquisada
		palavra = input("Informe a string para pesquisa: ")

		#Manda cada um dos servidores fazerem a pesquisa e retorna o resultado
		print("\nRESULTADO DA PESQUISA")
		for ip in dicionario_ip_resposta:
			dicionario_ip_resposta[ip][0].send(palavra.encode("utf-8"))
			dicionario_ip_resposta[ip][1] = dicionario_ip_resposta[ip][0].recv(1024).decode('utf-8')
			print("\n",dicionario_ip_resposta[ip][1],"\n\n")

		#sockobj.close()
###########################Main_APP###########################


#Construindo as threads
Servidor = threading.Thread(target=recebe_tarefa)
Cliente = threading.Thread(target=atribui_tarefa, args=(lista_de_ips,))

#Configuração que faz threads pais matarem as threads filhas
Servidor.daemon = True
Cliente.daemon = True

try:
	Servidor.start()
	Cliente.start()
	Cliente.join()
	Servidor.join()

except KeyboardInterrupt:
	print("\nCtrl-C/ Pesquisa cancelada!")
	sys.exit()
