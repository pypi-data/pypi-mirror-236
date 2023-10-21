#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'const' ]

#------------------------------------------------------------------
# Import from...
#  
from dataclasses import dataclass

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... # Do nothing here, because there are no pyConics modules
        # here to be imported.

from pyConics.errors import AttributeError

#------------------------------------------------------------------
# Import as...
#  
import numpy as np

#------------------------------------------------------------------
# Data Class Constants.
#  
@dataclass
class Constants:
    _inf: float = np.Inf
    _pi : float = np.pi

    @property
    def inf( self ) -> float:
        return self._inf
    
    @inf.setter
    def inf( self, inf_number: float ) -> None:
       raise AttributeError( self.__class__.__name__, Constants.inf.fset.__name__ )
    
    @property
    def pi( self ) -> float:
        return self._pi
    
    @pi.setter
    def pi( self, pi_number: float ) -> None:
       raise AttributeError( self.__class__.__name__, Constants.pi.fset.__name__ )
    

#--------------------------------------------------------------
# Global variable.
#
const = Constants()

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    print( f'The value of infinity is {const.inf}' )
    print( f'Is infinity equals to 0.0? {const.inf == 0.0}' )
    try:
        const.inf = 0.0
    except AttributeError as e:
        print( e )
    
    print( f'The value of pi is {const.pi:.6f}' )
    try:
        const.pi = 0.0
    except AttributeError as e:
        print( e )
    