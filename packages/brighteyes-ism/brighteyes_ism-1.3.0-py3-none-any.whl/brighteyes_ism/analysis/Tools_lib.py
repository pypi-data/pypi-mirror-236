import numpy as np

from .FRC_lib import radial_profile

def sigmoid(R: float, T: float, S: float):
    '''
    It generates a circularly-symmetric sigmoid function.

    Parameters
    ----------
    R : float
        Radial axis.
    T : float
        Cut-off frequency.
    S : float
        Sigmoid slope.

    Returns
    -------
    np.ndarray
        Sigmoid array. It has the same dimensions of R.

    '''

    return 1 / (1 + np.exp((R - T) / S))


def low_pass(img: np.ndarray, T: float, S: float, data: str = 'real'):
    '''
    It applies a low-pass sigmoidal filter to a 2D image.

    Parameters
    ----------
    img : np.ndarray
        2D image.
    T : float
        Cut-off frequency.
    S : float
        Sigmoid slope.
    data : str, optional
        Domain of the image: It can be 'real' or 'fourier'.
        The default is 'real'.

    Returns
    -------
    img_filt : np.ndarray
        Filtered 2D image, in the domain specified by 'data'.

    '''

    if data == 'real':
        img_fft = np.fft.fftn(img, axes=(0, 1))
        img_fft = np.fft.fftshift(img_fft, axes=(0, 1))
    elif data == 'fourier':
        img_fft = img
    else:
        raise ValueError('data has to be \'real\' or \'fourier\'')

    Nx = np.shape(img_fft)[0]
    Ny = np.shape(img_fft)[1]
    cx = int((Nx + np.mod(Nx, 2)) / 2)
    cy = int((Ny + np.mod(Ny, 2)) / 2)

    x = (np.arange(Nx) - cx) / Nx
    y = (np.arange(Ny) - cy) / Ny

    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X ** 2 + Y ** 2)

    sig = sigmoid(R, T, S)

    img_filt = np.einsum('ij..., ij -> ij...', img_fft, sig)

    if data == 'real':
        img_filt = np.fft.ifftshift(img_filt, axes=(0, 1))
        img_filt = np.fft.ifftn(img_filt, axes=(0, 1))
        img_filt = np.abs(img_filt)

    return img_filt


# %%

def Reorder(dset, inOrder: str, outOrder: str = 'rzxytc'):
    '''
    It reorders a dataset to match the desired order of dimensions.
    If some dimensions are missing, it adds new dimensions.

    Parameters
    ----------
    dset : ndarray
        ISM dataset.
    inOrder : str
        Order of the dimension of the data.
        It can contain any letter of the outOrder string.
    outOrder : str, optional
        Order of the output. The default is 'rzxytc'.

    Returns
    -------
    data : ndarray
        ISM dataset reordered.

    '''

    data = dset.copy()

    Nout = len(outOrder)
    Ndim = len(inOrder)

    if (Ndim < Nout):
        # check where the current dimensions are located
        idx = np.empty( Nout )
        for n, c in enumerate(outOrder):
            idx[n] = np.char.find(inOrder, c)
        idx = idx.astype('int')

        # add missing dimensions
        slices = []
        for i in idx:
            if i == -1:
                slices.append(np.newaxis)
            else:
                slices.append(np.s_[:])

        slices = tuple(slices)
        data = data[slices]

        # reorder final dimensions
        idx2 = np.empty( Ndim )
        for n, c in enumerate(inOrder):
            idx2[n] = np.char.find(outOrder, c)
        idx2 = idx2.astype('int')

        order = idx.copy()
        order[np.where(idx != -1)] = idx2
        order[np.where(idx == -1)] = np.argwhere(idx == -1).flatten()

        data = np.moveaxis(data, np.arange(Nout), order)

    else:
        # check where the dimensions are located
        idx = np.empty( Ndim )
        for n, c in enumerate(inOrder):
            idx[n] = np.char.find(outOrder, c)
        idx = idx.astype('int')

        # remove undesired dimensions
        slices = []
        for i in idx:
            if i == -1:
                slices.append(np.s_[0])
            else:
                slices.append(np.s_[:])

        slices = tuple(slices)
        data = data[slices]

        # reorder remaining dimensions
        order = idx[idx != -1]
        data = np.moveaxis(data, np.arange(Nout), order)

    return data


def CropEdge(dset, npx=10, edges='l', order: str = 'rzxytc'):
    '''
    It crops an ISM dataset along the specified edges of the xy plane.
    
    Parameters
    ----------
    dset : ndarray
        ISM dataset
    npx : int, optional
        Number of pixel to crop from each edge. The default is 10.
    edges : str, optional
        Cropped edges. The possible values are 'l' (left),'r' (right),
        'u' (up), and 'd' (down). Any combination is possible. The default is 'l'.
    order : str, optional
        Order of the dimensions of the dataset The default is 'rzxytc'.

    Returns
    -------
    dset_cropped : ndarray
        ISM dataset cropped

    '''

    default_order = 'rzxytc'

    dset_cropped = Reorder(dset, inOrder = order, outOrder = default_order)

    if 'l' in edges:
        dset_cropped = dset_cropped[..., npx:, :, :, :]

    if 'r' in edges:
        dset_cropped = dset_cropped[..., :-npx, :, :, :]

    if 'u' in edges:
        dset_cropped = dset_cropped[..., :, npx:, :, :]

    if 'd' in edges:
        dset_cropped = dset_cropped[..., :, :-npx, :, :]

    return Reorder(dset_cropped, inOrder = default_order, outOrder = order)


def DownSample(dset, ds: int = 2, order: str = 'rzxytc'):
    '''
    It downsamples an ISM dataset on the xy plane.
    
    Parameters
    ----------
    dset : ndarray
        ISM dataset.
    ds : int, optional
        Downsampling factor. The default is 2.
    order : str, optional
        Order of the dimensions of the dataset The default is 'rzxytc'.
        
    Returns
    -------
    dset_ds : ndarray
        ISM dataset downsampled.

    '''

    default_order = 'rzxytc'

    dset = Reorder(dset, inOrder = order, outOrder = default_order)

    dset_ds = dset[..., ::ds, ::ds, :, :]

    return Reorder(dset_ds, inOrder = default_order, outOrder = order)


def UpSample(dset, us: int = 2, npx: str = 'even', order: str = 'rzxytc'):
    '''
    It upsamples an ISM dataset on the xy plane.

    Parameters
    ----------
    dset : TYPE
        ISM dataset.
    us : int, optional
        Upsampling factor. The default is 2.. The default is 2.
    npx : str, optional
        Parity of the number of pixels on each axis. The default is 'even'.
    order : str, optional
        Order of the dimensions of the dataset The default is 'rzxytc'.

    Returns
    -------
    dset_us : ndarray
        ISM dataset upsampled.

    '''

    default_order = 'rzxytc'

    dset = Reorder(dset, inOrder = order, outOrder = default_order)

    sz = dset.shape

    if npx == 'even':
        sz_us = np.asarray(sz)
        sz_us[2] = sz_us[2] * us
        sz_us[3] = sz_us[3] * us
    elif npx == 'odd':
        sz_us = np.asarray(sz)
        sz_us[2] = sz_us[2] * us - 1
        sz_us[3] = sz_us[3] * us - 1

    dset_us = np.zeros(sz_us)
    dset_us[..., ::us, ::us, :, :] = dset

    return Reorder(dset_us, inOrder = default_order, outOrder = order)


def ArgMaxND(data):
    '''
    It finds the the maximum and the corresponding indeces of a N-dimensional array.

    Parameters
    ----------
    data : ndarray
        N-dimensional array.

    Returns
    -------
    arg : ndarray(int)
        indeces of the maximum.
    mx : float
        maximum value.

    '''

    idx = np.argmax(data)

    mx = np.array(data).ravel()[idx]

    arg = np.unravel_index(idx, np.array(data).shape)

    return arg, mx


def FWHM(x, y):
    '''
    It calculates the Full Width at Half Maximum of a 1D curve.

    Parameters
    ----------
    x : ndarray
        Horizontal axis.
    y : ndarray
        Curve.

    Returns
    -------
    FWHM: float
        Full Width at Half Maximum of the y curve.

    '''

    height = 0.5
    height_half_max = np.max(y) * height
    index_max = np.argmax(y)
    x_low = np.interp(height_half_max, y[:index_max], x[:index_max])
    x_high = np.interp(height_half_max, np.flip(y[index_max:]), np.flip(x[index_max:]))

    return x_high - x_low


def RadialSpectrum(img, pxsize: float = 1, normalize: bool = True):
    '''
    It calculates the radial spectrum of a 2D image.

    Parameters
    ----------
    img : ndarray
        2D image.
    pxsize : float, optional
        Pixel size. The default is 1.
    normalize : bool, optional
        If True, the result is divided by its maximum. The default is True.

    Returns
    -------
    ftR : ndarray
        Radial spectrum.
    space_f : ndarray
        Frequency axis.

    '''

    fft_img = np.fft.fftn(img, axes=[0, 1])
    fft_img = np.abs(np.fft.fftshift(fft_img, axes=[0, 1]))

    sx, sy = fft_img.shape
    c = (sx // 2, sy // 2)

    space_f = np.fft.fftfreq(sx, pxsize)[:c[0]]

    ftR = radial_profile(fft_img, c)

    ftR = ftR[0][:c[0]] / ftR[1][:c[0]]

    ftR = np.real(ftR)

    if normalize == True:
        ftR /= np.max(ftR)

    return ftR, space_f


def fingerprint(dset, volumetric=False):
    """
    Calculate the fingerprint of an ISM dataset.
    The last dimension has to be the spad array channel.

    Parameters
    ----------
    dset : np.array(Nz x Nx x Nx x ... x N*N)
        ISM dataset
    volumetric : bool
        if true, a fingerprint is returned for each axial plane

    Returns
    -------
    Fingerprint : np.array(Nz x N x N)
        Finger print

    """

    N = int(np.sqrt(dset.shape[-1]))

    if volumetric == True:
        Nz = dset.shape[0]
        f = np.empty((Nz, N * N))
        axis = tuple(range(1, dset.ndim - 1))
        f = np.sum(dset, axis=axis)
        f = f.reshape(Nz, N, N)
    else:
        axis = tuple(range(dset.ndim - 1))
        f = np.sum(dset, axis=axis)
        f = f.reshape(N, N)
    return f

def point_cloud_from_img(dset):
    """
    Transform the image (or stack of images) into a point cloud matrix.
    The matrix

    Parameters
    ----------
    dset : np.ndarray
        Image (Nz x Ny x Nx)

    Returns
    -------
    point_cloud_matrix : np.ndarray
        Point cloud matrix (Nz*Ny*Nx x 4)

    """
    shape = dset.shape

    N = dset.size

    indices = np.array(np.unravel_index(range(N), shape)).T

    values = dset.flatten()

    point_cloud_matrix = np.column_stack((indices, values))

    return point_cloud_matrix