import math

class Vector3:

    def __init__(self, x=0, y=0, z=0):
        """Inicializa al vector self como un punto en el origen cartesiano."""
        self.x = x
        self.y = y
        self.z = z
        return

    def __abs__(self):
        """Devuelve la norma del vector "self"."""
        return vector3_norm(self)

    def __add__(self, a):
        """Devuelve un vector igual a la suma de los vectores "self" y "a"."""
        return vector3_add(self, a)

    def __eq__(self, a):
        """Redefine al vector "self" como una copia del vector "a"."""
        self = vector3_copy(a)
        return

    def __hash__(self):
        """Devuelve el hash del vector "self"."""
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        """Devuelve una cadena que representa al vector "self"."""
        return vector3_repr(self)

    def __str__(self):
        """Devuelve una cadena que representa al vector "self"."""
        return vector3_repr(self)

    def __sub__(self, a):
        """Devuelve un vector igual a la resta de los vectores "self" y "a"."""
        return self + vector3_scale(a,-1)

    def rotate_about(self, pivot_vec, axis, angle):
        """Devuelve una copia del vector "self" girado alrededor del vector
        "angle_vec" con base en el punto "pivot_vec"."""
        # Crear copia del vector
        rotvec = vector3_copy(self)
        # Mover al origen
        rotvec -= pivot_vec
        # Rotar según la fórmula de Rodrigues
        # https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
        rotvec = \
            vector3_add(
                vector3_add(
                    vector3_scale(rotvec, math.cos(angle)),
                    vector3_scale(
                        vector3_cross_prod(axis, rotvec),
                        math.sin(angle))),
                vector3_scale(
                    vector3_scale(
                        axis,
                        vector3_dot_prod(axis, rotvec)),
                    1-math.cos(angle)))
        # Restaurar posición inicial
        rotvec += pivot_vec
        return rotvec
    
    def get_sph(self):
        """Devuelve las coordenadas esféricas del vector "self"."""
        return

    def set_sph(self, r, th_azi, th_pol):
        """Redefine el vector "self" según las coordenadas esféricas dadas. Ver
        vector3_init_sph."""
        vector3_init_sph(self, r, th_azi, th_pol)
        return


def vector3_init_xyz(vector, x, y, z):
    """Redefine al vector "vector" como un punto en las coordenadas cartesianas
    "x", "y" y "z"."""
    vector.x = x
    vector.y = y
    vector.z = z
    return

def vector3_init_sph(vector, r, th_azi, th_pol):
    """Redefine al vector "vector" con punta a "r" unidades del origen, ángulo
    azimutal "th_azi" y ángulo polar "th_pol"."""
    # El ángulo azimutal es el ángulo del giro desde el eje Z hasta
    # el punto de medición.
    # El ángulo polar es el ángulo entre el eje X y la proyección sobre el
    # plano XY del segmento entre el origen y el punto de medición.
    vector.x = r*math.sin(th_azi)*math.cos(th_pol)
    vector.y = r*math.sin(th_azi)*math.sin(th_pol)
    vector.z = r*math.cos(th_pol)
    return

def vector3_copy(vector):
    """Devuelve una copia del vector "vector"."""
    newvec = Vector3()
    newvec.x = vector.x
    newvec.y = vector.y
    newvec.z = vector.z
    return newvec

def vector3_scale(vector, scalar):
    """Devuelve una copia del vector "vector" escalada por el escalar
    "scalar"."""
    scaled = vector3_copy(vector)
    scaled.x *= scalar
    scaled.y *= scalar
    scaled.z *= scalar
    return scaled 

def vector3_add(a, b):
    """Devuelve un vector igual a la suma de "a" y "b"."""
    sum = vector3_copy(a)
    sum.x += b.x
    sum.y += b.y
    sum.z += b.z
    return sum

def vector3_norm(a):
    """Devuelve la norma del vector."""
    return math.sqrt(a.x**2 + a.y**2 + a.z**2)

def vector3_unit(a):
    """Devuelve una versión unitaria del vector "a"."""
    return a*1/vector3_norm(a)

def vector3_cross_prod(a, b):
    """Devuelve el producto cruz de los vectores "a" y "b"."""
    crossprod = Vector3()
    crossprod.x =     a.y*b.z - a.z*b.y
    crossprod.y = -1*(a.x*b.z - a.z*b.x)
    crossprod.z =     a.x*b.y - a.y*b.x
    return crossprod

def vector3_dot_prod(a, b):
    """Devuelve el producto punto de los vectores "a" y "b"."""
    dotprod =   a.x*b.x \
              + a.y*b.y \
              + a.z*b.z
    return dotprod

def vector3_repr(a):
    return f"Vector3({a.x}, {a.y}, {a.z})"

def vector3_fstr(a,n=3):
    return f"Vector3({a.x:.3f}, {a.y:.3f}, {a.z:.3f})"
