#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SarcLib - A library for handling the Nintendo SARC archive format
# Copyright (C) 2015-2018 RoadrunnerWMC, MasterVermilli0n / AboodXD

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################
################################################################

from .FileArchive import guessFileExt, File, Folder, SARC_Archive

__all__ = [guessFileExt, File, Folder, SARC_Archive]
