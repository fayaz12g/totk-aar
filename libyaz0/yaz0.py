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

import struct


def DecompressYaz(src):
    src_end = len(src)

    dest_end = struct.unpack(">I", src[4:8])[0]
    dest = bytearray(dest_end)

    code = src[16]

    src_pos = 17
    dest_pos = 0

    while src_pos < src_end and dest_pos < dest_end:
        for _ in range(8):
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            if code & 0x80:
                dest[dest_pos] = src[src_pos]; dest_pos += 1; src_pos += 1

            else:
                b1 = src[src_pos]; src_pos += 1
                b2 = src[src_pos]; src_pos += 1

                copy_src = dest_pos - ((b1 & 0x0f) << 8 | b2) - 1

                n = b1 >> 4
                if not n:
                    n = src[src_pos] + 0x12; src_pos += 1

                else:
                    n += 2

                for _ in range(n):
                    dest[dest_pos] = dest[copy_src]; dest_pos += 1; copy_src += 1

            code <<= 1

        else:
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            code = src[src_pos]; src_pos += 1

    return bytes(dest)


def compressionSearch(src, pos, max_len, search_range, src_end):
    found_len = 1
    found = 0

    if pos + 2 < src_end:
        search = pos - search_range
        if search < 0:
             search = 0

        cmp_end = pos + max_len
        if cmp_end > src_end:
            cmp_end = src_end

        c1 = src[pos:pos + 1]
        while search < pos:
            search = src.find(c1, search, pos)
            if search == -1:
                break

            cmp1 = search + 1
            cmp2 = pos + 1

            while cmp2 < cmp_end and src[cmp1] == src[cmp2]:
                cmp1 += 1; cmp2 += 1

            len_ = cmp2 - pos

            if found_len < len_:
                found_len = len_
                found = search
                if found_len == max_len:
                    break

            search += 1

    return found, found_len


def CompressYaz(src, level):
    if not level:
        search_range = 0

    elif level < 9:
        search_range = 0x10e0 * level // 9 - 0x0e0

    else:
        search_range = 0x1000

    pos = 0
    src_end = len(src)

    dest = bytearray()
    code_byte_pos = 0

    max_len = 0x111

    while pos < src_end:
        code_byte_pos = len(dest)
        dest.append(0)

        for i in range(8):
            if pos >= src_end:
                break

            found_len = 1

            if search_range:
                found, found_len = compressionSearch(src, pos, max_len, search_range, src_end)

            if found_len > 2:
                delta = pos - found - 1

                if found_len < 0x12:
                    dest.append(delta >> 8 | (found_len - 2) << 4)
                    dest.append(delta & 0xFF)

                else:
                    dest.append(delta >> 8)
                    dest.append(delta & 0xFF)
                    dest.append((found_len - 0x12) & 0xFF)

                pos += found_len

            else:
                dest[code_byte_pos] |= 1 << (7 - i)
                dest.append(src[pos]); pos += 1

    return bytes(dest)
