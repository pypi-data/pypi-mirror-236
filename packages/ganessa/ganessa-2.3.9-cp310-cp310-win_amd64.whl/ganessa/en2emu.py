"""

 Epanet compatibility functions with ganessa.sim and other useful methods
    by Dr. Pierre Antoine Jarrige

  1.00 - 2020.06.19 creation
  2.00 - 2023.09.28 extension with (owa-)epanet22: _emu_object = ENmodel() use default project
  2.01 - 2023.10.17 further extensions
"""

__version__ = '2.01'

from typing import Tuple, Union
import os.path as OP
from collections import defaultdict
import atexit
from numbers import Number
import re
import numpy as np
from ganessa import __version__ as _version
from ganessa.util import ws, tostr, hhmmss, strf3, X64


#****g* ganessa.epanet2/About
# PURPOSE
#   The module ganessa.epanet2 provides epanettools API for epanet 2.00.12.
#   It is a copy of epanettools 0.4.3, with minor fixes.
#****
#****g* ganessa.epanet22/About
# PURPOSE
#   The module ganessa.epanet22 provides epanettools API for epanet 2.2,
#   similar to Epanet 2.0 (legacy API to a single project).
#****
#****g* ganessa.owa_epanet22/About
# PURPOSE
#   The module ganessa.owa_epanet22 provides epanettools compatibility for owa-epanet
#   package, in the sense it hides the Epanet 2.2 project argument by using a
#   default single project, but allow to close / create that project for multiprocessing.
# HISTORY
#   * 2020-09-21: creation
#****
#****g* ganessa.en2emu/About
# PURPOSE
#   The module ganessa.en2emu provides compatibility for a limited set of functions
#   used by Ganessa tools, such as OpenFileMMI.SelectModel. It makes use of owa_epanet22
#   if owa-epanet is installed, otherwise it uses epanet22 legacy, limited API.
#
#   It creates a hidden _emu_object object handler for the current model, caching pipes,
#   tanks, hydaulic EPS results, pressure and flow unit and coefficients etc.
# HISTORY
#   * 2020-06-19: creation / interface with epanettools (epanet 2.0)
#   * 2023-10-17: extension with owa-epanet (epanet 2.2) and epanet22
#****

def ENretval_skip_retcode(args):
    """remove return errcode"""
    return args if isinstance(args, (str, bytes)) else (args[1] if len(args) == 2  else args[1:])

def ENretval_as_is(args):
    """keep as is"""
    return args

try:
    from ganessa import owa_epanet22 as et
    epanet_source = "owa-epanet " + et.__version__
    ENretval = ENretval_as_is
    is_owa_epanet = True
except ImportError:
    print("owa-epanet not found: using ganessa.epanet implementation")
    epanet_source = "custom epanettools integrated into ganessa"
    ENretval = ENretval_skip_retcode
    is_owa_epanet = False
    try:
        from ganessa import epanet22 as et
    except ImportError:
        from ganessa import epanet2 as et

_ENversion = ENretval(et.ENgetversion())
epanet_version = f"{_ENversion//10000}.{(_ENversion % 10000) // 100}"
print("\tEpanet version is:", epanet_version, f"(from {epanet_source})")


LINK = BRANCH = ARC = 1
NODE = NOEUD = 2
TANK = RESERVOIR = RSV = 3

_emu_folder = None
_emu_object = None
_fresult = ''
_debug = False


PIC2EPA_LINK_ATTRS = {"Q": et.EN_FLOW,
                      "V": et.EN_VELOCITY,
                      "L": et.EN_LENGTH,
                      "D": et.EN_DIAMETER,
                      "R": et.EN_ROUGHNESS,
                      "C": et.EN_ROUGHNESS,
                      "K": et.EN_MINORLOSS,
                      "PC": et.EN_HEADLOSS,
                      "HL": et.EN_HEADLOSS,
                      }
PIC2EPA_NODE_ATTRS = {"P": et.EN_PRESSURE,
                      "CH": et.EN_HEAD,
                      "HH": et.EN_HEAD,
                      "CS": et.EN_BASEDEMAND,
                      "CC": et.EN_DEMAND,
                      "Z": et.EN_ELEVATION,
                      "C1": et.EN_QUALITY,
                      }

class ENmodel:
    """Functions to be called while ENpackage is active i.e. between init and close
    init calls open that call et.ENopen that creates owa-epanet project if needed
    close deletes it"""
    FILE_ENCODING = "utf-8"
    MEM_X32 = 500
    MEM_X64 = 2000
    def __init__(self, fname : str, hnd, debug=False):
        self.err = []
        self.hnd = hnd
        self.debug = debug
        self.filename = fname
        self.tank_index = []
        self.pipe_index = []
        self.errcode = 0
        self.coords = {}
        self.vertices = {}
        self.labels = []
        self.backdrop = []
        self.vertices = defaultdict(list)
        self.open(fname)
        # self.get_coords()
        self.extra_text = []
        self.hydraulic_results = None

    def close(self):
        ''''Terminate'''
        self.tank_index = []
        self.pipe_index = []
        self.hydraulic_results = None
        et.ENclose()
        self.errcode = -1
        if is_owa_epanet:
            return et.ENdeleteproject()

    def save(self, fname : str, append=None) -> bool:
        """Save Epanet model; optionnally appends a section"""
        et.ENsaveinpfile(ws(fname))
        if append is None or not append:
            return True
        # insert "append" before "[END]"
        with open(fname, "r", encoding=self.FILE_ENCODING) as ef:
            content = ef.readlines()
        for k, line in enumerate(content[::-1]):
            if re.search("[END]", line, re.IGNORECASE):
                break
        else:
            return False
        pos = -1 - k
        content[pos:pos] = [line + "\n" for line in append]
        with open(fname, "w", encoding=self.FILE_ENCODING) as ef:
            ef.writelines(content)
        return True

    def save_as(self, fname):
        '''Copy the file with current coords / vertices / labels'''
        # with tempfile.NamedTemporaryFile(delete=False, suffix='.inp') as f:
        #     pass
        # self.save(f.name)
        sections = ('[COORD', '[VERTI', '[LABEL', '[BACKD')
        fcopy = True
        kw = dict(encoding=self.FILE_ENCODING)
        with open(self.filename, "r", **kw) as enfile, open(fname, "w", **kw) as fout:
            for text in self.extra_text:
                fout.write('; ' + text + '\n')
            for unstripped_line in enfile:
                line = unstripped_line.strip()
                if not line:
                    fout.write(unstripped_line)
                    continue
                if line[0] == ';':
                    fout.write(unstripped_line)
                    continue
                if line[0] != '[':
                    if fcopy:
                        fout.write(unstripped_line)
                    continue
                # section change
                fcopy = True
                fout.write(unstripped_line)
                for k, section in enumerate(sections):
                    if line.startswith(section):
                        fcopy = False
                        if k == 0:      # coords
                            for node, coords in self.coords.items():
                                x, y = coords
                                fout.write(f' {node} \t{strf3(x)} \t{strf3(y)}\n')
                        if k == 1:      # vertices
                            for link, points in self.vertices.items():
                                for x, y in points:
                                    fout.write(f' {link} \t{strf3(x)} \t{strf3(y)}\n')
                        if k == 2:      # labels
                            for x, y, label in self.labels:
                                fout.write(f' {strf3(x)} \t{strf3(y)} \t{label}\n')
                        if k == 3:      # backdrop
                            for scmd in self.backdrop:
                                skip = '; ' if scmd.startswith('DIMEN') else ' '
                                fout.write(f'{skip}{scmd}\n')
        # os.remove(f.name)

    def ENerr(self, ret, showerr: bool = False):
        "Error handler"
        val = 0
        if isinstance(ret, (list, tuple)):
            ret, val = ret
        elif ret is None:
            ret = 0
        else:
            val, ret = ret, 0
        if self.errcode == 0:
            self.errcode = ret
        if ret > 0:
            _r, error = et.ENgeterror(ret, 80)
            print(ret, error)
            self.err.append(error)
            # for msg in getENrpt_errors(self.rptd if self.debug else self.rpt):
            #     self.err.append(msg)
            #     if showerr:
            #         print(msg)
        return val

    def open(self, fname: str):
        """Opens Epanet model"""
        base, _ext = OP.splitext(fname)
        # base, ext = OP.splitext(fname)
        self.inp = ws(base + '.inp')
        self.rpt = ws(base + '.rpt')
        self.ENerr(et.ENopen(self.inp, self.rpt, ws("")), True)
        self.update_indexes()

    def update_indexes(self):
        """Update tank_index and pipe_index"""
        if not self.errcode:
            self.tank_index = [ix for ix in range(1, self.nodecount+1)
                               if ENretval(et.ENgetnodetype(ix)) == et.EN_TANK]
            self.pipe_index = [ix for ix in range(1, self.linkcount+1)
                               if ENretval(et.ENgetlinktype(ix)) == et.EN_PIPE]

    @property
    def linkcount(self) -> int:
        """link count"""
        return 0 if self.errcode else ENretval(et.ENgetcount(et.EN_LINKCOUNT))

    @property
    def nodecount(self) -> int:
        """node count"""
        return 0 if self.errcode else ENretval(et.ENgetcount(et.EN_NODECOUNT))

    @property
    def tankcount(self) -> int:
        """tank count"""
        return 0 if self.errcode else len(self.tank_index)

    @property
    def duration(self):
        """Simulation duration"""
        return 0 if self.errcode else ENretval(et.ENgettimeparam(et.EN_DURATION))

    def linknodes(self, link: Union[str, int], qavg:float = 0) -> Tuple[str, str]:
        """Return initial and final node ID in flow direction if given"""
        ix = link if isinstance(link, Number) else ENretval(et.ENgetlinkindex(link))
        if ix <= 0:
            return "", ""
        nix, nfx = ENretval(et.ENgetlinknodes(ix))
        ni = ENretval(et.ENgetnodeid(nix))
        nf = ENretval(et.ENgetnodeid(nfx))
        return (nf, ni) if qavg < 0 else (ni, nf)

    def pexists(self, p: str) -> bool:
        '''Returns the existence of pipe in the model'''
        if self.errcode:
            return 0
        ix = ENretval(et.ENgetlinkindex(p))
        return ix > 0

    def get_coords(self):
        '''Retrieve coords from .inp file - used by ChangeProj'''
        fcoords = fvertices = flabels = fbackdrop = False
        with open(self.filename, 'r', encoding=self.FILE_ENCODING) as enfile:
            for line in enfile:
                line = line.strip()
                if not line:
                    continue
                if line[0] == ';':
                    continue
                if line[0] == '[':
                    fcoords = line.startswith('[COORD')
                    fvertices = line.startswith('[VERTI')
                    flabels = line.startswith('[LABEL')
                    fbackdrop = line.startswith('[BACKD')
                    continue
                if fcoords or fvertices:
                    data = line.split()
                    if len(data) < 3:
                        continue
                    coords = float(data[1]), float(data[2])
                    if fcoords:
                        self.coords[data[0]] = coords
                    else:
                        self.vertices[data[0]].append(coords)
                if flabels:
                    data = line.split(maxsplit=2)
                    self.labels.append((float(data[0]), float(data[1]), data[2]))
                if fbackdrop:
                    self.backdrop.append(line)

    def getENerrmsg(self):
        return self.err

    def flowunitfactor(self) -> float:
        '''Returns a coefficient with respect to m3/s'''
        if self.err:
            return 1.0
        ix = self.ENerr(et.ENgetflowunits())
        qepa = {et.EN_CFS: 0.3048**3,
                et.EN_GPM: 0.003785411784/60.,
                et.EN_MGD: 3785.411784/86400., et.EN_IMGD: 4546.09/86400.,
                et.EN_AFD: 4046.86*0.3048/86400.,
                et.EN_LPS: 0.001, et.EN_LPM: 0.001/60., et.EN_MLD: 1000./86400.,
                et.EN_CMH: 1./3600., et.EN_CMD: 1./86400.}[ix]
        # qpic = float(pic.getvar('unite.Q'))
        return qepa

    def flowunitname(self) -> str:
        '''Returns a coefficient with respect to m3/s'''
        if self.err:
            return "?"
        ix = self.ENerr(et.ENgetflowunits())
        qepa = {et.EN_CFS: "cf/s",
                et.EN_GPM: "gpm",
                et.EN_MGD: "Mg/d", et.EN_IMGD: "iMg/d",
                et.EN_AFD: "afd",
                et.EN_LPS: "l/s", et.EN_LPM: "l/min", et.EN_MLD: "Ml/d",
                et.EN_CMH: "m3/h", et.EN_CMD: "m3/d"}[ix]
        # qpic = float(pic.getvar('unite.Q'))
        return qepa

    def pressureunitfactor(self) -> float:
        """returns a coefficient with respect to mcw"""
        if self.err:
            return 1.0
        ix = self.ENerr(et.ENgetflowunits())
        if ix in (et.EN_CFS, et.EN_GPM, et.EN_AFD, et.EN_MGD, et.EN_IMGD):
            # PSI
            return 0.7031
        return 1

    def pressureunitname(self) -> str:
        """returns a name with respect to mcw"""
        if self.err:
            return 1.0
        ix = self.ENerr(et.ENgetflowunits())
        if ix in (et.EN_CFS, et.EN_GPM, et.EN_AFD, et.EN_MGD, et.EN_IMGD):
            # PSI
            return "psi"
        return "m"

    def get_ENresults_asdict(self):
        '''Runs the simulation and collects all links and nodes results'''
        if self.err:
            return None, None, None, None, []
        linkcount, nodecount = self.linkcount, self.nodecount
        print('Model has', linkcount, 'links and', nodecount, 'nodes.')

        duration = self.ENerr(et.ENgettimeparam(et.EN_DURATION))
        # 8 * nbts * (duration / dt) < 0.5*10**9 -- double avec la transposition !
        dtmin = 8 * (1 + self.nodecount + self.linkcount) * duration / (5*10**8)
        maxsteps = 5*10**8 // (8 * (1 + self.nodecount + self.linkcount))
        print(f'Running simulation over {duration} s and collecting results')
        print(f'Avg sampling interval > {int(dtmin)} s')
        self.ENerr(et.ENopenH(), True)
        # qfact = self.EN2Picunitfactor()
        qfact = 1.0
        tank_index = self.tank_index
        tankcount = len(tank_index)
        mapresults = []
        tstep = 1
        show, stepcount, stepskips, step = 0, 0, 0, duration / 24
        self.ENerr(et.ENinitH(0), True)
        while tstep > 0:
            ret, t = et.ENrunH()
            if ret:
                self.err.append(et.ENgeterror(ret, 80)[1] + ' t=' + hhmmss(t))
            if t >= show:
                txt = f'\t{int(100*show/duration):3d}% - t= {hhmmss(t)}'
                if self.hnd:
                    self.hnd.v3.set(txt)
                    self.hnd.update()
                else:
                    print(txt)
                show += step
            # stepcount < t * maxsteps/duration
            if duration*stepcount <= t*maxsteps:
                stepcount += 1
                # Retrieve hydraulic results for time t
                flow = np.zeros(linkcount+1)
                pres = np.zeros(nodecount+1)
                levl = np.zeros(tankcount)
                for ix in range(1, nodecount+1):
                    _ret, v = et.ENgetnodevalue(ix, et.EN_PRESSURE)
                    pres[ix] = v
                for ix in range(1, linkcount+1):
                    _ret, v = et.ENgetlinkvalue(ix, et.EN_FLOW)
                    flow[ix] = v
                for k, ix in enumerate(tank_index):
                    _ret, v = et.ENgetnodevalue(ix, et.EN_HEAD)
                    levl[k] = v
                mapresults.append((t, flow*qfact, pres, levl))
            else:
                stepskips += 1
            _ret, tstep = et.ENnextH()
        _ret = et.ENcloseH()
        if self.err:
            print('\n'.join(self.err))

        # Transpose results by type and object
        steps = np.array([r[0] for r in mapresults])
        tmp = np.array([r[1] for r in mapresults])
        flows = {et.ENgetlinkid(ix)[1]: tmp[:, ix] for ix in range(1, linkcount+1)}
        tmp = np.array([r[2] for r in mapresults])
        press = {et.ENgetnodeid(ix)[1]: tmp[:, ix] for ix in range(1, nodecount+1)}
        tmp = np.array([r[3] for r in mapresults])
        levls = {et.ENgetnodeid(ix)[1]: tmp[:, k] for k, ix in enumerate(tank_index)}
        print(f'Stored {stepcount} - skipped {stepskips} steps')
        if self.hnd:
            tf = steps[-1]
            txt = 'terminée' if tf >= duration else 'interrompue à ' + hhmmss(tf)
            self.hnd.v3.set('Simulation hydraulique ' + txt)
            self.hnd.update()
        sr = stepcount/float(stepcount + stepskips)
        return (steps, flows, press, levls, mapresults, sr)

    def run_hydraulic_snapshot(self, time: int = 0):
        """Runs a steady-state (snapshot) simulation at given time"""
        et.ENsettimeparam(et.EN_DURATION, 0)
        et.ENsettimeparam(et.EN_PATTERNSTART, time)
        self.ENerr(et.ENopenH(), True)
        self.ENerr(et.ENinitH(0), True)
        et.ENrunH()
        et.ENcloseH()

    def run_hydraulic_eps(self, mem_max=None):
        '''Runs the simulation and collects all links and nodes results'''
        if self.err or self.errcode:
            self.hydraulic_results = None
            return None, None, None, None
        linkcount, nodecount, tankcount = self.linkcount, self.nodecount, self.tankcount
        if self.debug:
            print('Model has', linkcount, 'links and', nodecount, 'nodes.')

        duration = self.duration
        # 8 * nbts * (duration / dt) < 0.5*10**9 -- double avec la transposition !
        if mem_max is None:
            mem_max = self.MEM_X64 if X64 else self.MEM_X32
        mem_max *= 10**6
        dtmin = 8 * (1 + self.nodecount + self.linkcount) * duration / mem_max
        maxsteps = mem_max // (8 * (1 + self.nodecount + self.linkcount))
        if self.debug:
            print(f'Running simulation over {duration} s ({duration//3600} h) and collecting results')
            print(f'Avg sampling interval > {int(dtmin)} s')
        qfact = self.flowunitfactor()
         # rule_step = self.ENerr(et.ENgettimeparam(et.EN_RULESTEP))
        steps = []
        tstep = 1
        # preallocate matrix for handling results by time step
        hyd_step = self.ENerr(et.ENgettimeparam(et.EN_HYDSTEP))
        sz_steps = 3 * (duration // hyd_step) // 2
        if self.debug:
            print(f"Allocating {sz_steps} for expected {duration // hyd_step} hydraulic steps")
        flow = np.zeros((sz_steps, linkcount+1), dtype=np.float32)
        pres = np.zeros((sz_steps, nodecount+1), dtype=np.float32)
        levl = np.zeros((sz_steps, tankcount), dtype=np.float32)
        steps = np.zeros(sz_steps, dtype = np.float32)
        # Prepare and run simulation
        show, stepcount, stepskips, step = 0, 0, 0, duration / (50 if duration > 24 else 24)
        self.ENerr(et.ENopenH(), True)
        self.ENerr(et.ENinitH(0), True)
        while tstep > 0:
            t = et.ENrunH()
            if isinstance(t, (tuple, list)):
                ret, t = t
                if ret:
                    self.err.append(ENretval(et.ENgeterror(ret, 80)) + ' t=' + hhmmss(t))
            if t >= show:
                txt = f'\t{int(100*show/duration):3d}% - t= {hhmmss(t)}'
                if self.hnd:
                    self.hnd.v3.set(txt)
                elif self.debug:
                    print(txt)
                show += step
            if stepcount >= sz_steps:
                # resize if too small
                sz_steps = 5 * int(sz_steps * duration / t) // 4
                if self.debug:
                    print("Resizing result matrix to", sz_steps, "steps at", hhmmss(t))
                flow.resize((sz_steps, linkcount+1), refcheck=False)
                pres.resize((sz_steps, nodecount+1), refcheck=False)
                levl.resize((sz_steps, tankcount), refcheck=False)
                steps.resize(sz_steps, refcheck=False)
            # stepcount < t * maxsteps/duration
            if duration*stepcount <= t*maxsteps:
                # Retrieve hydraulic results for time t
                for ix in range(1, nodecount+1):
                    v = ENretval(et.ENgetnodevalue(ix, et.EN_PRESSURE))
                    pres[stepcount, ix] = v
                for ix in range(1, linkcount+1):
                    v = ENretval(et.ENgetlinkvalue(ix, et.EN_FLOW))
                    flow[stepcount, ix] = v
                for k, ix in enumerate(self.tank_index):
                    v = ENretval(et.ENgetnodevalue(ix, et.EN_HEAD))
                    levl[stepcount, k] = v
                steps[stepcount] = t
                stepcount += 1
            else:
                stepskips += 1
            tstep = ENretval(et.ENnextH())
        #
        et.ENcloseH()
        if self.err:
            if len(self.err) < 128:
                print('\n'.join(self.err))
            else:
                print('\n'.join(self.err[:64]))
                print('\t...')
                print('\n'.join(self.err[-64:]))

        # Transpose results by type and object
        if self.debug:
            print(f"Epanet simulation done ({stepcount} steps - skipped {stepskips})")
        steps.resize(stepcount, refcheck=False)
        flow.resize((stepcount, linkcount+1), refcheck=False)
        pres.resize((stepcount, nodecount+1), refcheck=False)
        levl.resize((stepcount, tankcount), refcheck=False)
        flow *= qfact
        # flows =  {ENretval(et.ENgetlinkid(ix)): flow[:, ix] for ix in range(1, linkcount+1)}
        # press = {ENretval(et.ENgetnodeid(ix)): pres[:, ix] for ix in range(1, nodecount+1)}
        # levls = {ENretval(et.ENgetnodeid(ix)): levl[:, k] for k, ix in enumerate(self.tank_index)}
        tf = steps[-1]
        txt = 'terminée' if tf >= duration else 'interrompue à ' + hhmmss(tf)
        txt = 'Simulation hydraulique ' + txt
        if self.hnd:
            self.hnd.v3.set(txt)
        if self.debug:
            print(txt)
        # Close and reopen to allow further use of ENsolveH
        self.ENerr(et.ENclose())
        self.ENerr(et.ENopen(ws(self.inp), ws(self.rpt), ws("")), True)
        self.hydraulic_results = steps, flow, pres, levl
        return steps, flow, pres, levl

class Elements:
    '''Generic iterator for model elements'''
    def __init__(self, typelt):
        if isinstance(typelt, Number):
            self.type = typelt
            self.nbmax = nbobjects(self.type)
            self.get_id = {LINK: et.ENgetlinkid,
                           NODE: et.ENgetnodeid,
                           TANK: get_tank_id}[typelt]
        self.index = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.index > self.nbmax:
            raise StopIteration
        elem = ENretval(self.get_id(self.index))
        self.index += 1
        return tostr(elem)
    def __len__(self):
        return self.nbmax
    next = __next__
    len = __len__

class Nodes(Elements):
    '''Node iterator'''
    def __init__(self):
        super(Nodes, self).__init__(NODE)

class Links(Elements):
    '''Links iterator'''
    def __init__(self):
        super(Links, self).__init__(LINK)

class Tanks(Elements):
    '''Tanks iterator'''
    def __init__(self):
        super(Tanks, self).__init__(TANK)

class Pipes:
    '''Pipe iterator for model elements - Returns ID or ID, value'''
    def __init__(self, attr: str = None):
        self.nbmax = 0 if _emu_object is None else len(_emu_object.pipe_index)
        self.index = 0
        self.en_attr = None
        if attr is None:
            return
        self.en_attr = PIC2EPA_LINK_ATTRS.get(attr.upper(), et.EN_FLOW)
    def __iter__(self):
        return self
    def __next__(self) -> Union[str, Tuple[str, float]]:
        if self.index >= self.nbmax:
            raise StopIteration
        idx = _emu_object.pipe_index[self.index]
        elem = ENretval(et.ENgetlinkid(idx))
        self.index += 1
        if self.en_attr is None:
            return tostr(elem)
        return tostr(elem), ENretval(et.ENgetlinkvalue(idx, self.en_attr))
    def __len__(self):
        return self.nbmax
    next = __next__
    len = __len__

class GanessaError(Exception):
    '''Error class - may be useless here'''
    def __init__(self, number, reason, text):
        self.number = number
        self.reason = reason
        self.text = tostr(text)
    def __str__(self):
        return __file__ + f' ERROR : ({self.number}) : {self.text}'

def epanet_model():
    """Returns the Epanet model (ENmodel) instance"""
    return _emu_object

def init(folder: str = None, silent: bool = False, debug: bool = False):
    """Emulate Piccolo/Ganessa_SIM init method"""
    global _emu_folder, _emu_object, _debug
    _emu_folder = folder
    _debug = debug
    # this is equivalent to close() - terminate default owa-epanet
    if _emu_object:
        _emu_object.close()
    _emu_object = None

def dll_version():
    return epanet_version

def full_version():
    '''Returns the version of the dll (after init)'''
    ret = f"Epanet {epanet_version} (from {epanet_source}) / (py)ganessa {_version}"
    return ret

def close(*args):
    """Ends Epanet model - kill owa-epanet project"""
    global _emu_object
    if _emu_object:
        _emu_object.close()
    _emu_object = None

atexit.register(close)

def setlang(new_lang):
    return 'en'

def useExceptions(enable=True):
    pass

def reset():
    """fake for Piccolo reset - close/reopen epanet project"""
    try:
        model_file = _emu_object.filename
    except AttributeError:
        model_file = ""
    et.ENclose()
    if model_file:
        cmdfile(model_file)

def cmdfile(fname: str, *args):
    """fake for piccolo cmdfile - Opens Epanet model"""
    global _emu_object
    _emu_object = ENmodel(fname, None, _debug)

def loadbin(fname: str):
    """fake for piccolo loadbin - Opens Epanet model"""
    global _emu_object
    close()
    _emu_object = ENmodel(fname, None, _debug)

def loadres():
    """fake for piccolo loadres - simulate ?"""
    if _emu_object:
        _emu_object.run_hydraulic_eps()
        return 0
    return 1

def runH(time: int = 0) -> int:
    """fake for piccolo solveH - snapshot simulation (Epanet: runH)"""
    if _emu_object:
        _emu_object.run_hydraulic_snapshot(time)
        return 0
    return 1

def clear_err(full=False):
    """Clear errors if any"""
    if _emu_object:
        _emu_object.errcode = 0
        if full:
            _emu_object.err = []
        return 0
    return 1

def cmd(arg):
    """fake for piccolo cmd"""
    print("Ignoring:", arg)
    return 0

def execute(*args):
    """fake for piccolo execute"""
    print("Ignoring execute", len(args), "commands")
    return 0

def save(fname: str):
    """save model as"""
    if _emu_object:
        _emu_object.save_as(fname)

def nbobjects(objtyp: int) -> int:
    """fake for piccolo nbobjects"""
    if _emu_object:
        return {LINK: _emu_object.linkcount,
                NODE: _emu_object.nodecount,
                TANK: _emu_object.tankcount,
                }[objtyp]
    return 0

def nbvertices() -> int:
    return len(_emu_object.vertices) if _emu_object else 0

def selectlen(text: str) -> Tuple[int, int]:
    """Return a count - valid for pipes only"""
    if text.upper() in ("TUYAU", "PIPE"):
        return len(_emu_object.pipe_index), LINK
    if text.upper() in ("TANK", "RESERVOIR") or "RESERVOIR".startswith(text.upper()):
        return len(_emu_object.tank_index), TANK
    return 0, LINK

def savemodel(fname: str):
    """save model"""
    if _emu_object:
        _emu_object.save(fname)

def get_tank_id(idx: int) -> str:
    """Return a tank ID for the current model (index starting at 1)"""
    if _emu_object:
        return ENretval(et.ENgetnodeid(_emu_object.tank_index[idx-1]))
    else:
        return ""

def getid(typelt: int, idx: int) -> str:
    """Return object ID by type (index starting at 1)"""
    if typelt == LINK:
        sid = et.ENgetlinkid(idx)
    elif typelt == NODE:
        sid = et.ENgetnodeid(idx)
    elif _emu_object:
        sid = et.ENgetnodeid(_emu_object.tank_index[idx-1])
    else:
        return ""
    return tostr(ENretval(sid))

def linknodes(link: Union[int, str], flow: float = 0) -> Tuple[str, str]:
    """Return from and to node IDs - link is either an ID or an index"""
    if _emu_object:
        return _emu_object.linknodes(link, flow)
    return "", ""

def nlinkattr(idx: int, attr: str) -> float:
    """fake for piccolo nlinkattr - implemented for a limited set of attributes"""
    et_attr = PIC2EPA_LINK_ATTRS[attr]
    v = ENretval(et.ENgetlinkvalue(idx, et_attr))
    return v

def linkattr(sid: str, attr: str) -> float:
    """fake for piccolo linkattr - implemented for a limited set of attributes"""
    ix = ENretval(et.ENgetlinkindex(sid))
    return nlinkattr(ix, attr)

def getindex(typelt: int, sid: str) -> int:
    """Return object index"""
    try:
        if typelt == LINK:
            idx = ENretval(et.ENgetlinkindex(sid))
        elif typelt == NODE:
            idx = ENretval(et.ENgetnodeindex(sid))
        elif _emu_object:
            idxn = ENretval(et.ENgetnodeindex(sid))
            idx = _emu_object.tank_index.index(idxn) + 1
    except ValueError:
        idx = 0
    return idx

def exists(typelt: int, sid: str) -> bool:
    """Returns true if object exists, false otherwise"""
    return getindex(typelt, sid) > 0

def nnodeattr(idx: int, attr: str) -> float:
    """fake for piccolo nnodeattr - implemented for a limited set of attributes"""
    if attr in ('X', 'Y'):
        nid = ENretval(et.ENgetnodeid(idx))
        try:
            return _emu_object.coords[nid]
        except (AttributeError, KeyError):
            return 0
    et_attr = PIC2EPA_NODE_ATTRS[attr]
    v = ENretval(et.ENgetnodevalue(idx, et_attr))
    return v

def nodeattr(nid: str, attr: str) -> float:
    """fake for piccolo nodeattr - implemented for a limited set of attributes"""
    if attr in ('X', 'Y'):
        try:
            return _emu_object.coords[nid][0 if attr == 'X' else 1]
        except (AttributeError, KeyError):
            return 0
    et_attr = PIC2EPA_NODE_ATTRS[attr]
    idx = ENretval(et.ENgetnodeindex(nid))
    v = ENretval(et.ENgetnodevalue(idx, et_attr))
    return v

def linkXYZV(sid: str, include_nodes: bool = True):
    """fake for piccolo linkXYZV"""
    x, y, z, v, nbp = [], [], [], [], 0
    if not _emu_object:
        return x, y, z, v, nbp
    ix = ENretval(et.ENgetlinkindex(sid))
    xni, xnf = ENretval(et.ENgetlinknodes(ix))
    zi = ENretval(et.ENgetnodevalue(xni, et.EN_ELEVATION))
    zf = ENretval(et.ENgetnodevalue(xnf, et.EN_ELEVATION))
    try:
        vertices = _emu_object.vertices[sid]
    except KeyError:
        if not include_nodes:
            return x, y, z, v, nbp
    else:
        x, y = zip(*vertices) if vertices else ([], [])
        nbp = len(x)
    if include_nodes:
        nbp += 2
    # faux mais bon...
    z = np.linspace(zi, zf, num=nbp)
    v = np.zeros(nbp)
    if include_nodes:
        x[0:0] = nnodeattr(xni, 'X')
        x.append(nnodeattr(xnf, 'X'))
        y[0:0] = nnodeattr(xni, 'Y')
        y.append(nnodeattr(xnf, 'Y'))
    return x, y, z, v, nbp

def getunitcoef(attr : str) -> float:
    """Returns the unit relative to Piccolo reference unit"""
    if attr.upper()[0] == "Q":
        return _emu_object.flowunitfactor()
    if attr.upper()[0] == "P":
        return _emu_object.pressureunitfactor()

def getunitname(attr : str) -> str:
    """Returns the unit name"""
    if attr.upper()[0] == "Q":
        return _emu_object.flowunitname()
    if attr.upper()[0] == "P":
        return _emu_object.pressureunitname()

def getvar(command : str) -> str:
    """fake for piccolo getvar"""
    command = command.upper()
    if m := re.match(r"Q(\d\d):NOEUD\.[XY]", command):
        if not _emu_object.coords:
            _emu_object.get_coords()
        xy = np.array(list(_emu_object.coords.values()))
        percentile = int(m[1])
        values = np.percentile(xy, percentile, axis=0)
        return strf3(values[0 if command[-1] == "X" else 1])
    return "#NAN#"

def get_labels():
    '''Returns the list of (x, y, labels) if any'''
    if not _emu_object:
        return []
    return _emu_object.labels

def set_coordinates(node, x, y):
    '''Resets the node coordinates'''
    if not _emu_object:
        return
    try:
        _emu_object.coords[node] = (x, y)
    except KeyError:
        pass

def set_vertices(link, x, y):
    '''Resets the link vertices'''
    if not _emu_object:
        return
    try:
        _emu_object.vertices[link] = list(zip(x, y))
    except KeyError:
        pass

def clear_labels():
    '''Add a new label'''
    if  _emu_object:
        _emu_object.labels = []

def add_label(x, y, label):
    '''Add a new label'''
    if _emu_object:
        _emu_object.labels.append((x, y, label))

def add_extra_text(text):
    '''Add a new comment'''
    if _emu_object:
        if not text.startswith(';'):
            text = ';' + text
        _emu_object.extra_text.append(text)

def total_demand() -> Tuple[float, float]:
    """Return total demand and deficit at current time"""
    nodecount = nbobjects(NODE)
    demand = deficit = 0
    for ix in range(1, nodecount+1):
        if ENretval(et.ENgetnodetype(ix)) == et.EN_JUNCTION:
            demand += ENretval(et.ENgetnodevalue(ix, et.EN_DEMAND))
            deficit += ENretval(et.ENgetnodevalue(ix, et.EN_DEMANDDEFICIT))
            # reduction += ENretval(et.ENgetnodevalue(ix, et.EN_DEMANDREDUCTION))
    return demand, deficit
