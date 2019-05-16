# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 21:47:36 2019

@author: XIAN
"""

from rdkit.Chem import AllChem as Chem
from collections import Counter
import pandas as pd
import numpy as np
import pybel

open_babel = True # if false, use rdkit
omit_repetition = False # omit repeated values in matrix

pd.set_option('display.width', 150)
pd.options.display.float_format = '{:.3f}'.format

def main():
    filename = '/Users/XIAN/Documents/xian fyp/test 3rings.txt'
    i2 = 0
    with open(filename, 'r+') as f:
        matrices = [] 
        for line in f.readlines():
            i2 += 1
            print (i2)
            mysmiles = line.strip('\n')
            smiles = [mysmiles]
            for smile in smiles:
                mol = Chem.MolFromSmiles(smile)
                mol = Chem.AddHs(mol)
                Chem.EmbedMolecule(mol, Chem.ETKDG())
                conf = mol.GetConformer()
                pymol = pybel.readstring('smi', smile)
                pymol.addh()
                pymol.make3D()
                n_atoms = mol.GetNumAtoms()
                z = [atom.GetAtomicNum() for atom in mol.GetAtoms()]
                if open_babel:
                    xyz = [pymol.atoms[index].coords for index in range(n_atoms)]
                else:
                    xyz = conf.GetPositions()
                m = np.zeros((n_atoms, n_atoms))
                for r in range(n_atoms):
                    for c in range(n_atoms):
                        if r == c:
                            m[r][c] = 0.5 * z[r] ** 2.4
                        elif r < c:
                            m[r][c] = z[r] * z[c] / np.linalg.norm(np.array(xyz[r]) - np.array(xyz[c])) * 0.52917721092
                            if not omit_repetition:
                                m[c][r] = m[r][c]
                        else:
                            continue
                syms = [atom.GetSymbol() for atom in mol.GetAtoms()]
                atoms = Counter(syms)
                bonds = Counter([bond.GetBondType().name for bond in mol.GetBonds()])

                print('\n')
                print('Molecule: ' + smile)
                print('Number of atoms: ' + str(n_atoms))
                print('Atom counts: ' + str(atoms))
                print('Bond counts: ' + str(bonds))  
                matrices.append(m)                  
                    
    max_atoms = max([m[0].shape[0] for m in matrices])
    
    for index, matrix in enumerate(matrices):
        n_atoms = matrix[0].shape[0]
        m = np.zeros((max_atoms, max_atoms))
        m[:n_atoms, :n_atoms] = matrix[0]
        matrices[index] = m
            
    np.save('/Users/XIAN/Documents/xian fyp/Coulumb Matrix 7994 ori without element', matrices)
        
if __name__== '__main__':
  main()