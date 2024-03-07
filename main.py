import pygame
import numpy
import pygame_widgets
from pygame_widgets.slider import Slider

print("Witaj w Armacie!!!")
print("Szybka uwaga - strzelasz PRAWYM PRZYCISKIEM!!!")

width=1000
height=600
run=True
alfa=0
g=10
punkty=0
black=(0,0,0)
white=(255,255,255)
kulaRadius=2
przeciwnikHeight=30
przeciwnikWidth=20
def rownanieX(t):
    x=v0*t*numpy.cos(alfa)
    return x

def generujPrzeciwnika():
    xPrzeciwnika = numpy.random.randint(maksZasieg - 200, maksZasieg)
    yPrzeciwnika = height-30
    RysujPrzeciwnika(xPrzeciwnika, yPrzeciwnika)
    return xPrzeciwnika,yPrzeciwnika

def RysujPrzeciwnika(x,y):
    pygame.draw.rect(screen, white, (x, y, przeciwnikWidth, przeciwnikHeight))

def sprawdzKolizje(x0,y0):
    if x0+kulaRadius>=xPrzeciwnika and x0+kulaRadius<=xPrzeciwnika+przeciwnikWidth:
        if y0-kulaRadius>=yPrzeciwnika and y0+kulaRadius<=yPrzeciwnika+przeciwnikHeight:
            return True
    if x0-kulaRadius>=xPrzeciwnika and x0+kulaRadius<=xPrzeciwnika+przeciwnikWidth:
        if y0-kulaRadius>=yPrzeciwnika and y0+kulaRadius<=yPrzeciwnika+przeciwnikHeight:
            return True
    return False
def rownanieY(t):
    y=v0*t*numpy.sin(alfa)-(g*(t*t))/2
    return y

def drawArmata(length,angle):
    pygame.draw.line(screen,white,(0,height),(length*numpy.cos(angle),height-length*numpy.sin(angle)),5)

def obliczKat():
    x, y = pygame.mouse.get_pos()
    y = height - y
    if(x<=0):
        return 0
    kat = numpy.arctan(y / x)
    return kat

def draw(x,y,widthText,heightText,string):
    pygame.draw.rect(screen,black,(x,y,widthText,heightText))
    text = font.render(string, True, white, black)
    textRect = text.get_rect()
    textRect.center = (x,heightText/2)
    screen.blit(text,textRect)
n=30
czas=numpy.linspace(0,n,n*10)

pygame.init()

font=pygame.font.Font('freesansbold.ttf',16)

screen=pygame.display.set_mode((width,height))

slider=Slider(screen,30,50,50,10,min=20,max=100,initial=60)

v0=slider.getValue()
maksZasieg = ((v0 * v0) * numpy.sin(2 * 0.7854)) / g
xPrzeciwnika, yPrzeciwnika = generujPrzeciwnika()
czyPrzeciwnik = True
draw(width-70,10,50,30,"Punkty "+str(punkty))
while run:
    v0=slider.getValue()
    draw(80,10,50,30,"Moc armaty to - "+str(v0))
    maksZasieg = ((v0 * v0) * numpy.sin(2 * 0.7854)) / g
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            alfa=obliczKat()
            for i in range(len(czas)-1):
                screen.fill(black)
                RysujPrzeciwnika(xPrzeciwnika, yPrzeciwnika)
                draw(width-100,10,30,30,"Punkty : "+str(punkty))
                drawArmata(20,alfa)
                x0=rownanieX(czas[i])
                y0=height-rownanieY(czas[i])
                if y0>height:
                    break
                pygame.draw.circle(screen,white,(x0,y0),2)
                pygame.time.delay(10)
                pygame.display.update()
                if sprawdzKolizje(x0,y0):
                    czyPrzeciwnik = False
                    punkty+=1
                    screen.fill(black)
                    drawArmata(20,alfa)
                    draw(width-100,10,30,30,"Punkty : "+str(punkty))
                    xPrzeciwnika,yPrzeciwnika=generujPrzeciwnika()
                    break
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,(0,0,0),(0,height-20,20,20))
            drawArmata(20,obliczKat())
        pygame_widgets.update(events)
        pygame.display.update()
pygame.quit()

