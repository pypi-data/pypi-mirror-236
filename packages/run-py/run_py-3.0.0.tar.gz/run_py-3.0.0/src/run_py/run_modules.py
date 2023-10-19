"""

    """

import re
import runpy
import shutil
from pathlib import Path

from githubdata import default_githubdata_dir as gd_default

class DefaultDirs :
    def __init__(self , make_default_dirs: bool = False) :
        self.t = Path('temp_data/')
        self.gd = gd_default

        if make_default_dirs :
            self.t.mkdir(exist_ok = True)
            self.gd.mkdir(exist_ok = True)

def run_modules(modules_dir: Path | str = Path.cwd()) -> None :
    """
    runs all modules in the modules directory that start with '_' in the order of the number after '_'.
    """

    ms = get_modules_to_run_fps(modules_dir)

    print(f'\n\t*** Number of Modules to run: {len(ms)} ***\n')
    print('\n\t*** Running The Following Modules In Order: ***\n')
    _ = [print('\t\t' , m.name) for m in ms]

    # run modules in order
    for m in ms :
        print('\n\t*** Running The Module \"{}\" ***\n'.format(m.name))

        runpy.run_path(str(m) , run_name = '__main__')

        print('\n\t*** The Module \"{}\" Done! ***\n'.format(m.name))

def get_modules_to_run_fps(modules_dir: Path | str) -> list[Path] :
    """
    finds all .py files in the modules_dir that start with '_' and sorts them based on the number after '_'. Returns a list of these files pathes.

    This is the convention I use to specify modules to run in order. The number after '_' is used to specify the order. There might be other modules in the same dir that are not prefixed with '_' and they will not be run. There are auxiliary modules.
    """

    # get all .py files in modules_dir
    pys = Path(modules_dir).glob('*.py')

    # filter those that start with '_'
    ms = [x for x in pys if re.fullmatch(r'm\d_.+\.py' , x.name)]

    # sort .py files them based on the number after _
    ms = sorted(ms)

    return ms

def rm_cache_dirs(inculding_set: set[Path] = None ,
                  excluding_set: set[Path] = None ,
                  inculde_defaults: bool = True
                  ) -> None :
    """
    removes cache dirs:
    some defaults + some to include - some to exculde

    include_defaults: whether to include defaults
    """

    # default args values
    if excluding_set is None :
        excluding_set = {}
    if inculding_set is None :
        inculding_set = {}

    # inculde default dirs
    if inculde_defaults :
        dd = DefaultDirs()
        dyrs = {dd.gd , dd.t}
    else :
        dyrs = {}

    # include & exclude manually
    dyrs = dyrs.union(inculding_set)
    dyrs = dyrs.difference(excluding_set)

    print('Removing Cache Dirs: ' , dyrs)

    for di in dyrs :
        shutil.rmtree(di , ignore_errors = True)

    print('All Specified Cache Dirs Got Removed.')
