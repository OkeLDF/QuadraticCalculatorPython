import matplotlib.pyplot as plot
import turtle
import tkinter as tk
from tkinter import ttk

# Data processing

class Equation:
    def __init__(self, a:float, b:float, c:float) -> None:
        self.set_coeficients(a, b, c)

    def __init__(self) -> None:
        self.a = 0
        self.b = 0
        self.c = 0
        self.x1 = 0
        self.x2 = 0
        self.delta = 0
        self.roots_quantity = 0

    def set_coeficients(self, a:float = 0, b:float = 0, c:float = 0) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.x1 = 0
        self.x2 = 0
        self.delta = 0
        self.roots_quantity = 0
        self.calculate()

    def calculate(self) -> None:
        if(self.a == self.b == self.c == 0):
            self.x1 = 0
            self.x2 = 0
            self.delta = 0
            self.roots_quantity = 0

        elif self.a:
            self.delta = (self.b*self.b) - (4 * self.a * self.c)
            self.roots_quantity = 2

            if self.delta > 0:
                self.x1 = (-self.b + self.delta**(1/2)) / (2*self.a) 
                self.x2 = (-self.b - self.delta**(1/2)) / (2*self.a)

            elif self.delta == 0:
                self.x1 = (-self.b + self.delta**(1/2)) / 2*self.a
                self.x2 = self.x1
                self.roots_quantity = 1
            
            else:
                self.x1 = -self.b/(2*self.a)
                self.x2 = ((-self.delta)**(1/2)) / (2*self.a)

        else:
            self.x1 = -(self.c/self.b)
            self.x2 = self.x2
            self.roots_quantity = 1

    def plot(self) -> None:
        x_axis = range(-100, 100)
        y_axis = []
        for x in x_axis:
            y_axis.append((self.a*x**2) + self.b*x + self.c)

        plot.plot(x_axis, y_axis, marker='.')
        plot.xlabel('X')
        plot.ylabel('Y')
        plot.title('Gráfico de %ix^2 + %ix + %i' % (self.a, self.b, self.c))
        plot.grid(True)
        plot.show()

    def __str__(self) -> str:
        string = '%.1f x² + %.1f x + %.1f = 0' % (self.a, self.b, self.c)
        string += '\n\ndelta: %.3f\nnúmero de raízes: %i' % (self.delta, self.roots_quantity)
        
        if self.delta<0:
            string += '\n\nx1 = %.3f + %.3f * i\nx2 = %.3f - %.3f * i' % (self.x1, self.x2, self.x1, self.x2)

        else:
            string += '\n\nx1 = %.3f\nx2 = %.3f' % (self.x1, self.x2)

        return string
    
# Start program class

class StartProgram(tk.Tk):
    def setWindow(self) -> None:
        super().__init__()
        x, y = int(self.winfo_screenwidth()/2-(self.SP_W/2)), int(self.winfo_screenheight()/2-(self.SP_H/2))
        self.geometry(f'{self.SP_W}x{self.SP_H}+{x}+{y}')
        self.overrideredirect(1)
        self.canvas = tk.Canvas(master = self, width = self.SP_W, height = self.SP_H, )
        self.canvas.pack()

    def drawTurtle(self) -> None:
        halfW = self.SP_W/2
        halfH = self.SP_H/2
        t = turtle.RawTurtle(self.canvas)
        
        t.hideturtle()
        t.speed('fast')
        t.pensize(2)

        t.penup()
        t.goto(0, -halfH+10)
        t.pendown()
        t.goto(0, halfH-10) # y axis

        t.penup()
        t.goto(-halfW+10, 0)
        t.pendown()
        t.goto(halfW-10, 0) # x axis

        f = lambda x:((0.005*(x**2))-100)

        t.penup()
        t.goto(-halfW+10, f(-halfW+10))
        t.pencolor('red')
        t.pensize(3)
        t.pendown()
        t.speed('fastest') # setup of function draw

        for i in range(-int(halfW)+10, int(halfW), 10):
            t.goto(i, f(i)) # curve of the quadratic

        t.penup()
        t.speed('slowest')
        t.forward(100) # wait a bit

    def __init__(self) -> None:
        self.SP_W = 400
        self.SP_H = 300

        self.setWindow()
        self.drawTurtle()
        self.destroy()

# Main Panel classes

class Coeficient(ttk.Entry):
    def __init__(self, master) -> None:
        super().__init__(
            master=master,
            width=50,
            font='Verdana 14')

class CoeficientsPanel:
    def __init__(self, root) -> None:
        self.frame = ttk.Frame(root)
        self.frame.pack()

        self.coeficients = [
            Coeficient(self.frame),
            Coeficient(self.frame),
            Coeficient(self.frame)
        ]
        for i, e in enumerate(self.coeficients):
            e.grid(row=i, column=1, pady=10, padx=10)
            e.insert(0, '')

        for i, t in enumerate(['a', 'b', 'c']):
            ttk.Label(
                self.frame,
                anchor=tk.E,
                text=t,
                font='Times 14 bold italic',
                padding=10
            ).grid(row=i, column=0)

    def get_coeficients(self) -> tuple:
        return self.coeficients[0].get(), self.coeficients[1].get(), self.coeficients[2].get()

class Result:
    def __init__(self, root, label:str = '', content:str = '0', width:int = 10) -> None:
        self.frame = ttk.Frame(root, width=width)
        self.labelText = label
        self.content = content

        self.label = ttk.Label(
            self.frame,
            text=self.labelText + ' = ' + content,
            font='Times 20 bold italic')
        self.label.grid(row=0, column=0)

    def grid(self, row:int = 0, column:int = 0) -> None:
        self.frame.grid(row=row, column=column, padx=30)

    def pack(self) -> None:
        self.frame.pack()

    def set_content(self, content:str = '0') -> None:
        self.content = content
        self.label.config(text=self.labelText + ' = ' + content)

    def set_label(self, label:str = '') -> None:
        self.labelText = label
        self.label.config(text=self.labelText + ' = ' + self.content)

class InfoPanel:
    def __init__(self, root) -> None:
        self.frame = ttk.Frame(root)
        self.frame.pack()

        self.show_equation()
        self.show_results()

        self.other_info = ttk.Frame(self.frame)
        self.other_info.pack()
        self.show_delta()
        self.show_nraizes()

    def show_equation(self) -> None:
        self.equation_frame = ttk.Frame(self.frame)
        self.equation_frame.pack(pady=10)
        self.equation = Result(self.equation_frame, label='ax² + bx + c')
        self.equation.pack()

    def show_results(self) -> None:
        self.results_frame = ttk.Frame(self.frame)
        self.results_frame.pack(pady=10)
        self.x1 = Result(self.results_frame, label="x'")
        self.x2 = Result(self.results_frame, label="x''")
        self.x1.grid(row=0, column=0)
        self.x2.grid(row=0, column=1)

    def show_delta(self) -> None:
        self.delta_frame = ttk.Frame(self.other_info)
        self.delta_frame.pack(pady=10, padx=30, side='left')
        self.delta = Result(self.delta_frame, label='delta')
        self.delta.pack()

    def show_nraizes(self) -> None:
        self.nraizes_frame = ttk.Frame(self.other_info)
        self.nraizes_frame.pack(pady=10, padx=30, side='left')
        self.nraizes = Result(self.nraizes_frame, label='n roots')
        self.nraizes.pack()

    def set_results(self, eq:Equation = None) -> None:
        self.equation.set_label('%.1fx² + %.1fx + %.1f' % (eq.a, eq.b, eq.c))
        
        if eq.delta>=0:
            self.x1.set_content('%.4f' % eq.x1)
            self.x2.set_content('%.4f' % eq.x2)
        else:
            imaginary = abs(eq.x2)
            self.x1.set_content('%.3f + %.3f * i' % (eq.x1, imaginary))
            self.x2.set_content('%.3f - %.3f * i' % (eq.x1, imaginary))

        self.delta.set_content('%.4f' % eq.delta)
        self.nraizes.set_content(str(eq.roots_quantity))

class MainPanel(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.eq = Equation()

        self.width = 720
        self.height = 480
        centerx, centery = int(self.winfo_screenwidth()/2-(self.width/2)), int(self.winfo_screenheight()/2-(self.height/2))
        self.geometry(f'{self.width}x{self.height}+{centerx}+{centery}')
        self.title('Quadratic Calculator (Python edition)')

        self.set_style()
        
        self.frame = ttk.Frame(self, padding=15)
        self.frame.pack()
        self.coef_panel = CoeficientsPanel(self.frame)
        self.info_panel = InfoPanel(self.frame)

        self.btn_panel = ttk.Frame(self.frame)
        self.btn_panel.pack(pady=30)

        self.calcular_btn = ttk.Button(self.btn_panel, text='Calculate', padding=10, command=self.calculate)
        self.showGraph_btn = ttk.Button(self.btn_panel, text='Show graph', padding=10, command=self.showGraph)
        self.calcular_btn.pack(side='left', padx=20)
        self.showGraph_btn.pack(side='left', padx=20)

    def calculate(self) -> None:
        coefs = self.coef_panel.get_coeficients()
        try:
            self.eq.set_coeficients(float(coefs[0]), float(coefs[1]), float(coefs[2]))
            self.info_panel.set_results(self.eq)
        except ValueError:
            print('Conversão para INT falhou:', coefs)

    def showGraph(self) -> None:
        minx, maxx = -100, 100
        
        if self.eq.x1 <= -100 or self.eq.x2 <= -100:
            minx = min([self.eq.x1, self.eq.x2]) - 100

        if self.eq.x1 >= 100 or self.eq.x2 >= 100:
            maxx = max([self.eq.x1, self.eq.x2]) + 100

        x_axis = range(int(minx), int(maxx))
        y_axis = []

        for x in x_axis:
            y_axis.append((self.eq.a*(x**2)) + (self.eq.b*x) + self.eq.c)

        miny, maxy = min(y_axis),max(y_axis)
        if miny > 0: miny = 0
        if maxy < 0: maxy = 0

        plot.plot([minx, maxx], [0,0], marker='', color='black')
        plot.plot([0,0], [miny, maxy], marker='', color='black')
        plot.text(102,0,'X')
        plot.text(0,maxy+3,'Y')
        plot.plot(x_axis, y_axis, marker='.')
        plot.xlabel('X')
        plot.ylabel('Y')
        plot.title('Gráfico de %.2fx^2 + %.2fx + %.2f' % (self.eq.a, self.eq.b, self.eq.c))
        plot.grid(True)
        plot.show()

    def set_style(self) -> None:
        style = ttk.Style()
        style.configure('TButton',
            font='Courier 16 bold')

if __name__ == '__main__':
    StartProgram()
    MainPanel().mainloop()