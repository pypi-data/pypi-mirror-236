import pygame
from hellopy.gameobject.gameobject import GameObject, rotate_point
from hellopy.collision import CollisionComponent
from hellopy.window import window

# 多边形函数
def polygon(points=[(100,50),(200,60),(210,160),(110,170)],color="yellow"):
    pygame.draw.polygon(window.screen,color,points)

# 多边形类
class Polygon(GameObject,CollisionComponent):
    def __init__(self,points=[(100,50),(200,60),(210,160),(110,170)],color="red"):
        self.points = points
        super().__init__(self.get_rect())
        self.color = color
        self.scale = 1
        self.line_width = 1
        self.angle = 0
        self.x = self.get_center()[0]
        self.y = self.get_center()[1]
        self.w = self.get_rect()[2]
        self.h = self.get_rect()[3]
        self.v_from_center = self.get_vectors()
    def get_vectors(self):
        nps=[]
        for p in self.points:
            nps.append((p[0]-self.x, p[1]-self.y))
        return nps
    def get_rect(self):
        x_list = []
        y_list = []
        for dot in self.points:
            x_list.append(dot[0])
            y_list.append(dot[1])
        return (min(x_list),min(y_list),max(x_list)-min(x_list),max(y_list)-min(y_list))
    def draw(self):
        self.update_points()
        pygame.draw.polygon(window.screen,self.color,self.points)
    def stroke(self):
        self.update_points()
        pygame.draw.polygon(window.screen,self.color,self.points,self.line_width)
    def update_points(self):
        # 更新位置
        nps = []
        for p in self.v_from_center:
            nps.append((self.x+p[0]*self.scale,self.y+p[1]*self.scale))
        self.points = nps.copy()
    def get_center(self):
        x_list = []
        y_list = []
        for dot in self.points:
            x_list.append(dot[0])
            y_list.append(dot[1])
        return (sum(x_list)//len(x_list), sum(y_list)//len(y_list))
    
    def rotate(self,angle=90,rotate_center=None):
        # 旋转一个角度
        rc = (self.x,self.y)
        if rotate_center != None:
            rc = rotate_center
        nc = rotate_point(rc,(self.x,self.y),angle)
        self.x = nc[0]
        self.y = nc[1]
        nps = []
        for p in self.v_from_center:
            nps.append(rotate_point((0,0),p,angle))
        self.v_from_center = nps.copy()
        self.angle = (self.angle + angle) % 360
    def rotate_to(self,angle=90,rotate_center=None):
        # 旋转到某个角度
        a = (angle - self.angle)
        rc = (self.x,self.y)
        if rotate_center != None:
            rc = rotate_center
        nc = rotate_point(rc,(self.x,self.y),a)
        nps = []
        for p in self.v_from_center:
            nps.append(rotate_point((0,0),p,a))
        self.v_from_center = nps.copy()
        self.angle = angle % 360
    def set_scale(self,scale):
        self.scale = scale