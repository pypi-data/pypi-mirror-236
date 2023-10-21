#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'Point' ]

#------------------------------------------------------------------
# Import from...
#
from typing import Any

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... # Do nothing here, because there are no pyConics modules
        # here to be imported.

from pyConics.agobj import AGObj
from pyConics.errors import PointTypeError
from pyConics.origin import origin
from pyConics.tolerance import tol

#------------------------------------------------------------------
# Import as...
#
import numpy as np
np.set_printoptions( formatter = { 'float': lambda x: "{0:0.4e}".format( x ) } )

#------------------------------------------------------------------
# Class Point.
#  
class Point( AGObj ):
    def __init__( self,
                  coord: tuple[ float, float ] | tuple[ float, float, float ] = ( 0.0, 0.0, 1.0 ),
                  name: str = '',
                  shift_origin: bool = True ) -> None:
        super().__init__( name )

        # Redim the geometric form.
        self._gform = _validate_point( coord )

        # Test for epsilon number condition.
        self._gform = tol.adjust2relzeros( self._gform )

        # Transform the point to an homogeneous coord.
        if ( self._gform[ -1 ] != 0.0 ):
            self._gform = self._gform / self._gform[ -1 ]

        # Store this value to be possible restore it to the origin.
        self._from_origin = self._gform

        # Translate the origin from ( 0, 0 ) to another origin in '(origin.x, origin.y )'.
        if ( shift_origin == True ):
            self.update_origin()

    def __repr__( self ) -> str:
        # return an info messsage for this class.
        info = f'{self.name}: {self.gform}'
        if ( self.gform[ -1 ] == 0.0 ):
            info += f' -> point at the infinity'
        return info

    def update_origin( self ) -> None:
        # Translate the origin from ( 0, 0 ) to another origin in '(origin.x, origin.y )'.
        self._gform = origin.change_point( self._from_origin )

    def cross( self, other: Point | Line ) -> Any[ Point | Line ]:
        from pyConics.functions import cross

        # Get the cross product.
        return cross( self, other )

    def __mul__( self, other: Point | Line ) -> Any[ Point | Line ]:
        # Get the cross product.
        return self.cross( other )

    def distance( self, other: Point | Line ) -> float:
        from pyConics.functions import distance
        return distance( self, other )
    
    def __eq__( self, other: Point ) -> bool:
        # Return True if p1 == p2.
        if ( self.distance( other ) == 0.0 ):
            return True
        return False
        
    def at_infinity( self ) -> bool:
        if ( self.gform[ 2 ] == 0.0 ):
            return True
        return False
    
    def are_coincident( self, other: Point ) -> bool:
        if ( self == other ):
            return True
        return False

#------------------------------------------------------------------
# Internal functions.
#  
def _validate_point( coord: tuple[ float, float ] | tuple[ float, float, float ] ) -> np.ndarray:
    if ( len( coord ) == 2 ):
        return np.array( coord + ( 1.0, ) )
    elif ( len( coord ) == 3 ):
        return np.array( coord )
    else:
        raise PointTypeError( Point.__name__, Point.gform.fset.__name__ )

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    # Keep this imports even there is no test code.
    from pyConics.point import Point
    from pyConics.line import Line

    import os
    os.system( 'cls' )

    # Shows info about a point.
    p0 = Point( ( 0 , 1 ) )
    print( p0 )
    print( p0.name, p0.gform, type( p0.gform ), p0.gform.shape )
    print()

    # Try to assign a value to the gform property.
    try:
        p0.gform = np.array( [ 1, 2, 3 ] )
    except AttributeError as e:
        print( e )
    print()

    # Try to create a point with only one dimension.
    try:
        p0 = Point( ( 0, ) ) # type: ignore
    except PointTypeError as e:
        print( e )
    print()

    # Change the origin.
    print( origin )
    p1 = Point( ( 1.0, 1.0 ) )
    print( p1 )
    origin.x = 2.0
    origin.y = 2.0
    p1.update_origin()
    print( origin )
    print( p1 )
    origin.reset()
    p1.update_origin()
    print( origin )
    print( p1 )
    print()

    # Points in HC.
    origin.reset()
    p2 = Point( ( 1, 2, 0 ) )
    p3 = Point( ( 0.001, 2, 3 ) )
    print( p2 )
    print( p3 )
    print()

    # How to use cross product.
    p1 = Point( ( 1, 1 ) )      # p1 = ( 1, 1 )
    p2 = Point( ( -1, -1 ) )    # p2 = ( -1, -1 ) 
    l1: Line = p1.cross( p2 )   # l1: y = x
    print( l1, '\n' )
    l1: Line = p1 * p2          # l1: y = x
    print( l1, '\n' )
    
    l1 = Line( ( 1, -1, 1 ) )
    l2 = Line( ( 1, -1, -1 ) )
    l3 = Line( ( -1, -1, 1 ) )
    p3: Point = l1.cross( l2 )  # p3 is a point at the infinity.
    print( p3, '\n' )
    p3: Point = l1 * l2         # p3 is a point at the infinity.
    print( p3, '\n' )
    p4: Point = l1.cross( l3 )  # p4 = ( 0, 1 )
    print( p4, '\n' )
    p4: Point = l1 * l3         # p4 = ( 0, 1 )
    print( p4, '\n' )
    p5: Point = l2.cross( l3 )  # p5 = ( 1, 0 )
    print( p5, '\n' )
    p5: Point = l2 * l3         # p5 = ( 1, 0 )
    print( p5, '\n' )

    p6 = Point( ( 1, 0 ) )
    l4: Line = l1.cross( p6 )  # l4 = ( 1, 1, -1 ) that pass through p6
    print( l4, '\n' )
    l4: Line = l1 * p6         # l4 = ( 1, 1, -1 ) that pass through p6
    print( l4, '\n' )
    l5: Line = p6.cross( l1 )  # l5 = ( 1, 1, -1 ) that pass through p6
    print( l5, '\n' )
    l5: Line = p6 * l1         # l5 = ( 1, 1, -1 ) that pass through p6
    print( l5, '\n' )

    # Shifting origin.
    origin.x = 3
    origin.y = 2
    print( origin )
    
    # Distance between 2 points.
    p1 = Point( ( 0, 1 ), 'p1' )
    p2 = Point( ( 1, 0 ), 'p2' )
    d12 = p1.distance( p2 )
    d21 = p2.distance( p1 )
    print( f'Distance from {p1}\nto {p2}\nis {d12:.4f}.\n' )
    print( f'Distance from {p2}\nto {p1}\nis {d21:.4f}.\n' )

    # Distance between a point and a line.
    p1 = Point( ( 1, 0 ), 'p1' )
    l1 = Line( ( 1, -1, 1 ), 'l1' )
    dlp = l1.distance( p1 )
    dpl =  p1.distance( l1 )
    print( f'Distance from {l1}\nto {p1}\nis {dlp:.4f}.\n' )
    print( f'Distance from {p1}\nto {l1}\nis {dpl:.4f}.\n' )

    # Resetting origin.
    origin.reset()
    print( origin )
    
    # Are these points the same?
    p1 = Point( ( 0, 1 ), 'p1' )
    p2 = Point( ( 1, 0 ), 'p2' )
    print( p1 )
    print( p2 )
    print( f'p1 == p1? {p1 == p1}.' )
    print( f'p1 == p2? {p1 == p2}.' )
    print( f'p2 == p1? {p2 == p1}.' )
    print( f'p2 == p2? {p2 == p2}.\n' )

    # Point at the infinity?
    p1 = Point( ( 1, 1, 0 ), 'p1' )
    p2 = Point( ( 1, -1, 1 ), 'p2' )
    print( p1 )
    print( p2 )
    print( f'Is p1 a point at the infinity? {p1.at_infinity()}.' )
    print( f'Is p2 a point at the infinity? {p2.at_infinity()}.\n' )

    # Distance between a finite point and a point at the infinity.
    d12 = p1.distance( p2 )
    print( f'Distance from {p1}\nto {p2}\nis {d12:.4f}.\n' )

    # Points are coindicents?
    p1 = Point( ( 0, 1 ), 'p1' )
    p2 = Point( ( 1, 0 ), 'p2' )
    print( f'Are p1 and p1 coincident points? {p1.are_coincident( p1 )}.' )
    print( f'Are p1 and p2 coincident points? {p1.are_coincident( p2 )}.' )

    