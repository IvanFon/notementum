# highlight_style.py - custom pygments syntax highlighting style
# Copyright (C) 2019  Ivan Fonseca
#
# This file is part of Notementum.
#
# Notementum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Notementum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Notementum.  If not, see <https://www.gnu.org/licenses/>.

from pygments.styles.monokai import MonokaiStyle


class NotementumStyle(MonokaiStyle):
    '''
    Custom Notementum syntax highlight style. Based on the default Pygments
    Monokai style.
    '''
