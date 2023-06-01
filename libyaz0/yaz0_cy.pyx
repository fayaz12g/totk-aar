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

from cpython cimport array
from cython cimport view
from libc.stdlib cimport malloc, free
from libc.string cimport memchr


ctypedef unsigned char u8
ctypedef char s8
ctypedef unsigned int u32


cpdef bytes DecompressYaz(bytes src_):
    cdef:
        array.array dataArr = array.array('B', src_)
        u8 *src = dataArr.data.as_uchars
        u8 *src_end = src + len(src_)

        u32 dest_len = (src[4] << 24 | src[5] << 16 | src[6] << 8 | src[7])
        u8 *dest = <u8 *>malloc(dest_len)
        u8 *dest_pos = dest
        u8 *dest_end = dest + dest_len

        u8 code = src[16]

        u8 b1, b2
        u8 *copy_src
        int n

    src += 17

    try:
        while src < src_end and dest < dest_end:
            for _ in range(8):
                if src >= src_end or dest >= dest_end:
                    break

                if code & 0x80:
                    dest[0] = src[0]; dest += 1; src += 1

                else:
                    b1 = src[0]; src += 1
                    b2 = src[0]; src += 1

                    copy_src = dest - ((b1 & 0x0f) << 8 | b2) - 1

                    n = b1 >> 4
                    if not n:
                        n = src[0] + 0x12; src += 1

                    else:
                        n += 2

                    for _ in range(n):
                        dest[0] = copy_src[0]; dest += 1; copy_src += 1

                code <<= 1

            else:
                if src >= src_end or dest >= dest_end:
                    break

                code = src[0]; src += 1

        return bytes(<u8[:dest - dest_pos]>dest_pos)

    finally:
        free(dest_pos)


cdef (u8 *, u32) compressionSearch(u8 *src, u8 *src_pos, int max_len, u32 range_, u8 *src_end):
    cdef:
        u32 found_len = 1

        u8 *found
        u8 *search
        u8 *cmp_end
        u8 c1
        u8 *cmp1
        u8 *cmp2
        int len_

    if src + 2 < src_end:
        search = src - range_
        if search < src_pos:
             search = src_pos

        cmp_end = src + max_len
        if cmp_end > src_end:
            cmp_end = src_end

        c1 = src[0]
        while search < src:
            search = <u8 *>memchr(search, c1, src - search)
            if not search:
                break

            cmp1 = search + 1
            cmp2 = src + 1

            while cmp2 < cmp_end and cmp1[0] == cmp2[0]:
                cmp1 += 1; cmp2 += 1

            len_ = cmp2 - src

            if found_len < len_:
                found_len = len_
                found = search
                if found_len == max_len:
                    break

            search += 1

    return found, found_len


cpdef bytes CompressYaz(bytes src_, u8 opt_compr):
    cdef u32 range_

    if not opt_compr:
        range_ = 0

    elif opt_compr < 9:
        range_ = 0x10e0 * opt_compr / 9 - 0x0e0

    else:
        range_ = 0x1000

    cdef:
        array.array dataArr = array.array('B', src_)
        u8 *src = dataArr.data.as_uchars
        u8 *src_pos = src
        u8 *src_end = src + len(src_)

        u8 *dest = <u8 *>malloc(len(src_) + (len(src_) + 8) // 8)
        u8 *dest_pos = dest
        u8 *code_byte = dest

        int max_len = 0x111

        int i
        u32 found_len, delta
        u8 *found

    try:
        while src < src_end:
            code_byte = dest
            dest[0] = 0; dest += 1

            for i in range(8):
                if src >= src_end:
                    break

                found_len = 1

                if range_:
                    found, found_len = compressionSearch(src, src_pos, max_len, range_, src_end)

                if found_len > 2:
                    delta = src - found - 1

                    if found_len < 0x12:
                        dest[0] = delta >> 8 | (found_len - 2) << 4; dest += 1
                        dest[0] = delta & 0xFF; dest += 1

                    else:
                        dest[0] = delta >> 8; dest += 1
                        dest[0] = delta & 0xFF; dest += 1
                        dest[0] = (found_len - 0x12) & 0xFF; dest += 1

                    src += found_len

                else:
                    code_byte[0] |= 1 << (7 - i)
                    dest[0] = src[0]; dest += 1; src += 1

        return bytes(<u8[:dest - dest_pos]>dest_pos)

    finally:
        free(dest_pos)
