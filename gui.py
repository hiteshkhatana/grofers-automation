from tkinter import *
import tkinter.messagebox as tmsg
from selenium_script import Order




#single class for complete applicaton
class GUI(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("700x465")
		self.minsize(550,460)
		self.configure(background = "cyan3")
		self.var = StringVar()
		self.var.set("Ready")
		self.order = Order()

	# Get common kitchen items from local text file and add them to the textbox
	def add_kitchen_items(self):
		with open("kitchen.txt" , "r") as file:
			kitchen_items = file.read()
		
		self.textbox.insert(END,kitchen_items)
		self.textbox.insert(END,"\n")

	# Get common items from local text file and add them to the textbox
	def add_other_items(self):
		with open("others.txt" , "r") as file:
			kitchen_items = file.read()
		
		self.textbox.insert(END,kitchen_items)
		self.textbox.insert(END,"\n")

	# Help for making entries
	def help_func(self):
		tmsg.showinfo("How to Enter products","Product name brand \n Eg. - red chilli powder mdh")

	# Adding menubar to main frame
	def add_menubar(self):

		main_menu = Menu(self)
		common_list = Menu(main_menu,tearoff = 0)
		common_list.add_command(label="Kitchen" , command= self.add_kitchen_items)
		common_list.add_command(label="Others" , command=self.add_other_items)
		main_menu.add_cascade(label="Add Commons",font = "Helvetica 20",menu=common_list)
		main_menu.add_command(label="Help",command=self.help_func)
		self.config(menu = main_menu)

	# Extract values from text box and pass it for further automation tasks
	def add_orders(self):
		self.var = "Adding products please wait............................"
		self.sbar.update()
		data = self.textbox.get("1.0","end-1c")

		if self.order.check_status():
			self.added , self.alternates = self.order.func(data.splitlines())
		else:
			self.added , self.alternates = self.order.start_browser(data.splitlines())
			

			
		# list for items not found after complete execution
		self.not_found = [i for i in data.splitlines() if i not in self.added]
		self.var = "done"
		self.sbar.update()
		self.reset()


	# Adding textwindow to the main frame
	def add_text_window(self):
		self.text_frame = Frame(self)
		self.text_frame.configure(background = "cyan3")
		self.text_frame.pack(fill = "both" , expand = TRUE)
		scrollbar = Scrollbar(self.text_frame)
		scrollbar.pack(side=RIGHT , fill = Y)
		self.textbox = Text(self.text_frame , height = 8,font = "Helvetica 20", relief = SUNKEN , borderwidth = 5,yscrollcommand = scrollbar.set)
		self.textbox.pack(padx = 20 , pady=10 ,fill = BOTH ,expand = TRUE)
		scrollbar.config(command = self.textbox.yview)

	# Add button to add items to cart
	def add_button(self):
		self.butt = Button(text = "Add to cart" , font = "Helvetica 25 bold" ,bg = "LightCyan2",relief = RAISED , borderwidth = 8, command = self.add_orders)
		self.butt.pack(pady=15)


	# Resetting frame for showing alternatives for not found products
	def reset(self):
		self.text_frame.pack_forget()
		self.butt.pack_forget()
		self.sbar.pack_forget()
		self.lift()
		self.attributes("-topmost", True)
		self.geometry("600x550")


		self.alter_label = Label(self,text = "Alternatives for not found products" ,borderwidth = 5 , relief = GROOVE, bg = "white" , fg = "black" , font = "Helvetica 15 bold")
		self.alter_label.pack(fill = "y")

		self.list_frame = Frame(self)
		self.list_frame.pack(pady = 5 , fill = X , expand = "true")


		scrollbar = Scrollbar(self.list_frame)
		scrollbar.pack(side= "right" , fill = Y)

		self.canvas = Canvas(self.list_frame ,height = 400 , yscrollcommand = scrollbar.set)
		self.canvas.pack(side = "left" , fill = "x" , expand = "true")
		scrollbar.config(command = self.canvas.yview)

		self.listbox = Frame(self.canvas)

		self.canvas_frame = self.canvas.create_window((0,0),window = self.listbox  ,anchor = "w" )

		self.bind('<Configure>' ,self.set_scrollregion)
		self.canvas.bind('<Configure>', self.FrameWidth)

		self.buttons = Frame()
		self.buttons.pack( pady = "8")
		self.back_ = Button(self.buttons , text = "Back" , font = "Helvetica 20 bold" , command = self.back_to_main)
		self.back_.grid(row = 0 , column = 0)
		self.add_more = Button(self.buttons , text = "Add to cart" , font = "Helvetica 20 bold" , command = self.add_alter_to_cart)
		self.add_more.grid(row = 0 , column = 1)

		self.add_alternatives_list()

	def FrameWidth(self, event):
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

	def set_scrollregion(self,event = None):
		self.canvas.configure(scrollregion = self.canvas.bbox('all'))


	# Adding checkbuttons for alternatives in the new frame

	def add_alternatives_list(self):
		self.check_dic = {}

		for item in self.not_found:
			Label(self.listbox , text = f"{item}" ,font = "Helvetica 20 bold", bg = "grey" , relief = RIDGE ,borderwidth = 2).pack(fill = "x" , expand = "true")

			if self.alternates[item] != []:
				if len(self.alternates[item]) > 3:
					for alter in self.alternates[item][:3]:
						self.check_var = IntVar()
						self.check = Checkbutton(self.listbox ,font = "Helvetica 10 ", text =alter,variable = self.check_var , relief = RAISED , borderwidth = 2).pack(fill = "x", expand = "true")
						self.check_dic[alter] = self.check_var

				else:
					for alter in self.alternates[item]:
						self.check_var = IntVar()
						self.check = Checkbutton(self.listbox ,font = "Helvetica 10 ", text =alter,variable = self.check_var , relief = RAISED , borderwidth = 2).pack(fill = "x", expand = "true")
						self.check_dic[alter] = self.check_var


	# Redirecting to the main window

	def back_to_main(self):
		self.alter_label.pack_forget()
		self.list_frame.pack_forget()
		self.buttons.pack_forget()

		self.add_menubar()
		self.add_text_window()
		self.add_button()
		self.add_status()
		self.attributes("-topmost", False)
		self.geometry("600x465")


	def add_alter_to_cart(self):
		values = [item for item, var in self.check_dic.items() if var.get() == 1]
		self.order.func_reorder(values)
		tmsg.showinfo("Success","All products are added to your cart :)")
		ans = tmsg.askquestion("","Do you want to add more ? ")
		if ans == "yes":
			self.back_to_main()

		else:
			self.quit()

	# Adding status bar in the bottom of the main window
	def add_status(self):

		self.sbar = Label(self,textvariable = self.var , relief = SUNKEN , anchor = "w")

		self.sbar.pack(side = BOTTOM , fill=X)




if __name__ == '__main__':
	app = GUI()
	app.add_menubar()
	app.add_text_window()
	app.add_button()
	app.add_status()
	app.mainloop()