import numpy as np
from hyperspy.components1d import Gaussian
import fpd_data_processing.make_diffraction_test_data as mdtd
from fpd_data_processing.pixelated_stem_class import DPCSignal2D


def get_disk_shift_simple_test_signal():
    """Get HyperSpy 2D signal with 2D navigation dimensions for DPC testing.

    Probe size x/y (20, 20), and image size x/y (50, 50).
    Disk moves from 22-28 x/y.
    """
    disk_x, disk_y = np.mgrid[22:28:20j, 22:28:20j]
    s = mdtd.generate_4d_data(
            probe_size_x=20, probe_size_y=20,
            image_size_x=50, image_size_y=50,
            disk_x=disk_x, disk_y=disk_y, disk_r=2,
            ring_x=None, add_noise=True)
    return(s)


def get_holz_simple_test_signal():
    """Get HyperSpy 2D signal with 2D navigation dimensions for HOLZ testing.

    Probe size x/y (20, 20), and image size x/y (50, 50).
    Contains a disk and a ring. The disk stays at x, y = 25, 25, with radius 2.
    The ring has a radius of 20, and moves from x, y = 24-26, 24-26.
    """
    ring_x, ring_y = np.mgrid[24:26:20j, 24:26:20j]
    s = mdtd.generate_4d_data(
            probe_size_x=20, probe_size_y=20,
            image_size_x=50, image_size_y=50,
            disk_x=25, disk_y=25, disk_r=2, disk_I=20,
            ring_x=ring_x, ring_y=ring_y, ring_r=15, ring_I=10,
            add_noise=True)
    return(s)


def get_holz_heterostructure_test_signal():
    """Get HyperSpy 2D signal with 2D navigation dimensions for HOLZ testing.

    The centre, radius and intensity of the ring varies as a function of probe
    position. The disk centre position varies as a function of probe position.

    Returns
    -------
    holz_signal : HyperSpy 2D signal

    Example
    -------
    >>> import fpd_data_processing.api as fp
    >>> s = fp.dummy_data.get_holz_heterostructure_test_signal()
    >>> s.plot()

    """
    probe_size_x, probe_size_y = 40, 40
    px, py = np.mgrid[0:probe_size_x:1, 0:probe_size_y:1]
    x, y = np.mgrid[36:38:40j, 41:43:40j]
    disk_r = 10
    disk_I = np.ones_like(x)*100 + np.random.random()*20
    g_r = Gaussian(A=20, centre=25, sigma=5)
    ring_r = np.ones_like(x)*30 + g_r.function(py)
    g_I = Gaussian(A=30, centre=25, sigma=3)
    ring_I = np.ones_like(x)*20 + g_I.function(py)
    s = mdtd.generate_4d_data(
            probe_size_x=probe_size_x, probe_size_y=probe_size_y,
            image_size_x=80, image_size_y=80,
            disk_x=x, disk_y=y, disk_r=disk_r, disk_I=disk_I,
            ring_x=x, ring_y=y, ring_r=ring_r, ring_I=ring_I,
            add_noise=True)
    return(s)


def get_single_ring_diffraction_signal():
    """Get HyperSpy 2D signal with a single ring with centre position.

    The ring has a centre at x=105 and y=67, and radius=40.
    """
    data = mdtd.MakeTestData(size_x=200, size_y=150, default=False, blur=True)
    x, y = 105, 67
    data.add_ring(x, y, r=40)
    s = data.signal
    s.axes_manager[0].offset, s.axes_manager[1].offset = -x, -y
    return(s)


def get_simple_dpc_signal():
    """Get a simple DPCSignal2D with a zero point in the centre.

    Example
    -------
    >>> import fpd_data_processing.api as fp
    >>> s = fp.dummy_data.get_simple_dpc_signal()

    """
    data = np.mgrid[-5:5:100j, -5:5:100j]
    s = DPCSignal2D(data)
    return s


def get_stripe_pattern_dpc_signal():
    """Get a 2D DPC signal with a stripe pattern.

    The stripe pattern only has an x-component, with alternating left/right
    directions. There is a small a net moment in the positive x-direction
    (leftwards).

    Returns
    -------
    stripe_dpc_signal : DPCSignal2D

    Example
    -------
    >>> import fpd_data_processing.api as fp
    >>> s = fp.dummy_data.get_stripe_pattern_dpc_signal()

    """
    data = np.zeros((2, 100, 50))
    for i in range(10, 90, 20):
        data[0, i:i+10, 10:40] = 1.1
        data[0, i+10:i+20, 10:40] = -1
    s = DPCSignal2D(data)
    return s
