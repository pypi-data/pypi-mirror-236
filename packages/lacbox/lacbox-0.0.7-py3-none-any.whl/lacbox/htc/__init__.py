from pathlib import Path
import random
import shutil

import numpy as np

from .htc_file import HTCFile


def make_steady(htc_path, wsps, tilt=None, basename=None,
                htc_dir='./htc_steady/', clean_htc=False, time_start=200, time_stop=400,
                modelpath=None, res_dir='./res_steady/', subfolder='', rigid=False,
                withdrag=True):
    """HTC files with steady wind, no shear, and no tower shadow from turb or step-wind base.
    Saves to folder that can be overwritten.
    
    Parameters
    ----------
    htc_path : str or pathlib.Path
        Path to base (turbulent) htc file. NOTE!!! This base file must be a turbulent
        file, not a step-wind or HAWCStab2 file.
    wsps : iterable
        List of wind speeds to simulate.
    tilt : int or float, optional
        Tilt angle in degrees. Use `None` to keep tilt angle unchanged. The default is
        `None`.
    basename : str, optional
        Base name for the htc files to be saved. The created htc files are named
        $BASENAME_XX.X.htc, where the Xs are the wind speed. The default basename is
        None, which means the basename is the same name as the master file.
    htc_dir : str or pathlib.Path, optional
        Relative path to directory to which we should save the htc files. Folder will be
        created if it doesn't exist or deleted and recreated if it does. The default is
        "./htc_steady/".
    clean_htc : boolean, optional
        Whether to delete all files in `htc_dir` if the folder exists. The default is
        False.
    time_start : int or float, optional
        Time to start recording output. The default is 200.
    time_stop : int or float, optional
        End of simulation time. The default is 400.
    modelpath : str or pathlib.Path, optional
        Relative path from htc file to model folder, passed into HTCFile. The default is
        None.
    res_dir : str or pathlib.Path, optional
        Name of folder to specify in output file path. HAWC2 results files will be saved
        as $RES_DIR/$FILENAME. Passed into HTCFile.set_name/(). Default is 
        `'./res_steady/`.
    subfolder : str, optional
        Subfolder to which log/res files should be saved, passed into
        `HTCFile.set_name()`. The default is `''` (no subfolder).
    rigid : boolean, optional
        Whether the tower/blades should be flexible or rigid. Default is false (flexible).
    withdrag : boolean, optional
        Whether aerodynamic drag should be included in the simulation. Default is True.
    """
    # sanitize inputs
    htc_path = Path(htc_path)
    htc_dir = Path(htc_dir)
    # define intermediate variables
    if basename is None:
        basename = htc_path.stem  # name of master file w/o extension
    # clear or create the htc directory
    _clean_directory(htc_dir, clean_htc)
    # load the master htc file
    htc = HTCFile(htc_path, modelpath=modelpath)
    # set important values true for all htc files
    htc.set_time(start=time_start, stop=time_stop)  # simulation times
    htc.wind.tint = 0  # no TI
    htc.wind.turb_format = 0  # no turbulence
    htc.wind.tower_shadow_method = 0  # no tower shadow
    if type(tilt) in [int, float]:
        shaft_ori = htc.new_htc_structure.orientation.relative__2
        shaft_ori.mbdy2_eulerang__2 = [tilt, 0, 0]
    elif tilt is not None:
        raise ValueError('Keyword argument "tilt" must be None, int or float!')
    if rigid:  # set rigid tower/blades if requested
        htc.new_htc_structure.main_body.timoschenko_input.set = [1, 2]
        htc.new_htc_structure.main_body__7.timoschenko_input.set = [1, 2]
    if not withdrag:
        del htc.aerodrag
    # loop over wind speeds
    for wsp in wsps:
        # define filenames
        fname = basename + '_' + ('%.1f' % (wsp)).zfill(4)  # name of htc file w/o extension
        # set parameters that change with wsp
        htc.wind.wsp = wsp
        htc.wind.shear_format = [1, wsp]
        # set name
        htc.set_name(fname, resdir=res_dir, subfolder=subfolder, htcdir=htc_dir)
        # save file
        htc.save(htc_dir / subfolder / (fname + '.htc'))
    return


def make_turb(htc_path, wsps, turbclass, nseeds=6,
              htc_dir='./htc_turb/', res_dir='./res_turb/', subfolder='',
              basename=None, clean_htc=False,
              modelpath=None, time_start=100, time_stop=700, seed=None):
    """Turbulent wind simulations according to IEC wind class from turb or step-wind base.
    Saves to folder that can be overwritten.

    Parameters
    ----------
    htc_path : str or pathlib.Path
        Path to base (turbulent) htc file. NOTE!!! This base file must be a turbulent
        file, not a step-wind or HAWCStab2 file.
    wsps : iterable
        List of wind speeds to simulate.
    turbclass : str
        IEC turbulence class. Should be "a", "b", or "c" (case-insensitive).
    nseeds : int, optional
        Number of random seeds at each wind speed. The default is 6.
    htc_dir : str or pathlib.Path, optional
        Relative path to directory to which we should save the htc files. Folder will be
        created if it doesn't exist or deleted and recreated if it does. The default is
        "./htc_turb/".
    res_dir : str or pathlib.Path, optional
        Name of folder to specify in output file path. HAWC2 results files will be saved
        as $RES_DIR/$FILENAME. Passed into HTCFile.set_name/(). Default is 
        `'./res_turb/`.
    subfolder : str, optional
        Subfolder to which log/res files should be saved, passed into
        `HTCFile.set_name()`. The default is `''` (no subfolder).
    basename : str, optional
        Base name for the htc files to be saved. The created htc files are named
        $BASENAME_XX.X.htc, where the Xs are the wind speed. The default basename is
        None, which means the basename is the same name as the master file.
    clean_htc : boolean, optional
        Whether to delete all files in `htc_dir` if the folder exists. The default is
        False.
    modelpath : str or pathlib.Path, optional
        Relative path from htc file to model folder, passed into HTCFile. The default is
        None.
    time_start : int or float, optional
        Time to start recording output. The default is 100.
    time_stop : int or float, optional
        End of simulation time. The default is 700.
    seed : int, optional
        The random seed to initialize the random-number generator. Useful if you want to
        recreate the same set of wind files as a previous run. The default is None, which
        is new random seeds every time.
    """
    
    # sanitize inputs
    htc_path = Path(htc_path)
    htc_dir = Path(htc_dir)
    # define intermediate variables/constants, initialize random number generator
    if basename is None:
        basename = htc_path.stem  # name of master file w/o extension
    iref = dict(a=0.16, b=0.14, c=0.12)[turbclass.lower()]
    nx = 1024
    random.seed(seed)
    # clear or create the htc directory
    _clean_directory(htc_dir, clean_htc)
    # load the master htc file
    htc = HTCFile(htc_path, modelpath=modelpath)
    # set important values true for all htc files
    htc.set_time(start=time_start, stop=time_stop)  # simulation times
    htc.wind.turb_format = 1  # no turbulence
    htc.wind.tower_shadow_method = 3  # no tower shadow
    htc.wind.shear_format = [3, 0.2]  # power law shear
    # loop over wind speeds
    for wsp in wsps:
        # calculate turbulence intensity and box length
        tint = iref * (0.75 * wsp + 5.6) / wsp
        dx = (time_stop - time_start) * float(wsp) / float(nx)
        # loop over nseeds
        for js in range(nseeds):
            # define seed number and filenames
            seed = random.randrange(int(2**16))
            fname = basename + '_' + ('%.1f' % (wsp)).zfill(4) + ('_%i' % seed)  # name of htc file w/o extension
            # set parameters
            htc.wind.wsp = wsp
            htc.wind.tint = tint
            htc.wind.mann.create_turb_parameters = [29.4, 1.0, 3.9, seed, 0]
            htc.wind.mann.filename_u = f'./turb/{fname}_turb_u.bin'
            htc.wind.mann.filename_v = f'./turb/{fname}_turb_v.bin'
            htc.wind.mann.filename_w = f'./turb/{fname}_turb_w.bin'
            htc.wind.mann.box_dim_u = [nx, dx]
            # set name
            htc.set_name(fname, resdir=res_dir, subfolder=subfolder, htcdir=htc_dir)
            # save file
            htc.save(htc_dir / subfolder / (fname + '.htc'))
    return


def _clean_directory(htc_dir, clean_htc):
    """Clean or create a directory as requested"""
    # sanitize inputs
    htc_dir = Path(htc_dir)
    # if the folder exists but we want a clean run
    if htc_dir.is_dir() and clean_htc:
        print(f'! Folder {htc_dir} exists: deleting contents. !')
        shutil.rmtree(htc_dir) # delete the folder
        htc_dir.mkdir(parents=True)  # make an empty folder
    # if the folder doesn't exists
    elif not htc_dir.is_dir():
        htc_dir.mkdir(parents=True)  # make the folder
    return
