"""
LDTP v2 Mouse.

@author: Eitan Isaacson <eitan@ascender.com>
@author: Nagappan Alagappan <nagappan@gmail.com>
@copyright: Copyright (c) 2009 Eitan Isaacson
@copyright: Copyright (c) 2009-13 Nagappan Alagappan
@license: LGPL

http://ldtp.freedesktop.org

This file may be distributed and/or modified under the terms of the GNU Lesser General
Public License version 2 as published by the Free Software Foundation. This file
is distributed without any warranty; without even the implied warranty of 
merchantability or fitness for a particular purpose.

See 'COPYING' in the source distribution for more information.

Headers in this file shall remain intact.
"""

import time
import pyatspi 
from .utils import Utils
from .server_exception import LdtpServerException

class Mouse(Utils):
    """
    Mouse related events
    """
    def generatemouseevent(self, x, y, eventType = 'b1c'):
        """
        Generate mouse event on x, y co-ordinates.
        
        @param x: X co-ordinate
        @type x: int
        @param y: Y co-ordinate
        @type y: int
        @param eventType: Mouse click type
        @type eventType: string

        @return: 1 on success.
        @rtype: integer
        """
        return self._mouse_event(x, y, eventType)

    def mouseleftclick(self, window_name, object_name):
        """
        Mouse left click on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        obj = self._get_object(window_name, object_name)

        self._grab_focus(obj)

        _coordinates = self._get_size(obj)
        return self._mouse_event(_coordinates.x + _coordinates.width / 2,
                                 _coordinates.y + _coordinates.height / 2,
                                 'b1c')

    def mousemove(self, window_name, object_name):
        """
        Mouse move on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        obj = self._get_object(window_name, object_name)

        self._grab_focus(obj)

        _coordinates = self._get_size(obj)
        return self._mouse_event(_coordinates.x + _coordinates.width / 2,
                                 _coordinates.y + _coordinates.height / 2,
                                 'abs')

    def mouserightclick(self, window_name, object_name):
        """
        Mouse right click on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        obj = self._get_object(window_name, object_name)

        self._grab_focus(obj)

        _coordinates = self._get_size(obj)
        return self._mouse_event(_coordinates.x + _coordinates.width / 2,
                                 _coordinates.y + _coordinates.height / 2,
                                 'b3c')

    def doubleclick(self, window_name, object_name):
        """
        Double click on the object
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        obj = self._get_object(window_name, object_name)

        self._grab_focus(obj)

        _coordinates = self._get_size(obj)
        return self._mouse_event(_coordinates.x + _coordinates.width / 2,
                                 _coordinates.y + _coordinates.height / 2,
                                 'b1d')

    def simulatemousemove(self, source_x, source_y, dest_x, dest_y, delay = 0.0):
        """
        @param source_x: Source X
        @type source_x: integer
        @param source_y: Source Y
        @type source_y: integer
        @param dest_x: Dest X
        @type dest_x: integer
        @param dest_y: Dest Y
        @type dest_y: integer
        @param delay: Sleep time between the mouse move
        @type delay: double

        @return: 1 if simulation was successful, 0 if not.
        @rtype: integer
        """
        size = self._get_geometry()
        if (source_x < size[0] or source_y < size[1] or \
                dest_x > size[2] or dest_y > size[3]) or \
                (source_x > size[2] or source_y > size[3] or \
                     dest_x < size[0] or dest_y < size[1]):
            return 0

        # int() to assure being a natural number
        steps = int(max(abs(source_x-dest_x), abs(source_y-dest_y)))
        step = 0
        while True:
            current_x = int(source_x + ((dest_x-source_x) * step) / steps)
            current_y = int(source_y + ((dest_y-source_y) * step) / steps)
            step = step + 1
            if delay:
                time.sleep(delay)
            # Start mouse move from source_x, source_y to dest_x, dest_y
            self.generatemouseevent(current_x, current_y, 'abs')
            if step == steps:
                break
        return 1
