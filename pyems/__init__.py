try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from .protocols import SCHEMES
from .utils import expected, get_module_class, EvoStreamException


class Api(object):
    def __init__(self, uri):
        url = urlparse.urlparse(uri)
        try:
            protocol_class = get_module_class(SCHEMES[url.scheme])
        except KeyError:
            raise EvoStreamException('Invalid uri "%s"' % uri)
        self.protocol = protocol_class(url.hostname, url.port)

    @expected('uri', 'keepAlive', 'localStreamName', 'forceTcp', 'tcUrl',
              'pageUrl', 'swfUrl', 'rangeStart', 'rangeEnd', 'ttl', 'tos',
              'rtcpDetectionInterval', 'emulateUserAgent', 'isAudio',
              'audioCodecBytes', 'spsBytes', 'ppsBytes', 'ssmIp', 'httpProxy')
    def pull_stream(self, uri, **kwargs):
        """
        This will try to pull in a stream from an external source. Once a
        stream has been successfully pulled it is assigned a 'local stream
        name' which can be used to access the stream from the EMS.

        :param uri: The URI of the external stream. Can be RTMP, RTSP or
            unicast/multicast (d) mpegts
        :type uri: str

        :param keepAlive: If keepAlive is set to 1, the server will attempt to
            reestablish connection with a stream source after a connection has
            been lost. The reconnect will be attempted once every second
            (default: 1 true)
        :type keepAlive: int

        :param localStreamName: If provided, the stream will be given this
            name. Otherwise, a fallback techniques used to determine the stream
            name (based on the URI)
        :type localStreamName: str

        :param forceTcp: If 1 and if the stream is RTSP, a TCP connection will
            be forced. Otherwise the transport mechanism will be negotiated
            (UDP or TCP) (default: 1 true)
        :type forceTcp: int

        :param tcUrl: When specified, this value will be used to set the TC URL
            in the initial RTMP connect invoke
        :type tcUrl: str

        :param pageUrl: When specified, this value will be used to set the
            originating web page address in the initial RTMP connect invoke
        :type pageUrl: str

        :param swfUrl: When specified, this value will be used to set the
            originating swf URL in the initial RTMP connect invoke
        :type swfUrl: str

        :param rangeStart: For RTSP and RTMP connections. A value from which
            the playback should start expressed in seconds. There are 2 special
            values: -2 and -1. For more information, please read about
            start/len parameters here:
            http://livedocs.adobe.com/flashmediaserver/3.0/hpdocs/help.html?content=00000185.html
        :type rangeStart: int

        :param rangeEnd: The length in seconds for the playback. -1 is a
            special value. For more information, please read about start/len
            parameters here:
            http://livedocs.adobe.com/flashmediaserver/3.0/hpdocs/help.html?content=00000185.html
        :type rangeEnd: int

        :param ttl: Sets the IP_TTL (time to live) option on the socket
        :type ttl: int

        :param tos: Sets the IP_TOS (Type of Service) option on the socket
        :type tos: int

        :param rtcpDetectionInterval: How much time (in seconds) should the
            server wait for RTCP packets before declaring the RTSP stream as a
            RTCP-less stream
        :type rtcpDetectionInterval: int

        :param emulateUserAgent: When specified, this value will be used as the
            user agent string. It is meaningful only for RTMP
        :type emulateUserAgent: str

        :param isAudio: If 1 and if the stream is RTP, it indicates that the
            currently pulled stream is an audio source. Otherwise the pulled
            source is assumed as a video source
        :type isAudio: int

        :param audioCodecBytes: The audio codec setup of this RTP stream if it
            is audio. Represented as hex format without '0x' or 'h'. For
            example: audioCodecBytes=1190
        :type audioCodecBytes: str

        :param spsBytes: The video SPS bytes of this RTP stream if it is video.
            It should be base 64 encoded.
        :type spsBytes: str

        :param ppsBytes: The video PPS bytes of this RTP stream if it is video.
            It should be base 64 encoded
        :type ppsBytes: str

        :param ssmIp: The source IP from source-specific-multicast. Only usable
            when doing UDP based pull
        :type ssmIp: str

        :param httpProxy: This parameter has two valid values: IP:Port - This
            value combination specifies an RTSP HTTP Proxy from which the RTSP
            stream should be pulled from Self - Specifying "self" as the value
            implies pulling RTSP over HTTP
        :type httpProxy: str

        :link: http://docs.evostream.com/ems_api_definition/pullstream
        """
        return self.protocol.execute('pullStream', uri=uri, **kwargs)

    @expected('uri', 'keepAlive', 'localStreamName', 'targetStreamName',
              'targetStreamType', 'tcUrl', 'pageUrl', 'swfUrl', 'ttl', 'tos',
              'emulateUserAgent', 'rtmpAbsoluteTimestamps',
              'sendChunkSizeRequest', 'useSourcePts')
    def push_stream(self, uri, **kwargs):
        """
        Try to push a local stream to an external destination. The pushed
        stream can only use the RTMP, RTSP or MPEG-TS unicast/multicast
        protocol.

        :param uri: The URI of the external stream. Can be RTMP, RTSP or
            unicast/multicast (d) mpegts
        :type uri: str

        :param keepAlive: If keepAlive is set to 1, the server will attempt to
            reestablish connection with a stream source after a connection has
            been lost. The reconnect will be attempted once every second
            (default: 1 true)
        :type keepAlive: int

        :param localStreamName: If provided, the stream will be given this
            name. Otherwise, a fallback techniques used to determine the stream
            name (based on the URI)
        :type localStreamName: str

        :param targetStreamName: The name of the stream at destination. If not
            provided, the target stream name willbe the same as the local
            stream name
        :type targetStreamName: str

        :param targetStreamType: It can be one of following: **live**,
            **record**, **append**. It is meaningful only for RTMP
        :type targetStreamType: str

        :param tcUrl: When specified, this value will be used to set the TC
            URL in the initial RTMP connect invoke
        :type tcUrl: str

        :param pageUrl: When specified, this value will be used to set the
            originating web page address in the initial RTMP connect invoke
        :type pageUrl: str

        :param swfUrl: When specified, this value will be used to set the
            originating swf URL in the initial RTMP connect invoke
        :type swfUrl: str

        :param ttl: Sets the IP_TTL (time to live) option on the socket
        :type ttl: int

        :param tos: Sets the IP_TOS (Type of Service) option on the socket
        :type tos: int

        :param emulateUserAgent: When specified, this value will be used as the
            user agent string. It is meaningful only for RTMP
        :type emulateUserAgent: str

        :param rtmpAbsoluteTimestamps: Forces the timestamps to be absolute
            when using RTMP.
        :type rtmpAbsoluteTimestamps: int

        :param sendChunkSizeRequest: Sets whether the RTMP stream will or will
            not send a "Set Chunk Length" message. This is significant when
            pushing to Akamai's new RTMP HD ingest point where this parameter
            should be set to 0 so that Akamai will not drop the connection.
        :type sendChunkSizeRequest: int

        :param useSourcePts: When value is true, timestamps on source inbound
            RTMP stream are passed directly to the outbound (pushed) RTMP
            streams. This affects only pushed Outbound Net RTMP with net RTMP
            source. This parameter overrides the value of the config.lua
            option of the same name.
        :type useSourcePts: int

        :link: http://docs.evostream.com/ems_api_definition/pushstream
        """
        return self.protocol.execute('pushStream', uri=uri, **kwargs)

    @expected('localStreamNames', 'targetFolder', 'keepAlive',
              'overwriteDestination', 'staleRetentionCount',
              'createMasterPlaylist', 'cleanupDestination', 'bandwidths',
              'groupName', 'playlistType', 'playlistLength', 'playlistName',
              'chunkLength', 'maxChunkLength', 'chunkBaseName', 'chunkOnIDR',
              'drmType', 'AESKeyCount', 'audioOnly', 'hlsResume',
              'cleanupOnClose', 'useByteRange', 'fileLength', 'useSystemTime',
              'offsetTime', 'startOffset')
    def create_hls_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create an HTTP Live Stream (HLS) out of an existing H.264/AAC stream.
        HLS is used to stream live feeds to iOS devices such as iPhones and
        iPads.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local stream
            names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the .ts/.m3u8 files will be
            stored. This folder must be accessible by the HLS clients. It is
            usually in the web-root of the server.
        :type targetFolder: str

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If true, it will force overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: The number of old files kept besides the
            ones listed in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param createMasterPlaylist: If true, a master playlist will be
            created.
        :type createMasterPlaylist: int

        :param cleanupDestination: If true, all *.ts and *.m3u8 files in the
            target folder will be removed before HLS creation is started.
        :type cleanupDestination: int

        :param bandwidths: The corresponding bandwidths for each stream listed
            in localStreamNames. Again, this can be a comma-delimited list.
        :type bandwidths: int

        :param groupName: The name assigned to the HLS stream or group. If the
            localStreamNames parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param playlistType: Either appending or rolling.
        :type playlistType: str

        :param playlistLength: The length (number of elements) of the playlist.
            Used only when playlistType is rolling. Ignored otherwise.
        :type playlistLength: int

        :param playlistName: The file name of the playlist (*.m3u8).
        :type playlistName: str

        :param chunkLength: The length (in seconds) of each playlist element
            (*.ts file). Minimum value is 1 (second).
        :type chunkLength: int

        :param maxChunkLength: Maximum length (in seconds) the EMS will allow
            any single chunk to be. This is primarily in the case of
            chunkOnIDR=true where the EMS will wait for the next key-frame. If
            the maxChunkLength is less than chunkLength, the parameter shall
            be ignored.
        :type maxChunkLength: int

        :param chunkBaseName: The base name used to generate the *.ts chunks.
        :type chunkBaseName: str

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param drmType: Type of DRM encryption to use. Options are: none
            (no encryption), evo (AES Encryption), SAMPLE-AES (Sample-AES),
            verimatrix (Verimatrix DRM). For Verimatrix DRM, the "drm" section
            of the config.lua file must be active and properly configured.
        :type drmType: str

        :param AESKeyCount: Number of keys that will be automatically generated
            and rotated over while encrypting this HLS stream.
        :type AESKeyCount: int

        :param audioOnly: If true, stream will be audio only.
        :type audioOnly: int

        :param hlsResume: If true, HLS will resume in appending segments to
            previously created child playlist even in cases of EMS shutdown or
            cut off stream source.
        :type hlsResume: int

        :param cleanupOnClose: If true, corresponding hls files to a stream
            will be deleted if the said stream is removed or shut down or
            disconnected.
        :type cleanupOnClose: int

        :param useByteRange: If true, will use the EXT-X-BYTERANGE feature of
            HLS (version 4 and up).
        :type useByteRange: int

        :param fileLength: When using useByteRange=1, this parameter needs to
            be set too. This will be the size of file before chunking it to
            another file, this replace the chunkLength in case of
            EXT-X-BYTERANGE, since chunkLength will be the byte range chunk.
        :type fileLength: int

        :param useSystemTime: If true, uses UTC in playlist time stamp
            otherwise will use the local server time.
        :type useSystemTime: int

        :param offsetTime:
        :type offsetTime: int

        :param startOffset: A parameter valid only for HLS v.6 onwards. This
            will indicate the start offset time (in seconds) for the playback
            of the playlist.
        :type startOffset: int

        :link: http://docs.evostream.com/ems_api_definition/createhlsstream
        """
        return self.protocol.execute('createhlsstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)

    @expected('localStreamNames', 'targetFolder', 'bandwidths',
              'chunkBaseName', 'chunkLength', 'chunkOnIDR', 'groupName',
              'keepAlive', 'manifestName', 'overwriteDestination',
              'playlistType', 'playlistLength', 'staleRetentionCount',
              'createMasterPlaylist', 'cleanupDestination')
    def create_hds_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create an HDS (HTTP Dynamic Streaming) stream out of an existing
        H.264/AAC stream. HDS is used to stream standard MP4 media over
        regular HTTP connections.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local stream
            names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest (*.f4m) and
            fragment (f4v*) files will be stored. This folder must be
            accessible by the HDS clients. It is usually in the web-root of
            the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in localStreamNames. Again, this can be a comma-delimited list.
        :type bandwidths: int

        :param chunkBaseName: The base name used to generate the fragments.
        :type chunkBaseName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
            Minimum value is 1 (second).
        :type chunkLength: int

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param groupName: The name assigned to the HDS stream or group. If the
            localStreamNames parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param overwriteDestination: If true, it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param playlistType: Either appending or rolling.
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            playlistType is "rolling". Ignored otherwise.
        :type playlistLength: int

        :param staleRetentionCount: The number of old files kept besides the
            ones listed in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param createMasterPlaylist: If true, a master playlist will be
            created.
        :type createMasterPlaylist: int

        :param cleanupDestination: If true, all manifest and fragment files in
            the target folder will be removed before HDS creation is started.
        :type cleanupDestination: int

        :link: http://docs.evostream.com/ems_api_definition/createhdsstream
        """
        return self.protocol.execute('createhdsstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)

    @expected('localStreamNames', 'targetFolder', 'bandwidths', 'groupName',
              'playlistType', 'playlistLength', 'manifestName', 'chunkLength',
              'chunkOnIDR', 'keepAlive', 'overwriteDestination',
              'staleRetentionCount', 'cleanupDestination', 'ismType',
              'isLive', 'publishingPoint', 'ingestMode')
    def create_mss_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create a Microsoft Smooth Stream (MSS) out of an existing H.264/AAC
        stream. Smooth Streaming was developed by Microsoft to compete with
        other adaptive streaming technologies.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local
            stream names)
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest and fragment
            files will be stored. This folder must be accessible by the MSS
            clients. It is usually in the web-root of the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in `localStreamNames`. Again, this can be a comma-delimited list.
        :type bandwidths: int or str

        :param groupName: The name assigned to the MSS stream or group. If the
            `localStreamNames` parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param playlistType: Either `appending` or `rolling`
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            `playlistType` is `rolling`. Ignored otherwise.
        :type playlistLength: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
        :type chunkLength: int

        :param chunkOnIDR: If 1 (true), chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param keepAlive: If 1 (true), the EMS will attempt to reconnect to
            the stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If 1 (true), it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: How many old files are kept besides the
            ones present in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param cleanupDestination: If 1 (true), all manifest and fragment
            files in the target folder will be removed before MSS creation is
            started.
        :type cleanupDestination: int

        :param ismType: Either ismc for serving content to client or isml for
            serving content to smooth server.
        :type ismType: int

        :param isLive: If true, creates a live MSS stream, otherwise set to 0
            for VOD.
        :type isLive: int

        :param publishingPoint: This parameter is needed when `ismType=isml`,
            it is the REST URI where the mss contents will be ingested.
        :type publishingPoint: str

        :param ingestMode: Either `single` for a non looping ingest or `loop`
            for looping an ingest.
        :type ingestMode: str

        :link: http://docs.evostream.com/ems_api_definition/createmssstream
        """
        return self.protocol.execute('createmssstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)

    @expected('localStreamNames', 'targetFolder', 'bandwidths', 'groupName',
              'playlistType', 'playlistLength', 'manifestName', 'chunkLength',
              'chunkOnIDR', 'keepAlive', 'overwriteDestination',
              'staleRetentionCount', 'cleanupDestination', 'dynamicProfile')
    def create_dash_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create Dynamic Adaptive Streaming over HTTP (DASH) out of an existing
        H.264/AAC stream. DASH was developed by the Moving Picture Experts
        Group (MPEG) to establish a standard for HTTP adaptive-bitrate
        streaming that would be accepted by multiple vendors and facilitate
        interoperability.

        :param localStreamNames: The stream(s) that will be used as the
            input. This is a comma-delimited list of active stream names
            (local stream names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest and fragment
            files will be stored. This folder must be accessible by the DASH
            clients. It is usually in the web-root of the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in `localStreamNames`. Again, this can be a comma-delimited list.
        :type bandwidths: int or str

        :param groupName: The name assigned to the DASH stream or group. If
            the `localStreamNames` parameter contains only one entry and
            `groupName` is not specified, `groupName` will have the value of
            the input stream name.
        :type groupName: str

        :param playlistType: Either `appending` or `rolling`.
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            `playlistType` is `rolling`. Ignored otherwise.
        :type playlistLength: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
        :type chunkLength: int

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If true, it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: How many old files are kept besides the
            ones present in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param cleanupDestination: If true, all manifest and fragment files in
            the target folder will be removed before DASH creation is started.
        :type cleanupDestination: int

        :param dynamicProfile: Set this parameter to 1 (default) for a live
            DASH, otherwise set it to 0 for a VOD.
        :type dynamicProfile: int

        :link: http://docs.evostream.com/ems_api_definition/createdashstream
        """
        return self.protocol.execute('createdashstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)

    @expected('localStreamName', 'pathToFile', 'type', 'overwrite',
              'keepAlive', 'chunkLength', 'waitForIDR', 'winQtCompat',
              'dateFolderStructure')
    def record(self, localStreamName, pathToFile, **kwargs):
        """
        Records any inbound stream. The record command allows users to record
        a stream that may not yet exist. When a new stream is brought into
        the server, it is checked against a list of streams to be recorded.

        Streams can be recorded as FLV files, MPEG-TS files or as MP4 files.

        :param localStreamName: The name of the stream to be used as input
            for recording.
        :type localStreamName: str

        :param pathToFile: Specify path and file name to write to.
        :type pathToFile: str

        :param type: `ts`, `mp4` or `flv`
        :type type: str

        :param overwrite: If false, when a file already exists for the stream
            name, a new file will be created with the next appropriate number
            appended. If 1 (true), files with the same name will be
            overwritten.
        :type overwrite: int

        :param keepAlive: If 1 (true), the server will restart recording every
            time the stream becomes available again.
        :type keepAlive: int

        :param chunkLength: If non-zero the record command will start a new
            recording file after ChunkLength seconds have elapsed.
        :type chunkLength: int

        :param waitForIDR: This is used if the recording is being chunked.
            When true, new files will only be created on IDR boundaries.
        :type waitForIDR: int

        :param winQtCompat: Mandates 32bit header fields to ensure
            compatibility with Windows QuickTime.
        :type winQtCompat: int

        :param dateFolderStructure: If set to 1 (true), folders will be
            created with names in `YYYYMMDD` format. Recorded files will be
            placed inside these folders based on the date they were created.
        :type dateFolderStructure: int

        :link: http://docs.evostream.com/ems_api_definition/record
        """
        return self.protocol.execute('record',
                                     localStreamName=localStreamName,
                                     pathToFile=pathToFile, **kwargs)

    @expected('source', 'destinations', 'targetStreamNames', 'groupName',
              'videoBitrates', 'videoSizes', 'videoAdvancedParamsProfiles',
              'audioBitrates', 'audioChannelsCounts', 'audioFrequencies',
              'audioAdvancedParamsProfiles', 'overlays', 'croppings',
              'keepAlive', 'commandFlags')
    def transcode(self, source, destinations, **kwargs):
        """
        Changes the compression characteristics of an audio and/or video
        stream. Allows you to change the resolution of a source stream, change
        the bitrate of a stream, change a VP8 or MPEG2 stream into H.264 and
        much more. Allow users to create overlays on the final stream as well
        as crop streams.

        :param source: Can be a URI or a local stream name from EMS.
        :type source: str

        :param destinations: The target URI(s) or stream name(s) of the
            transcoded stream. If only a name is given, it will be pushed
            back to the EMS.
        :type destinations: str

        :param targetStreamNames: The name of the stream(s) at destination(s).
            If not specified, and a full URI is provided to destinations,
            name will have a time stamped value.
        :type targetStreamNames: str

        :param groupName: The group name assigned to this process. If not
            specified, groupName will have a random value.
        :type groupName: str

        :param videoBitrates: Target output video bitrate(s) (in bits/s,
            append `k` to value for kbits/s). Accepts the value `copy` to
            copy the input bitrate. An empty value passed would mean no video.
        :type videoBitrates: str

        :param videoSizes: Target output video size(s) in wxh (width x height)
            format. IE: 240x480.
        :type videoSizes: str

        :param videoAdvancedParamsProfiles: Name of video profile template
            that will be used.
        :type videoAdvancedParamsProfiles: str

        :param audioBitrates: Target output audio bitrate(s) (in bits/s,
            append `k` to value for kbits/s). Accepts the value `copy` to
            copy the input bitrate. An empty value passed would mean no audio.
        :type audioBitrates: str

        :param audioChannelsCounts: Target output audio channel(s) count(s).
            Valid values are 1 (mono), 2 (stereo), and so on. Actual supported
            channel count is dependent on the number of input audio channels.
        :type audioChannelsCounts: str

        :param audioFrequencies: Target output audio frequency(ies) (in Hz,
            append `k` to value for kHz).
        :type audioFrequencies: str

        :param audioAdvancedParamsProfiles: Name of audio profile template
            that will be used.
        :type audioAdvancedParamsProfiles: str

        :param overlays: Location of the overlay source(s) to be used. These
            are transparent images (normally in PNG format) that have the same
            or smaller size than the video. Image is placed at the top-left
            position of the video.
        :type overlays: str

        :param croppings: Target video cropping position(s) and size(s) in
            `left : top : width : height` format (e.g. 0:0:200:100. Positions
            are optional (200:100 for a centered cropping of 200 width and 100
            height in pixels). Values are limited to the actual size of the
            video.
        :type croppings: str

        :param keepAlive: If keepAlive is set to 1, the server will restart
            transcoding if it was previously activated.
        :type keepAlive: int

        :param commandFlags: Other commands to the transcode process that are
            not supported by the baseline transcode command.
        :type commandFlags: str

        :link: http://docs.evostream.com/ems_api_definition/transcode
        """
        return self.protocol.execute('transcode', source=source,
                                     destinations=destinations, **kwargs)

    def list_streams_ids(self):
        """
        Get a list of IDs for every active stream.

        :link: http://docs.evostream.com/ems_api_definition/liststreamsids
        """
        return self.protocol.execute('listStreamsIds')

    @expected('id', 'localStreamName')
    def get_stream_info(self, **kwargs):
        """
        Returns a detailed set of information about a stream.

        :param id: The uniqueId of the stream. Usually a value returned by
            listStreamsIDs. This parameter is not mandatory but either this or
            the localStreamName should be present to identify the particular
            stream
        :type id: int

        :param localStreamName: The name of the stream. This parameter is not
            mandatory but either this or the id should be present to identify
            the particular stream
        :type localStreamName: str

        :link: http://docs.evostream.com/ems_api_definition/getstreaminfo
        """
        return self.protocol.execute('getStreamInfo', **kwargs)

    @expected('disableInternalStreams')
    def list_streams(self, **kwargs):
        """
        Provides a detailed description of all active streams.

        :param disableInternalStreams: If this is 1 (true), internal streams
            (origin-edge related) are filtered out from the list
        :type disableInternalStreams: int

        :link: http://docs.evostream.com/ems_api_definition/liststreams
        """
        return self.protocol.execute('listStreams', **kwargs)

    def get_streams_count(self):
        """
        Returns the number of active streams.

        :link: http://docs.evostream.com/ems_api_definition/getstreamscount
        """
        return self.protocol.execute('getStreamsCount')

    @expected('id', 'localStreamName', 'permanently')
    def shutdown_stream(self, **kwargs):
        """
        Terminates a specific stream. When permanently=1 is used, this command
        is analogous to removeConfig.

        :param id: The uniqueId of the stream that needs to be terminated. The
            stream ID's can be obtained using the listStreams command. This
            parameter is not mandatory but either this or localStreamName
            should be present to identify the particular stream
        :type id: int

        :param localStreamName: The name of the inbound stream which you wish
            to terminate. This will also terminate any outbound streams that
            are dependent upon this input stream. This parameter is not
            mandatory but either this or the id should be present to identify
            the particular stream
        :type localStreamName: str

        :param permanently: If true, the corresponding push/pull configuration
            will also be terminated. Therefore, the stream will NOT be
            reconnected when the server restarts
        :type permanently: int

        :link: http://docs.evostream.com/ems_api_definition/shutdownstream
        """
        return self.protocol.execute('shutdownStream', **kwargs)

    def list_config(self):
        """
        Returns a list with all push/pull configurations.

        Whenever the pullStream or pushStream interfaces are called, a record
        containing the details of the pull or push is created in the
        pullpushconfig.xml file. Then, the next time the EMS is started, the
        pullpushconfig.xml file is read, and the EMS attempts to reconnect all
        of the previous pulled or pushed streams.

        :link: http://docs.evostream.com/ems_api_definition/listconfig
        """
        return self.protocol.execute('listConfig')

    @expected('id', 'groupName', 'removeHlsHdsFiles')
    def remove_config(self, **kwargs):
        """
        This command will both stop the stream and remove the corresponding
        configuration entry. This command is the same as performing
        shutdownStream permanently=1.

        :param id: The configId of the configuration that needs to be removed.
            ConfigId's can be obtained from the listConfig interface.
            Removing an inbound stream will also automatically remove all
            associated outbound streams.
        :type id: int

        :param groupName: The name of the group that needs to be removed
            (applicable to HLS, HDS and external processes). Mandatory only if
            the id parameter is not specified.
        :type groupName: str

        :param removeHlsHdsFiles: If 1 (true) and the stream is HLS or HDS, the
            folder associated with it will be removed
        :type removeHlsHdsFiles: int

        :link: http://docs.evostream.com/ems_api_definition/removeconfig
        """
        return self.protocol.execute('removeConfig', **kwargs)

    @expected('id', )
    def get_config_info(self, id):
        """
        Returns the information of the stream by the configId.

        :param id: The configId of the configuration to get some information
        :type id: int

        :link: http://docs.evostream.com/ems_api_definition/getconfiginfo
        """
        return self.protocol.execute('getConfigInfo', id=id)

    @expected('id', 'localStreamName')
    def is_stream_running(self, **kwargs):
        """
        Checks a specific stream if it is running or not.

        :param id: The unique id of the stream to check.
        :type id: int

        :param localStreamName: The name of the stream to check.
        :type localStreamName: str

        :link: http://docs.evostream.com/ems_api_definition/isstreamrunning
        """
        return self.protocol.execute('isStreamRunning', **kwargs)

    @expected('localStreamName', 'aliasName', 'expirePeriod')
    def add_stream_alias(self, localStreamName, aliasName, **kwargs):
        """
        Allows you to create secondary name(s) for internal streams. Once an
        alias is created the localstreamname cannot be used to request
        playback of that stream. Once an alias is used (requested by a client)
        the alias is removed. Aliases are designed to be used to protect/hide
        your source streams.

        :param localStreamName: The original stream name
        :type localStreamName: str

        :param aliasName: The alias alternative to the localStreamName
        :type aliasName: str

        :param expirePeriod: The expiration period for this alias. Negative
            values will be treated as one-shot but no longer than the absolute
            positive value in seconds, 0 means it will not expire, positive
            values mean the alias can be used multiple times but expires after
            this many seconds. The default is -600 (one-shot, 10 mins)
        :type expirePeriod: int

        :link: http://docs.evostream.com/ems_api_definition/addstreamalias
        """
        return self.protocol.execute('addStreamAlias',
                                     localStreamName=localStreamName,
                                     aliasName=aliasName, **kwargs)

    def list_stream_aliases(self):
        """
        Returns a complete list of aliases.

        :link: http://docs.evostream.com/ems_api_definition/liststreamaliases
        """
        return self.protocol.execute('listStreamAliases')

    @expected('aliasName', )
    def remove_stream_alias(self, aliasName):
        """
        Removes an alias of a stream.

        :param aliasName: The alias to delete
        :type aliasName: str

        :link: http://docs.evostream.com/ems_api_definition/removestreamalias
        """
        return self.protocol.execute('removeStreamAlias', aliasName=aliasName)

    def flush_stream_aliases(self):
        """
        Invalidates all streams aliases.

        :link: http://docs.evostream.com/ems_api_definition/flushstreamaliases
        """
        return self.protocol.execute('flushStreamAliases')

    @expected('groupName', 'aliasName')
    def add_group_name_alias(self, groupName, aliasName):
        """
        Creates secondary name(s) for group names. Once an alias is created the
        group name cannot be used to request HTTP playback of that stream. Once
        an alias is used (requested by a client) the alias is removed. Aliases
        are designed to be used to protect/hide your source streams.

        :param groupName: The original group name
        :type groupName: str

        :param aliasName: The alias alternative to the group name
        :type aliasName: str

        :link: http://docs.evostream.com/ems_api_definition/addgroupnamealias
        """
        return self.protocol.execute('addGroupNameAlias', groupName=groupName,
                                     aliasName=aliasName)

    def flush_group_name_aliases(self):
        """
        Invalidates all group name aliases.

        :link: http://docs.evostream.com/ems_api_definition/flushgroupnamealiases
        """
        return self.protocol.execute('flushGroupNameAliases')

    @expected('aliasName')
    def get_group_name_by_alias(self, aliasName):
        """
        Returns the group name given the alias name.

        :param aliasName: The group name alias
        :type aliasName: str

        :link: http://docs.evostream.com/ems_api_definition/getgroupnamebyalias
        """
        return self.protocol.execute('getGroupNameByAlias',
                                     aliasName=aliasName)

    def list_group_name_aliases(self):
        """
        Returns a complete list of group name aliases.

        :link: http://docs.evostream.com/ems_api_definition/listgroupnamealiases
        """
        return self.protocol.execute('listGroupNameAliases')

    @expected('aliasName')
    def remove_group_name_alias(self, aliasName):
        """
        Removes an alias of a group.

        :param aliasName: The alias alternative to be removed from the group
            name.
        :type aliasName: str

        :link: http://docs.evostream.com/ems_api_definition/removegroupnamealiases
        """
        return self.protocol.execute('removeGroupNameAlias',
                                     aliasName=aliasName)

    def list_http_streaming_sessions(self):
        """
        Lists all currently active HTTP streaming sessions.

        :link: http://docs.evostream.com/ems_api_definition/listhttpstreamingsessions
        """
        return self.protocol.execute('listHttpStreamingSessions')

    @expected('privateStreamName', 'publicStreamName')
    def create_ingest_point(self, privateStreamName, publicStreamName):
        """
        Creates an RTMP ingest point, which mandates that streams pushed into
        the EMS have a target stream name which matches one Ingest Point
        privateStreamName.

        :param privateStreamName: The name that RTMP Target Stream Names must
            match.
        :type privateStreamName: str

        :param publicStreamName: The name that is used to access the stream
            pushed to the privateStreamName. The publicStreamName becomes the
            streams localStreamName.
        :type publicStreamName: str

        :link: http://docs.evostream.com/ems_api_definition/createingestpoint
        """
        return self.protocol.execute('createIngestPoint',
                                     privateStreamName=privateStreamName,
                                     publicStreamName=publicStreamName)

    @expected('privateStreamName')
    def remove_ingest_point(self, privateStreamName):
        """
        Removes an RTMP ingest point.

        :param privateStreamName: The Ingest Point is identified by the
            privateStreamName, so only that is required to delete it.
        :type privateStreamName: str

        :link: http://docs.evostream.com/ems_api_definition/removeingestpoint
        """
        return self.protocol.execute('removeIngestPoint',
                                     privateStreamName=privateStreamName)

    def list_ingest_points(self):
        """
        Lists the currently available Ingest Points.

        :link: http://docs.evostream.com/ems_api_definition/listingestpoints
        """
        return self.protocol.execute('listIngestPoints')

    def start_web_rtc(self, ersip, ersport, roomId):
        """
        Starts a WebRTC signalling client to an ERS (Evostream Rendezvous
        Server).

        :param ersip: IP address (xx.yy.zz.xx) of ERS.
        :type ersip: str

        :param ersport: IP port of ERS.
        :type ersport: int

        :param roomId: Unique room Identifier within ERS that will be used by
            client browsers to connect to this EMS.
        :type roomId: str

        :link: http://docs.evostream.com/ems_api_definition/startwebrtc
        """
        return self.protocol.execute('startwebrtc', ersip=ersip, ersport=ersport,
                                     roomId=roomId)
