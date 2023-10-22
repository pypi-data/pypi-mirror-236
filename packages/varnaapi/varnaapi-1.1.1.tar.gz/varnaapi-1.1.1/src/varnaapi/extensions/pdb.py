from collections import namedtuple
from pathlib import Path
import requests
from io import StringIO

import numpy as np
import pandas as pd
from mmcif.io.PdbxReader import PdbxReader
import RNA

from varnaapi.models import Structure

Chain = namedtuple('Chain', ['id', 'auth'])


class Nuc(namedtuple('Nuc', ['nuc', 'chain', 'pos', 'model', 'insert'], defaults=['.'])):

    @classmethod
    def from_bgsu_unit_id(cls, id):
        lst = id.split('|')
        if len(lst) >= 8 and lst[7]:
            return cls(lst[3], lst[2], lst[4], lst[1], lst[7])
        else:
            return cls(lst[3], lst[2], lst[4], lst[1])



Bp = namedtuple('Bp', 'i j type')

BPS = ['AU', 'CG', 'GC', 'GU', 'UA', 'UG']

# asym_id: strand id
# pdb_strand_id: author strand id
# seq_id: 

PolyAttrName = ['type', 'pdbx_strand_id', 'pdbx_seq_one_letter_code_can']
ChainAttrName = ['asym_id', 'pdb_strand_id']
NucAttrName = ['seq_id', 'pdb_seq_num', 'mon_id', 'pdb_ins_code']



CIF = "https://files.rcsb.org/download/{}.cif"
FR3D = "http://rna.bgsu.edu/rna3dhub/pdb/{}/interactions/fr3d/basepairs/csv"


class _PDB:
    def __init__(self, mmcifIO, fr3dIO, model=0):
        # self.id = pdbid
        self.mmcif_obj = mmcif_seq_obj(mmcifIO)
        self.chain_seq = get_RNA_seq(self.mmcif_obj)
        self.seq_scheme_obj = self.mmcif_obj.getObj('pdbx_poly_seq_scheme')
        self.seq_scheme_chainIdx = get_chainIdx(self.seq_scheme_obj)
        self.seq_scheme_nucIdx = get_nucIdx(self.seq_scheme_obj)
        self.seq_scheme = np.array(self.seq_scheme_obj.data)

        self.chainid_list = np.array([x for x in np.unique(self.seq_scheme[:,self.seq_scheme_chainIdx], axis=0)])
        # nuc_pos_all = pd.DataFrame([tuple(x) for x in self.seq_scheme[:, self.seq_scheme_chainIdx+self.seq_scheme_nucIdx]], columns=ChainAttrName+NucAttrName)
        # nuc_pos_all[['seq_id', 'pdb_seq_num']] = nuc_pos_all[['seq_id', 'pdb_seq_num']].astype(int)
        # Get RNA only chain
        self.nuc_pos_all = self._rna_only()
        self.bp_data = self.load_bp_csv(fr3dIO)

    @classmethod
    def from_id(cls, pdbid, model=0):
        pdb = cls(mmcifIO_from_pdbid(pdbid), fr3dIO_from_pdbid(pdbid), model=model)
        pdb.pdbid = pdbid
        return pdb

    def _rna_only(self):
        nuc_pos_all = self.seq_scheme[:, self.seq_scheme_chainIdx+self.seq_scheme_nucIdx]
        nuc_pos_all = nuc_pos_all[np.where(np.isin(nuc_pos_all[:,1], list(self.chain_seq.keys())))]
        for chainid, seq in self.chain_seq.items():
            nuc_pos_all[np.where(nuc_pos_all[:,1]==chainid), 4] = np.array(list(seq))

        return nuc_pos_all


    def load_bp_csv(self, fr3dIO):
        """Get all  pair interactions from BGSU csv file
        In addition, convert residue author ID to pdb id
        """
        bp_data = bp_data_from_csv(fr3dIO)
        if not len(bp_data) == 0:
            bp_data[:,2] = self.nuc_pos_bgsu_to_pdb(bp_data[:,[0,1,2,4]])
            bp_data[:,7] = self.nuc_pos_bgsu_to_pdb(bp_data[:,[5,6,7,9]])
        return bp_data


    def chainid_convert(self, chainid, auth):
        idlist = self.chainid_list[np.where(self.chainid_list[:, int(auth)] == chainid)][0]
        return idlist[int(not auth)]


    def bps_of_chains(self, chainid, auth=True):
        """Returns all bp interections in given chain
        """
        # Make sure given chain id is author provided id
        if len(self.bp_data) == 0:
            return []
        if not auth:
            chainid = self.chainid_convert(chainid, True)
        return self.bp_data[np.where((self.bp_data[:,1]==chainid) & (self.bp_data[:,6]==chainid))]


    def get_all_bps_of_chain(self, chainid, auth=True):
        """Returns all base pair interactions within the given chain
        Note that position is 1-index
        """
        within_chain =self.bps_of_chains(chainid, auth)
        if len(within_chain) == 0:
            return []
        return [(int(t[2]), int(t[7]), t[10]) for t in within_chain]


    def canonical_bps_of_chain(self, chainid, auth=True):
        within_chain =self.bps_of_chains(chainid, auth)
        if len(within_chain) == 0:
            return []
        # wwbps = within_chain[np.where(np.isin(within_chain[:,8], ['cWW', 'ncWW']))]
        wwbps = within_chain[np.where(np.isin(within_chain[:,10], ['cWW']))]
        return wwbps[np.where(np.isin(np.char.add(wwbps[:,0],wwbps[:,5]), BPS))]

    def ncBPs_of_chain(self, chainid, auth=True):
        within_chain =self.bps_of_chains(chainid, auth)
        if len(within_chain) == 0:
            return []
        ncbps = within_chain[np.where(np.logical_not(np.isin(within_chain[:,10], ['cWW'])))]
        return ncbps


    def nuc_pos_bgsu_to_pdb(self, data):
        a = self.nuc_pos_all[:,[4,1,3,5]]
        match = (data[:, None] == a).all(-1)
        tmp = self.nuc_pos_all[np.where((data[:, None] == a).all(-1))[1], 2]
        return tmp

    def length_of_chain(self, chainid, auth=True):
        return np.sum(self.nuc_pos_all[:,int(auth)] == chainid)

    def dbn_of_chain(self, chainid, auth=True, model=0):
        dbns = []
        seqlen = int(self.length_of_chain(chainid, auth))
        bps_all = self.canonical_bps_of_chain(chainid, auth)
        # No bp interaction
        if len(bps_all) == 0:
            return '.'*seqlen
        models = list(np.unique(bps_all[:,3]))
        models.sort(key = lambda t:int(t))
        m = models[model]
        ptable = [seqlen] + [0]*seqlen
        bps = bps_all[np.where((bps_all[:,3]==m)&(bps_all[:,8]==m))]
        for bp in bps:
            i, j = int(bp[2]), int(bp[7])
            ptable[i], ptable[j] = j, i

        return RNA.db_from_ptable(ptable)


class PDBStructure(Structure, _PDB):
    def __init__(self, mmcifIO, fr3dIO, chainid, model=0):
        self.chainid = chainid
        _PDB.__init__(self, mmcifIO, fr3dIO, model=model)
        Structure.__init__(self, structure=self.dbn_of_chain(self.chainid))


    @classmethod
    def from_id(cls, pdbid, chainid, model=0):
        pdb = cls(mmcifIO_from_pdbid(pdbid), fr3dIO_from_pdbid(pdbid), chainid, model=model)
        pdb.pdbid = pdbid
        return pdb


    def savefig(self, output, show:bool=False):
        tmp = [t for t in self.aux_BPs]
        for bp in self.ncBPs_of_chain(self.chainid):
            i = bp[2]
            j = bp[7]
            if bp[-1][-3] == 'c':
                stericity = 'cis'
            else:
                stericity = 'trans'
            if bp[-1][-2] == 'W':
                edge5 = "WC"
            else:
                edge5 = bp[-1][-2]
            if bp[-1][-1] == 'W':
                edge3 = "WC"
            else:
                edge3 = bp[-1][-1]
            keep = edge3 != "WC" or edge5 != "WC"
            self.add_aux_BP(i, j, edge5=edge5, edge3=edge3, stericity=stericity, color='red', keep=keep)

        Structure.savefig(self, output, show)
        self.aux_BPs = tmp


#############
#           #
#   mmcif   #
#           #
#############

def mmcifIO_from_pdbid(pdbid):
    r = requests.get(CIF.format(pdbid))
    return StringIO(r.text)


def mmcif_seq_obj(mmcifIO):
    """Get mmcif seq scheme object for given file
    """
    data = []
    pRd = PdbxReader(mmcifIO)
    pRd.read(data)
    return data[0]


def get_RNA_seq(mmcif_obj):
    res = {}
    entity_poly = mmcif_obj.getObj('entity_poly')
    tmpIndx = [entity_poly.getAttributeIndex(t) for t in PolyAttrName]
    for t in entity_poly.getRowList():
        if t[tmpIndx[0]] == 'polyribonucleotide':
            for chainid in t[tmpIndx[1]].split(','):
                res[chainid] = t[tmpIndx[2]].replace('\n', '')

    return res


def get_chainIdx(seq_scheme):
    return [seq_scheme.getAttributeIndex(t) for t in ChainAttrName]

def get_nucIdx(seq_scheme):
    return [seq_scheme.getAttributeIndex(t) for t in NucAttrName]



#############
#           #
#   bsgu    #
#           #
#############


# TODO: complete BGSU unit-id parser
def bp_from_line(bgsu_line):
    lst = bgsu_line.split(',')
    bptype =  lst[1][1:-1]
    resi = Nuc.from_bgsu_unit_id(lst[0][1:-1])
    resj = Nuc.from_bgsu_unit_id(lst[2][1:-1])
    if (int(resi.pos) < int(resj.pos)):
        return Bp(resi, resj, bptype)
    return None


def fr3dIO_from_pdbid(pdbid):
    r = requests.get(FR3D.format(pdbid))
    return StringIO(r.text)


def bp_data_from_csv(fr3dIO):
    """Get all base pair interactions from BGSU csv file
    """
    bps = []
    for line in fr3dIO.readlines():
        if line.startswith("No interactions"):
            return bps
        bp = bp_from_line(line.strip())
        if bp is not None:
            bps.append(list(bp.i)+list(bp.j)+[bp.type])
    return np.array(bps)
