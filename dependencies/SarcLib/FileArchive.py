#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SarcLib - A library for handling the Nintendo SARC archive format
# Copyright (C) 2015-2019 RoadrunnerWMC, MasterVermilli0n / AboodXD

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

import struct


def bytes_to_string(data, offset):
    end = data.find(b'\0', offset)
    if end == -1:
        return data[offset:].decode('utf-8')

    return data[offset:end].decode('utf-8')


def guessFileExt(data):
    if data[:8] == b'BNTX\0\0\0\0':
        return ".bntx"

    elif data[:8] == b'BNSH\0\0\0\0':
        return ".bnsh"

    elif data[:8] == b'MsgStdBn':
        return ".msbt"

    elif data[:8] == b'MsgPrjBn':
        return ".msbp"

    elif data[:4] == b'SARC':
        return ".sarc"

    elif data[:4] in [b'Yaz0', b'Yaz1']:
        return ".szs"

    elif data[:4] == b'FFNT':
        return ".bffnt"

    elif data[:4] == b'CFNT':
        return ".bcfnt"

    elif data[:4] == b'CSTM':
        return ".bcstm"

    elif data[:4] == b'FSTM':
        return ".bfstm"

    elif data[:4] == b'FSTP':
        return ".bfstp"

    elif data[:4] == b'CWAV':
        return ".bcwav"

    elif data[:4] == b'FWAV':
        return ".bfwav"

    elif data[:4] == b'Gfx2':
        return ".gtx"

    elif data[:4] == b'FRES':
        return ".bfres"

    elif data[:4] == b'AAHS':
        return ".sharc"

    elif data[:4] == b'BAHS':
        return ".sharcfb"

    elif data[:4] == b'FSHA':
        return ".bfsha"

    elif data[:4] == b'FLAN':
        return ".bflan"

    elif data[:4] == b'FLYT':
        return ".bflyt"

    elif data[:4] == b'CLAN':
        return ".bclan"

    elif data[:4] == b'CLYT':
        return ".bclyt"

    elif data[:4] == b'CTPK':
        return ".ctpk"

    elif data[:4] == b'CGFX':
        return ".bcres"

    elif data[:4] == b'AAMP':
        return ".aamp"

    elif data[-0x28:-0x24] == b'FLIM':
        return ".bflim"

    elif data[-0x28:-0x24] == b'CLIM':
        return ".bclim"

    elif data[:2] in [b'YB', b'BY']:
        return ".byml"

    elif data[0xC:0x10] == b'SCDL':
        return ".bcd"

    else:
        return ".bin"


class File:
    """
    Class that represents a file of unknown format
    """

    def __init__(self, name='', data=b'', hasFilename=True):
        self.name = name
        self.data = data
        self.hasFilename = hasFilename


class Folder:
    """
    Class that represents a folder
    """

    def __init__(self, name='', contents=None):
        self.name = name

        if contents is not None:
            self.contents = contents
        else:
            self.contents = set()

    def addFile(self, file):
        self.contents.add(file)

    def removeFile(self, file):
        self.contents.remove(file)

    def addFolder(self, folder):
        self.contents.add(folder)

    def removeFolder(self, folder):
        self.contents.remove(folder)


class FileArchive:
    """
    Class that represents any Nintendo file archive
    """

    def __init__(self):
        self.contents = set()
        self.endianness = '>'

    def clear(self):
        self.contents = set()

    def __str__(self):
        """
        Returns a string representation of this archive
        """
        s = ''

        def addFolderStructure(folder, indent):
            """
            Adds a folder structure to the repr with an indent level set to indent
            """
            nonlocal s

            folders = set()
            files = set()

            for thing in folder:
                if isinstance(thing, File):
                    files.add(thing)

                else:
                    folders.add(thing)

            folders = sorted(folders, key=lambda entry: entry.name)
            files = sorted(files, key=lambda entry: entry.name)

            for folder in folders:
                s = ''.join([s, '\n', (' ' * indent), folder.name, '/'])
                addFolderStructure(folder.contents, indent + 2)

            for file in files:
                s = ''.join([s, '\n', (' ' * indent), file.name])

        addFolderStructure(self.contents, 0)
        return s[1:]  # Remove the leading \n

    def __getitem__(self, key):
        """
        Returns the file requested when one indexes this archive
        """
        currentPlaceToLook = self.contents
        folderStructure = key.replace('\\', '/').split('/')

        for folderName in folderStructure[:-1]:
            for lookObj in currentPlaceToLook:
                if isinstance(lookObj, Folder) and lookObj.name == folderName:
                    currentPlaceToLook = lookObj.contents
                    break

            else:
                raise KeyError('File/Folder not found')

        for file in currentPlaceToLook:
            if file.name == folderStructure[-1]:
                return file

        raise KeyError('File/Folder not found')

    def __setitem__(self, key, val):
        """
        Handles the request to set a value to an index of the archive
        """
        if not isinstance(val, (Folder, File)):
            raise TypeError('New value is not a file or folder!')

        currentPlaceToLook = self.contents
        folderStructure = key.replace('\\', '/').split('/')

        File.name = folderStructure[-1]

        for folderName in folderStructure[1:]:
            for lookObj in currentPlaceToLook:
                if isinstance(lookObj, Folder) and lookObj.name == folderName:
                    currentPlaceToLook = lookObj.contents
                    break

            else:
                newFolder = Folder(folderName)
                currentPlaceToLook.add(newFolder)
                currentPlaceToLook = newFolder.contents

        for file in currentPlaceToLook:
            if file.name == key:
                currentPlaceToLook.remove(file)

        currentPlaceToLook.add(val)

    def __delitem__(self, key):
        """
        Handles the request to delete an index of the archive
        """
        currentPlaceToLook = self.contents
        folderStructure = key.replace('\\', '/').split('/')

        for folderName in folderStructure[1:]:
            for lookObj in currentPlaceToLook:
                if isinstance(lookObj, Folder) and lookObj.name == folderName:
                    currentPlaceToLook = lookObj.contents
                    break

            else:
                raise KeyError('File/Folder not found')

        for file in currentPlaceToLook:
            if file.name == key:
                currentPlaceToLook.remove(file)
                return

        raise KeyError('File/Folder not found')

    def addFile(self, file):
        self.contents.add(file)

    def removeFile(self, file):
        self.contents.remove(file)

    def addFolder(self, folder):
        self.contents.add(folder)

    def removeFolder(self, folder):
        self.contents.remove(folder)


class SARC_Archive(FileArchive):
    """
    Class that represents a Nintendo SARC Archive
    """

    def __init__(self, data=None, endianness='>', hashKey=0x65):
        super().__init__()

        self.endianness = endianness
        self.hashKey = hashKey

        if data is not None:
            self.load(data)

    def load(self, data):
        """
        Loads a SARC file from data
        """

        result = self._load(bytes(data))
        if result:
            raise ValueError('This is not a valid SARC file! Error code: %d' % result)

    def _load(self, data):

        # SARC Header -----------------------------------------

        # File magic (0x00 - 0x03)
        if data[:0x04] != b'SARC':
            return 1

        # Come back to header length later, when we have endianness

        # Endianness/BOM (0x06 - 0x07)
        bom = data[0x06:0x08]
        try:
            endians = {b'\xFE\xFF': '>', b'\xFF\xFE': '<'}
            self.endianness = endians[bom]

        except KeyError:
            return 2

        # Header length (0x04 - 0x05)
        headLen = struct.unpack(self.endianness + 'H', data[0x04:0x06])[0]
        if headLen != 0x14:
            return 3

        # File Length (0x08 - 0x0B)
        filelen = struct.unpack(self.endianness + 'I', data[0x08:0x0C])[0]
        if len(data) != filelen:
            return 4

        # Beginning Of Data offset (0x0C - 0x0F)
        dataStartOffset = struct.unpack(self.endianness + 'I', data[0x0C:0x10])[0]

        # SFAT Header -----------------------------------------

        # Sanity check (0x14 - 0x17)
        if data[0x14:0x18] != b'SFAT':
            return 5

        # Header length (0x18 - 0x19)
        headLen = struct.unpack(self.endianness + 'H', data[0x18:0x1A])[0]
        if headLen != 0x0C:
            return 6

        # Node count (0x1A - 0x1C)
        nodeCount = struct.unpack(self.endianness + 'H', data[0x1A:0x1C])[0]

        # Hash key (0x1D - 0x1F)
        self.hashKey = struct.unpack(self.endianness + 'I', data[0x1C:0x20])[0]

        # SFAT Nodes (0x20 - 0x20+(0x10*nodeCount))
        SFATNodes = []

        SFATNodeOffset = 0x20
        for nodeNum in range(nodeCount):
            fileNameHash = struct.unpack(
                self.endianness + 'I', data[SFATNodeOffset:SFATNodeOffset + 4])[0]

            fileNameTableEntryID = struct.unpack(
                self.endianness + 'I', data[SFATNodeOffset + 4:SFATNodeOffset + 8])[0]

            hasFilename = fileNameTableEntryID >> 24
            fileNameTableEntryOffset = fileNameTableEntryID & 0xFFFFFF

            # Beginning of Node File Data
            fileDataStart = struct.unpack(
                self.endianness + 'I', data[SFATNodeOffset + 8:SFATNodeOffset + 0x0C])[0]

            # End of Node File Data
            fileDataEnd = struct.unpack(
                self.endianness + 'I', data[SFATNodeOffset + 0x0C:SFATNodeOffset + 0x10])[0]

            # Calculate file data length
            fileDataLength = fileDataEnd - fileDataStart

            # Add an entry to the node list
            SFATNodes.append(
                (fileNameHash, hasFilename, fileNameTableEntryOffset, fileDataStart, fileDataLength))

            # Increment the offset counter
            SFATNodeOffset += 0x10

        # SFNT Header -----------------------------------------

        # From now on we need to keep track of an offset variable
        offset = 0x20 + (0x10 * nodeCount)

        # Sanity check (offset - offset+0x03)
        if data[offset:offset + 0x04] != b'SFNT':
            return 7

        # Header length (offset+0x04 - offset+0x05)
        headLen = struct.unpack(self.endianness + 'H', data[offset + 0x04:offset + 0x06])[0]
        if headLen != 0x08:
            return 8

        # Increment the offset
        offset += 0x08

        # Add the files to the self.contents set --------------
        self.contents.clear()
        for fileNameHash, hasFilename, fileNameTableEntryOffset, fileDataStart, fileDataLength in SFATNodes:

            # Get the file data
            fileData = data[dataStartOffset + fileDataStart:
                            dataStartOffset + fileDataStart + fileDataLength]

            # Get the file name (search for the first null byte manually)
            nameOffset = offset + (fileNameTableEntryOffset * 4)
            if hasFilename:
                name = bytes_to_string(data, nameOffset)

            else:
                name = ''.join(["hash_" + hex(fileNameHash), guessFileExt(fileData)])

            # Split it into its folders
            folderStructure = name.split('/')

            # Handle it differently if the file is not in a folder
            if len(folderStructure) == 1:
                self.contents.add(File(name, fileData, hasFilename))

            else:

                # Get the first folder, or make one if needed
                folderName = folderStructure[0]
                for foundFolder in self.contents:
                    if not isinstance(foundFolder, Folder):
                        continue

                    if foundFolder.name == folderName:
                        break

                else:
                    foundFolder = Folder(folderName)
                    self.contents.add(foundFolder)

                # Now find/make the rest of them
                outerFolder = foundFolder
                for folderName in folderStructure[1:-1]:
                    for foundFolder in outerFolder.contents:
                        if not isinstance(foundFolder, Folder):
                            continue

                        if foundFolder.name == folderName:
                            break

                    else:
                        foundFolder = Folder(folderName)
                        outerFolder.addFolder(foundFolder)

                    outerFolder = foundFolder

                # Now make a new file and add it to self.contents
                outerFolder.addFile(File(folderStructure[-1], fileData, hasFilename))

        # We're done! Return True so no exception will be thrown.
        return 0

    @staticmethod
    def filenameHash(filename, endianness, key):
        """
        Returns the hash that should be used by an SFAT node.
        """
        result = 0
        for char in filename:
            result = (result * key + ord(char)) & 0xFFFFFFFF

        return struct.pack(endianness + 'I', result)

    @staticmethod
    def getDataAlignment(data):
        if data[:4] == b'SARC':  # Archive
            return 0x2000  # Ahh, SARC inside a SARC... the irony...

        elif data[:4] in [b'Yaz0', b'Yaz1']:  # Yaz0 compressed archive
            return 0x80

        elif data[:4] == b'FFNT':  # Wii U/Switch Binary font
            return 0x2000

        elif data[:4] == b'CFNT':  # 3DS Binary font
            return 0x80

        elif data[:4] in [b'CSTM', b'FSTM', b'FSTP', b'CWAV', b'FWAV']:  # Audio data
            return 0x20

        elif data[:8] in [b'BNTX\0\0\0\0', b'BNSH\0\0\0\0', b'FSHA    ']:  # Switch GPU data
            return 0x1000

        elif data[:4] in [b'Gfx2', b'FRES', b'AAHS', b'BAHS'] or data[-0x28:-0x24] == b'FLIM':  # Wii U GPU data and Wii U/Switch Binary Resources
            return 0x2000

        elif data[:4] == b'CTPK':  # 3DS Texture package
            return 0x10

        elif data[:4] == b'CGFX' or data[-0x28:-0x24] == b'CLIM':  # 3DS Layout image and Binary Resources
            return 0x80

        elif data[:4] == b'AAMP':  # Environment settings
            return 8

        elif (data[:2] in [b'YB', b'BY']
                  or data[:8] in [b'MsgStdBn', b'MsgPrjBn']):  # Binary text
            return 0x80

        elif data[0xC:0x10] == b'SCDL':  # SMM2 Course data
            return 0x100

        else:
            return 4

    def save(self, dataStartOffset=0):
        """
        Returns a bytes object that can be saved to a file.
        """
        # Flatten the file list
        flatList = []

        def addToFlatList(folder, path):
            nonlocal flatList

            if "\\" in path:
                path = "/".join(path.split("\\"))

            if path[-1] != "/":
                path += "/"

            for checkObj in folder.contents:
                if isinstance(checkObj, File):
                    flatList.append((path + checkObj.name, checkObj))

                else:
                    addToFlatList(checkObj, path + checkObj.name)

        for checkObj in self.contents:
            if isinstance(checkObj, File):
                flatList.append((checkObj.name, checkObj))

            else:
                addToFlatList(checkObj, checkObj.name)

        def sortByHash(filetuple):
            if filetuple[1].hasFilename:
                return struct.unpack(
                    self.endianness + 'I',
                    self.filenameHash(filetuple[0], self.endianness, self.hashKey),
                )

            else:
                return [int(filetuple[1].name[5:].split('.')[0].split()[0], 16)]

        # Sort the files by hash
        flatList.sort(
            key=sortByHash,
        )

        # Put each file object into a list
        files = [[file, ] for file in flatList]

        # Create the File Names table
        fileNamesTable = b''
        for i, filetuplelist in enumerate(files):
            filepath = filetuplelist[0][0]
            files[i] = [filetuplelist[0][1], ]
            file = files[i]

            if not file[0].hasFilename:
                # The file has no name, set the offset to 0
                file.append(0)

            else:
                # Add the name offset, this will be used later
                file.append(len(fileNamesTable))

                # Add the name to the table
                fileNamesTable += filepath.encode('utf-8')

                # Pad to 0x04
                fileNamesTable += b'\x00' * (0x04 - (len(fileNamesTable) % 0x04))

        # Determine the length of the SFAT Nodes table
        SFATNodesTableLen = 0x10 * len(files)

        def round_up(x, y):
            return ((x - 1) | (y - 1)) + 1

        # Determine the Beginning Of Data offset
        dataStartOffset = max(
            round_up(0x20 + SFATNodesTableLen + 0x08 + len(fileNamesTable), 0x04),
            round_up(dataStartOffset, 0x04),
        )

        maxAlignment = 0

        # Create the File Data table
        fileDataTable = b''
        for idx, file in enumerate(files):
            # Align the data
            alignment = self.getDataAlignment(file[0].data)
            totalFileLen = round_up(len(fileDataTable), alignment)
            maxAlignment = max(maxAlignment, alignment)

            fileDataTable += b'\x00' * (totalFileLen - len(fileDataTable))

            # Add the data offset, this will be used later
            file.append(len(fileDataTable))

            # Add the data to the table
            fileDataTable += file[0].data

        dataStartOffset = round_up(dataStartOffset, maxAlignment)

        # Calculate total file length
        totalFileLen = dataStartOffset + len(fileDataTable)

        # SARC Header -----------------------------------------

        # File magic
        sarcHead = b'SARC'

        # Header length (always 0x14)
        sarcHead += struct.pack(self.endianness + 'H', 0x14)

        # BOM
        sarcHead += b'\xFE\xFF' if self.endianness == '>' else b'\xFF\xFE'

        # File Length
        sarcHead += struct.pack(self.endianness + 'I', totalFileLen)

        # Beginning Of Data offset
        sarcHead += struct.pack(self.endianness + 'I', dataStartOffset)

        # Unknown value
        if self.endianness == '>':
            sarcHead += b'\1\0\0\0'

        else:
            sarcHead += b'\0\1\0\0'

        # SFAT Header -----------------------------------------

        # File magic
        sfatHead = b'SFAT'

        # Header length (always 0x0C)
        sfatHead += struct.pack(self.endianness + 'H', 0x0C)

        # Number of files
        sfatHead += struct.pack(self.endianness + 'H', len(files))

        # Hash key
        sfatHead += struct.pack(self.endianness + 'I', self.hashKey)

        # SFAT Nodes
        sfat = b''
        for (_, filenameoffset, filedataoffset), (filepath, file) in zip(files, flatList):
            if not file.hasFilename:
                # Filename Hash
                sfat += struct.pack(self.endianness + 'I', int(file.name[5:].split('.')[0].split()[0], 16))

                # Filename Offset
                sfat += b'\0\0\0\0'

            else:
                # Filename Hash
                sfat += self.filenameHash(filepath, self.endianness, self.hashKey)

                # Filename Offset (3 bytes + ID)
                sfat += struct.pack(self.endianness + 'I', (filenameoffset // 4) | 0x1000000)

            # Filedata Offset
            sfat += struct.pack(self.endianness + 'I', filedataoffset)

            # Filedata Length + Filedata Offset
            sfat += struct.pack(self.endianness + 'I', filedataoffset + len(file.data))

        # SFNT Header -----------------------------------------

        # File magic
        sfntHead = b'SFNT'

        # Header length (always 0x08)
        if self.endianness == '>':
            sfntHead += b'\x00\x08'

        else:
            sfntHead += b'\x08\x00'

        # 2-byte padding
        sfntHead += b'\x00\x00'

        # File Data Table Padding
        headerSize = len(sarcHead + sfatHead + sfat + sfntHead + fileNamesTable)
        fileDataTablePadding = b''

        if dataStartOffset > headerSize:
            fileDataTablePadding = b'\0' * (dataStartOffset - headerSize)

        # Put It All Together ---------------------------------

        fileData = b''.join([
            sarcHead, sfatHead, sfat,
            sfntHead + fileNamesTable,
            fileDataTablePadding + fileDataTable,
        ])

        # Return the data
        return fileData, maxAlignment
