# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 21:47:36 2019
@author: XIAN

Reference:
Cameron Jones, 2018.Coulomb Matrix Generator.
https://github.com/cameronus/coulomb-matrix/blob/master/generate.py

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
                    
                for n, i in enumerate(syms):
                    if i == 'C':
                        syms[n] = 6
                    if i == 'H':
                        syms[n] = 1
                    if i == 'N':
                        syms[n] = 7
                    if i == 'O':
                        syms[n] = 8
                    if i == 'Si':
                        syms[n] = 14
                    if i == 'P':
                        syms[n] = 15
                    if i == 'Se':
                        syms[n] = 34
                    if i == 'S':
                        syms[n] = 16
                    
                m = np.column_stack((syms,m))
                syms = np.insert(syms, 0, 0,axis = 0)
                m = np.insert(m, 0 , syms, axis = 0) 
                print(m)
                matrices.append(m)

    max_atoms = 27     
    for index, matrix in enumerate(matrices):
        n_atoms = matrix[0].shape[0]
        m = np.zeros((max_atoms , max_atoms ))
        m[:n_atoms, :n_atoms] = matrix[:n_atoms]
        matrices[index] = m    
            
    np.save('/Users/XIAN/Documents/xian fyp/Coulumb Matrix 44', matrices)
        
if __name__== '__main__':
  main()
