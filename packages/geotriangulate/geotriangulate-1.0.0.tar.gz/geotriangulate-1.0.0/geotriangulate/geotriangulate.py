from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Dict, List, Set, Optional
from math import cos, sin, radians, degrees, sqrt, atan
from pprint import pprint

class IntersectError(Exception):
    # ошибка при нахождении пересечения
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

@dataclass
class CartCoords(object):
    x: float
    y: float
    z: float

@dataclass
class SphCoords(object):    
    lon: float
    lat: float

@dataclass
class Plane(object):
    A: float
    B: float
    C: float
    D: float


EarthR = 6371.0088
NPoleCoords = SphCoords(0, 90)
    

class Measurement(object):


    def __init__(self, lon: float, lat: float, alpha: float) -> None:
        self.sphCoords: SphCoords = SphCoords(lon,lat)
        self.alpha: float = alpha
        self.__cartCoords: CartCoords = CartCoords(0,0,0)
        self.__plane: Plane = Plane(0,0,0,0)

        self.calculate_self_cart()
        self.calculate_self_plane()


    @staticmethod
    def calculate_projection(cart: CartCoords) -> SphCoords:
        # Проецирование точки на сферу (проводя линию через начало координат)

        if (cart.x == 0 and cart.y == 0 and cart.z == 0):
            # Обработки для этого нет
            raise RuntimeError("can not project point on sphere (three coords are zero)")

        if (cart.x == 0):
            # Обрабатываем отдельно, так как в тангенсе делим на x
            if (cart.y > 0):
                lon = 90
            else:
                lon = -90

        elif (cart.x * cart.y >= 0):
            if (cart.x > 0):
                lon = degrees(atan(cart.y / cart.x))
            
            else:
                lon = - 180 + degrees(atan(cart.y / cart.x))
        else:
            if (cart.x > 0):
                lon = degrees(atan(cart.y / cart.x))
            else:
                lon = 180 + degrees(atan(cart.y / cart.x))
        

        if (cart.x == 0 and cart.y == 0):
            if (cart.z > 0):
                lat = 90
            else:
                lat = -90
        
        else:
            lat = degrees(atan(cart.z / sqrt((cart.x)**2 + (cart.y)**2)))


        
        return SphCoords(lon, lat)
        
        
        

    @staticmethod
    def calculate_cart(sphcoords: SphCoords) -> CartCoords:
        # Находит декартовы координаты по сферическим (точка на поверхности)
        return CartCoords(
            cos(radians(sphcoords.lat)) * cos(radians(sphcoords.lon)) * EarthR,
            cos(radians(sphcoords.lat)) * sin(radians(sphcoords.lon)) * EarthR,
            sin(radians(sphcoords.lat)) * EarthR
        )
    
    
    
    
    def calculate_self_cart(self) -> None:
        self.__cartCoords = Measurement.calculate_cart(self.sphCoords)

    def calculate_self_plane(self) -> None:
        if (self.__cartCoords == CartCoords(0,0,0)):
            raise RuntimeError("no cartesian")
        
        PoleCords: CartCoords = Measurement.calculate_cart(NPoleCoords)
        
        tan_plane = Plane(
            self.__cartCoords.x,
            self.__cartCoords.y,
            self.__cartCoords.z,
            -self.__cartCoords.x ** 2 - self.__cartCoords.y ** 2 - self.__cartCoords.z ** 2
        )

        # Проецируем на касательную плоскость
        t = (-tan_plane.A * PoleCords.x - tan_plane.B * PoleCords.y - tan_plane.C * PoleCords.z - tan_plane.D) / (tan_plane.A ** 2 + tan_plane.B ** 2 + tan_plane.C ** 2)

        x_proect = tan_plane.A * t + PoleCords.x
        y_proect = tan_plane.B * t + PoleCords.y
        z_proect = tan_plane.C * t + PoleCords.z
        unrot_vec = (x_proect - self.__cartCoords.x, y_proect - self.__cartCoords.y, z_proect - self.__cartCoords.z)

        a_sin = sin(radians(self.alpha))
        a_cos = cos(radians(self.alpha))

        # Нормируем вектор оси
        x_normed = self.__cartCoords.x / sqrt(self.__cartCoords.x ** 2 + self.__cartCoords.y ** 2 + self.__cartCoords.z ** 2)
        y_normed = self.__cartCoords.y / sqrt(self.__cartCoords.x ** 2 + self.__cartCoords.y ** 2 + self.__cartCoords.z ** 2)
        z_normed = self.__cartCoords.z / sqrt(self.__cartCoords.x ** 2 + self.__cartCoords.y ** 2 + self.__cartCoords.z ** 2)
        rot_matrix = (
            (a_cos + (1 - a_cos) * x_normed ** 2, (1 - a_cos) * x_normed * y_normed + a_sin * z_normed, (1 - a_cos) * x_normed * z_normed - a_sin * y_normed),
            ((1 - a_cos) * y_normed * x_normed - a_sin * z_normed, a_cos + (1 - a_cos) * y_normed ** 2, (1 - a_cos) * y_normed * z_normed + a_sin * x_normed),
            ((1 - a_cos) * z_normed * x_normed + a_sin * y_normed, (1 - a_cos) * z_normed * y_normed - a_sin * x_normed, a_cos + (1 - a_cos) * z_normed ** 2)
        )
        
        # Координаты вектора направления
        meas_plane_vector = (
            rot_matrix[0][0] * unrot_vec[0] + rot_matrix[0][1] * unrot_vec[1] + rot_matrix[0][2] * unrot_vec[2],
            rot_matrix[1][0] * unrot_vec[0] + rot_matrix[1][1] * unrot_vec[1] + rot_matrix[1][2] * unrot_vec[2],
            rot_matrix[2][0] * unrot_vec[0] + rot_matrix[2][1] * unrot_vec[1] + rot_matrix[2][2] * unrot_vec[2],
                    
        )

        
        self.plane = Plane(
            self.__cartCoords.y * meas_plane_vector[2] - self.__cartCoords.z * meas_plane_vector[1],
            self.__cartCoords.z * meas_plane_vector[0] - self.__cartCoords.x * meas_plane_vector[2],
            self.__cartCoords.x * meas_plane_vector[1] - self.__cartCoords.y * meas_plane_vector[0],
            0
        )

    


    

    @staticmethod
    def find_inter(m1: Measurement, m2: Measurement) -> CartCoords:
        # Нахождение точек пересечения двух больших кругов
        if (m1.plane == Plane(0,0,0,0) or m2.plane == Plane(0,0,0,0)):
            raise RuntimeError("no plane")
        

        l1 = m1.plane.B * m2.plane.C - m2.plane.B * m1.plane.C
        l2 = m2.plane.A * m1.plane.C - m1.plane.A * m2.plane.C
        l3 = m1.plane.A * m2.plane.B - m2.plane.A * m1.plane.B

        # Если плоскости совпадают, то не учитываем их пересечение
        if (l1 == 0 and l2 == 0 and l3 == 0):
            raise IntersectError("planes are same")

        t1 = EarthR / sqrt(l1**2 + l2**2 + l3**2)
        t2 = - EarthR / sqrt(l1**2 + l2**2 + l3**2)

        dist_point1_to_m1 = sqrt((l1 * t1 - m1.__cartCoords.x) ** 2 + (l2 * t1 - m1.__cartCoords.y) ** 2 + (l3 * t1 - m1.__cartCoords.z) ** 2)
        dist_point1_to_m2 = sqrt((l1 * t1 - m2.__cartCoords.x) ** 2 + (l2 * t1 - m2.__cartCoords.y) ** 2 + (l3 * t1 - m2.__cartCoords.z) ** 2)
        dist_point2_to_m1 = sqrt((l1 * t2 - m1.__cartCoords.x) ** 2 + (l2 * t2 - m1.__cartCoords.y) ** 2 + (l3 * t2 - m1.__cartCoords.z) ** 2)
        dist_point2_to_m2 = sqrt((l1 * t2 - m2.__cartCoords.x) ** 2 + (l2 * t2 - m2.__cartCoords.y) ** 2 + (l3 * t2 - m2.__cartCoords.z) ** 2)

        if (dist_point1_to_m1 + dist_point1_to_m2 < dist_point2_to_m1 + dist_point2_to_m2):
            return CartCoords(l1 * t1, l2 * t1, l3 * t1)
        else:
            return CartCoords(l1 * t2, l2 * t2, l3 * t2)
        

    
class TargObj(object):

    _measurements: Dict[int, Measurement]
    _InterPoints: Dict[int, CartCoords]
    # текущее среднее положение в сферических координатах
    CurMedPos: SphCoords
    # словарь {id измерения : множество точек пересечения с другими измерениями}
    _measurements_points: Dict[int, Set[int]]
    # словарь {id точки : два измерения, которые в ней пересекаются}
    _points_measurements: Dict[int, Tuple[int, int]]

    _last_meas_id: int
    _last_point_id: int

    def __init__(self) -> None:
        self._measurements = {}
        self._InterPoints = {}
        self.CurMedPos = SphCoords(1000,1000)
        self._measurements_points = {}
        self._points_measurements = {}

        self._last_meas_id = 0
        self._last_point_id = 0


    def find_CurMedPos(self) -> None:
        # Находит среднее положение объекта

        if (len(self._InterPoints) == 0):
            self.CurMedPos = SphCoords(1000,1000)
            return
        if (len(self._InterPoints) == 1):
            self.CurMedPos = Measurement.calculate_projection(list(self._InterPoints.values())[0])
            return
        
        x: float = sum(map(lambda v: v.x, self._InterPoints.values())) / len(self._InterPoints)
        y: float = sum(map(lambda v: v.y, self._InterPoints.values())) / len(self._InterPoints)
        z: float = sum(map(lambda v: v.z, self._InterPoints.values())) / len(self._InterPoints)

        # Проекция на сферу

        self.CurMedPos = Measurement.calculate_projection(CartCoords(x,y,z))


    def AddMeasurement(self, m: Measurement) -> Optional[int]:
        # Добавляет измерение возвращает id, присвоенное измерению или None, если такое измерение уже есть


        # Если это первое измерение
        if (len(self._measurements) == 0):
            self._last_meas_id += 1
            self._measurements_points[self._last_meas_id] = set()

            self._measurements[self._last_meas_id] = m

            return self._last_meas_id


            
        else:
            # Проверка измерения на значимость
            
            for cur_meas_id, cur_meas in self._measurements.items():
                try:
                    Measurement.find_inter(m, cur_meas)
                except IntersectError:
                    print("Equivalent measurement already exists")

                    return None
                
            # Если проверка пройдена, то учитываем это измерение
            self._last_meas_id += 1
            self._measurements_points[self._last_meas_id] = set()
                
            for cur_meas_id, cur_meas in self._measurements.items():
                self._last_point_id += 1
                
                new_inter_point: CartCoords = Measurement.find_inter(m, cur_meas)
                
                self._InterPoints[self._last_point_id] = new_inter_point

                self._measurements_points[cur_meas_id].add(self._last_point_id)
                self._measurements_points[self._last_meas_id].add(self._last_point_id)

                self._points_measurements[self._last_point_id] = (cur_meas_id, self._last_meas_id)
            
            self._measurements[self._last_meas_id] = m

            # Пересчитываем среднее значение
            self.find_CurMedPos()

            return self._last_meas_id

    def DeleteMeasurement(self, meas_id: int) -> None:
        # Удаляет измерение по id

        if (meas_id not in self._measurements):
            raise RuntimeError("No measurement with this id")

        self._measurements.pop(meas_id)
        meas_points_ids: Set[int] = self._measurements_points.pop(meas_id)
        
        # Проходим по списку точек и удаляем их по id из второго измерения, которое находим через _points_measurements
        for point_id in meas_points_ids:
            self._InterPoints.pop(point_id)
            
            if (self._points_measurements[point_id][0] != meas_id):
                self._measurements_points[self._points_measurements[point_id][0]].remove(point_id)
            else:
                self._measurements_points[self._points_measurements[point_id][1]].remove(point_id)

        # Пересчитываем среднее значение
        self.find_CurMedPos()



if __name__ == "__main__":
    p = TargObj()

    arr_ids = []


    arr_ids.append(p.AddMeasurement(Measurement(37.683212, 55.641244, -33)))
    arr_ids.append(p.AddMeasurement(Measurement(37.655787, 55.646462, 66)))
    arr_ids.append(p.AddMeasurement(Measurement(37.652679, 55.655788, 130)))


    for elem in p._InterPoints.values():
        pprint(Measurement.calculate_projection(elem))

    print()
    pprint(p._InterPoints)
    pprint(p.CurMedPos)
    print(p.CurMedPos.lat, p.CurMedPos.lon)

    
    # 55.6470805871564 37.67401229739445
    
    # p.DeleteMeasurement(1)
    # pprint(p._InterPoints)
    # pprint(p.CurMedPos)
    

