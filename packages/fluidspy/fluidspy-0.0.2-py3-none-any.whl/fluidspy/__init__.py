from .src.constant import DIRECTION, DIM, METHOD, ORDER
from .src.taylor.taylor_caller import taylor_methods
from .src.orders.first_order import FirstOrder
from .src.orders.second_order import SecondOrder
from .src.pde.explicit import Explicit
from .src.pde.implicit import Implicit
from .src.pde.finite_element_methods import finite_element_method