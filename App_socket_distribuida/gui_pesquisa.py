import tkinter as tk
from tkinter import ttk #ttk da um estilo pros widgets


def sair():
	exit()

def ajuda():
	pass

login = ""
passwd = ""

class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#self.geometry("300x300")

		#Adiciona menubar na aplicação 
		#menubar = tk.Menu(self)
		#menubar.add_command(label="Ajuda", command=ajuda)
		#menubar.add_command(label="Sair", command=sair)
		#self.config(menu=menubar)
		

		#Coloca o Icone do app
		logo = tk.PhotoImage(file='pet.png')
		self.call('wm', 'iconphoto', self._w, logo)

		#Coloca o Título do app
		tk.Tk.wm_title(self, "Aplicativo Generico")
		

		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}

		#Adiciona as paginas no dicionário para serem usadas pelo show_frame
		for F in (StartPage, PageOne):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	#Traz a pagina que foi adicionada no dicionário ao topo
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):					#Essa parte inicia a pagina como um Frame
	def __init__(self, parent, controller):	#
		tk.Frame.__init__(self, parent)		#


		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Pagina de Login", font=("Arial","12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self,text="Login:")
		label1.grid(row=1, column=0, sticky="w")

		ed1 = ttk.Entry(self, textvariable=login)
		ed1.grid(row=1, column=1 ,sticky="w")

		label2 = ttk.Label(self,text="Password:")
		label2.grid(row=2, column=0, sticky="e")

		ed2 = ttk.Entry(self, textvariable=passwd)
		ed2.grid(row=2, column=1, sticky="w")

		button1 = ttk.Button(self, text="OK", command=lambda: controller.show_frame(PageOne))
		button1.grid(row=3, columnspan=2, pady=10)


class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Page One", font=("Verdana","12"))
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()

	

app = app()

#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))

app.mainloop()

