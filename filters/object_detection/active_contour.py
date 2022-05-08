from PyQt5.QtGui import QPixmap
from ..filter import Filter
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QDoubleValidator 
import qimage2ndarray
import numpy as np
import enum
import matplotlib.pyplot as plt
from PyQt5.QtCore import QPoint
import seaborn as sns

class PHI_VALUE(enum.Enum):
    BACKGROUND = 3
    LOUT = 1
    LIN = -1
    OBJECT = -3
class ActiveContour():
        
    def __init__(self):
        super().__init__()
        self.sup_left_qpoint = None
        self.inf_right_qpoint = None
        self.epsilon = 0.1
        self.max_iter = 100
        self.object_thetas = None
        self.phi_mask = None
        self.Lin = None
        self.Lout = None

    def apply(self, img_arr: np.ndarray): 
        
        # 1.1 Indicar la region inicial con un rectangulo dentro del objeto de interes 
        if self.object_thetas is None:
            obj_region, self.object_thetas = self.get_initial_region(img_arr, self.sup_left_qpoint, self.inf_right_qpoint)
        
        # 1.2 Definir Lout (puntos de borde fuera del objeto) y Lin (puntos de borde dentro del objeto)   
        if self.phi_mask is None:
            self.phi_mask = self.calculate_phi_mask(img_arr)
        if self.Lin is None:
            self.Lin = self.calculate_border(self.phi_mask, self.is_Lin, PHI_VALUE.LIN.value)
        if self.Lout is None:
            self.Lout = self.calculate_border(self.phi_mask, self.is_Lout, PHI_VALUE.LOUT.value)
     
        # Actualizar bordes

        iterations_limits = []
        i = 0
        while i < self.max_iter and not self.end_condition(img_arr):
        
            self.update_edges(img_arr)
           
            iterations_limits.append([np.array(list(self.Lin)),np.array(list(self.Lout))])     # draw all iterations figures
        
            #self.plot_phi_mask(self.phi_mask)

            i += 1

        if self.end_condition(img_arr):
            print(f"END CONDITION MET with i={i}")

        return iterations_limits
    

    def in_bounds_arr(self, arr, w, h):
        return arr[(arr[:,0] >= 0) & (arr[:,0] < h) & (arr[:,1] >= 0) & (arr[:,1] < w)]
                
    DIRECTIONS = np.array([
            [-1, 0], #top
            [0, -1], #left
            [0, 1], #right
            [1, 0] #bottom
            ])
    def get_neighbours(self, x, y) -> np.ndarray:
        return np.array([x,y]) + ActiveContour.DIRECTIONS

    def is_Lin(self, x: int, y: int, phi_mask: np.ndarray) -> bool:
        n_idxs = self.in_bounds_arr(self.get_neighbours(x,y), phi_mask.shape[1], phi_mask.shape[0])
        # print(n_idxs)
        # print("phy mask type: ",type(phi_mask))
        # print(phi_mask[n_idxs[:,0], n_idxs[:,1]])
        # print(phi_mask[n_idxs[:,0], n_idxs[:,1]] > 0)
        # print(np.any(phi_mask[n_idxs[:,0], n_idxs[:,1]] > 0))
        # print(phi_mask[x,y] < 0)
        return phi_mask[x,y] < 0 and np.any(phi_mask[n_idxs[:,0], n_idxs[:,1]] > 0)
    
    def is_Lout(self, x: int, y: int, phi_mask: np.ndarray) -> bool:
        # print("phy mask type: ",type(self.phi_mask))
        # print(phi_mask[n_idxs[:,0], n_idxs[:,1]])
        n_idxs = self.in_bounds_arr(self.get_neighbours(x,y), phi_mask.shape[1], phi_mask.shape[0])
        return phi_mask[x,y] > 0 and np.any(phi_mask[n_idxs[:,0], n_idxs[:,1]] < 0)

    def get_initial_region(self, img_arr, sup_left_qpoint: QPoint, inf_right_qpoint: QPoint) -> tuple:
        #sup_left_point = (x,y) 
        rectangle = img_arr[sup_left_qpoint.x():inf_right_qpoint.x(), sup_left_qpoint.y():inf_right_qpoint.y()]
        object_thetas = np.mean(rectangle, axis=(0,1))
        return rectangle, object_thetas # thetas = object colors by channel


    def calculate_phi_mask(self, img_arr: np.ndarray):
       # phi(x) = 3 si x es fondo, 1 si esta en lout, -1 si estan en lin, -3 si esta en el objeto
        phi_mask = np.ones((img_arr.shape[0], img_arr.shape[1])) * PHI_VALUE.BACKGROUND.value                                                       # Background
        phi_mask[self.sup_left_qpoint.x():self.inf_right_qpoint.x(), self.sup_left_qpoint.y():self.inf_right_qpoint.y()] = PHI_VALUE.OBJECT.value   # Object
        return phi_mask

    def calculate_border(self, phi_mask: np.ndarray, comparator, update_value: int):
        print(type(comparator))
        height = phi_mask.shape[0]
        width = phi_mask.shape[1]
        LBorder = set()
        #TODO(scott): mejorar
        for i in range(height):
            for j in range(width):
                if(comparator(i,j,phi_mask)): # Interior Edge
                    phi_mask[i,j] = update_value
                    LBorder.add((i,j))
        return LBorder
    
    def Fd(self, pixel_thetas: np.ndarray) -> int:
         
        if np.linalg.norm(pixel_thetas - self.object_thetas) < self.epsilon: 
            return 1    # Is in object of interest
        else:
            return -1 
         

    def update_edges(self, img_arr: np.ndarray): 
        for ix, iy in self.Lout.copy(): 
            pixel = img_arr[ix, iy]

            # Convert to Lin
            if self.Fd(pixel) > 0: 
                self.Lout.remove((ix, iy))
                self.Lin.add((ix, iy))
                self.phi_mask[ix, iy] = PHI_VALUE.LIN.value
                # Add neihbours to Lout
                for neighbour in self.get_neighbours(ix, iy):
                    if self.phi_mask[neighbour[0], neighbour[1]] == PHI_VALUE.BACKGROUND.value: 
                        self.Lout.add((neighbour[0], neighbour[1]))
                        self.phi_mask[neighbour[0], neighbour[1]] = PHI_VALUE.LOUT.value

        # remove old internal edge 
        for ix, iy in self.Lin.copy(): 
            if not self.is_Lin(ix, iy, self.phi_mask): 
                self.Lin.remove((ix, iy))

        # IDEM FOR LIN
        for ix, iy in self.Lin.copy(): 
            pixel = img_arr[ix, iy]

            # Convert to Lout
            if self.Fd(pixel) < 0: 
                self.Lin.remove((ix, iy))
                self.Lout.add((ix, iy))
                self.phi_mask[ix, iy] = PHI_VALUE.LOUT.value
                # Add neihbours to Lin
                for neighbour in self.get_neighbours(ix, iy):
                    if self.phi_mask[neighbour[0], neighbour[1]] == PHI_VALUE.OBJECT.value: 
                        self.Lin.add((neighbour[0], neighbour[1]))
                        self.phi_mask[neighbour[0], neighbour[1]] = PHI_VALUE.LIN.value
        
        # remove old internal edge 
        for ix, iy in self.Lout.copy(): 
            if not self.is_Lout(ix, iy, self.phi_mask): 
                self.Lout.remove((ix,iy))
    
    # def update_edges(self, img_arr: np.ndarray, object_thetas: np.ndarray, L_type): 
        
    #     if L_type == "Lin": 
    #         Lincrease = self.Lin
    #         Ldecrease = self.Lout 

    #     elif L_type == 'Lout': 
    #         Lincrease = self.Lout
    #         Ldecrease = self.Lin 
        
    #     for ix, iy in Lincrease.copy(): 
    #         pixel = img_arr[ix, iy]

    #         # Convert to Lincrease
    #         if self.Fd(pixel, object_thetas) > 0: 
    #             Lincrease.remove((ix, iy))
    #             Ldecrease.add((ix, iy))
    #             self.phi_mask[ix, iy] = PHI_VALUE.LIN.value
    #             # Add neihbours to Ldecrease
    #             for neighbour in self.get_neighbours(ix, iy):
    #                 if self.phi_mask[neighbour[0], neighbour[1]] == PHI_VALUE.BACKGROUND.value: 
    #                     self.Lout.add((neighbour[0], neighbour[1]))
    #                     self.phi_mask[neighbour[0], neighbour[1]] = PHI_VALUE.LOUT.value

    #     # remove old internal edge 
    #     for ix, iy in Ldecrease.copy(): 
    #         self.remove_old_edge(L_type, ix, iy)

    # def remove_old_edge(self, L, ix, iy): 
    #     if L == "lin": 
    #         if self.is_Lin(ix, iy): 
    #             np.delete(self.Lin, [[ix, iy]]) 
    #     elif L == "lout": 
    #         if self.is_Lout(ix, iy): 
    #             np.delete(self.Lout, [[ix, iy]])                   
    
    def end_condition(self, img_arr: np.ndarray) -> bool:
    
        return all(list(map(lambda idxs: self.Fd(img_arr[idxs[0],idxs[1]]) > 0, self.Lin))) and all(list(map(lambda idxs: self.Fd(img_arr[idxs[0],idxs[1]]) < 0, self.Lout)))

    def plot_phi_mask(self,phi_mask):
        ax = sns.heatmap(phi_mask, linewidth=0.5)
        plt.show()

    def setSupLeftPoint(self, sup_left_qpoint: QPoint) -> None:
        self.sup_left_qpoint = sup_left_qpoint


    def setInfRightPoint(self, inf_right_qpoint: QPoint) -> None:
        self.inf_right_qpoint = inf_right_qpoint


    def setEpsilon(self, epsilon: float) -> None:
        self.epsilon = epsilon

