import queue
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
from unit import unit
from ga import GA
from tkinter.simpledialog import askinteger
from queue import Queue
import copy
import ga_thread

class mygui:

    def __init__(self, master):
        self.master = master
        self.n_units = 0
        self.n_intervals = 0
        self.ref_list = []
        self.top = self.top_result = None
        self.queue = Queue()

        frm = tkinter.Frame(master)
        frm.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.title('Assignment 2: The Plant Maintenance Problem')
        master.resizable(False, False)
        master.geometry('600x300')
        frm.grid_columnconfigure(0, weight=1)

        greeting = tkinter.Label(frm, text="Please load problem file by clicking button below",
                                 font=(None, 16))
        greeting.grid(row=0, column=0)

        filebtn = tkinter.Button(frm, text='Load File', command=lambda: self.mouseclick(frm))
        filebtn.grid(row=1, column=0, sticky='N')
        exitbtn = tkinter.Button(frm, text="Quit", command=root.destroy)
        exitbtn.grid(row=6, column=0, sticky='N')

        for r in range(frm.grid_size()[1]):
            frm.rowconfigure(r, weight=1)

    def queue_checkert(self):
        if not self.queue.empty():
            try:
               self.draw_result(self.queue.get())
            except queue.Empty:
                pass
        else:
            self.master.after(200, lambda: self.queue_checkert())

    def draw_result(self, result):
        self.top_result = tkinter.Toplevel(self.master)
        self.top_result.grab_set()
        w = int(self.master.winfo_screenwidth()*0.7)
        h = int(self.master.winfo_screenheight()*0.7)
        geo = "%dx%d" % (w, h)
        self.top_result.geometry(geo)
        frm = tkinter.Frame(self.top_result, width=w, height=h)
        frm.grid(row=0, column=0, sticky=tkinter.NSEW)
        canv = tkinter.Canvas(frm, width=w, height=h)
        opt_label = tkinter.Label(frm, text="The optimal schedule")
        opt_label.grid(row=0, column=0)

        cell_size = int(self.master.winfo_screenwidth() * 0.5 / self.n_units)

        for i in range(0, self.n_units):
            canv.create_text((i*cell_size)+(cell_size/2)+60, 10, text="unit" + str(i+1))
        for i in range(0, self.n_intervals):
            canv.create_text(25, (i*cell_size)+(cell_size/2)+35, text="interval" + str(i+1))

        for i in range(self.n_intervals):
            for j in range(self.n_units):
                canv.create_rectangle(cell_size*j+60, (cell_size*i)+35, cell_size*(j+1)+60, cell_size*(i+1)+35, fill='white', outline='black')

        canv.grid(row=1, column=0, sticky=tkinter.NSEW)
        for ind, i in enumerate(zip(*result)):
            for ind2, j in enumerate(i):
                if j == '1':
                    canv.create_text((ind2*cell_size)+(cell_size/2)+60, (ind*cell_size)+(cell_size/2)+35, text="*", font=(None, 20))




    def run_ga(self):
        userinputs = []
        children = self.top.winfo_children()[0].winfo_children()
        for child in children:
            if 'Entry' in child.winfo_class():
                userinputs.append(child.get())
        user_pop_size = int(userinputs[0])
        user_tournament_size = int(userinputs[1])
        user_gen = int(userinputs[2])
        self.top.grab_release()
        self.top.destroy()

        gt = ga_thread.GaThread(self.queue, user_pop_size, user_tournament_size, user_gen, self.ref_list, self.n_intervals)
        gt.start()
        self.queue_checkert()

    def user_input_window(self):
        self.top = tkinter.Toplevel(self.master)
        self.top.grab_set()
        self.top.geometry("700x200")
        self.top.grid_columnconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.top.title("Configuration")
        top_frm = tkinter.Frame(self.top)
        top_frm.grid(row=0, column=0, sticky="nsew")
        top_frm.config()
        self.top.children
        instruction = tkinter.Label(top_frm,
                                    text="Defaults for the following paramters have been set as follow. \n Please "
                                         "modify should you wish to do so.",
                                    font=(None, 12))
        instruction.grid(row=0, column=0, columnspan=3)
        pop_label = tkinter.Label(top_frm, text="Population size:", font=(None, 12))
        pop_label.grid(row=3, column=0)
        tour_label = tkinter.Label(top_frm, text="Tournament size:", font=(None, 12))
        tour_label.grid(row=3, column=1)
        gen_label = tkinter.Label(top_frm, text="Number of generations:", font=(None, 12))
        gen_label.grid(row=3, column=2)
        pop_entry = tkinter.Entry(top_frm)
        pop_entry.grid(row=4, column=0)
        pop_entry.insert(0, '100')
        tour_entry = tkinter.Entry(top_frm)
        tour_entry.grid(row=4, column=1)
        tour_entry.insert(0, '8')
        gen_entry = tkinter.Entry(top_frm)
        gen_entry.grid(row=4, column=2)
        gen_entry.insert(0, '100')

        solve_btn = tkinter.Button(top_frm, text="Solve", command=self.run_ga)
        solve_btn.grid(row=6, column=1)

        for r in range(top_frm.grid_size()[1]):
            top_frm.rowconfigure(r, minsize=25, weight=1)
        for s in range(top_frm.grid_size()[0]):
            top_frm.columnconfigure(s, minsize=50, weight=1)

    def mouseclick(self, frame: tkinter.Frame):
        file = tkinter.filedialog.askopenfile(mode='r', title="Select file",
                                              filetypes=[("text files", ".txt")])
        if not file:
            return
        else:
            self.n_units = int(file.readline())
            self.n_intervals = int(file.readline())

            for r in range(self.n_units):
                temp = unit()
                st = file.readline().split()
                temp.num = int(st[0])
                temp.capacity = int(st[1])
                temp.required_int = int(st[2])
                self.ref_list.append(temp)

            file.close()
            loaded_lbl = tkinter.Label(frame, text="File loaded. Press 'solve' button to run genetic algorithm",
                                       font=('Times New Roman', 16))
            loaded_lbl.grid(row=2, column=0)
            solve_btn = tkinter.Button(frame, text='Solve', command=self.user_input_window)
            solve_btn.grid(row=3, column=0)


root = tkinter.Tk()
my_gui = mygui(root)

root.mainloop()
