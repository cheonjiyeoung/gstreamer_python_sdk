"""자동 생성된 타입 스텁 — 직접 수정하지 마세요.

    python -m gstreamer_python_sdk.codegen

생성 환경: GStreamer 1.20.3
엘리먼트 63개
"""

from fractions import Fraction
from typing import Any, ClassVar

from ..caps import Caps
from ..element import Element, Prop
from ..enums import GstEnum, GstFlags
from ..introspect import ElementSpec

CURATED: dict[str, str]

def make(class_name: str, factory_name: str) -> type[Element]: ...
def available() -> dict[str, str]: ...
def _nested_enums(class_name: str, spec: ElementSpec) -> dict[str, Any]: ...

# 이 시스템에 설치되지 않아 제외됨:
#   NvVideoConvert (nvvideoconvert)

class AggregatorStartTimeSelection(GstEnum):
    """GstAggregatorStartTimeSelection"""
    ZERO = 0  # zero
    FIRST = 1  # first
    SET = 2  # set

class AppLeakyType(GstEnum):
    """GstAppLeakyType"""
    NONE = 0  # none
    UPSTREAM = 1  # upstream
    DOWNSTREAM = 2  # downstream

class AppStreamType(GstEnum):
    """GstAppStreamType"""
    STREAM = 0  # stream
    SEEKABLE = 1  # seekable
    RANDOM_ACCESS = 2  # random-access

class AudioDitherMethod(GstEnum):
    """GstAudioDitherMethod"""
    NONE = 0  # none
    RPDF = 1  # rpdf
    TPDF = 2  # tpdf
    TPDF_HF = 3  # tpdf-hf

class AudioNoiseShapingMethod(GstEnum):
    """GstAudioNoiseShapingMethod"""
    NONE = 0  # none
    ERROR_FEEDBACK = 1  # error-feedback
    SIMPLE = 2  # simple
    MEDIUM = 3  # medium
    HIGH = 4  # high

class AudioResamplerFilterInterpolation(GstEnum):
    """GstAudioResamplerFilterInterpolation"""
    NONE = 0  # none
    LINEAR = 1  # linear
    CUBIC = 2  # cubic

class AudioResamplerFilterMode(GstEnum):
    """GstAudioResamplerFilterMode"""
    INTERPOLATED = 0  # interpolated
    FULL = 1  # full
    AUTO = 2  # auto

class AudioResamplerMethod(GstEnum):
    """GstAudioResamplerMethod"""
    NEAREST = 0  # nearest
    LINEAR = 1  # linear
    CUBIC = 2  # cubic
    BLACKMAN_NUTTALL = 3  # blackman-nuttall
    KAISER = 4  # kaiser

class AudioTestSrcWave(GstEnum):
    """GstAudioTestSrcWave"""
    SINE = 0  # sine
    SQUARE = 1  # square
    SAW = 2  # saw
    TRIANGLE = 3  # triangle
    SILENCE = 4  # silence
    WHITE_NOISE = 5  # white-noise
    PINK_NOISE = 6  # pink-noise
    SINE_TABLE = 7  # sine-table
    TICKS = 8  # ticks
    GAUSSIAN_NOISE = 9  # gaussian-noise
    RED_NOISE = 10  # red-noise
    BLUE_NOISE = 11  # blue-noise
    VIOLET_NOISE = 12  # violet-noise

class BufferFlags(GstFlags):
    """GstBufferFlags"""
    LIVE = 16  # live
    DECODE_ONLY = 32  # decode-only
    DISCONT = 64  # discont
    RESYNC = 128  # resync
    CORRUPTED = 256  # corrupted
    MARKER = 512  # marker
    HEADER = 1024  # header
    GAP = 2048  # gap
    DROPPABLE = 4096  # droppable
    DELTA_UNIT = 8192  # delta-unit
    TAG_MEMORY = 16384  # tag-memory
    SYNC_AFTER = 32768  # sync-after
    NON_DROPPABLE = 65536  # non-droppable
    LAST = 1048576  # last

class CapsFilterCapsChangeMode(GstEnum):
    """GstCapsFilterCapsChangeMode"""
    IMMEDIATE = 0  # immediate
    DELAYED = 1  # delayed

class CaptureBufferDynamicAllocationModes(GstEnum):
    """CaptureBufferDynamicAllocationModes"""
    CAP_BUF_DYN_ALLOC_DISABLED = 0  # cap_buf_dyn_alloc_disabled
    FW_CAP_BUF_DYN_ALLOC_ENABLED = 1  # fw_cap_buf_dyn_alloc_enabled
    RW_CAP_BUF_DYN_ALLOC_ENABLED = 2  # rw_cap_buf_dyn_alloc_enabled
    FW_RW_CAP_BUF_DYN_ALLOC_ENABLED = 3  # fw_rw_cap_buf_dyn_alloc_enabled

class FakeSinkStateError(GstEnum):
    """GstFakeSinkStateError"""
    NONE = 0  # none
    NULL_TO_READY = 1  # null-to-ready
    READY_TO_PAUSED = 2  # ready-to-paused
    PAUSED_TO_PLAYING = 3  # paused-to-playing
    PLAYING_TO_PAUSED = 4  # playing-to-paused
    PAUSED_TO_READY = 5  # paused-to-ready
    READY_TO_NULL = 6  # ready-to-null

class FileSinkBufferMode(GstEnum):
    """GstFileSinkBufferMode"""
    DEFAULT = -1  # default
    FULL = 0  # full
    LINE = 1  # line
    UNBUFFERED = 2  # unbuffered

class Format(GstEnum):
    """GstFormat"""
    UNDEFINED = 0  # undefined
    DEFAULT = 1  # default
    BYTES = 2  # bytes
    TIME = 3  # time
    BUFFERS = 4  # buffers
    PERCENT = 5  # percent

class GLRotateMethod(GstEnum):
    """GstGLRotateMethod"""
    NONE = 0  # none
    CLOCKWISE = 1  # clockwise
    ROTATE_180 = 2  # rotate-180
    COUNTERCLOCKWISE = 3  # counterclockwise
    HORIZONTAL_FLIP = 4  # horizontal-flip
    VERTICAL_FLIP = 5  # vertical-flip
    UPPER_LEFT_DIAGONAL = 6  # upper-left-diagonal
    UPPER_RIGHT_DIAGONAL = 7  # upper-right-diagonal
    AUTOMATIC = 8  # automatic

class GLStereoDownmix(GstEnum):
    """GstGLStereoDownmix"""
    GREEN_MAGENTA_DUBOIS = 0  # green-magenta-dubois
    RED_CYAN_DUBOIS = 1  # red-cyan-dubois
    AMBER_BLUE_DUBOIS = 2  # amber-blue-dubois

class GTlsCertificateFlags(GstFlags):
    """GTlsCertificateFlags"""
    UNKNOWN_CA = 1  # unknown-ca
    BAD_IDENTITY = 2  # bad-identity
    NOT_ACTIVATED = 4  # not-activated
    EXPIRED = 8  # expired
    REVOKED = 16  # revoked
    INSECURE = 32  # insecure
    GENERIC_ERROR = 64  # generic-error

class IDCTMethod(GstEnum):
    """GstIDCTMethod"""
    ISLOW = 0  # islow
    IFAST = 1  # ifast
    FLOAT = 2  # float

class InterpolationMethod(GstEnum):
    """GstInterpolationMethod"""
    NEAREST = 0  # Nearest
    BILINEAR = 1  # Bilinear
    V5_TAP = 2  # 5-Tap
    V10_TAP = 3  # 10-Tap
    SMART = 4  # Smart
    NICEST = 5  # Nicest

class LibAVVidDecLowres(GstEnum):
    """GstLibAVVidDecLowres"""
    FULL = 0  # full
    V1_2_SIZE = 1  # 1/2-size
    V1_4_SIZE = 2  # 1/4-size

class LibAVVidDecSkipFrame(GstEnum):
    """GstLibAVVidDecSkipFrame"""
    SKIP_NOTHING = 0  # Skip nothing
    SKIP_B_FRAMES = 1  # Skip B-frames
    SKIP_IDCT_DEQUANTIZATION = 2  # Skip IDCT/Dequantization
    SKIP_EVERYTHING = 5  # Skip everything

class LibAVVidDecThreadType(GstFlags):
    """GstLibAVVidDecThreadType"""
    AUTO = 0  # 0

class NvArgusCamAeAntiBandingMode(GstEnum):
    """GstNvArgusCamAeAntiBandingMode"""
    AEANTIBANDINGMODE_OFF = 0  # AeAntibandingMode_Off
    AEANTIBANDINGMODE_AUTO = 1  # AeAntibandingMode_Auto
    AEANTIBANDINGMODE_50HZ = 2  # AeAntibandingMode_50HZ
    AEANTIBANDINGMODE_60HZ = 3  # AeAntibandingMode_60HZ

class NvArgusCamEEMode(GstEnum):
    """GstNvArgusCamEEMode"""
    EDGEENHANCEMENT_OFF = 0  # EdgeEnhancement_Off
    EDGEENHANCEMENT_FAST = 1  # EdgeEnhancement_Fast
    EDGEENHANCEMENT_HIGHQUALITY = 2  # EdgeEnhancement_HighQuality

class NvArgusCamTNRMode(GstEnum):
    """GstNvArgusCamTNRMode"""
    NOISEREDUCTION_OFF = 0  # NoiseReduction_Off
    NOISEREDUCTION_FAST = 1  # NoiseReduction_Fast
    NOISEREDUCTION_HIGHQUALITY = 2  # NoiseReduction_HighQuality

class NvArgusCamWBMode(GstEnum):
    """GstNvArgusCamWBMode"""
    OFF = 0  # off
    AUTO = 1  # auto
    INCANDESCENT = 2  # incandescent
    FLUORESCENT = 3  # fluorescent
    WARM_FLUORESCENT = 4  # warm-fluorescent
    DAYLIGHT = 5  # daylight
    CLOUDY_DAYLIGHT = 6  # cloudy-daylight
    TWILIGHT = 7  # twilight
    SHADE = 8  # shade
    MANUAL = 9  # manual

class NvIDCTMethod(GstEnum):
    """GstNvIDCTMethod"""
    ISLOW = 0  # islow
    IFAST = 1  # ifast
    FLOAT = 2  # float

class NvV4l2DecCaptureIOMode(GstEnum):
    """GstNvV4l2DecCaptureIOMode"""
    AUTO = 0  # auto
    MMAP = 2  # mmap

class NvV4l2DecOutputIOMode(GstEnum):
    """GstNvV4l2DecOutputIOMode"""
    AUTO = 0  # auto
    MMAP = 2  # mmap
    USERPTR = 3  # userptr

class NvV4l2EncCaptureIOMode(GstEnum):
    """GstNvV4l2EncCaptureIOMode"""
    AUTO = 0  # auto
    MMAP = 2  # mmap

class NvV4l2EncOutputIOMode(GstEnum):
    """GstNvV4l2EncOutputIOMode"""
    AUTO = 0  # auto
    MMAP = 2  # mmap
    DMABUF_IMPORT = 5  # dmabuf-import

class NvVidConvBufMemoryType(GstEnum):
    """GstNvVidConvBufMemoryType"""
    NVBUF_MEM_DEFAULT = 0  # nvbuf-mem-default
    NVBUF_MEM_CUDA_PINNED = 1  # nvbuf-mem-cuda-pinned
    NVBUF_MEM_CUDA_DEVICE = 2  # nvbuf-mem-cuda-device
    NVBUF_MEM_SURFACE_ARRAY = 4  # nvbuf-mem-surface-array

class NvVidConvComputeHWType(GstEnum):
    """GstNvVidConvComputeHWType"""
    DEFAULT = 0  # Default
    GPU = 1  # GPU
    VIC = 2  # VIC

class NvVideoFlipMethod(GstEnum):
    """GstNvVideoFlipMethod"""
    NONE = 0  # none
    COUNTERCLOCKWISE = 1  # counterclockwise
    ROTATE_180 = 2  # rotate-180
    CLOCKWISE = 3  # clockwise
    HORIZONTAL_FLIP = 4  # horizontal-flip
    UPPER_RIGHT_DIAGONAL = 5  # upper-right-diagonal
    VERTICAL_FLIP = 6  # vertical-flip
    UPPER_LEFT_DIAGONAL = 7  # upper-left-diagonal

class PlayFlags(GstFlags):
    """GstPlayFlags"""
    VIDEO = 1  # video
    AUDIO = 2  # audio
    TEXT = 4  # text
    VIS = 8  # vis
    SOFT_VOLUME = 16  # soft-volume
    NATIVE_AUDIO = 32  # native-audio
    NATIVE_VIDEO = 64  # native-video
    DOWNLOAD = 128  # download
    BUFFERING = 256  # buffering
    DEINTERLACE = 512  # deinterlace
    SOFT_COLORBALANCE = 1024  # soft-colorbalance
    FORCE_FILTERS = 2048  # force-filters
    FORCE_SW_DECODERS = 4096  # force-sw-decoders

class QTMuxDtsMethods(GstEnum):
    """GstQTMuxDtsMethods"""
    DD = 0  # dd
    REORDER = 1  # reorder
    ASC = 2  # asc

class QTMuxFragmentMode(GstEnum):
    """GstQTMuxFragmentMode"""
    DASH_OR_MSS = 0  # dash-or-mss
    FIRST_MOOV_THEN_FINALISE = 1  # first-moov-then-finalise

class QueueLeaky(GstEnum):
    """GstQueueLeaky"""
    NO = 0  # no
    UPSTREAM = 1  # upstream
    DOWNSTREAM = 2  # downstream

class RTPJitterBufferMode(GstEnum):
    """RTPJitterBufferMode"""
    NONE = 0  # none
    SLAVE = 1  # slave
    BUFFER = 2  # buffer
    SYNCED = 4  # synced

class RTSPBackchannel(GstEnum):
    """GstRTSPBackchannel"""
    NONE = 0  # none
    ONVIF = 1  # onvif

class RTSPLowerTrans(GstFlags):
    """GstRTSPLowerTrans"""
    UNKNOWN = 0  # 0

class RTSPNatMethod(GstEnum):
    """GstRTSPNatMethod"""
    NONE = 0  # none
    DUMMY = 1  # dummy

class RTSPSrcBufferMode(GstEnum):
    """GstRTSPSrcBufferMode"""
    NONE = 0  # none
    SLAVE = 1  # slave
    BUFFER = 2  # buffer
    AUTO = 3  # auto
    SYNCED = 4  # synced

class RTSPSrcNtpTimeSource(GstEnum):
    """GstRTSPSrcNtpTimeSource"""
    NTP = 0  # ntp
    UNIX = 1  # unix
    RUNNING_TIME = 2  # running-time
    CLOCK_TIME = 3  # clock-time

class RTSPVersion(GstEnum):
    """GstRTSPVersion"""
    INVALID = 0  # invalid
    V1_0 = 16  # 1-0
    V1_1 = 17  # 1-1
    V2_0 = 32  # 2-0

class RtpH264AggregateMode(GstEnum):
    """GstRtpH264AggregateMode"""
    NONE = 0  # none
    ZERO_LATENCY = 1  # zero-latency
    MAX_STAP = 2  # max-stap

class RtpH265AggregateMode(GstEnum):
    """GstRtpH265AggregateMode"""
    NONE = 0  # none
    ZERO_LATENCY = 1  # zero-latency
    MAX = 2  # max

class SkipFrame(GstEnum):
    """SkipFrame"""
    DECODE_ALL = 0  # decode_all
    DECODE_NON_REF = 1  # decode_non_ref
    DECODE_KEY = 2  # decode_key

class SocketTimestampMode(GstEnum):
    """GstSocketTimestampMode"""
    DISABLED = 0  # disabled
    REALTIME = 1  # realtime

class SoupLoggerLogLevel(GstEnum):
    """SoupLoggerLogLevel"""
    NONE = 0  # none
    MINIMAL = 1  # minimal
    HEADERS = 2  # headers
    BODY = 3  # body

class TeePullMode(GstEnum):
    """GstTeePullMode"""
    NEVER = 0  # never
    SINGLE = 1  # single

class V4L2VideoEncHwPreset(GstEnum):
    """GstV4L2VideoEncHwPreset"""
    DISABLEPRESET = 0  # DisablePreset
    ULTRAFASTPRESET = 1  # UltraFastPreset
    FASTPRESET = 2  # FastPreset
    MEDIUMPRESET = 3  # MediumPreset
    SLOWPRESET = 4  # SlowPreset

class V4L2VideoEncProfileType(GstEnum):
    """GstV4L2VideoEncProfileType"""
    MAIN = 0  # Main
    MAIN10 = 1  # Main10
    FREXT = 3  # FREXT

class V4L2_TV_norms(GstEnum):
    """V4L2_TV_norms"""
    NONE = 0  # none
    NTSC = 45056  # NTSC
    NTSC_M = 4096  # NTSC-M
    NTSC_M_JP = 8192  # NTSC-M-JP
    NTSC_M_KR = 32768  # NTSC-M-KR
    NTSC_443 = 16384  # NTSC-443
    PAL = 255  # PAL
    PAL_BG = 7  # PAL-BG
    PAL_B = 1  # PAL-B
    PAL_B1 = 2  # PAL-B1
    PAL_G = 4  # PAL-G
    PAL_H = 8  # PAL-H
    PAL_I = 16  # PAL-I
    PAL_DK = 224  # PAL-DK
    PAL_D = 32  # PAL-D
    PAL_D1 = 64  # PAL-D1
    PAL_K = 128  # PAL-K
    PAL_M = 256  # PAL-M
    PAL_N = 512  # PAL-N
    PAL_NC = 1024  # PAL-Nc
    PAL_60 = 2048  # PAL-60
    SECAM = 16711680  # SECAM
    SECAM_B = 65536  # SECAM-B
    SECAM_G = 262144  # SECAM-G
    SECAM_H = 524288  # SECAM-H
    SECAM_DK = 3276800  # SECAM-DK
    SECAM_D = 131072  # SECAM-D
    SECAM_K = 1048576  # SECAM-K
    SECAM_K1 = 2097152  # SECAM-K1
    SECAM_L = 4194304  # SECAM-L
    SECAM_LC = 8388608  # SECAM-Lc

class V4l2DeviceTypeFlags(GstFlags):
    """GstV4l2DeviceTypeFlags"""
    CAPTURE = 1  # capture
    OUTPUT = 2  # output
    OVERLAY = 4  # overlay
    VBI_CAPTURE = 16  # vbi-capture
    VBI_OUTPUT = 32  # vbi-output
    TUNER = 65536  # tuner
    AUDIO = 131072  # audio

class V4l2IOMode(GstEnum):
    """GstV4l2IOMode"""
    AUTO = 0  # auto
    RW = 1  # rw
    MMAP = 2  # mmap
    USERPTR = 3  # userptr
    DMABUF = 4  # dmabuf
    DMABUF_IMPORT = 5  # dmabuf-import

class V4l2VideoEncProfileType(GstEnum):
    """GstV4l2VideoEncProfileType"""
    BASELINE = 0  # Baseline
    CONSTRAINED_BASELINE = 1  # Constrained-Baseline
    MAIN = 2  # Main
    HIGH = 4  # High
    CONSTRAINED_HIGH = 17  # Constrained-High
    HIGH444 = 7  # High444

class V4l2VideoEncRateControlType(GstEnum):
    """GstV4l2VideoEncRateControlType"""
    VARIABLE_BITRATE = 0  # variable_bitrate
    CONSTANT_BITRATE = 1  # constant_bitrate

class VPXEncEndUsage(GstEnum):
    """GstVPXEncEndUsage"""
    VBR = 0  # vbr
    CBR = 1  # cbr
    CQ = 2  # cq

class VPXEncErFlags(GstFlags):
    """GstVPXEncErFlags"""
    DEFAULT = 1  # default
    PARTITIONS = 2  # partitions

class VPXEncKfMode(GstEnum):
    """GstVPXEncKfMode"""
    AUTO = 1  # auto
    DISABLED = 0  # disabled

class VPXEncMultipassMode(GstEnum):
    """GstVPXEncMultipassMode"""
    ONE_PASS = 0  # one-pass
    FIRST_PASS = 1  # first-pass
    LAST_PASS = 2  # last-pass

class VPXEncScalingMode(GstEnum):
    """GstVPXEncScalingMode"""
    NORMAL = 0  # normal
    V4_5 = 1  # 4:5
    V3_5 = 2  # 3:5
    V1_2 = 3  # 1:2

class VPXEncTokenPartitions(GstEnum):
    """GstVPXEncTokenPartitions"""
    V1 = 0  # 1
    V2 = 1  # 2
    V4 = 2  # 4
    V8 = 3  # 8

class VPXEncTuning(GstEnum):
    """GstVPXEncTuning"""
    PSNR = 0  # psnr
    SSIM = 1  # ssim

class ValveDropMode(GstEnum):
    """GstValveDropMode"""
    DROP_ALL = 0  # drop-all
    FORWARD_STICKY_EVENTS = 1  # forward-sticky-events
    TRANSFORM_TO_GAP = 2  # transform-to-gap

class VideoAlphaMode(GstEnum):
    """GstVideoAlphaMode"""
    COPY = 0  # copy
    SET = 1  # set
    MULT = 2  # mult

class VideoChromaMode(GstEnum):
    """GstVideoChromaMode"""
    FULL = 0  # full
    UPSAMPLE_ONLY = 1  # upsample-only
    DOWNSAMPLE_ONLY = 2  # downsample-only
    NONE = 3  # none

class VideoDecoderRequestSyncPointFlags(GstFlags):
    """GstVideoDecoderRequestSyncPointFlags"""
    DISCARD_INPUT = 1  # discard-input
    CORRUPT_OUTPUT = 2  # corrupt-output

class VideoDitherMethod(GstEnum):
    """GstVideoDitherMethod"""
    NONE = 0  # none
    VERTERR = 1  # verterr
    FLOYD_STEINBERG = 2  # floyd-steinberg
    SIERRA_LITE = 3  # sierra-lite
    BAYER = 4  # bayer

class VideoFlipMethod(GstEnum):
    """GstVideoFlipMethod"""
    NONE = 0  # none
    CLOCKWISE = 1  # clockwise
    ROTATE_180 = 2  # rotate-180
    COUNTERCLOCKWISE = 3  # counterclockwise
    HORIZONTAL_FLIP = 4  # horizontal-flip
    VERTICAL_FLIP = 5  # vertical-flip
    UPPER_LEFT_DIAGONAL = 6  # upper-left-diagonal
    UPPER_RIGHT_DIAGONAL = 7  # upper-right-diagonal
    AUTOMATIC = 8  # automatic

class VideoGammaMode(GstEnum):
    """GstVideoGammaMode"""
    NONE = 0  # none
    REMAP = 1  # remap

class VideoMatrixMode(GstEnum):
    """GstVideoMatrixMode"""
    FULL = 0  # full
    INPUT_ONLY = 1  # input-only
    OUTPUT_ONLY = 2  # output-only
    NONE = 3  # none

class VideoMultiviewFlags(GstFlags):
    """GstVideoMultiviewFlags"""
    NONE = 0  # 0

class VideoMultiviewFramePacking(GstEnum):
    """GstVideoMultiviewFramePacking"""
    NONE = -1  # none
    MONO = 0  # mono
    LEFT = 1  # left
    RIGHT = 2  # right
    SIDE_BY_SIDE = 3  # side-by-side
    SIDE_BY_SIDE_QUINCUNX = 4  # side-by-side-quincunx
    COLUMN_INTERLEAVED = 5  # column-interleaved
    ROW_INTERLEAVED = 6  # row-interleaved
    TOP_BOTTOM = 7  # top-bottom
    CHECKERBOARD = 8  # checkerboard

class VideoMultiviewMode(GstEnum):
    """GstVideoMultiviewMode"""
    NONE = -1  # none
    MONO = 0  # mono
    LEFT = 1  # left
    RIGHT = 2  # right
    SIDE_BY_SIDE = 3  # side-by-side
    SIDE_BY_SIDE_QUINCUNX = 4  # side-by-side-quincunx
    COLUMN_INTERLEAVED = 5  # column-interleaved
    ROW_INTERLEAVED = 6  # row-interleaved
    TOP_BOTTOM = 7  # top-bottom
    CHECKERBOARD = 8  # checkerboard
    FRAME_BY_FRAME = 32  # frame-by-frame
    MULTIVIEW_FRAME_BY_FRAME = 33  # multiview-frame-by-frame
    SEPARATED = 34  # separated

class VideoOrientationMethod(GstEnum):
    """GstVideoOrientationMethod"""
    IDENTITY = 0  # identity
    V90R = 1  # 90r
    V180 = 2  # 180
    V90L = 3  # 90l
    HORIZ = 4  # horiz
    VERT = 5  # vert
    UL_LR = 6  # ul-lr
    UR_LL = 7  # ur-ll
    AUTO = 8  # auto
    CUSTOM = 9  # custom

class VideoPrimariesMode(GstEnum):
    """GstVideoPrimariesMode"""
    NONE = 0  # none
    MERGE_ONLY = 1  # merge-only
    FAST = 2  # fast

class VideoResamplerMethod(GstEnum):
    """GstVideoResamplerMethod"""
    NEAREST = 0  # nearest
    LINEAR = 1  # linear
    CUBIC = 2  # cubic
    SINC = 3  # sinc
    LANCZOS = 4  # lanczos

class VideoScaleMethod(GstEnum):
    """GstVideoScaleMethod"""
    NEAREST_NEIGHBOUR = 0  # nearest-neighbour
    BILINEAR = 1  # bilinear
    V4_TAP = 2  # 4-tap
    LANCZOS = 3  # lanczos
    BILINEAR2 = 4  # bilinear2
    SINC = 5  # sinc
    HERMITE = 6  # hermite
    SPLINE = 7  # spline
    CATROM = 8  # catrom
    MITCHELL = 9  # mitchell

class VideoTestSrcAnimationMode(GstEnum):
    """GstVideoTestSrcAnimationMode"""
    FRAMES = 0  # frames
    WALL_TIME = 1  # wall-time
    RUNNING_TIME = 2  # running-time

class VideoTestSrcMotionType(GstEnum):
    """GstVideoTestSrcMotionType"""
    WAVY = 0  # wavy
    SWEEP = 1  # sweep
    HSWEEP = 2  # hsweep

class VideoTestSrcPattern(GstEnum):
    """GstVideoTestSrcPattern"""
    SMPTE = 0  # smpte
    SNOW = 1  # snow
    BLACK = 2  # black
    WHITE = 3  # white
    RED = 4  # red
    GREEN = 5  # green
    BLUE = 6  # blue
    CHECKERS_1 = 7  # checkers-1
    CHECKERS_2 = 8  # checkers-2
    CHECKERS_4 = 9  # checkers-4
    CHECKERS_8 = 10  # checkers-8
    CIRCULAR = 11  # circular
    BLINK = 12  # blink
    SMPTE75 = 13  # smpte75
    ZONE_PLATE = 14  # zone-plate
    GAMUT = 15  # gamut
    CHROMA_ZONE_PLATE = 16  # chroma-zone-plate
    SOLID_COLOR = 17  # solid-color
    BALL = 18  # ball
    SMPTE100 = 19  # smpte100
    BAR = 20  # bar
    PINWHEEL = 21  # pinwheel
    SPOKES = 22  # spokes
    GRADIENT = 23  # gradient
    COLORS = 24  # colors
    SMPTE_RP_219 = 25  # smpte-rp-219

class X264EncAnalyse(GstFlags):
    """GstX264EncAnalyse"""
    I4X4 = 1  # i4x4
    I8X8 = 2  # i8x8
    P8X8 = 16  # p8x8
    P4X4 = 32  # p4x4
    B8X8 = 256  # b8x8

class X264EncFramePacking(GstEnum):
    """GstX264EncFramePacking"""
    AUTO = -1  # auto
    CHECKERBOARD = 0  # checkerboard
    COLUMN_INTERLEAVED = 1  # column-interleaved
    ROW_INTERLEAVED = 2  # row-interleaved
    SIDE_BY_SIDE = 3  # side-by-side
    TOP_BOTTOM = 4  # top-bottom
    FRAME_INTERLEAVED = 5  # frame-interleaved

class X264EncMe(GstEnum):
    """GstX264EncMe"""
    DIA = 0  # dia
    HEX = 1  # hex
    UMH = 2  # umh
    ESA = 3  # esa
    TESA = 4  # tesa

class X264EncPass(GstEnum):
    """GstX264EncPass"""
    CBR = 0  # cbr
    QUANT = 4  # quant
    QUAL = 5  # qual
    PASS1 = 17  # pass1
    PASS2 = 18  # pass2
    PASS3 = 19  # pass3

class X264EncPreset(GstEnum):
    """GstX264EncPreset"""
    NONE = 0  # None
    ULTRAFAST = 1  # ultrafast
    SUPERFAST = 2  # superfast
    VERYFAST = 3  # veryfast
    FASTER = 4  # faster
    FAST = 5  # fast
    MEDIUM = 6  # medium
    SLOW = 7  # slow
    SLOWER = 8  # slower
    VERYSLOW = 9  # veryslow
    PLACEBO = 10  # placebo

class X264EncPsyTune(GstEnum):
    """GstX264EncPsyTune"""
    NONE = 0  # none
    FILM = 1  # film
    ANIMATION = 2  # animation
    GRAIN = 3  # grain
    PSNR = 4  # psnr
    SSIM = 5  # ssim

class X264EncTune(GstFlags):
    """GstX264EncTune"""
    STILLIMAGE = 1  # stillimage
    FASTDECODE = 2  # fastdecode
    ZEROLATENCY = 4  # zerolatency

class X265LogLevel(GstEnum):
    """GstX265LogLevel"""
    NONE = -1  # none
    ERROR = 0  # error
    WARNING = 1  # warning
    INFO = 2  # info
    DEBUG = 3  # debug
    FULL = 4  # full

class X265SpeedPreset(GstEnum):
    """GstX265SpeedPreset"""
    NO_PRESET = 0  # No preset
    ULTRAFAST = 1  # ultrafast
    SUPERFAST = 2  # superfast
    VERYFAST = 3  # veryfast
    FASTER = 4  # faster
    FAST = 5  # fast
    MEDIUM = 6  # medium
    SLOW = 7  # slow
    SLOWER = 8  # slower
    VERYSLOW = 9  # veryslow
    PLACEBO = 10  # placebo

class X265Tune(GstEnum):
    """GstX265Tune"""
    NO_TUNNING = 0  # No tunning
    PSNR = 1  # psnr
    SSIM = 2  # ssim
    GRAIN = 3  # grain
    ZEROLATENCY = 4  # zerolatency
    FASTDECODE = 5  # fastdecode
    ANIMATION = 6  # animation

class AppSink(Element):
    """appsink — AppSink

    klass: Generic/Sink
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "appsink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    caps: Prop[Caps, Caps | str]
    eos: bool  # 기본값: True
    emit_signals: bool  # 기본값: False
    max_buffers: int  # 기본값: 0
    drop: bool  # 기본값: False
    wait_on_eos: bool  # 기본값: True
    buffer_list: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        caps: Caps | str = ...,
        emit_signals: bool = ...,
        max_buffers: int = ...,
        drop: bool = ...,
        wait_on_eos: bool = ...,
        buffer_list: bool = ...,
    ) -> None: ...

class AppSrc(Element):
    """appsrc — AppSrc

    klass: Generic/Source
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "appsrc"
    LeakyType = AppLeakyType
    StreamType = AppStreamType
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    caps: Prop[Caps, Caps | str]
    size: int  # 기본값: -1
    stream_type: Prop[AppStreamType, AppStreamType | str | int]  # 기본값: stream
    max_bytes: int  # 기본값: 200000
    max_buffers: int  # 기본값: 0
    max_time: int  # 기본값: 0
    format: Prop[Format, Format | str | int]  # 기본값: bytes
    block: bool  # 기본값: False
    is_live: bool  # 기본값: False
    min_latency: int  # 기본값: -1
    max_latency: int  # 기본값: -1
    emit_signals: bool  # 기본값: True
    min_percent: int  # 기본값: 0
    current_level_bytes: int  # 기본값: 0
    current_level_buffers: int  # 기본값: 0
    current_level_time: int  # 기본값: 0
    duration: int  # 기본값: 18446744073709551615
    handle_segment_change: bool  # 기본값: False
    leaky_type: Prop[AppLeakyType, AppLeakyType | str | int]  # 기본값: none

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        caps: Caps | str = ...,
        size: int = ...,
        stream_type: AppStreamType | str | int = ...,
        max_bytes: int = ...,
        max_buffers: int = ...,
        max_time: int = ...,
        format: Format | str | int = ...,
        block: bool = ...,
        is_live: bool = ...,
        min_latency: int = ...,
        max_latency: int = ...,
        emit_signals: bool = ...,
        min_percent: int = ...,
        duration: int = ...,
        handle_segment_change: bool = ...,
        leaky_type: AppLeakyType | str | int = ...,
    ) -> None: ...

class AudioConvert(Element):
    """audioconvert — Audio converter

    klass: Filter/Converter/Audio
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "audioconvert"
    Dithering = AudioDitherMethod
    NoiseShaping = AudioNoiseShapingMethod
    qos: bool  # 기본값: False
    dithering: Prop[AudioDitherMethod, AudioDitherMethod | str | int]  # 기본값: tpdf
    noise_shaping: Prop[AudioNoiseShapingMethod, AudioNoiseShapingMethod | str | int]  # 기본값: none
    mix_matrix: Any

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        dithering: AudioDitherMethod | str | int = ...,
        noise_shaping: AudioNoiseShapingMethod | str | int = ...,
        mix_matrix: Any = ...,
    ) -> None: ...

class AudioResample(Element):
    """audioresample — Audio resampler

    klass: Filter/Converter/Audio
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "audioresample"
    rFilterInterpolation = AudioResamplerFilterInterpolation
    rFilterMode = AudioResamplerFilterMode
    rMethod = AudioResamplerMethod
    qos: bool  # 기본값: False
    quality: int  # 기본값: 4
    resample_method: Prop[AudioResamplerMethod, AudioResamplerMethod | str | int]  # 기본값: kaiser
    sinc_filter_mode: Prop[AudioResamplerFilterMode, AudioResamplerFilterMode | str | int]  # 기본값: auto
    sinc_filter_auto_threshold: int  # 기본값: 1048576
    sinc_filter_interpolation: Prop[AudioResamplerFilterInterpolation, AudioResamplerFilterInterpolation | str | int]  # 기본값: cubic

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        quality: int = ...,
        resample_method: AudioResamplerMethod | str | int = ...,
        sinc_filter_mode: AudioResamplerFilterMode | str | int = ...,
        sinc_filter_auto_threshold: int = ...,
        sinc_filter_interpolation: AudioResamplerFilterInterpolation | str | int = ...,
    ) -> None: ...

class AudioTestSrc(Element):
    """audiotestsrc — Audio test source

    klass: Source/Audio
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "audiotestsrc"
    Wave = AudioTestSrcWave
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    samplesperbuffer: int  # 기본값: 1024
    wave: Prop[AudioTestSrcWave, AudioTestSrcWave | str | int]  # 기본값: sine
    freq: float  # 기본값: 440.0
    volume: float  # 기본값: 0.8
    is_live: bool  # 기본값: False
    timestamp_offset: int  # 기본값: 0
    sine_periods_per_tick: int  # 기본값: 10
    tick_interval: int  # 기본값: 1000000000
    marker_tick_period: int  # 기본값: 0
    marker_tick_volume: float  # 기본값: 1.0
    apply_tick_ramp: bool  # 기본값: False
    can_activate_push: bool  # 기본값: True
    can_activate_pull: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        samplesperbuffer: int = ...,
        wave: AudioTestSrcWave | str | int = ...,
        freq: float = ...,
        volume: float = ...,
        is_live: bool = ...,
        timestamp_offset: int = ...,
        sine_periods_per_tick: int = ...,
        tick_interval: int = ...,
        marker_tick_period: int = ...,
        marker_tick_volume: float = ...,
        apply_tick_ramp: bool = ...,
        can_activate_push: bool = ...,
        can_activate_pull: bool = ...,
    ) -> None: ...

class AutoAudioSink(Element):
    """autoaudiosink — Auto audio sink

    klass: Sink/Audio
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "autoaudiosink"
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    filter_caps: Prop[Caps, Caps | str]
    sync: bool  # 기본값: True
    ts_offset: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        filter_caps: Caps | str = ...,
        sync: bool = ...,
        ts_offset: int = ...,
    ) -> None: ...

class AutoVideoSink(Element):
    """autovideosink — Auto video sink

    klass: Sink/Video
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "autovideosink"
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    filter_caps: Prop[Caps, Caps | str]
    sync: bool  # 기본값: True
    ts_offset: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        filter_caps: Caps | str = ...,
        sync: bool = ...,
        ts_offset: int = ...,
    ) -> None: ...

class AvDecH264(Element):
    """avdec_h264 — libav H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 decoder

    klass: Codec/Decoder/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "avdec_h264"
    AutomaticRequestSyncPointFlags = VideoDecoderRequestSyncPointFlags
    Lowres = LibAVVidDecLowres
    SkipFrame = LibAVVidDecSkipFrame
    ThreadType = LibAVVidDecThreadType
    qos: bool  # 기본값: True
    max_errors: int  # 기본값: 10
    min_force_key_unit_interval: int  # 기본값: 0
    discard_corrupted_frames: bool  # 기본값: False
    automatic_request_sync_points: bool  # 기본값: False
    automatic_request_sync_point_flags: Prop[VideoDecoderRequestSyncPointFlags, VideoDecoderRequestSyncPointFlags | str | int]  # 기본값: discard-input+corrupt-output
    lowres: Prop[LibAVVidDecLowres, LibAVVidDecLowres | str | int]  # 기본값: full
    skip_frame: Prop[LibAVVidDecSkipFrame, LibAVVidDecSkipFrame | str | int]  # 기본값: Skip nothing
    direct_rendering: bool  # 기본값: True
    debug_mv: bool  # 기본값: False
    max_threads: int  # 기본값: 0
    output_corrupt: bool  # 기본값: True
    thread_type: Prop[LibAVVidDecThreadType, LibAVVidDecThreadType | str | int]  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        max_errors: int = ...,
        min_force_key_unit_interval: int = ...,
        discard_corrupted_frames: bool = ...,
        automatic_request_sync_points: bool = ...,
        automatic_request_sync_point_flags: VideoDecoderRequestSyncPointFlags | str | int = ...,
        lowres: LibAVVidDecLowres | str | int = ...,
        skip_frame: LibAVVidDecSkipFrame | str | int = ...,
        direct_rendering: bool = ...,
        debug_mv: bool = ...,
        max_threads: int = ...,
        output_corrupt: bool = ...,
        thread_type: LibAVVidDecThreadType | str | int = ...,
    ) -> None: ...

class AvDecH265(Element):
    """avdec_h265 — libav HEVC (High Efficiency Video Coding) decoder

    klass: Codec/Decoder/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "avdec_h265"
    AutomaticRequestSyncPointFlags = VideoDecoderRequestSyncPointFlags
    Lowres = LibAVVidDecLowres
    SkipFrame = LibAVVidDecSkipFrame
    ThreadType = LibAVVidDecThreadType
    qos: bool  # 기본값: True
    max_errors: int  # 기본값: 10
    min_force_key_unit_interval: int  # 기본값: 0
    discard_corrupted_frames: bool  # 기본값: False
    automatic_request_sync_points: bool  # 기본값: False
    automatic_request_sync_point_flags: Prop[VideoDecoderRequestSyncPointFlags, VideoDecoderRequestSyncPointFlags | str | int]  # 기본값: discard-input+corrupt-output
    lowres: Prop[LibAVVidDecLowres, LibAVVidDecLowres | str | int]  # 기본값: full
    skip_frame: Prop[LibAVVidDecSkipFrame, LibAVVidDecSkipFrame | str | int]  # 기본값: Skip nothing
    direct_rendering: bool  # 기본값: True
    debug_mv: bool  # 기본값: False
    max_threads: int  # 기본값: 0
    output_corrupt: bool  # 기본값: True
    thread_type: Prop[LibAVVidDecThreadType, LibAVVidDecThreadType | str | int]  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        max_errors: int = ...,
        min_force_key_unit_interval: int = ...,
        discard_corrupted_frames: bool = ...,
        automatic_request_sync_points: bool = ...,
        automatic_request_sync_point_flags: VideoDecoderRequestSyncPointFlags | str | int = ...,
        lowres: LibAVVidDecLowres | str | int = ...,
        skip_frame: LibAVVidDecSkipFrame | str | int = ...,
        direct_rendering: bool = ...,
        debug_mv: bool = ...,
        max_threads: int = ...,
        output_corrupt: bool = ...,
        thread_type: LibAVVidDecThreadType | str | int = ...,
    ) -> None: ...

class CapsFilter(Element):
    """capsfilter — CapsFilter

    klass: Generic
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "capsfilter"
    CapsChangeMode = CapsFilterCapsChangeMode
    qos: bool  # 기본값: False
    caps: Prop[Caps, Caps | str]
    caps_change_mode: Prop[CapsFilterCapsChangeMode, CapsFilterCapsChangeMode | str | int]  # 기본값: immediate

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        caps: Caps | str = ...,
        caps_change_mode: CapsFilterCapsChangeMode | str | int = ...,
    ) -> None: ...

class DecodeBin(Element):
    """decodebin — Decoder Bin

    klass: Generic/Bin/Decoder
    pads: sink sink (always), src src_%u (sometimes)
    """
    FACTORY: ClassVar[str]  # "decodebin"
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    caps: Prop[Caps, Caps | str]
    subtitle_encoding: str | None
    sink_caps: Prop[Caps, Caps | str]
    use_buffering: bool  # 기본값: False
    force_sw_decoders: bool  # 기본값: False
    low_percent: int  # 기본값: 10
    high_percent: int  # 기본값: 99
    max_size_bytes: int  # 기본값: 0
    max_size_buffers: int  # 기본값: 0
    max_size_time: int  # 기본값: 0
    post_stream_topology: bool  # 기본값: False
    expose_all_streams: bool  # 기본값: True
    connection_speed: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        caps: Caps | str = ...,
        subtitle_encoding: str | None = ...,
        sink_caps: Caps | str = ...,
        use_buffering: bool = ...,
        force_sw_decoders: bool = ...,
        low_percent: int = ...,
        high_percent: int = ...,
        max_size_bytes: int = ...,
        max_size_buffers: int = ...,
        max_size_time: int = ...,
        post_stream_topology: bool = ...,
        expose_all_streams: bool = ...,
        connection_speed: int = ...,
    ) -> None: ...

class FakeSink(Element):
    """fakesink — Fake Sink

    klass: Sink
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "fakesink"
    StateError = FakeSinkStateError
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    state_error: Prop[FakeSinkStateError, FakeSinkStateError | str | int]  # 기본값: none
    silent: bool  # 기본값: True
    dump: bool  # 기본값: False
    signal_handoffs: bool  # 기본값: False
    drop_out_of_segment: bool  # 기본값: True
    last_message: str | None
    can_activate_push: bool  # 기본값: True
    can_activate_pull: bool  # 기본값: False
    num_buffers: int  # 기본값: -1

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        state_error: FakeSinkStateError | str | int = ...,
        silent: bool = ...,
        dump: bool = ...,
        signal_handoffs: bool = ...,
        drop_out_of_segment: bool = ...,
        can_activate_push: bool = ...,
        can_activate_pull: bool = ...,
        num_buffers: int = ...,
    ) -> None: ...

class FileSink(Element):
    """filesink — File Sink

    klass: Sink/File
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "filesink"
    BufferMode = FileSinkBufferMode
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    location: str | None
    buffer_mode: Prop[FileSinkBufferMode, FileSinkBufferMode | str | int]  # 기본값: default
    buffer_size: int  # 기본값: 65536
    append: bool  # 기본값: False
    o_sync: bool  # 기본값: False
    max_transient_error_timeout: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        location: str | None = ...,
        buffer_mode: FileSinkBufferMode | str | int = ...,
        buffer_size: int = ...,
        append: bool = ...,
        o_sync: bool = ...,
        max_transient_error_timeout: int = ...,
    ) -> None: ...

class FileSrc(Element):
    """filesrc — File Source

    klass: Source/File
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "filesrc"
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    location: str | None

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        location: str | None = ...,
    ) -> None: ...

class FlvMux(Element):
    """flvmux — FLV muxer

    klass: Codec/Muxer
    pads: sink video (request), sink audio (request), src src (always)
    """
    FACTORY: ClassVar[str]  # "flvmux"
    StartTimeSelection = AggregatorStartTimeSelection
    latency: int  # 기본값: 0
    min_upstream_latency: int  # 기본값: 0
    start_time_selection: Prop[AggregatorStartTimeSelection, AggregatorStartTimeSelection | str | int]  # 기본값: zero
    start_time: int  # 기본값: 18446744073709551615
    emit_signals: bool  # 기본값: False
    streamable: bool  # 기본값: False
    metadatacreator: str | None
    encoder: str | None
    skip_backwards_streams: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        latency: int = ...,
        min_upstream_latency: int = ...,
        start_time_selection: AggregatorStartTimeSelection | str | int = ...,
        start_time: int = ...,
        emit_signals: bool = ...,
        streamable: bool = ...,
        metadatacreator: str | None = ...,
        encoder: str | None = ...,
        skip_backwards_streams: bool = ...,
    ) -> None: ...

class GlImageSink(Element):
    """glimagesink — GL Sink Bin

    klass: Sink/Video
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "glimagesink"
    OutputMultiviewDownmixMode = GLStereoDownmix
    OutputMultiviewFlags = VideoMultiviewFlags
    OutputMultiviewMode = VideoMultiviewMode
    RotateMethod = GLRotateMethod
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    sink: Any
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    contrast: float  # 기본값: 1.0
    brightness: float  # 기본값: 0.0
    hue: float  # 기본값: 0.0
    saturation: float  # 기본값: 1.0
    rotate_method: Prop[GLRotateMethod, GLRotateMethod | str | int]  # 기본값: none
    force_aspect_ratio: bool  # 기본값: True
    pixel_aspect_ratio: Fraction | tuple[int, int]
    handle_events: bool  # 기본값: True
    context: Any
    ignore_alpha: bool  # 기본값: True
    show_preroll_frame: bool  # 기본값: True
    output_multiview_mode: Prop[VideoMultiviewMode, VideoMultiviewMode | str | int]  # 기본값: mono
    output_multiview_flags: Prop[VideoMultiviewFlags, VideoMultiviewFlags | str | int]  # 기본값: 0
    output_multiview_downmix_mode: Prop[GLStereoDownmix, GLStereoDownmix | str | int]  # 기본값: green-magenta-dubois
    render_rectangle: Any

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        sink: Any = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        contrast: float = ...,
        brightness: float = ...,
        hue: float = ...,
        saturation: float = ...,
        rotate_method: GLRotateMethod | str | int = ...,
        force_aspect_ratio: bool = ...,
        pixel_aspect_ratio: Fraction | tuple[int, int] = ...,
        handle_events: bool = ...,
        ignore_alpha: bool = ...,
        show_preroll_frame: bool = ...,
        output_multiview_mode: VideoMultiviewMode | str | int = ...,
        output_multiview_flags: VideoMultiviewFlags | str | int = ...,
        output_multiview_downmix_mode: GLStereoDownmix | str | int = ...,
        render_rectangle: Any = ...,
    ) -> None: ...

class H264Parse(Element):
    """h264parse — H.264 parser

    klass: Codec/Parser/Converter/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "h264parse"
    disable_passthrough: bool  # 기본값: False
    config_interval: int  # 기본값: 0
    update_timecode: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        disable_passthrough: bool = ...,
        config_interval: int = ...,
        update_timecode: bool = ...,
    ) -> None: ...

class H265Parse(Element):
    """h265parse — H.265 parser

    klass: Codec/Parser/Converter/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "h265parse"
    disable_passthrough: bool  # 기본값: False
    config_interval: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        disable_passthrough: bool = ...,
        config_interval: int = ...,
    ) -> None: ...

class Identity(Element):
    """identity — Identity

    klass: Generic
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "identity"
    DropBufferFlags = BufferFlags
    qos: bool  # 기본값: False
    sleep_time: int  # 기본값: 0
    error_after: int  # 기본값: -1
    drop_probability: float  # 기본값: 0.0
    drop_buffer_flags: Prop[BufferFlags, BufferFlags | str | int]  # 기본값: 0
    datarate: int  # 기본값: 0
    silent: bool  # 기본값: True
    single_segment: bool  # 기본값: False
    last_message: str | None
    dump: bool  # 기본값: False
    sync: bool  # 기본값: False
    ts_offset: int  # 기본값: 0
    check_imperfect_timestamp: bool  # 기본값: False
    check_imperfect_offset: bool  # 기본값: False
    signal_handoffs: bool  # 기본값: True
    drop_allocation: bool  # 기본값: False
    eos_after: int  # 기본값: -1
    stats: dict[str, Any] | str

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        sleep_time: int = ...,
        error_after: int = ...,
        drop_probability: float = ...,
        drop_buffer_flags: BufferFlags | str | int = ...,
        datarate: int = ...,
        silent: bool = ...,
        single_segment: bool = ...,
        dump: bool = ...,
        sync: bool = ...,
        ts_offset: int = ...,
        check_imperfect_timestamp: bool = ...,
        check_imperfect_offset: bool = ...,
        signal_handoffs: bool = ...,
        drop_allocation: bool = ...,
        eos_after: int = ...,
    ) -> None: ...

class JpegDec(Element):
    """jpegdec — JPEG image decoder

    klass: Codec/Decoder/Image
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "jpegdec"
    AutomaticRequestSyncPointFlags = VideoDecoderRequestSyncPointFlags
    IdctMethod = IDCTMethod
    qos: bool  # 기본값: True
    min_force_key_unit_interval: int  # 기본값: 0
    discard_corrupted_frames: bool  # 기본값: False
    automatic_request_sync_points: bool  # 기본값: False
    automatic_request_sync_point_flags: Prop[VideoDecoderRequestSyncPointFlags, VideoDecoderRequestSyncPointFlags | str | int]  # 기본값: discard-input+corrupt-output
    idct_method: Prop[IDCTMethod, IDCTMethod | str | int]  # 기본값: ifast
    max_errors: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        discard_corrupted_frames: bool = ...,
        automatic_request_sync_points: bool = ...,
        automatic_request_sync_point_flags: VideoDecoderRequestSyncPointFlags | str | int = ...,
        idct_method: IDCTMethod | str | int = ...,
        max_errors: int = ...,
    ) -> None: ...

class JpegEnc(Element):
    """jpegenc — JPEG image encoder

    klass: Codec/Encoder/Image
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "jpegenc"
    IdctMethod = IDCTMethod
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    quality: int  # 기본값: 85
    idct_method: Prop[IDCTMethod, IDCTMethod | str | int]  # 기본값: ifast
    snapshot: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        quality: int = ...,
        idct_method: IDCTMethod | str | int = ...,
        snapshot: bool = ...,
    ) -> None: ...

class MatroskaMux(Element):
    """matroskamux — Matroska muxer

    klass: Codec/Muxer
    pads: sink video_%u (request), sink audio_%u (request), sink subtitle_%u (request), src src (always)
    """
    FACTORY: ClassVar[str]  # "matroskamux"
    writing_app: str | None
    version: int  # 기본값: 2
    min_index_interval: int  # 기본값: 0
    streamable: bool  # 기본값: False
    timecodescale: int  # 기본값: 1000000
    min_cluster_duration: int  # 기본값: 500000000
    max_cluster_duration: int  # 기본값: 65535000000
    offset_to_zero: bool  # 기본값: False
    creation_time: Any
    cluster_timestamp_offset: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        writing_app: str | None = ...,
        version: int = ...,
        min_index_interval: int = ...,
        streamable: bool = ...,
        timecodescale: int = ...,
        min_cluster_duration: int = ...,
        max_cluster_duration: int = ...,
        offset_to_zero: bool = ...,
        creation_time: Any = ...,
        cluster_timestamp_offset: int = ...,
    ) -> None: ...

class Mp4Mux(Element):
    """mp4mux — MP4 Muxer

    klass: Codec/Muxer
    pads: src src (always), sink audio_%u (request), sink video_%u (request), sink subtitle_%u (request)
    """
    FACTORY: ClassVar[str]  # "mp4mux"
    DtsMethod = QTMuxDtsMethods
    FragmentMode = QTMuxFragmentMode
    StartTimeSelection = AggregatorStartTimeSelection
    latency: int  # 기본값: 0
    min_upstream_latency: int  # 기본값: 0
    start_time_selection: Prop[AggregatorStartTimeSelection, AggregatorStartTimeSelection | str | int]  # 기본값: zero
    start_time: int  # 기본값: 18446744073709551615
    emit_signals: bool  # 기본값: False
    movie_timescale: int  # 기본값: 0
    trak_timescale: int  # 기본값: 0
    faststart: bool  # 기본값: False
    faststart_file: str | None
    moov_recovery_file: str | None
    fragment_duration: int  # 기본값: 0
    reserved_max_duration: int  # 기본값: 18446744073709551615
    reserved_duration_remaining: int  # 기본값: 0
    reserved_moov_update_period: int  # 기본값: 18446744073709551615
    reserved_bytes_per_sec: int  # 기본값: 550
    reserved_prefill: bool  # 기본값: False
    dts_method: Prop[QTMuxDtsMethods, QTMuxDtsMethods | str | int]  # 기본값: reorder
    presentation_time: bool  # 기본값: True
    interleave_bytes: int  # 기본값: 0
    interleave_time: int  # 기본값: 250000000
    force_chunks: bool  # 기본값: False
    max_raw_audio_drift: int  # 기본값: 40000000
    start_gap_threshold: int  # 기본값: 0
    force_create_timecode_trak: bool  # 기본값: False
    fragment_mode: Prop[QTMuxFragmentMode, QTMuxFragmentMode | str | int]  # 기본값: dash-or-mss
    streamable: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        latency: int = ...,
        min_upstream_latency: int = ...,
        start_time_selection: AggregatorStartTimeSelection | str | int = ...,
        start_time: int = ...,
        emit_signals: bool = ...,
        movie_timescale: int = ...,
        trak_timescale: int = ...,
        faststart: bool = ...,
        faststart_file: str | None = ...,
        moov_recovery_file: str | None = ...,
        fragment_duration: int = ...,
        reserved_max_duration: int = ...,
        reserved_moov_update_period: int = ...,
        reserved_bytes_per_sec: int = ...,
        reserved_prefill: bool = ...,
        dts_method: QTMuxDtsMethods | str | int = ...,
        presentation_time: bool = ...,
        interleave_bytes: int = ...,
        interleave_time: int = ...,
        force_chunks: bool = ...,
        max_raw_audio_drift: int = ...,
        start_gap_threshold: int = ...,
        force_create_timecode_trak: bool = ...,
        fragment_mode: QTMuxFragmentMode | str | int = ...,
        streamable: bool = ...,
    ) -> None: ...

class MpegTsMux(Element):
    """mpegtsmux — MPEG Transport Stream Muxer

    klass: Codec/Muxer
    pads: sink sink_%d (request), src src (always)
    """
    FACTORY: ClassVar[str]  # "mpegtsmux"
    StartTimeSelection = AggregatorStartTimeSelection
    latency: int  # 기본값: 0
    min_upstream_latency: int  # 기본값: 0
    start_time_selection: Prop[AggregatorStartTimeSelection, AggregatorStartTimeSelection | str | int]  # 기본값: zero
    start_time: int  # 기본값: 18446744073709551615
    emit_signals: bool  # 기본값: False
    prog_map: dict[str, Any] | str
    pat_interval: int  # 기본값: 9000
    pmt_interval: int  # 기본값: 9000
    alignment: int  # 기본값: -1
    si_interval: int  # 기본값: 9000
    bitrate: int  # 기본값: 0
    pcr_interval: int  # 기본값: 3600
    scte_35_pid: int  # 기본값: 0
    scte_35_null_interval: int  # 기본값: 27000000
    m2ts_mode: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        latency: int = ...,
        min_upstream_latency: int = ...,
        start_time_selection: AggregatorStartTimeSelection | str | int = ...,
        start_time: int = ...,
        emit_signals: bool = ...,
        prog_map: dict[str, Any] | str = ...,
        pat_interval: int = ...,
        pmt_interval: int = ...,
        alignment: int = ...,
        si_interval: int = ...,
        bitrate: int = ...,
        pcr_interval: int = ...,
        scte_35_pid: int = ...,
        scte_35_null_interval: int = ...,
        m2ts_mode: bool = ...,
    ) -> None: ...

class Nv3dSink(Element):
    """nv3dsink — Nvidia 3D sink

    klass: Sink/Video
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nv3dsink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    show_preroll_frame: bool  # 기본값: True
    window_x: int  # 기본값: 10
    window_y: int  # 기본값: 10
    window_width: int  # 기본값: 0
    window_height: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        show_preroll_frame: bool = ...,
        window_x: int = ...,
        window_y: int = ...,
        window_width: int = ...,
        window_height: int = ...,
    ) -> None: ...

class NvArgusCameraSrc(Element):
    """nvarguscamerasrc — NvArgusCameraSrc

    klass: Video/Capture
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "nvarguscamerasrc"
    Aeantibanding = NvArgusCamAeAntiBandingMode
    EeMode = NvArgusCamEEMode
    TnrMode = NvArgusCamTNRMode
    Wbmode = NvArgusCamWBMode
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    silent: bool  # 기본값: False
    show_latency: bool  # 기본값: False
    timeout: int  # 기본값: 0
    wbmode: Prop[NvArgusCamWBMode, NvArgusCamWBMode | str | int]  # 기본값: auto
    saturation: float  # 기본값: 1.0
    sensor_id: int  # 기본값: 0
    sensor_mode: int  # 기본값: -1
    total_sensor_modes: int  # 기본값: 0
    exposuretimerange: str | None  # 기본값: '34000 358733000'
    gainrange: str | None  # 기본값: '1 16'
    ispdigitalgainrange: str | None  # 기본값: '1 256'
    tnr_strength: float  # 기본값: -1.0
    tnr_mode: Prop[NvArgusCamTNRMode, NvArgusCamTNRMode | str | int]  # 기본값: NoiseReduction_Fast
    ee_mode: Prop[NvArgusCamEEMode, NvArgusCamEEMode | str | int]  # 기본값: EdgeEnhancement_Fast
    ee_strength: float  # 기본값: -1.0
    aeantibanding: Prop[NvArgusCamAeAntiBandingMode, NvArgusCamAeAntiBandingMode | str | int]  # 기본값: AeAntibandingMode_Auto
    exposurecompensation: float  # 기본값: 0.0
    aelock: bool  # 기본값: False
    aeregion: str | None
    awblock: bool  # 기본값: False
    event_wait: int  # 기본값: 3000000000
    acquire_wait: int  # 기본값: 5000000000

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        silent: bool = ...,
        show_latency: bool = ...,
        timeout: int = ...,
        wbmode: NvArgusCamWBMode | str | int = ...,
        saturation: float = ...,
        sensor_id: int = ...,
        sensor_mode: int = ...,
        exposuretimerange: str | None = ...,
        gainrange: str | None = ...,
        ispdigitalgainrange: str | None = ...,
        tnr_strength: float = ...,
        tnr_mode: NvArgusCamTNRMode | str | int = ...,
        ee_mode: NvArgusCamEEMode | str | int = ...,
        ee_strength: float = ...,
        aeantibanding: NvArgusCamAeAntiBandingMode | str | int = ...,
        exposurecompensation: float = ...,
        aelock: bool = ...,
        aeregion: str | None = ...,
        awblock: bool = ...,
        event_wait: int = ...,
        acquire_wait: int = ...,
    ) -> None: ...

class NvDrmVideoSink(Element):
    """nvdrmvideosink — Nvidia Drm Video Sink

    klass: Video Sink
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvdrmvideosink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    show_preroll_frame: bool  # 기본값: True
    conn_id: int  # 기본값: 2147483647
    plane_id: int  # 기본값: 2147483647
    set_mode: bool  # 기본값: False
    offset_x: int  # 기본값: 2147483647
    offset_y: int  # 기본값: 2147483647
    color_range: int  # 기본값: 2

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        show_preroll_frame: bool = ...,
        conn_id: int = ...,
        plane_id: int = ...,
        set_mode: bool = ...,
        offset_x: int = ...,
        offset_y: int = ...,
        color_range: int = ...,
    ) -> None: ...

class NvEglGlesSink(Element):
    """nveglglessink — EGL/GLES vout Sink

    klass: Sink/Video
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nveglglessink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    show_preroll_frame: bool  # 기본값: True
    create_window: bool  # 기본값: True
    force_aspect_ratio: bool  # 기본값: True
    display: Any
    window_x: int  # 기본값: 10
    window_y: int  # 기본값: 10
    window_width: int  # 기본값: 0
    window_height: int  # 기본값: 0
    rows: int  # 기본값: 1
    columns: int  # 기본값: 1
    profile: int  # 기본값: 0
    winsys: str | None  # 기본값: 'x11'
    show_latency: bool  # 기본값: True
    bufapi_version: bool  # 기본값: False
    ivisurf_id: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        show_preroll_frame: bool = ...,
        create_window: bool = ...,
        force_aspect_ratio: bool = ...,
        display: Any = ...,
        window_x: int = ...,
        window_y: int = ...,
        window_width: int = ...,
        window_height: int = ...,
        rows: int = ...,
        columns: int = ...,
        profile: int = ...,
        winsys: str | None = ...,
        show_latency: bool = ...,
        bufapi_version: bool = ...,
        ivisurf_id: int = ...,
    ) -> None: ...

class NvJpegDec(Element):
    """nvjpegdec — JPEG image decoder

    klass: Codec/Decoder/Image
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "nvjpegdec"
    AutomaticRequestSyncPointFlags = VideoDecoderRequestSyncPointFlags
    IdctMethod = NvIDCTMethod
    qos: bool  # 기본값: True
    min_force_key_unit_interval: int  # 기본값: 0
    discard_corrupted_frames: bool  # 기본값: False
    automatic_request_sync_points: bool  # 기본값: False
    automatic_request_sync_point_flags: Prop[VideoDecoderRequestSyncPointFlags, VideoDecoderRequestSyncPointFlags | str | int]  # 기본값: discard-input+corrupt-output
    idct_method: Prop[NvIDCTMethod, NvIDCTMethod | str | int]  # 기본값: ifast
    max_errors: int  # 기본값: 0
    Enableperf: bool  # 기본값: False
    rgbaoutput: bool  # 기본값: False
    nv12output: bool  # 기본값: False
    mjpegdecode: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        discard_corrupted_frames: bool = ...,
        automatic_request_sync_points: bool = ...,
        automatic_request_sync_point_flags: VideoDecoderRequestSyncPointFlags | str | int = ...,
        idct_method: NvIDCTMethod | str | int = ...,
        max_errors: int = ...,
        Enableperf: bool = ...,
        rgbaoutput: bool = ...,
        nv12output: bool = ...,
        mjpegdecode: bool = ...,
    ) -> None: ...

class NvJpegEnc(Element):
    """nvjpegenc — JPEG image encoder

    klass: Codec/Encoder/Image
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvjpegenc"
    IdctMethod = NvIDCTMethod
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    quality: int  # 기본값: 85
    idct_method: Prop[NvIDCTMethod, NvIDCTMethod | str | int]  # 기본값: ifast
    Enableperf: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        quality: int = ...,
        idct_method: NvIDCTMethod | str | int = ...,
        Enableperf: bool = ...,
    ) -> None: ...

class NvV4l2Av1Enc(Element):
    """nvv4l2av1enc — V4L2 AV1 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2av1enc"
    CaptureIoMode = NvV4l2EncCaptureIOMode
    ControlRate = V4l2VideoEncRateControlType
    OutputIoMode = NvV4l2EncOutputIOMode
    PresetLevel = V4L2VideoEncHwPreset
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    device: str | None
    device_name: str | None
    device_fd: int  # 기본값: -1
    output_io_mode: Prop[NvV4l2EncOutputIOMode, NvV4l2EncOutputIOMode | str | int]  # 기본값: auto
    capture_io_mode: Prop[NvV4l2EncCaptureIOMode, NvV4l2EncCaptureIOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    bitrate: int  # 기본값: 4000000
    control_rate: Prop[V4l2VideoEncRateControlType, V4l2VideoEncRateControlType | str | int]  # 기본값: constant_bitrate
    iframeinterval: int  # 기본값: 30
    peak_bitrate: int  # 기본값: 0
    quant_i_frames: int  # 기본값: 4294967295
    quant_p_frames: int  # 기본값: 4294967295
    quant_b_frames: int  # 기본값: 4294967295
    preset_level: Prop[V4L2VideoEncHwPreset, V4L2VideoEncHwPreset | str | int]  # 기본값: UltraFastPreset
    qp_range: str | None  # 기본값: '-1,-1:-1,-1:-1,-1'
    vbv_size: int  # 기본값: 4000000
    MeasureEncoderLatency: bool  # 기본값: False
    ratecontrol_enable: bool  # 기본값: True
    maxperf_enable: bool  # 기본값: False
    idrinterval: int  # 기본값: 256
    copy_timestamp: bool  # 기본값: False
    enable_headers: bool  # 기본값: False
    tiles: str | None  # 기본값: '0,0'
    disable_cdf: bool  # 기본값: True
    enable_srdo: bool  # 기본값: False
    num_Ref_Frames: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        output_io_mode: NvV4l2EncOutputIOMode | str | int = ...,
        capture_io_mode: NvV4l2EncCaptureIOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        bitrate: int = ...,
        control_rate: V4l2VideoEncRateControlType | str | int = ...,
        iframeinterval: int = ...,
        peak_bitrate: int = ...,
        quant_i_frames: int = ...,
        quant_p_frames: int = ...,
        quant_b_frames: int = ...,
        preset_level: V4L2VideoEncHwPreset | str | int = ...,
        qp_range: str | None = ...,
        vbv_size: int = ...,
        MeasureEncoderLatency: bool = ...,
        ratecontrol_enable: bool = ...,
        maxperf_enable: bool = ...,
        idrinterval: int = ...,
        copy_timestamp: bool = ...,
        enable_headers: bool = ...,
        tiles: str | None = ...,
        disable_cdf: bool = ...,
        enable_srdo: bool = ...,
        num_Ref_Frames: int = ...,
    ) -> None: ...

class NvV4l2CameraSrc(Element):
    """nvv4l2camerasrc — NvV4l2CameraSrc

    klass: Video/Capture
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2camerasrc"
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    device: str | None  # 기본값: '/dev/video0'
    cap_buffers: int  # 기본값: 6

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        device: str | None = ...,
        cap_buffers: int = ...,
    ) -> None: ...

class NvV4l2Decoder(Element):
    """nvv4l2decoder — NVIDIA v4l2 video decoder

    klass: Codec/Decoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2decoder"
    AutomaticRequestSyncPointFlags = VideoDecoderRequestSyncPointFlags
    CaptureBufferDynamicAllocation = CaptureBufferDynamicAllocationModes
    CaptureIoMode = NvV4l2DecCaptureIOMode
    OutputIoMode = NvV4l2DecOutputIOMode
    SkipFrames = SkipFrame
    qos: bool  # 기본값: True
    max_errors: int  # 기본값: 10
    min_force_key_unit_interval: int  # 기본값: 0
    discard_corrupted_frames: bool  # 기본값: False
    automatic_request_sync_points: bool  # 기본값: False
    automatic_request_sync_point_flags: Prop[VideoDecoderRequestSyncPointFlags, VideoDecoderRequestSyncPointFlags | str | int]  # 기본값: discard-input+corrupt-output
    device: str | None
    device_name: str | None
    device_fd: int  # 기본값: -1
    output_io_mode: Prop[NvV4l2DecOutputIOMode, NvV4l2DecOutputIOMode | str | int]  # 기본값: auto
    capture_io_mode: Prop[NvV4l2DecCaptureIOMode, NvV4l2DecCaptureIOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    skip_frames: Prop[SkipFrame, SkipFrame | str | int]  # 기본값: decode_all
    drop_frame_interval: int  # 기본값: 30
    num_extra_surfaces: int  # 기본값: 55
    disable_dpb: bool  # 기본값: False
    enable_full_frame: bool  # 기본값: False
    enable_frame_type_reporting: bool  # 기본값: False
    enable_error_check: bool  # 기본값: False
    enable_max_performance: bool  # 기본값: False
    mjpeg: bool  # 기본값: False
    is_gdr_stream: bool  # 기본값: False
    capture_buffer_dynamic_allocation: Prop[CaptureBufferDynamicAllocationModes, CaptureBufferDynamicAllocationModes | str | int]  # 기본값: cap_buf_dyn_alloc_disabled

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        max_errors: int = ...,
        min_force_key_unit_interval: int = ...,
        discard_corrupted_frames: bool = ...,
        automatic_request_sync_points: bool = ...,
        automatic_request_sync_point_flags: VideoDecoderRequestSyncPointFlags | str | int = ...,
        output_io_mode: NvV4l2DecOutputIOMode | str | int = ...,
        capture_io_mode: NvV4l2DecCaptureIOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        skip_frames: SkipFrame | str | int = ...,
        drop_frame_interval: int = ...,
        num_extra_surfaces: int = ...,
        disable_dpb: bool = ...,
        enable_full_frame: bool = ...,
        enable_frame_type_reporting: bool = ...,
        enable_error_check: bool = ...,
        enable_max_performance: bool = ...,
        mjpeg: bool = ...,
        is_gdr_stream: bool = ...,
        capture_buffer_dynamic_allocation: CaptureBufferDynamicAllocationModes | str | int = ...,
    ) -> None: ...

class NvV4l2H264Enc(Element):
    """nvv4l2h264enc — V4L2 H.264 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2h264enc"
    CaptureIoMode = NvV4l2EncCaptureIOMode
    ControlRate = V4l2VideoEncRateControlType
    OutputIoMode = NvV4l2EncOutputIOMode
    PresetLevel = V4L2VideoEncHwPreset
    Profile = V4l2VideoEncProfileType
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    device: str | None
    device_name: str | None
    device_fd: int  # 기본값: -1
    output_io_mode: Prop[NvV4l2EncOutputIOMode, NvV4l2EncOutputIOMode | str | int]  # 기본값: auto
    capture_io_mode: Prop[NvV4l2EncCaptureIOMode, NvV4l2EncCaptureIOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    bitrate: int  # 기본값: 4000000
    control_rate: Prop[V4l2VideoEncRateControlType, V4l2VideoEncRateControlType | str | int]  # 기본값: constant_bitrate
    iframeinterval: int  # 기본값: 30
    peak_bitrate: int  # 기본값: 0
    quant_i_frames: int  # 기본값: 4294967295
    quant_p_frames: int  # 기본값: 4294967295
    quant_b_frames: int  # 기본값: 4294967295
    preset_level: Prop[V4L2VideoEncHwPreset, V4L2VideoEncHwPreset | str | int]  # 기본값: UltraFastPreset
    qp_range: str | None  # 기본값: '-1,-1:-1,-1:-1,-1'
    vbv_size: int  # 기본값: 4000000
    MeasureEncoderLatency: bool  # 기본값: False
    ratecontrol_enable: bool  # 기본값: True
    maxperf_enable: bool  # 기본값: False
    idrinterval: int  # 기본값: 256
    copy_timestamp: bool  # 기본값: False
    profile: Prop[V4l2VideoEncProfileType, V4l2VideoEncProfileType | str | int]  # 기본값: Baseline
    insert_vui: bool  # 기본값: False
    insert_sps_pps: bool  # 기본값: False
    insert_aud: bool  # 기본값: False
    num_B_Frames: int  # 기본값: 0
    disable_cabac: bool  # 기본값: False
    bit_packetization: bool  # 기본값: False
    SliceIntraRefreshInterval: int  # 기본값: 60
    EnableTwopassCBR: bool  # 기본값: False
    EnableMVBufferMeta: bool  # 기본값: False
    slice_header_spacing: int  # 기본값: 0
    num_Ref_Frames: int  # 기본값: 1
    poc_type: int  # 기본값: 0
    enable_lossless: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        output_io_mode: NvV4l2EncOutputIOMode | str | int = ...,
        capture_io_mode: NvV4l2EncCaptureIOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        bitrate: int = ...,
        control_rate: V4l2VideoEncRateControlType | str | int = ...,
        iframeinterval: int = ...,
        peak_bitrate: int = ...,
        quant_i_frames: int = ...,
        quant_p_frames: int = ...,
        quant_b_frames: int = ...,
        preset_level: V4L2VideoEncHwPreset | str | int = ...,
        qp_range: str | None = ...,
        vbv_size: int = ...,
        MeasureEncoderLatency: bool = ...,
        ratecontrol_enable: bool = ...,
        maxperf_enable: bool = ...,
        idrinterval: int = ...,
        copy_timestamp: bool = ...,
        profile: V4l2VideoEncProfileType | str | int = ...,
        insert_vui: bool = ...,
        insert_sps_pps: bool = ...,
        insert_aud: bool = ...,
        num_B_Frames: int = ...,
        disable_cabac: bool = ...,
        bit_packetization: bool = ...,
        SliceIntraRefreshInterval: int = ...,
        EnableTwopassCBR: bool = ...,
        EnableMVBufferMeta: bool = ...,
        slice_header_spacing: int = ...,
        num_Ref_Frames: int = ...,
        poc_type: int = ...,
        enable_lossless: bool = ...,
    ) -> None: ...

class NvV4l2H265Enc(Element):
    """nvv4l2h265enc — V4L2 H.265 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2h265enc"
    CaptureIoMode = NvV4l2EncCaptureIOMode
    ControlRate = V4l2VideoEncRateControlType
    OutputIoMode = NvV4l2EncOutputIOMode
    PresetLevel = V4L2VideoEncHwPreset
    Profile = V4L2VideoEncProfileType
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    device: str | None
    device_name: str | None
    device_fd: int  # 기본값: -1
    output_io_mode: Prop[NvV4l2EncOutputIOMode, NvV4l2EncOutputIOMode | str | int]  # 기본값: auto
    capture_io_mode: Prop[NvV4l2EncCaptureIOMode, NvV4l2EncCaptureIOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    bitrate: int  # 기본값: 4000000
    control_rate: Prop[V4l2VideoEncRateControlType, V4l2VideoEncRateControlType | str | int]  # 기본값: constant_bitrate
    iframeinterval: int  # 기본값: 30
    peak_bitrate: int  # 기본값: 0
    quant_i_frames: int  # 기본값: 4294967295
    quant_p_frames: int  # 기본값: 4294967295
    quant_b_frames: int  # 기본값: 4294967295
    preset_level: Prop[V4L2VideoEncHwPreset, V4L2VideoEncHwPreset | str | int]  # 기본값: UltraFastPreset
    qp_range: str | None  # 기본값: '-1,-1:-1,-1:-1,-1'
    vbv_size: int  # 기본값: 4000000
    MeasureEncoderLatency: bool  # 기본값: False
    ratecontrol_enable: bool  # 기본값: True
    maxperf_enable: bool  # 기본값: False
    idrinterval: int  # 기본값: 256
    copy_timestamp: bool  # 기본값: False
    insert_sps_pps: bool  # 기본값: False
    profile: Prop[V4L2VideoEncProfileType, V4L2VideoEncProfileType | str | int]  # 기본값: Main
    insert_vui: bool  # 기본값: False
    insert_aud: bool  # 기본값: False
    bit_packetization: bool  # 기본값: False
    slice_header_spacing: int  # 기본값: 0
    SliceIntraRefreshInterval: int  # 기본값: 60
    EnableTwopassCBR: bool  # 기본값: False
    EnableMVBufferMeta: bool  # 기본값: False
    num_B_Frames: int  # 기본값: 0
    num_Ref_Frames: int  # 기본값: 1
    enable_lossless: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        output_io_mode: NvV4l2EncOutputIOMode | str | int = ...,
        capture_io_mode: NvV4l2EncCaptureIOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        bitrate: int = ...,
        control_rate: V4l2VideoEncRateControlType | str | int = ...,
        iframeinterval: int = ...,
        peak_bitrate: int = ...,
        quant_i_frames: int = ...,
        quant_p_frames: int = ...,
        quant_b_frames: int = ...,
        preset_level: V4L2VideoEncHwPreset | str | int = ...,
        qp_range: str | None = ...,
        vbv_size: int = ...,
        MeasureEncoderLatency: bool = ...,
        ratecontrol_enable: bool = ...,
        maxperf_enable: bool = ...,
        idrinterval: int = ...,
        copy_timestamp: bool = ...,
        insert_sps_pps: bool = ...,
        profile: V4L2VideoEncProfileType | str | int = ...,
        insert_vui: bool = ...,
        insert_aud: bool = ...,
        bit_packetization: bool = ...,
        slice_header_spacing: int = ...,
        SliceIntraRefreshInterval: int = ...,
        EnableTwopassCBR: bool = ...,
        EnableMVBufferMeta: bool = ...,
        num_B_Frames: int = ...,
        num_Ref_Frames: int = ...,
        enable_lossless: bool = ...,
    ) -> None: ...

class NvV4l2Vp9Enc(Element):
    """nvv4l2vp9enc — V4L2 VP9 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "nvv4l2vp9enc"
    CaptureIoMode = NvV4l2EncCaptureIOMode
    ControlRate = V4l2VideoEncRateControlType
    OutputIoMode = NvV4l2EncOutputIOMode
    PresetLevel = V4L2VideoEncHwPreset
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    device: str | None
    device_name: str | None
    device_fd: int  # 기본값: -1
    output_io_mode: Prop[NvV4l2EncOutputIOMode, NvV4l2EncOutputIOMode | str | int]  # 기본값: auto
    capture_io_mode: Prop[NvV4l2EncCaptureIOMode, NvV4l2EncCaptureIOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    bitrate: int  # 기본값: 4000000
    control_rate: Prop[V4l2VideoEncRateControlType, V4l2VideoEncRateControlType | str | int]  # 기본값: constant_bitrate
    iframeinterval: int  # 기본값: 30
    peak_bitrate: int  # 기본값: 0
    quant_i_frames: int  # 기본값: 4294967295
    quant_p_frames: int  # 기본값: 4294967295
    quant_b_frames: int  # 기본값: 4294967295
    preset_level: Prop[V4L2VideoEncHwPreset, V4L2VideoEncHwPreset | str | int]  # 기본값: UltraFastPreset
    qp_range: str | None  # 기본값: '-1,-1:-1,-1:-1,-1'
    vbv_size: int  # 기본값: 4000000
    MeasureEncoderLatency: bool  # 기본값: False
    ratecontrol_enable: bool  # 기본값: True
    maxperf_enable: bool  # 기본값: False
    idrinterval: int  # 기본값: 256
    copy_timestamp: bool  # 기본값: False
    enable_headers: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        output_io_mode: NvV4l2EncOutputIOMode | str | int = ...,
        capture_io_mode: NvV4l2EncCaptureIOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        bitrate: int = ...,
        control_rate: V4l2VideoEncRateControlType | str | int = ...,
        iframeinterval: int = ...,
        peak_bitrate: int = ...,
        quant_i_frames: int = ...,
        quant_p_frames: int = ...,
        quant_b_frames: int = ...,
        preset_level: V4L2VideoEncHwPreset | str | int = ...,
        qp_range: str | None = ...,
        vbv_size: int = ...,
        MeasureEncoderLatency: bool = ...,
        ratecontrol_enable: bool = ...,
        maxperf_enable: bool = ...,
        idrinterval: int = ...,
        copy_timestamp: bool = ...,
        enable_headers: bool = ...,
    ) -> None: ...

class NvVidConv(Element):
    """nvvidconv — NvVidConv Plugin

    klass: Filter/Converter/Video/Scaler
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "nvvidconv"
    BufMemoryType = NvVidConvBufMemoryType
    ComputeHWType = NvVidConvComputeHWType
    FlipMethod = NvVideoFlipMethod
    qos: bool  # 기본값: False
    silent: bool  # 기본값: False
    flip_method: Prop[NvVideoFlipMethod, NvVideoFlipMethod | str | int]  # 기본값: none
    output_buffers: int  # 기본값: 4
    interpolation_method: Prop[InterpolationMethod, InterpolationMethod | str | int]  # 기본값: Nearest
    left: int  # 기본값: 0
    right: int  # 기본값: 0
    top: int  # 기본값: 0
    bottom: int  # 기본값: 0
    bl_output: bool  # 기본값: True
    gpu_id: int  # 기본값: 0
    compute_hw: Prop[NvVidConvComputeHWType, NvVidConvComputeHWType | str | int]  # 기본값: Default
    nvbuf_memory_type: Prop[NvVidConvBufMemoryType, NvVidConvBufMemoryType | str | int]  # 기본값: nvbuf-mem-default

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        silent: bool = ...,
        flip_method: NvVideoFlipMethod | str | int = ...,
        output_buffers: int = ...,
        interpolation_method: InterpolationMethod | str | int = ...,
        left: int = ...,
        right: int = ...,
        top: int = ...,
        bottom: int = ...,
        bl_output: bool = ...,
        gpu_id: int = ...,
        compute_hw: NvVidConvComputeHWType | str | int = ...,
        nvbuf_memory_type: NvVidConvBufMemoryType | str | int = ...,
    ) -> None: ...

class PlayBin(Element):
    """playbin — Player Bin 2

    klass: Generic/Bin/Player
    """
    FACTORY: ClassVar[str]  # "playbin"
    Flags = PlayFlags
    VideoMultiviewMode = VideoMultiviewFramePacking
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    delay: int  # 기본값: 0
    auto_flush_bus: bool  # 기본값: True
    latency: int  # 기본값: 18446744073709551615
    uri: str | None
    current_uri: str | None
    suburi: str | None
    current_suburi: str | None
    source: Any
    flags: Prop[PlayFlags, PlayFlags | str | int]  # 기본값: video+audio+text+soft-volume+deinterlace+soft-colorbalance
    n_video: int  # 기본값: 0
    current_video: int  # 기본값: -1
    n_audio: int  # 기본값: 0
    current_audio: int  # 기본값: -1
    n_text: int  # 기본값: 0
    current_text: int  # 기본값: -1
    subtitle_encoding: str | None
    audio_sink: Any
    video_sink: Any
    vis_plugin: Any
    text_sink: Any
    video_stream_combiner: Any
    audio_stream_combiner: Any
    text_stream_combiner: Any
    volume: float  # 기본값: 1.0
    mute: bool  # 기본값: False
    sample: Any
    subtitle_font_desc: str | None
    connection_speed: int  # 기본값: 0
    buffer_size: int  # 기본값: -1
    buffer_duration: int  # 기본값: -1
    av_offset: int  # 기본값: 0
    text_offset: int  # 기본값: 0
    ring_buffer_max_size: int  # 기본값: 0
    force_aspect_ratio: bool  # 기본값: True
    audio_filter: Any
    video_filter: Any
    video_multiview_mode: Prop[VideoMultiviewFramePacking, VideoMultiviewFramePacking | str | int]  # 기본값: none
    video_multiview_flags: Prop[VideoMultiviewFlags, VideoMultiviewFlags | str | int]  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        delay: int = ...,
        auto_flush_bus: bool = ...,
        latency: int = ...,
        uri: str | None = ...,
        suburi: str | None = ...,
        flags: PlayFlags | str | int = ...,
        current_video: int = ...,
        current_audio: int = ...,
        current_text: int = ...,
        subtitle_encoding: str | None = ...,
        audio_sink: Any = ...,
        video_sink: Any = ...,
        vis_plugin: Any = ...,
        text_sink: Any = ...,
        video_stream_combiner: Any = ...,
        audio_stream_combiner: Any = ...,
        text_stream_combiner: Any = ...,
        volume: float = ...,
        mute: bool = ...,
        subtitle_font_desc: str | None = ...,
        connection_speed: int = ...,
        buffer_size: int = ...,
        buffer_duration: int = ...,
        av_offset: int = ...,
        text_offset: int = ...,
        ring_buffer_max_size: int = ...,
        force_aspect_ratio: bool = ...,
        audio_filter: Any = ...,
        video_filter: Any = ...,
        video_multiview_mode: VideoMultiviewFramePacking | str | int = ...,
        video_multiview_flags: VideoMultiviewFlags | str | int = ...,
    ) -> None: ...

class QtMux(Element):
    """qtmux — QuickTime Muxer

    klass: Codec/Muxer
    pads: src src (always), sink audio_%u (request), sink video_%u (request), sink subtitle_%u (request), sink caption_%u (request)
    """
    FACTORY: ClassVar[str]  # "qtmux"
    DtsMethod = QTMuxDtsMethods
    FragmentMode = QTMuxFragmentMode
    StartTimeSelection = AggregatorStartTimeSelection
    latency: int  # 기본값: 0
    min_upstream_latency: int  # 기본값: 0
    start_time_selection: Prop[AggregatorStartTimeSelection, AggregatorStartTimeSelection | str | int]  # 기본값: zero
    start_time: int  # 기본값: 18446744073709551615
    emit_signals: bool  # 기본값: False
    movie_timescale: int  # 기본값: 0
    trak_timescale: int  # 기본값: 0
    faststart: bool  # 기본값: False
    faststart_file: str | None
    moov_recovery_file: str | None
    fragment_duration: int  # 기본값: 0
    reserved_max_duration: int  # 기본값: 18446744073709551615
    reserved_duration_remaining: int  # 기본값: 0
    reserved_moov_update_period: int  # 기본값: 18446744073709551615
    reserved_bytes_per_sec: int  # 기본값: 550
    reserved_prefill: bool  # 기본값: False
    dts_method: Prop[QTMuxDtsMethods, QTMuxDtsMethods | str | int]  # 기본값: reorder
    presentation_time: bool  # 기본값: True
    interleave_bytes: int  # 기본값: 0
    interleave_time: int  # 기본값: 250000000
    force_chunks: bool  # 기본값: False
    max_raw_audio_drift: int  # 기본값: 40000000
    start_gap_threshold: int  # 기본값: 0
    force_create_timecode_trak: bool  # 기본값: False
    fragment_mode: Prop[QTMuxFragmentMode, QTMuxFragmentMode | str | int]  # 기본값: dash-or-mss
    streamable: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        latency: int = ...,
        min_upstream_latency: int = ...,
        start_time_selection: AggregatorStartTimeSelection | str | int = ...,
        start_time: int = ...,
        emit_signals: bool = ...,
        movie_timescale: int = ...,
        trak_timescale: int = ...,
        faststart: bool = ...,
        faststart_file: str | None = ...,
        moov_recovery_file: str | None = ...,
        fragment_duration: int = ...,
        reserved_max_duration: int = ...,
        reserved_moov_update_period: int = ...,
        reserved_bytes_per_sec: int = ...,
        reserved_prefill: bool = ...,
        dts_method: QTMuxDtsMethods | str | int = ...,
        presentation_time: bool = ...,
        interleave_bytes: int = ...,
        interleave_time: int = ...,
        force_chunks: bool = ...,
        max_raw_audio_drift: int = ...,
        start_gap_threshold: int = ...,
        force_create_timecode_trak: bool = ...,
        fragment_mode: QTMuxFragmentMode | str | int = ...,
        streamable: bool = ...,
    ) -> None: ...

class Queue(Element):
    """queue — Queue

    klass: Generic
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "queue"
    Leaky = QueueLeaky
    current_level_buffers: int  # 기본값: 0
    current_level_bytes: int  # 기본값: 0
    current_level_time: int  # 기본값: 0
    max_size_buffers: int  # 기본값: 200
    max_size_bytes: int  # 기본값: 10485760
    max_size_time: int  # 기본값: 1000000000
    min_threshold_buffers: int  # 기본값: 0
    min_threshold_bytes: int  # 기본값: 0
    min_threshold_time: int  # 기본값: 0
    leaky: Prop[QueueLeaky, QueueLeaky | str | int]  # 기본값: no
    silent: bool  # 기본값: False
    flush_on_eos: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        max_size_buffers: int = ...,
        max_size_bytes: int = ...,
        max_size_time: int = ...,
        min_threshold_buffers: int = ...,
        min_threshold_bytes: int = ...,
        min_threshold_time: int = ...,
        leaky: QueueLeaky | str | int = ...,
        silent: bool = ...,
        flush_on_eos: bool = ...,
    ) -> None: ...

class Queue2(Element):
    """queue2 — Queue 2

    klass: Generic
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "queue2"
    current_level_buffers: int  # 기본값: 0
    current_level_bytes: int  # 기본값: 0
    current_level_time: int  # 기본값: 0
    max_size_buffers: int  # 기본값: 100
    max_size_bytes: int  # 기본값: 2097152
    max_size_time: int  # 기본값: 2000000000
    use_buffering: bool  # 기본값: False
    use_tags_bitrate: bool  # 기본값: False
    use_rate_estimate: bool  # 기본값: True
    low_percent: int  # 기본값: 1
    high_percent: int  # 기본값: 99
    low_watermark: float  # 기본값: 0.01
    high_watermark: float  # 기본값: 0.99
    temp_template: str | None
    temp_location: str | None
    temp_remove: bool  # 기본값: True
    ring_buffer_max_size: int  # 기본값: 0
    avg_in_rate: int  # 기본값: 0
    use_bitrate_query: bool  # 기본값: True
    bitrate: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        max_size_buffers: int = ...,
        max_size_bytes: int = ...,
        max_size_time: int = ...,
        use_buffering: bool = ...,
        use_tags_bitrate: bool = ...,
        use_rate_estimate: bool = ...,
        low_percent: int = ...,
        high_percent: int = ...,
        low_watermark: float = ...,
        high_watermark: float = ...,
        temp_template: str | None = ...,
        temp_remove: bool = ...,
        ring_buffer_max_size: int = ...,
        use_bitrate_query: bool = ...,
    ) -> None: ...

class RtpH264Depay(Element):
    """rtph264depay — RTP H264 depayloader

    klass: Codec/Depayloader/Network/RTP
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "rtph264depay"
    stats: dict[str, Any] | str
    source_info: bool  # 기본값: False
    max_reorder: int  # 기본값: 100
    auto_header_extension: bool  # 기본값: True
    wait_for_keyframe: bool  # 기본값: False
    request_keyframe: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        source_info: bool = ...,
        max_reorder: int = ...,
        auto_header_extension: bool = ...,
        wait_for_keyframe: bool = ...,
        request_keyframe: bool = ...,
    ) -> None: ...

class RtpH264Pay(Element):
    """rtph264pay — RTP H264 payloader

    klass: Codec/Payloader/Network/RTP
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "rtph264pay"
    AggregateMode = RtpH264AggregateMode
    mtu: int  # 기본값: 1400
    pt: int  # 기본값: 96
    ssrc: int  # 기본값: 4294967295
    timestamp_offset: int  # 기본값: 4294967295
    seqnum_offset: int  # 기본값: -1
    max_ptime: int  # 기본값: -1
    min_ptime: int  # 기본값: 0
    timestamp: int  # 기본값: 0
    seqnum: int  # 기본값: 0
    perfect_rtptime: bool  # 기본값: True
    ptime_multiple: int  # 기본값: 0
    stats: dict[str, Any] | str
    source_info: bool  # 기본값: False
    onvif_no_rate_control: bool  # 기본값: False
    scale_rtptime: bool  # 기본값: True
    auto_header_extension: bool  # 기본값: True
    sprop_parameter_sets: str | None
    config_interval: int  # 기본값: 0
    aggregate_mode: Prop[RtpH264AggregateMode, RtpH264AggregateMode | str | int]  # 기본값: none

    def __init__(
        self,
        *,
        name: str | None = ...,
        mtu: int = ...,
        pt: int = ...,
        ssrc: int = ...,
        timestamp_offset: int = ...,
        seqnum_offset: int = ...,
        max_ptime: int = ...,
        min_ptime: int = ...,
        perfect_rtptime: bool = ...,
        ptime_multiple: int = ...,
        source_info: bool = ...,
        onvif_no_rate_control: bool = ...,
        scale_rtptime: bool = ...,
        auto_header_extension: bool = ...,
        sprop_parameter_sets: str | None = ...,
        config_interval: int = ...,
        aggregate_mode: RtpH264AggregateMode | str | int = ...,
    ) -> None: ...

class RtpH265Pay(Element):
    """rtph265pay — RTP H265 payloader

    klass: Codec/Payloader/Network/RTP
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "rtph265pay"
    AggregateMode = RtpH265AggregateMode
    mtu: int  # 기본값: 1400
    pt: int  # 기본값: 96
    ssrc: int  # 기본값: 4294967295
    timestamp_offset: int  # 기본값: 4294967295
    seqnum_offset: int  # 기본값: -1
    max_ptime: int  # 기본값: -1
    min_ptime: int  # 기본값: 0
    timestamp: int  # 기본값: 0
    seqnum: int  # 기본값: 0
    perfect_rtptime: bool  # 기본값: True
    ptime_multiple: int  # 기본값: 0
    stats: dict[str, Any] | str
    source_info: bool  # 기본값: False
    onvif_no_rate_control: bool  # 기본값: False
    scale_rtptime: bool  # 기본값: True
    auto_header_extension: bool  # 기본값: True
    config_interval: int  # 기본값: 0
    aggregate_mode: Prop[RtpH265AggregateMode, RtpH265AggregateMode | str | int]  # 기본값: none

    def __init__(
        self,
        *,
        name: str | None = ...,
        mtu: int = ...,
        pt: int = ...,
        ssrc: int = ...,
        timestamp_offset: int = ...,
        seqnum_offset: int = ...,
        max_ptime: int = ...,
        min_ptime: int = ...,
        perfect_rtptime: bool = ...,
        ptime_multiple: int = ...,
        source_info: bool = ...,
        onvif_no_rate_control: bool = ...,
        scale_rtptime: bool = ...,
        auto_header_extension: bool = ...,
        config_interval: int = ...,
        aggregate_mode: RtpH265AggregateMode | str | int = ...,
    ) -> None: ...

class RtpJitterBuffer(Element):
    """rtpjitterbuffer — RTP packet jitter-buffer

    klass: Filter/Network/RTP
    pads: src src (always), sink sink (always), sink sink_rtcp (request)
    """
    FACTORY: ClassVar[str]  # "rtpjitterbuffer"
    Mode = RTPJitterBufferMode
    latency: int  # 기본값: 200
    drop_on_latency: bool  # 기본값: False
    ts_offset: int  # 기본값: 0
    max_ts_offset_adjustment: int  # 기본값: 0
    do_lost: bool  # 기본값: False
    post_drop_messages: bool  # 기본값: False
    drop_messages_interval: int  # 기본값: 200
    mode: Prop[RTPJitterBufferMode, RTPJitterBufferMode | str | int]  # 기본값: slave
    percent: int  # 기본값: 0
    do_retransmission: bool  # 기본값: False
    rtx_next_seqnum: bool  # 기본값: True
    rtx_delay: int  # 기본값: -1
    rtx_min_delay: int  # 기본값: 0
    rtx_delay_reorder: int  # 기본값: 3
    rtx_retry_timeout: int  # 기본값: -1
    rtx_min_retry_timeout: int  # 기본값: -1
    rtx_retry_period: int  # 기본값: -1
    rtx_max_retries: int  # 기본값: -1
    rtx_deadline: int  # 기본값: -1
    rtx_stats_timeout: int  # 기본값: 1000
    stats: dict[str, Any] | str
    max_rtcp_rtp_time_diff: int  # 기본값: 1000
    max_dropout_time: int  # 기본값: 60000
    max_misorder_time: int  # 기본값: 2000
    rfc7273_sync: bool  # 기본값: False
    faststart_min_packets: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        latency: int = ...,
        drop_on_latency: bool = ...,
        ts_offset: int = ...,
        max_ts_offset_adjustment: int = ...,
        do_lost: bool = ...,
        post_drop_messages: bool = ...,
        drop_messages_interval: int = ...,
        mode: RTPJitterBufferMode | str | int = ...,
        do_retransmission: bool = ...,
        rtx_next_seqnum: bool = ...,
        rtx_delay: int = ...,
        rtx_min_delay: int = ...,
        rtx_delay_reorder: int = ...,
        rtx_retry_timeout: int = ...,
        rtx_min_retry_timeout: int = ...,
        rtx_retry_period: int = ...,
        rtx_max_retries: int = ...,
        rtx_deadline: int = ...,
        rtx_stats_timeout: int = ...,
        max_rtcp_rtp_time_diff: int = ...,
        max_dropout_time: int = ...,
        max_misorder_time: int = ...,
        rfc7273_sync: bool = ...,
        faststart_min_packets: int = ...,
    ) -> None: ...

class RtspSrc(Element):
    """rtspsrc — RTSP packet receiver

    klass: Source/Network
    pads: src stream_%u (sometimes)
    """
    FACTORY: ClassVar[str]  # "rtspsrc"
    Backchannel = RTSPBackchannel
    BufferMode = RTSPSrcBufferMode
    DefaultRtspVersion = RTSPVersion
    NatMethod = RTSPNatMethod
    NtpTimeSource = RTSPSrcNtpTimeSource
    Protocols = RTSPLowerTrans
    TlsValidationFlags = GTlsCertificateFlags
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    location: str | None
    protocols: Prop[RTSPLowerTrans, RTSPLowerTrans | str | int]  # 기본값: unknown+udp+unknown+udp-mcast+unknown+tcp
    debug: bool  # 기본값: False
    retry: int  # 기본값: 20
    timeout: int  # 기본값: 5000000
    tcp_timeout: int  # 기본값: 20000000
    latency: int  # 기본값: 2000
    drop_on_latency: bool  # 기본값: False
    connection_speed: int  # 기본값: 0
    nat_method: Prop[RTSPNatMethod, RTSPNatMethod | str | int]  # 기본값: dummy
    do_rtcp: bool  # 기본값: True
    do_rtsp_keep_alive: bool  # 기본값: True
    proxy: str | None
    proxy_id: str | None  # 기본값: ''
    proxy_pw: str | None  # 기본값: ''
    rtp_blocksize: int  # 기본값: 0
    user_id: str | None
    user_pw: str | None
    buffer_mode: Prop[RTSPSrcBufferMode, RTSPSrcBufferMode | str | int]  # 기본값: auto
    port_range: str | None
    udp_buffer_size: int  # 기본값: 524288
    short_header: bool  # 기본값: False
    probation: int  # 기본값: 2
    udp_reconnect: bool  # 기본값: True
    multicast_iface: str | None
    ntp_sync: bool  # 기본값: False
    use_pipeline_clock: bool  # 기본값: False
    sdes: dict[str, Any] | str
    tls_validation_flags: Prop[GTlsCertificateFlags, GTlsCertificateFlags | str | int]  # 기본값: unknown-ca+bad-identity+not-activated+expired+revoked+insecure+generic-error+unknown-ca+bad-identity+not-activated+expired+revoked+insecure+generic-error+validate-all
    tls_database: Any
    tls_interaction: Any
    do_retransmission: bool  # 기본값: True
    ntp_time_source: Prop[RTSPSrcNtpTimeSource, RTSPSrcNtpTimeSource | str | int]  # 기본값: ntp
    user_agent: str | None  # 기본값: 'GStreamer/1.20.3'
    max_rtcp_rtp_time_diff: int  # 기본값: 1000
    rfc7273_sync: bool  # 기본값: False
    max_ts_offset_adjustment: int  # 기본값: 0
    max_ts_offset: int  # 기본값: 3000000000
    default_rtsp_version: Prop[RTSPVersion, RTSPVersion | str | int]  # 기본값: 1-0
    backchannel: Prop[RTSPBackchannel, RTSPBackchannel | str | int]  # 기본값: none
    teardown_timeout: int  # 기본값: 100000000
    onvif_mode: bool  # 기본값: False
    onvif_rate_control: bool  # 기본값: True
    is_live: bool  # 기본값: True
    ignore_x_server_reply: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        location: str | None = ...,
        protocols: RTSPLowerTrans | str | int = ...,
        debug: bool = ...,
        retry: int = ...,
        timeout: int = ...,
        tcp_timeout: int = ...,
        latency: int = ...,
        drop_on_latency: bool = ...,
        connection_speed: int = ...,
        nat_method: RTSPNatMethod | str | int = ...,
        do_rtcp: bool = ...,
        do_rtsp_keep_alive: bool = ...,
        proxy: str | None = ...,
        proxy_id: str | None = ...,
        proxy_pw: str | None = ...,
        rtp_blocksize: int = ...,
        user_id: str | None = ...,
        user_pw: str | None = ...,
        buffer_mode: RTSPSrcBufferMode | str | int = ...,
        port_range: str | None = ...,
        udp_buffer_size: int = ...,
        short_header: bool = ...,
        probation: int = ...,
        udp_reconnect: bool = ...,
        multicast_iface: str | None = ...,
        ntp_sync: bool = ...,
        use_pipeline_clock: bool = ...,
        sdes: dict[str, Any] | str = ...,
        tls_validation_flags: GTlsCertificateFlags | str | int = ...,
        tls_database: Any = ...,
        tls_interaction: Any = ...,
        do_retransmission: bool = ...,
        ntp_time_source: RTSPSrcNtpTimeSource | str | int = ...,
        user_agent: str | None = ...,
        max_rtcp_rtp_time_diff: int = ...,
        rfc7273_sync: bool = ...,
        max_ts_offset_adjustment: int = ...,
        max_ts_offset: int = ...,
        default_rtsp_version: RTSPVersion | str | int = ...,
        backchannel: RTSPBackchannel | str | int = ...,
        teardown_timeout: int = ...,
        onvif_mode: bool = ...,
        onvif_rate_control: bool = ...,
        is_live: bool = ...,
        ignore_x_server_reply: bool = ...,
    ) -> None: ...

class SoupHttpSrc(Element):
    """souphttpsrc — HTTP client source

    klass: Source/Network
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "souphttpsrc"
    HttpLogLevel = SoupLoggerLogLevel
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    location: str | None  # 기본값: ''
    is_live: bool  # 기본값: False
    user_agent: str | None  # 기본값: 'GStreamer souphttpsrc 1.20.3 '
    automatic_redirect: bool  # 기본값: True
    proxy: str | None  # 기본값: ''
    user_id: str | None  # 기본값: ''
    user_pw: str | None  # 기본값: ''
    proxy_id: str | None  # 기본값: ''
    proxy_pw: str | None  # 기본값: ''
    cookies: Any
    iradio_mode: bool  # 기본값: True
    timeout: int  # 기본값: 15
    extra_headers: dict[str, Any] | str
    http_log_level: Prop[SoupLoggerLogLevel, SoupLoggerLogLevel | str | int]  # 기본값: headers
    compress: bool  # 기본값: False
    keep_alive: bool  # 기본값: True
    ssl_strict: bool  # 기본값: True
    ssl_ca_file: str | None
    ssl_use_system_ca_file: bool  # 기본값: True
    tls_database: Any
    retries: int  # 기본값: 3
    method: str | None
    tls_interaction: Any

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        location: str | None = ...,
        is_live: bool = ...,
        user_agent: str | None = ...,
        automatic_redirect: bool = ...,
        proxy: str | None = ...,
        user_id: str | None = ...,
        user_pw: str | None = ...,
        proxy_id: str | None = ...,
        proxy_pw: str | None = ...,
        cookies: Any = ...,
        iradio_mode: bool = ...,
        timeout: int = ...,
        extra_headers: dict[str, Any] | str = ...,
        http_log_level: SoupLoggerLogLevel | str | int = ...,
        compress: bool = ...,
        keep_alive: bool = ...,
        ssl_strict: bool = ...,
        ssl_ca_file: str | None = ...,
        ssl_use_system_ca_file: bool = ...,
        tls_database: Any = ...,
        retries: int = ...,
        method: str | None = ...,
        tls_interaction: Any = ...,
    ) -> None: ...

class Tee(Element):
    """tee — Tee pipe fitting

    klass: Generic
    pads: src src_%u (request), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "tee"
    PullMode = TeePullMode
    num_src_pads: int  # 기본값: 0
    has_chain: bool  # 기본값: True
    silent: bool  # 기본값: True
    last_message: str | None
    pull_mode: Prop[TeePullMode, TeePullMode | str | int]  # 기본값: never
    alloc_pad: Any
    allow_not_linked: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        has_chain: bool = ...,
        silent: bool = ...,
        pull_mode: TeePullMode | str | int = ...,
        alloc_pad: Any = ...,
        allow_not_linked: bool = ...,
    ) -> None: ...

class UdpSink(Element):
    """udpsink — UDP packet sender

    klass: Sink/Network
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "udpsink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    bytes_to_serve: int  # 기본값: 0
    bytes_served: int  # 기본값: 0
    socket: Any
    socket_v6: Any
    close_socket: bool  # 기본값: True
    used_socket: Any
    used_socket_v6: Any
    clients: str | None
    auto_multicast: bool  # 기본값: True
    multicast_iface: str | None
    ttl: int  # 기본값: 64
    ttl_mc: int  # 기본값: 1
    loop: bool  # 기본값: True
    force_ipv4: bool  # 기본값: False
    qos_dscp: int  # 기본값: -1
    send_duplicates: bool  # 기본값: True
    buffer_size: int  # 기본값: 0
    bind_address: str | None
    bind_port: int  # 기본값: 0
    host: str | None  # 기본값: 'localhost'
    port: int  # 기본값: 5004

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        socket: Any = ...,
        socket_v6: Any = ...,
        close_socket: bool = ...,
        clients: str | None = ...,
        auto_multicast: bool = ...,
        multicast_iface: str | None = ...,
        ttl: int = ...,
        ttl_mc: int = ...,
        loop: bool = ...,
        force_ipv4: bool = ...,
        qos_dscp: int = ...,
        send_duplicates: bool = ...,
        buffer_size: int = ...,
        bind_address: str | None = ...,
        bind_port: int = ...,
        host: str | None = ...,
        port: int = ...,
    ) -> None: ...

class UdpSrc(Element):
    """udpsrc — UDP packet receiver

    klass: Source/Network
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "udpsrc"
    SocketTimestamp = SocketTimestampMode
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    port: int  # 기본값: 5004
    multicast_group: str | None  # 기본값: '0.0.0.0'
    multicast_iface: str | None
    uri: str | None  # 기본값: 'udp://0.0.0.0:5004'
    caps: Prop[Caps, Caps | str]
    socket: Any
    buffer_size: int  # 기본값: 0
    timeout: int  # 기본값: 0
    skip_first_bytes: int  # 기본값: 0
    close_socket: bool  # 기본값: True
    used_socket: Any
    auto_multicast: bool  # 기본값: True
    reuse: bool  # 기본값: True
    address: str | None  # 기본값: '0.0.0.0'
    loop: bool  # 기본값: True
    retrieve_sender_address: bool  # 기본값: True
    mtu: int  # 기본값: 1492
    socket_timestamp: Prop[SocketTimestampMode, SocketTimestampMode | str | int]  # 기본값: realtime

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        port: int = ...,
        multicast_group: str | None = ...,
        multicast_iface: str | None = ...,
        uri: str | None = ...,
        caps: Caps | str = ...,
        socket: Any = ...,
        buffer_size: int = ...,
        timeout: int = ...,
        skip_first_bytes: int = ...,
        close_socket: bool = ...,
        auto_multicast: bool = ...,
        reuse: bool = ...,
        address: str | None = ...,
        loop: bool = ...,
        retrieve_sender_address: bool = ...,
        mtu: int = ...,
        socket_timestamp: SocketTimestampMode | str | int = ...,
    ) -> None: ...

class UriDecodeBin(Element):
    """uridecodebin — URI Decoder

    klass: Generic/Bin/Decoder
    pads: src src_%u (sometimes)
    """
    FACTORY: ClassVar[str]  # "uridecodebin"
    async_handling: bool  # 기본값: False
    message_forward: bool  # 기본값: False
    uri: str | None
    source: Any
    connection_speed: int  # 기본값: 0
    caps: Prop[Caps, Caps | str]
    subtitle_encoding: str | None
    buffer_size: int  # 기본값: -1
    buffer_duration: int  # 기본값: -1
    download: bool  # 기본값: False
    use_buffering: bool  # 기본값: False
    force_sw_decoders: bool  # 기본값: False
    expose_all_streams: bool  # 기본값: True
    ring_buffer_max_size: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        async_handling: bool = ...,
        message_forward: bool = ...,
        uri: str | None = ...,
        connection_speed: int = ...,
        caps: Caps | str = ...,
        subtitle_encoding: str | None = ...,
        buffer_size: int = ...,
        buffer_duration: int = ...,
        download: bool = ...,
        use_buffering: bool = ...,
        force_sw_decoders: bool = ...,
        expose_all_streams: bool = ...,
        ring_buffer_max_size: int = ...,
    ) -> None: ...

class V4l2Src(Element):
    """v4l2src — Video (video4linux2) Source

    klass: Source/Video
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "v4l2src"
    Flags = V4l2DeviceTypeFlags
    IoMode = V4l2IOMode
    Norm = V4L2_TV_norms
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    device: str | None  # 기본값: '/dev/video0'
    device_name: str | None
    device_fd: int  # 기본값: -1
    flags: Prop[V4l2DeviceTypeFlags, V4l2DeviceTypeFlags | str | int]  # 기본값: 0
    brightness: int  # 기본값: 0
    contrast: int  # 기본값: 0
    saturation: int  # 기본값: 0
    hue: int  # 기본값: 0
    norm: Prop[V4L2_TV_norms, V4L2_TV_norms | str | int]  # 기본값: none
    io_mode: Prop[V4l2IOMode, V4l2IOMode | str | int]  # 기본값: auto
    extra_controls: dict[str, Any] | str
    pixel_aspect_ratio: str | None  # 기본값: '1/1'
    force_aspect_ratio: bool  # 기본값: True

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        device: str | None = ...,
        brightness: int = ...,
        contrast: int = ...,
        saturation: int = ...,
        hue: int = ...,
        norm: V4L2_TV_norms | str | int = ...,
        io_mode: V4l2IOMode | str | int = ...,
        extra_controls: dict[str, Any] | str = ...,
        pixel_aspect_ratio: str | None = ...,
        force_aspect_ratio: bool = ...,
    ) -> None: ...

class Valve(Element):
    """valve — Valve element

    klass: Filter
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "valve"
    DropMode = ValveDropMode
    drop: bool  # 기본값: False
    drop_mode: Prop[ValveDropMode, ValveDropMode | str | int]  # 기본값: drop-all

    def __init__(
        self,
        *,
        name: str | None = ...,
        drop: bool = ...,
        drop_mode: ValveDropMode | str | int = ...,
    ) -> None: ...

class VideoConvert(Element):
    """videoconvert — Colorspace converter

    klass: Filter/Converter/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "videoconvert"
    AlphaMode = VideoAlphaMode
    ChromaMode = VideoChromaMode
    ChromaResampler = VideoResamplerMethod
    Dither = VideoDitherMethod
    GammaMode = VideoGammaMode
    MatrixMode = VideoMatrixMode
    PrimariesMode = VideoPrimariesMode
    qos: bool  # 기본값: False
    dither: Prop[VideoDitherMethod, VideoDitherMethod | str | int]  # 기본값: bayer
    dither_quantization: int  # 기본값: 1
    chroma_resampler: Prop[VideoResamplerMethod, VideoResamplerMethod | str | int]  # 기본값: linear
    alpha_mode: Prop[VideoAlphaMode, VideoAlphaMode | str | int]  # 기본값: copy
    alpha_value: float  # 기본값: 1.0
    chroma_mode: Prop[VideoChromaMode, VideoChromaMode | str | int]  # 기본값: full
    matrix_mode: Prop[VideoMatrixMode, VideoMatrixMode | str | int]  # 기본값: full
    gamma_mode: Prop[VideoGammaMode, VideoGammaMode | str | int]  # 기본값: none
    primaries_mode: Prop[VideoPrimariesMode, VideoPrimariesMode | str | int]  # 기본값: none
    n_threads: int  # 기본값: 1

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        dither: VideoDitherMethod | str | int = ...,
        dither_quantization: int = ...,
        chroma_resampler: VideoResamplerMethod | str | int = ...,
        alpha_mode: VideoAlphaMode | str | int = ...,
        alpha_value: float = ...,
        chroma_mode: VideoChromaMode | str | int = ...,
        matrix_mode: VideoMatrixMode | str | int = ...,
        gamma_mode: VideoGammaMode | str | int = ...,
        primaries_mode: VideoPrimariesMode | str | int = ...,
        n_threads: int = ...,
    ) -> None: ...

class VideoCrop(Element):
    """videocrop — Crop

    klass: Filter/Effect/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "videocrop"
    qos: bool  # 기본값: False
    left: int  # 기본값: 0
    right: int  # 기본값: 0
    top: int  # 기본값: 0
    bottom: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        left: int = ...,
        right: int = ...,
        top: int = ...,
        bottom: int = ...,
    ) -> None: ...

class VideoFlip(Element):
    """videoflip — Video flipper

    klass: Filter/Effect/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "videoflip"
    Method = VideoFlipMethod
    VideoDirection = VideoOrientationMethod
    video_direction: Prop[VideoOrientationMethod, VideoOrientationMethod | str | int]  # 기본값: identity
    qos: bool  # 기본값: False
    method: Prop[VideoFlipMethod, VideoFlipMethod | str | int]  # 기본값: none

    def __init__(
        self,
        *,
        name: str | None = ...,
        video_direction: VideoOrientationMethod | str | int = ...,
        qos: bool = ...,
        method: VideoFlipMethod | str | int = ...,
    ) -> None: ...

class VideoRate(Element):
    """videorate — Video rate adjuster

    klass: Filter/Effect/Video
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "videorate"
    qos: bool  # 기본값: False
    in_: int  # 기본값: 0
    out: int  # 기본값: 0
    duplicate: int  # 기본값: 0
    drop: int  # 기본값: 0
    silent: bool  # 기본값: True
    new_pref: float  # 기본값: 1.0
    skip_to_first: bool  # 기본값: False
    drop_only: bool  # 기본값: False
    average_period: int  # 기본값: 0
    max_rate: int  # 기본값: 2147483647
    rate: float  # 기본값: 1.0
    max_duplication_time: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        silent: bool = ...,
        new_pref: float = ...,
        skip_to_first: bool = ...,
        drop_only: bool = ...,
        average_period: int = ...,
        max_rate: int = ...,
        rate: float = ...,
        max_duplication_time: int = ...,
    ) -> None: ...

class VideoScale(Element):
    """videoscale — Video scaler

    klass: Filter/Converter/Video/Scaler
    pads: sink sink (always), src src (always)
    """
    FACTORY: ClassVar[str]  # "videoscale"
    Method = VideoScaleMethod
    qos: bool  # 기본값: False
    method: Prop[VideoScaleMethod, VideoScaleMethod | str | int]  # 기본값: bilinear
    add_borders: bool  # 기본값: True
    sharpness: float  # 기본값: 1.0
    sharpen: float  # 기본값: 0.0
    dither: bool  # 기본값: False
    envelope: float  # 기본값: 2.0
    gamma_decode: bool  # 기본값: False
    n_threads: int  # 기본값: 1

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        method: VideoScaleMethod | str | int = ...,
        add_borders: bool = ...,
        sharpness: float = ...,
        sharpen: float = ...,
        dither: bool = ...,
        envelope: float = ...,
        gamma_decode: bool = ...,
        n_threads: int = ...,
    ) -> None: ...

class VideoTestSrc(Element):
    """videotestsrc — Video test source

    klass: Source/Video
    pads: src src (always)
    """
    FACTORY: ClassVar[str]  # "videotestsrc"
    AnimationMode = VideoTestSrcAnimationMode
    MotionType = VideoTestSrcMotionType
    Pattern = VideoTestSrcPattern
    blocksize: int  # 기본값: 4096
    num_buffers: int  # 기본값: -1
    typefind: bool  # 기본값: False
    do_timestamp: bool  # 기본값: False
    pattern: Prop[VideoTestSrcPattern, VideoTestSrcPattern | str | int]  # 기본값: smpte
    timestamp_offset: int  # 기본값: 0
    is_live: bool  # 기본값: False
    k0: int  # 기본값: 0
    kx: int  # 기본값: 0
    ky: int  # 기본값: 0
    kt: int  # 기본값: 0
    kxt: int  # 기본값: 0
    kyt: int  # 기본값: 0
    kxy: int  # 기본값: 0
    kx2: int  # 기본값: 0
    ky2: int  # 기본값: 0
    kt2: int  # 기본값: 0
    xoffset: int  # 기본값: 0
    yoffset: int  # 기본값: 0
    foreground_color: int  # 기본값: 4294967295
    background_color: int  # 기본값: 4278190080
    horizontal_speed: int  # 기본값: 0
    animation_mode: Prop[VideoTestSrcAnimationMode, VideoTestSrcAnimationMode | str | int]  # 기본값: frames
    motion: Prop[VideoTestSrcMotionType, VideoTestSrcMotionType | str | int]  # 기본값: wavy
    flip: bool  # 기본값: False

    def __init__(
        self,
        *,
        name: str | None = ...,
        blocksize: int = ...,
        num_buffers: int = ...,
        typefind: bool = ...,
        do_timestamp: bool = ...,
        pattern: VideoTestSrcPattern | str | int = ...,
        timestamp_offset: int = ...,
        is_live: bool = ...,
        k0: int = ...,
        kx: int = ...,
        ky: int = ...,
        kt: int = ...,
        kxt: int = ...,
        kyt: int = ...,
        kxy: int = ...,
        kx2: int = ...,
        ky2: int = ...,
        kt2: int = ...,
        xoffset: int = ...,
        yoffset: int = ...,
        foreground_color: int = ...,
        background_color: int = ...,
        horizontal_speed: int = ...,
        animation_mode: VideoTestSrcAnimationMode | str | int = ...,
        motion: VideoTestSrcMotionType | str | int = ...,
        flip: bool = ...,
    ) -> None: ...

class VpxEnc(Element):
    """vp8enc — On2 VP8 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "vp8enc"
    EndUsage = VPXEncEndUsage
    ErrorResilient = VPXEncErFlags
    HorizontalScalingMode = VPXEncScalingMode
    KeyframeMode = VPXEncKfMode
    MultipassMode = VPXEncMultipassMode
    TokenPartitions = VPXEncTokenPartitions
    Tuning = VPXEncTuning
    VerticalScalingMode = VPXEncScalingMode
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    end_usage: Prop[VPXEncEndUsage, VPXEncEndUsage | str | int]  # 기본값: vbr
    target_bitrate: int  # 기본값: 0
    min_quantizer: int  # 기본값: 4
    max_quantizer: int  # 기본값: 63
    dropframe_threshold: int  # 기본값: 0
    resize_allowed: bool  # 기본값: False
    resize_up_threshold: int  # 기본값: 30
    resize_down_threshold: int  # 기본값: 60
    undershoot: int  # 기본값: 100
    overshoot: int  # 기본값: 100
    buffer_size: int  # 기본값: 6000
    buffer_initial_size: int  # 기본값: 4000
    buffer_optimal_size: int  # 기본값: 5000
    twopass_vbr_bias: int  # 기본값: 50
    twopass_vbr_minsection: int  # 기본값: 0
    twopass_vbr_maxsection: int  # 기본값: 0
    keyframe_mode: Prop[VPXEncKfMode, VPXEncKfMode | str | int]  # 기본값: auto
    keyframe_max_dist: int  # 기본값: 128
    temporal_scalability_number_layers: int  # 기본값: 1
    temporal_scalability_target_bitrate: Any
    temporal_scalability_rate_decimator: Any
    temporal_scalability_periodicity: int  # 기본값: 0
    temporal_scalability_layer_id: Any
    temporal_scalability_layer_flags: Any
    temporal_scalability_layer_sync_flags: Any
    multipass_mode: Prop[VPXEncMultipassMode, VPXEncMultipassMode | str | int]  # 기본값: one-pass
    multipass_cache_file: str | None  # 기본값: 'multipass.cache'
    error_resilient: Prop[VPXEncErFlags, VPXEncErFlags | str | int]  # 기본값: 0
    lag_in_frames: int  # 기본값: 0
    threads: int  # 기본값: 0
    deadline: int  # 기본값: 1000000
    horizontal_scaling_mode: Prop[VPXEncScalingMode, VPXEncScalingMode | str | int]  # 기본값: normal
    vertical_scaling_mode: Prop[VPXEncScalingMode, VPXEncScalingMode | str | int]  # 기본값: normal
    cpu_used: int  # 기본값: 0
    auto_alt_ref: bool  # 기본값: False
    noise_sensitivity: int  # 기본값: 0
    sharpness: int  # 기본값: 0
    static_threshold: int  # 기본값: 1
    token_partitions: Prop[VPXEncTokenPartitions, VPXEncTokenPartitions | str | int]  # 기본값: 1
    arnr_maxframes: int  # 기본값: 0
    arnr_strength: int  # 기본값: 3
    arnr_type: int  # 기본값: 3
    tuning: Prop[VPXEncTuning, VPXEncTuning | str | int]  # 기본값: psnr
    cq_level: int  # 기본값: 10
    max_intra_bitrate: int  # 기본값: 0
    timebase: Fraction | tuple[int, int]
    bits_per_pixel: float  # 기본값: 0.04340000078082085

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        end_usage: VPXEncEndUsage | str | int = ...,
        target_bitrate: int = ...,
        min_quantizer: int = ...,
        max_quantizer: int = ...,
        dropframe_threshold: int = ...,
        resize_allowed: bool = ...,
        resize_up_threshold: int = ...,
        resize_down_threshold: int = ...,
        undershoot: int = ...,
        overshoot: int = ...,
        buffer_size: int = ...,
        buffer_initial_size: int = ...,
        buffer_optimal_size: int = ...,
        twopass_vbr_bias: int = ...,
        twopass_vbr_minsection: int = ...,
        twopass_vbr_maxsection: int = ...,
        keyframe_mode: VPXEncKfMode | str | int = ...,
        keyframe_max_dist: int = ...,
        temporal_scalability_number_layers: int = ...,
        temporal_scalability_target_bitrate: Any = ...,
        temporal_scalability_rate_decimator: Any = ...,
        temporal_scalability_periodicity: int = ...,
        temporal_scalability_layer_id: Any = ...,
        temporal_scalability_layer_flags: Any = ...,
        temporal_scalability_layer_sync_flags: Any = ...,
        multipass_mode: VPXEncMultipassMode | str | int = ...,
        multipass_cache_file: str | None = ...,
        error_resilient: VPXEncErFlags | str | int = ...,
        lag_in_frames: int = ...,
        threads: int = ...,
        deadline: int = ...,
        horizontal_scaling_mode: VPXEncScalingMode | str | int = ...,
        vertical_scaling_mode: VPXEncScalingMode | str | int = ...,
        cpu_used: int = ...,
        auto_alt_ref: bool = ...,
        noise_sensitivity: int = ...,
        sharpness: int = ...,
        static_threshold: int = ...,
        token_partitions: VPXEncTokenPartitions | str | int = ...,
        arnr_maxframes: int = ...,
        arnr_strength: int = ...,
        arnr_type: int = ...,
        tuning: VPXEncTuning | str | int = ...,
        cq_level: int = ...,
        max_intra_bitrate: int = ...,
        timebase: Fraction | tuple[int, int] = ...,
        bits_per_pixel: float = ...,
    ) -> None: ...

class X264Enc(Element):
    """x264enc — x264 H.264 Encoder

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "x264enc"
    Analyse = X264EncAnalyse
    FramePacking = X264EncFramePacking
    Me = X264EncMe
    Pass = X264EncPass
    Preset = X264EncPreset
    PsyTune = X264EncPsyTune
    Tune = X264EncTune
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    threads: int  # 기본값: 0
    sliced_threads: bool  # 기본값: False
    sync_lookahead: int  # 기본값: -1
    pass_: Prop[X264EncPass, X264EncPass | str | int]  # 기본값: cbr
    quantizer: int  # 기본값: 21
    multipass_cache_file: str | None  # 기본값: 'x264.log'
    byte_stream: bool  # 기본값: False
    bitrate: int  # 기본값: 2048
    intra_refresh: bool  # 기본값: False
    vbv_buf_capacity: int  # 기본값: 600
    me: Prop[X264EncMe, X264EncMe | str | int]  # 기본값: hex
    subme: int  # 기본값: 1
    analyse: Prop[X264EncAnalyse, X264EncAnalyse | str | int]  # 기본값: 0
    dct8x8: bool  # 기본값: False
    ref: int  # 기본값: 3
    bframes: int  # 기본값: 0
    b_adapt: bool  # 기본값: True
    b_pyramid: bool  # 기본값: False
    weightb: bool  # 기본값: False
    sps_id: int  # 기본값: 0
    aud: bool  # 기본값: True
    trellis: bool  # 기본값: True
    key_int_max: int  # 기본값: 0
    cabac: bool  # 기본값: True
    qp_min: int  # 기본값: 10
    qp_max: int  # 기본값: 51
    qp_step: int  # 기본값: 4
    ip_factor: float  # 기본값: 1.399999976158142
    pb_factor: float  # 기본값: 1.2999999523162842
    mb_tree: bool  # 기본값: True
    rc_lookahead: int  # 기본값: 40
    noise_reduction: int  # 기본값: 0
    interlaced: bool  # 기본값: False
    option_string: str | None  # 기본값: ''
    speed_preset: Prop[X264EncPreset, X264EncPreset | str | int]  # 기본값: medium
    psy_tune: Prop[X264EncPsyTune, X264EncPsyTune | str | int]  # 기본값: none
    tune: Prop[X264EncTune, X264EncTune | str | int]  # 기본값: 0
    frame_packing: Prop[X264EncFramePacking, X264EncFramePacking | str | int]  # 기본값: auto
    insert_vui: bool  # 기본값: True

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        threads: int = ...,
        sliced_threads: bool = ...,
        sync_lookahead: int = ...,
        pass_: X264EncPass | str | int = ...,
        quantizer: int = ...,
        multipass_cache_file: str | None = ...,
        byte_stream: bool = ...,
        bitrate: int = ...,
        intra_refresh: bool = ...,
        vbv_buf_capacity: int = ...,
        me: X264EncMe | str | int = ...,
        subme: int = ...,
        analyse: X264EncAnalyse | str | int = ...,
        dct8x8: bool = ...,
        ref: int = ...,
        bframes: int = ...,
        b_adapt: bool = ...,
        b_pyramid: bool = ...,
        weightb: bool = ...,
        sps_id: int = ...,
        aud: bool = ...,
        trellis: bool = ...,
        key_int_max: int = ...,
        cabac: bool = ...,
        qp_min: int = ...,
        qp_max: int = ...,
        qp_step: int = ...,
        ip_factor: float = ...,
        pb_factor: float = ...,
        mb_tree: bool = ...,
        rc_lookahead: int = ...,
        noise_reduction: int = ...,
        interlaced: bool = ...,
        option_string: str | None = ...,
        speed_preset: X264EncPreset | str | int = ...,
        psy_tune: X264EncPsyTune | str | int = ...,
        tune: X264EncTune | str | int = ...,
        frame_packing: X264EncFramePacking | str | int = ...,
        insert_vui: bool = ...,
    ) -> None: ...

class X265Enc(Element):
    """x265enc — x265enc

    klass: Codec/Encoder/Video
    pads: src src (always), sink sink (always)
    """
    FACTORY: ClassVar[str]  # "x265enc"
    LogLevel = X265LogLevel
    SpeedPreset = X265SpeedPreset
    Tune = X265Tune
    qos: bool  # 기본값: False
    min_force_key_unit_interval: int  # 기본값: 0
    bitrate: int  # 기본값: 2048
    qp: int  # 기본값: -1
    option_string: str | None  # 기본값: ''
    log_level: Prop[X265LogLevel, X265LogLevel | str | int]  # 기본값: none
    speed_preset: Prop[X265SpeedPreset, X265SpeedPreset | str | int]  # 기본값: medium
    tune: Prop[X265Tune, X265Tune | str | int]  # 기본값: ssim
    key_int_max: int  # 기본값: 0

    def __init__(
        self,
        *,
        name: str | None = ...,
        qos: bool = ...,
        min_force_key_unit_interval: int = ...,
        bitrate: int = ...,
        qp: int = ...,
        option_string: str | None = ...,
        log_level: X265LogLevel | str | int = ...,
        speed_preset: X265SpeedPreset | str | int = ...,
        tune: X265Tune | str | int = ...,
        key_int_max: int = ...,
    ) -> None: ...

class XvImageSink(Element):
    """xvimagesink — Video sink

    klass: Sink/Video
    pads: sink sink (always)
    """
    FACTORY: ClassVar[str]  # "xvimagesink"
    sync: bool  # 기본값: True
    max_lateness: int  # 기본값: -1
    qos: bool  # 기본값: False
    async_: bool  # 기본값: True
    ts_offset: int  # 기본값: 0
    enable_last_sample: bool  # 기본값: True
    last_sample: Any
    blocksize: int  # 기본값: 4096
    render_delay: int  # 기본값: 0
    throttle_time: int  # 기본값: 0
    max_bitrate: int  # 기본값: 0
    processing_deadline: int  # 기본값: 20000000
    stats: dict[str, Any] | str
    show_preroll_frame: bool  # 기본값: True
    contrast: int  # 기본값: 0
    brightness: int  # 기본값: 0
    hue: int  # 기본값: 0
    saturation: int  # 기본값: 0
    display: str | None
    synchronous: bool  # 기본값: False
    pixel_aspect_ratio: str | None  # 기본값: '1/1'
    force_aspect_ratio: bool  # 기본값: True
    handle_events: bool  # 기본값: True
    device: str | None  # 기본값: '0'
    device_name: str | None
    handle_expose: bool  # 기본값: True
    double_buffer: bool  # 기본값: True
    autopaint_colorkey: bool  # 기본값: True
    colorkey: int  # 기본값: 0
    draw_borders: bool  # 기본값: True
    window_width: int  # 기본값: 0
    window_height: int  # 기본값: 0
    render_rectangle: Any

    def __init__(
        self,
        *,
        name: str | None = ...,
        sync: bool = ...,
        max_lateness: int = ...,
        qos: bool = ...,
        async_: bool = ...,
        ts_offset: int = ...,
        enable_last_sample: bool = ...,
        blocksize: int = ...,
        render_delay: int = ...,
        throttle_time: int = ...,
        max_bitrate: int = ...,
        processing_deadline: int = ...,
        show_preroll_frame: bool = ...,
        contrast: int = ...,
        brightness: int = ...,
        hue: int = ...,
        saturation: int = ...,
        display: str | None = ...,
        synchronous: bool = ...,
        pixel_aspect_ratio: str | None = ...,
        force_aspect_ratio: bool = ...,
        handle_events: bool = ...,
        device: str | None = ...,
        handle_expose: bool = ...,
        double_buffer: bool = ...,
        autopaint_colorkey: bool = ...,
        colorkey: int = ...,
        draw_borders: bool = ...,
        render_rectangle: Any = ...,
    ) -> None: ...
