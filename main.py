import tkinter as tk
import numexpr as ne
from scipy import integrate

window = tk.Tk()

CANVASSIZE = 480

canvas = tk.Canvas(width=CANVASSIZE, height=CANVASSIZE, bg='#FFFFFF')

functionEntry = tk.Entry()
scaleXEntry = tk.Entry()
scaleYEntry = tk.Entry()
lim1Entry = tk.Entry()
lim2Entry = tk.Entry()
resolutionEntry = tk.Entry()


def translateToCanvas(coords):
    x = coords[0]
    y = coords[1]
    x += round(CANVASSIZE / 2)
    y += round(CANVASSIZE / 2)
    return [x, y]


def createGraph():
    centre = round(CANVASSIZE / 2)
    canvas.create_line(centre, 0, centre, CANVASSIZE + 10)
    canvas.create_line(0, centre, CANVASSIZE + 10, centre)
    canvas.place(x=0, y=0)


def createTicks(coords, place):
    coords = translateToCanvas(coords)
    if place == 'x':
        canvas.create_line(coords[0], coords[1] - 5, coords[0], coords[1] + 5, tags='ticks')
    else:
        canvas.create_line(coords[0] - 5, coords[1], coords[0] + 5, coords[1], tags='ticks')


# Work on area finding, turn string into operable nump integrand
def findArea():
    pass
    canvas.delete('area')
    result = integrate.quad(functionEntry.get())
    canvas.create_text(CANVASSIZE * 0.3, CANVASSIZE * 0.3, tags='area')


areaButton = tk.Button(text='Find area', command=findArea)


def drawScaleMark(coords, x, place):
    coords = translateToCanvas(coords)
    if place == 'x':
        canvas.create_text(coords[0], coords[1] - 10, text=f'{x}', tags='scale')
    else:
        canvas.create_text(coords[0] + 20, coords[1], text=f'{x}', tags='scale')


def drawFunction():
    scaleX = float(scaleXEntry.get())
    scaleY = float(scaleYEntry.get())
    f = functionEntry.get()
    # Scaling of the axis'
    canvas.delete('ticks')
    canvas.delete('scale')
    canvas.delete("y")
    canvas.delete("x")
    canvas.delete("points")
    canvas.delete("function")
    # noinspection PyArgumentList
    canvas.create_text(0.1 * CANVASSIZE, 0.03 * CANVASSIZE, text=f'y = {f}', tag="function")
    # noinspection PyArgumentList
    canvas.create_text(CANVASSIZE / 2 + 0.05 * CANVASSIZE, 0.03 * CANVASSIZE, text='y', tag="y")
    # noinspection PyArgumentList
    canvas.create_text(CANVASSIZE - 0.03 * CANVASSIZE, CANVASSIZE / 2 - 0.05 * CANVASSIZE, text='x', tag="x")
    for i in range(int(round(-CANVASSIZE / 2)), int((round(CANVASSIZE / 2)) + 1)):
        x = i
        nx = scaleX * x
        temp = f.replace('x', f'{nx}')
        y = ne.evaluate(temp) * -1
        Ny = i * 1 / scaleY
        ny = y * scaleY
        if x % float(resolutionEntry.get()) == 0:
            createTicks([x, 0], 'x')
            drawScaleMark([x, 0], nx, 'x')
            # Have to make the y scaling independent of the x-axis.
            createTicks([0, x], 'y')
            drawScaleMark([0, x], -Ny, 'y')
        coords = [x, ny]
        coords = translateToCanvas(coords)
        # noinspection PyArgumentList
        canvas.create_oval(coords[0] - 1, coords[1] - 1, coords[0] + 1, coords[1] + 1, tag='points')
    canvas.update()


displayButton = tk.Button(text='Display', command=drawFunction)


def placeLabels():
    functionLabel = tk.Label(text='Function:')
    scaleXLabel = tk.Label(text='Scaling x factor:')
    scaleYLabel = tk.Label(text='Scaling y factor:')
    resolutionLabel = tk.Label(text='Resolution of axis:')
    area1Label = tk.Label(text='Input 1st limit of area')
    area2Label = tk.Label(text='Input 2nd limit of area')
    array = [functionLabel, functionEntry, scaleXLabel, scaleXEntry, scaleYLabel, scaleYEntry, resolutionLabel,
             resolutionEntry, displayButton, area1Label, lim1Entry, area2Label, lim2Entry, areaButton]
    for i, thing in enumerate(array):
        thing.place(x=485, y=i * 25)


def createWindow():
    window.title('Graph Plotter')
    window_width = 640
    window_height = 480
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.resizable(False, False)
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


createWindow()
createGraph()
placeLabels()

window.mainloop()
