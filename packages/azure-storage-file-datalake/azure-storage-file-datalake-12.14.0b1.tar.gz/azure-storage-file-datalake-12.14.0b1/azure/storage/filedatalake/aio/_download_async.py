# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from typing import AsyncIterator, IO, Optional

from .._deserialize import from_blob_properties


class StorageStreamDownloader(object):
    """A streaming object to download from Azure Storage.

    :ivar str name:
        The name of the file being downloaded.
    :ivar ~azure.storage.filedatalake.FileProperties properties:
        The properties of the file being downloaded. If only a range of the data is being
        downloaded, this will be reflected in the properties.
    :ivar int size:
        The size of the total data in the stream. This will be the byte range if specified,
        otherwise the total size of the file.
    """

    def __init__(self, downloader):
        self._downloader = downloader
        self.name = self._downloader.name

        # Parse additional Datalake-only properties
        encryption_context = self._downloader._response.response.headers.get('x-ms-encryption-context')  # pylint: disable=line-too-long,protected-access

        self.properties = from_blob_properties(self._downloader.properties, encryption_context=encryption_context)  # pylint: disable=protected-access
        self.size = self._downloader.size

    def __len__(self):
        return self.size

    def chunks(self) -> AsyncIterator[bytes]:
        """Iterate over chunks in the download stream.

        :returns: An async iterator over the chunks in the download stream.
        :rtype: AsyncIterator[bytes]
        """
        return self._downloader.chunks()

    async def read(self, size: Optional[int] = -1) -> bytes:
        """
        Read up to size bytes from the stream and return them. If size
        is unspecified or is -1, all bytes will be read.

        :param Optional[int] size:
            The number of bytes to download from the stream. Leave unspecified
            or set to -1 to download all bytes.
        :returns:
            The requested data as bytes. If the return value is empty, there is no more data to read.
        :rtype: bytes
        """
        return await self._downloader.read(size)

    async def readall(self) -> bytes:
        """Download the contents of this file.

        This operation is blocking until all data is downloaded.
        :returns: The contents of the file.
        :rtype: bytes
        """
        return await self._downloader.readall()

    async def readinto(self, stream: IO[bytes]) -> int:
        """Download the contents of this file to a stream.

        :param IO[bytes] stream:
            The stream to download to. This can be an open file-handle,
            or any writable stream. The stream must be seekable if the download
            uses more than one parallel connection.
        :returns: The number of bytes read.
        :rtype: int
        """
        return await self._downloader.readinto(stream)
