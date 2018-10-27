from colorsafe.constants import MagicByte

from colorsafe import constants
from colorsafe.csdatastructures import ColorChannels
from colorsafe.decoder.csdecoder import DotDecoder, DotByteDecoder, DotRowDecoder
from colorsafe.encoder.csencoder import DotEncoder, DotRowEncoder, DotByteEncoder

# Dot


def test_dot_encode_colordepth1():
    dot = DotEncoder([1])
    assert dot.getChannels() == (1.0, 1.0, 1.0)

    dot = DotEncoder([0])
    assert dot.getChannels() == (0.0, 0.0, 0.0)


def test_dot_encode_colordepth2():
    # White
    dot = DotEncoder([0, 0])
    assert dot.getChannels() == (1.0, 1.0, 1.0)

    # Magenta
    dot = DotEncoder([0, 1])
    assert dot.getChannels() == (1.0, 0.0, 1.0)

    # Cyan
    dot = DotEncoder([1, 0])
    assert dot.getChannels() == (0, 1.0, 1.0)

    # Yellow
    dot = DotEncoder([1, 1])
    assert dot.getChannels() == (1.0, 1.0, 0)

    dot = DotEncoder([1, 1, 0, 0])
    assert dot.getChannels() == (0, 1.0 / 3.0, 1.0 / 3.0)


def test_dot_encode_colordepth3():
    dot = DotEncoder([0, 0, 0])
    assert dot.getChannels() == (0.0, 0.0, 0.0)

    dot = DotEncoder([1, 0, 1])
    assert dot.getChannels() == (1.0, 0.0, 1.0)

    dot = DotEncoder([1, 1, 1])
    assert dot.getChannels() == (1.0, 1.0, 1.0)

    dot = DotEncoder([1, 0, 0, 0, 1, 1])
    assert dot.getChannels() == (85.0 / constants.ColorDepthMax, 0, 1.0)

    dot = DotEncoder([1, 1, 1, 1, 1, 1, 1, 1, 1])
    assert dot.getChannels() == (1.0, 1.0, 1.0)


def test_dot_decode_colordepth1():
    dot = DotDecoder(ColorChannels(1.0, 1.0, 1.0), 1)
    assert dot.bitList == [1]

    dot = DotDecoder(ColorChannels(0.0, 0.0, 0.0), 1)
    assert dot.bitList == [0]

    dot = DotDecoder(ColorChannels(0.25, 0.25, 0.25), 1, 0.5)
    assert dot.bitList == [0]

    dot = DotDecoder(ColorChannels(0.95, 0.95, 0.95), 1, 0.5)
    assert dot.bitList == [1]

    dot = DotDecoder(ColorChannels(0.93, 0.95, 0.91), 1, 0.5)
    assert dot.bitList == [1]

    dot = DotDecoder(ColorChannels(0.05, 0.1, 0.07), 1, 0.5)
    assert dot.bitList == [0]

    dot = DotDecoder(ColorChannels(0.05, 0.0, 0.0), 1, 0.5)
    assert dot.bitList == [0]

    dot = DotDecoder(ColorChannels(1.0, 1.0, 0.9), 1, 0.5)
    assert dot.bitList == [1]


def test_dot_decode_colordepth2():
    dot = DotDecoder(ColorChannels(1.0, 1.0, 1.0), 2)
    assert dot.bitList == [0, 0]

    dot = DotDecoder(ColorChannels(0.0, 1.0, 1.0), 2)
    assert dot.bitList == [1, 0]

    dot = DotDecoder(ColorChannels(1.0, 1.0, 0.0), 2)
    assert dot.bitList == [1, 1]

    dot = DotDecoder(ColorChannels(0, 63.0 / constants.ColorDepthMax, 63.0 / constants.ColorDepthMax), 4)
    assert dot.bitList == [1, 1, 0, 0]


def test_dot_decode_colordepth3():
    dot = DotDecoder(ColorChannels(0, 0, 0), 3)
    assert dot.bitList == [0, 0, 0]

    dot = DotDecoder(ColorChannels(1.0, 0, 1.0), 3)
    assert dot.bitList == [1, 0, 1]

    dot = DotDecoder(ColorChannels(1.0, 1.0, 1.0), 3)
    assert dot.bitList == [1, 1, 1]

    dot = DotDecoder(ColorChannels(1.0 / 3.0, 0.0, 1.0), 6)
    assert dot.bitList == [1, 0, 0, 0, 1, 1]

    dot = DotDecoder(ColorChannels(1.0, 1.0, 1.0), 9)
    assert dot.bitList == [1, 1, 1, 1, 1, 1, 1, 1, 1]

# DotByte


def test_dotByte_encode():
    dotByte = DotByteEncoder([0xFF], 1)
    assert len(dotByte.dots) == constants.ByteSize
    assert dotByte.dots[0].getChannels() == (1.0, 1.0, 1.0)

    dotByte = DotByteEncoder([0xFF, 0xFF], 2)
    assert len(dotByte.dots) == constants.ByteSize
    assert dotByte.dots[0].getChannels() == (1.0, 1.0, 0.0)

    dotByte = DotByteEncoder([0xFF, 0xFF, 0xFF], 3)
    assert len(dotByte.dots) == constants.ByteSize
    assert dotByte.dots[0].getChannels() == (1.0, 1.0, 1.0)

    dotByte = DotByteEncoder([0xFF, 0xFF, 0xFF], 6)
    assert len(dotByte.dots) == constants.ByteSize
    assert dotByte.dots[0].getChannels() == (1.0, 1.0 / 3.0, 0.0)


def test_dotByte_decode():
    c = ColorChannels(1.0, 1.0, 1.0)
    dotByte = DotByteDecoder([c] * constants.ByteSize, 1)
    assert dotByte.bytesList == [0xFF]

    c = ColorChannels(1.0, 1.0, 0.0)
    dotByte = DotByteDecoder([c] * constants.ByteSize, 2)
    assert dotByte.bytesList == [0xFF, 0xFF]

    c = ColorChannels(1.0, 1.0, 1.0)
    dotByte = DotByteDecoder([c] * constants.ByteSize, 3)
    assert dotByte.bytesList == [0xFF, 0xFF, 0xFF]

    c = ColorChannels(1.0, 1.0 / 3.0, 0.0)
    dotByte = DotByteDecoder([c] * constants.ByteSize, 6)
    assert dotByte.bytesList == [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00]

    c = [
        ColorChannels(0, 0, 0),
        ColorChannels(0, 0, 0),
        ColorChannels(1, 1, 1),
        ColorChannels(1, 1, 1),
    ]
    dotByte = DotByteDecoder(c * 2, 1)
    assert dotByte.bytesList == [0b11001100]

    # Blurred image
    c = [
        ColorChannels(0.05, 0.05, 0.05),
        ColorChannels(0.05, 0.05, 0.05),
        ColorChannels(0.95, 0.95, 0.95),
        ColorChannels(0.95, 0.95, 0.95),
    ]
    dotByte = DotByteDecoder(c * 2, 1)
    assert dotByte.bytesList == [255]

# DotRow


def test_dotRow_encode():
    dotRow = DotRowEncoder([85, 170, 85, 170], 2, 16, 0, False)
    assert dotRow.dotBytes[0].dots[0].getChannels() == (0.0, 1.0, 1.0)

    dotRow = DotRowEncoder([85, 170, 85, 170], 2, 16, 0, True)
    assert dotRow.dotBytes[0].dots[0].getChannels() == (1.0, 0.0, 1.0)


def test_dotRow_decode():
    c = ColorChannels(1.0, 0.0, 1.0)
    dotRow = DotRowDecoder([c] * 16, 2, 16, 0.5, False)
    assert dotRow.bytesList == [170, 85, 170, 85]

    c = ColorChannels(0.9, 0.1, 0.9)
    dotRow = DotRowDecoder([c] * 16, 2, 16, 0.5, False)
    assert dotRow.bytesList == [170, 85, 170, 85]

    c = [
        ColorChannels(0.0, 0.0, 0.0),
        ColorChannels(0.0, 0.0, 0.0),
        ColorChannels(1.0, 1.0, 1.0),
        ColorChannels(1.0, 1.0, 1.0),
    ]
    dotRow = DotRowDecoder(c * 4, 1, 16, 0.5, False)
    assert dotRow.bytesList == [102, 102]

    # Randomly blurred image
    c = [
        ColorChannels(0.05, 0.1, 0.07),
        ColorChannels(0.05, 0.0, 0.0),
        ColorChannels(1.0, 1.0, 0.9),
        ColorChannels(0.93, 0.95, 0.91),
    ]
    dotRow = DotRowDecoder(c * 4, 1, 16, 0.5, False)
    assert dotRow.bytesList == [85, 85]
