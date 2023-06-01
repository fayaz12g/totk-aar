#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libyaz0
# Version 0.5
# Copyright © 2017-2018 MasterVermilli0n / AboodXD

# This file is part of libyaz0.

# libyaz0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# libyaz0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################
################################################################

try:
    from . import yaz0_pyd as yaz0

except:
    try:
        from . import yaz0_so as yaz0

    except:
        try:
            import pyximport
            pyximport.install()

            from . import yaz0_cy as yaz0

        except:
            from . import yaz0


def IsYazCompressed(data):
    return data[:4] in [b'Yaz0', b'Yaz1']


def decompress(data):
    isYaz = IsYazCompressed(data)

    if isYaz:
        return yaz0.DecompressYaz(bytes(data))

    else:
        raise ValueError("Not Yaz0 compressed!")


def compress(data, alignment=0, level=1):
    compressed_data = yaz0.CompressYaz(bytes(data), level)

    result = bytearray(b'Yaz0')
    result += len(data).to_bytes(4, "big")
    result += alignment.to_bytes(4, "big")
    result += b'\0\0\0\0'
    result += compressed_data

    return result


def guessFileExt(data):
    if data[0:4] == b"FRES":
       return ".bfres"

    elif data[0:4] == b"FFNT":
       return ".bffnt"

    elif data[0:4] == b"BNTX":
       return ".bntx"

    elif data[0:4] == b"BNSH":
        return ".bnsh"

    elif data[0:4] == b"FLAN":
        return ".bflan"

    elif data[0:4] == b"FLYT":
        return ".bflyt"

    elif data[0:4] == b"Gfx2":
        return ".gtx"

    elif data[0:4] == b"SARC":
        return ".sarc"

    elif data[0:4] == b"Yaz0":
        return ".szs"

    elif data[-0x28:-0x24] == b"FLIM":
        return ".bflim"

    else:  # Couldn't guess the file extension
        return ".bin"


__all__ = [IsYazCompressed, decompress, compress, guessFileExt]
