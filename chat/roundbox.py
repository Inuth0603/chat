# Copyright 2014, Sugar Labs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import math

from gi.repository import Gtk
from gi.repository import Graphene

from sugar4.graphics import style

_BORDER_DEFAULT = style.LINE_WIDTH


class RoundBox(Gtk.Box):
    __gtype_name__ = 'RoundBox'

    def __init__(self, **kwargs):
        kwargs['orientation'] = Gtk.Orientation.HORIZONTAL
        Gtk.Box.__init__(self, **kwargs)
        self._radius = style.zoom(15)
        self.border_color = style.COLOR_BLACK
        self.tail = None
        self.background_color = None

    def append(self, child):
        child.set_margin_start(style.zoom(5))
        child.set_margin_end(style.zoom(5))
        child.set_margin_top(style.zoom(5))
        child.set_margin_bottom(style.zoom(5))
        super().append(child)

    def pack_start(self, child, expand, fill, padding):
        '''GTK3 compat wrapper — just delegates to append.'''
        self.append(child)

    def add(self, child):
        '''GTK3 compat wrapper — just delegates to append.'''
        self.append(child)

    def do_snapshot(self, snapshot):
        w = self.get_width()
        h = self.get_height()
        rect = Graphene.Rect().init(0, 0, w, h)
        cr = snapshot.append_cairo(rect)

        hmargin = style.zoom(15)
        x = hmargin
        y = 0
        width = w - _BORDER_DEFAULT * 2. - hmargin * 2
        if self.tail is None:
            height = h - _BORDER_DEFAULT * 2.
        else:
            height = h - _BORDER_DEFAULT * 2. - self._radius

        cr.move_to(x + self._radius, y)
        cr.arc(x + width - self._radius, y + self._radius,
               self._radius, math.pi * 1.5, math.pi * 2)
        tail_height = style.zoom(5)
        if self.tail == 'right':
            cr.arc(x + width - self._radius, y + height - self._radius * 2,
                   self._radius, 0, math.pi * 0.5)
            cr.line_to(x + width - self._radius, y + height)
            cr.line_to(x + width - tail_height * self._radius,
                       y + height - self._radius)
            cr.arc(x + self._radius, y + height - self._radius * 2,
                   self._radius, math.pi * 0.5, math.pi)
        elif self.tail == 'left':
            cr.arc(x + width - self._radius, y + height - self._radius * 2,
                   self._radius, 0, math.pi * 0.5)
            cr.line_to(x + self._radius * tail_height,
                       y + height - self._radius)
            cr.line_to(x + self._radius, y + height)
            cr.line_to(x + self._radius, y + height - self._radius)
            cr.arc(x + self._radius, y + height - self._radius * 2,
                   self._radius, math.pi * 0.5, math.pi)
        else:
            cr.arc(x + width - self._radius, y + height - self._radius,
                   self._radius, 0, math.pi * 0.5)
            cr.arc(x + self._radius, y + height - self._radius,
                   self._radius, math.pi * 0.5, math.pi)
        cr.arc(x + self._radius, y + self._radius, self._radius,
               math.pi, math.pi * 1.5)
        cr.close_path()

        if self.background_color is not None:
            r, g, b, __ = self.background_color.get_rgba()
            cr.set_source_rgb(r, g, b)
            cr.fill_preserve()

        if self.border_color is not None:
            r, g, b, __ = self.border_color.get_rgba()
            cr.set_source_rgb(r, g, b)
            cr.set_line_width(_BORDER_DEFAULT)
            cr.stroke()

        # Render children on top of the background
        Gtk.Box.do_snapshot(self, snapshot)

