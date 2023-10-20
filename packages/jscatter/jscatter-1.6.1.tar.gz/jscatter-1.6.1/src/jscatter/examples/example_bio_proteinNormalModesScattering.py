""" Alcohol dehydrogenase (yeast) example for normal mode analysis
#
# See Biehl et al.PRL 101, 138102 (2008)

In this example we consecutivly
 - load the protein
 - create normal modes
 - calc effective diffusion
 - calc the dynamic mode formfactor from normal modes
 - show how the intermediate scattering function looks with diffusion and internal normal mode relaxation

Finally, we build from this a model that can be used for fitting

"""
##1
# create universe with protein inside that adds hydrogens
#  - load PDB structure
#  - repair structure e.g. missing atoms 
#  - add hydrogens using pdb2pqr, saving this to 3cln_h.pdb
#  - adds scattering amlitudes, volume determination

%matplotlib
import jscatter as js
import numpy as np

adh = js.bio.fetch_pdb('4w6z.pdb1')
# the 2 dimers in are in model 1 and 2 and need to be merged into one.
adhmerged = js.bio.mergePDBModel(adh)
u = js.bio.scatteringUniverse(adhmerged)
u.atoms.deuteration = 0
protein = u.select_atoms("protein")
S0 = js.bio.nscatIntUniv(protein, cubesize=0.5, getVolume='once')


# ## Create normal modes based on residues
nm = js.bio.vibNM(protein.residues)

# ## Calc effective diffusion with trans/rot contributions
# - determine $D_{trans}$ and $D_{rot}$ using HULLRAD
# - calc Deff
D_hr = js.bio.hullRad(u)
Dt = D_hr['Dt'] * 1e2  # conversion to nm²/ps
Dr = D_hr['Dr'] * 1e-12  # conversion to 1/ps
u.qlist = np.r_[0.01, 0.1:3:0.2]
Deff = js.bio.diffusionTRUnivTensor(u.residues, DTT=Dt, DRR=Dr, cubesize=0.5)

p=js.mplot()
p.Plot(Deff.X, Deff.Y*1e5, li=1, le='rigid ADH protein')
p.Xaxis(label='$Q / nm^{-1}$')
p.Yaxis(label='$D_{eff} /A^2/ns$')


# ### Normal mode relaxation in small displacement approximation
Ph678 = js.dL()
for NN in [6,7,8]:
   Ph = js.bio.intScatFuncPMode(nm, NN, output=0, qlist=Deff.X)
   Ph678.append(Ph)

# ## effective diffusion Deff in initial slope (compare to cumulant fit)
a=1000.
rate = 1/30000 # 1/ps
for Ph in Ph678:
   d = Deff.interp(Ph.X) + rate * a**2 * Ph._Pn / (Ph._Fq+a**2*Ph._Pn) / Ph.X**2
   p.Plot(Ph.X,1e5*d ,li='', le=f'rigid ADH + mode {Ph.modeNumber}  rmsd={Ph.kTrmsd*a:.2f} A')

p.Title('Alcohol dehydrogenase (ADH) effective diffusion \nwith additional normal mode relaxations')
p.Legend(x=1.5,y=5.5)
# p.savefig(js.examples.imagepath+'/ADHNM_Deff.jpg', dpi=100)

# Assume a common relaxation on top of diffusion
# that we add to  Deff
u.qlist = np.r_[0.2:2:0.2]    # [1/nm]
u.tlist = np.r_[1, 10:1e5:50]  # [ps]
Iqt = js.bio.intScatFuncYlm(u.residues,Dtrans=Dt,Drot=Dr,cubesize=1,getVolume='once')

# ### dyanamic mode formfactor P() and relaxation in small displacement approximation with aplitude A(Q)
sumP = Ph678.Y.array.sum(axis=0)
def Aq(a):
    # NM mode formfactor amplitude sum
    aq = a**2*sumP / (Ph678[0]._Fq + a**2*sumP)
    return js.dA(np.c_[Ph678[0].X, aq].T)

p2=js.mplot()
p2.Yaxis(min=0.01, max=1, label='I(Q,t)/I(Q,0)')
p2.Xaxis(min=0, max=100000, label='t / ps')

Iqt2 = Iqt.copy()
l=1/10000  # 1/ps
Aqa = Aq(a)
for i, qt in enumerate(Iqt2):
    diff = qt.Y *(1-Aqa.interp(qt.q))
    qt.Y = qt.Y *((1-Aqa.interp(qt.q)) + Aqa.interp(qt.q)*np.exp(-l*qt.X))
     
    p2.Plot(qt.X, qt.Y * 0.8**i,sy=0,li=[3,2,i+1],le=f'{qt.q:.1f}')
    p2.Plot(qt.X, diff* 0.8**i,sy=0,li=[1,2,i+1])
    
p2.Yaxis(min=0.001,max=1,label='I(Q,t)/I(Q,0)',scale='log')
p2.Xaxis(min=0.1,max=100000,label='t / ps')
p2.Title('Intermediate scattering function with/without NM relaxation')
p2.Subtitle('scaled for visibility')
p2.Legend()
# p2.savefig(js.examples.imagepath+'/ADHNM_Iqt.jpg', dpi=100)

if 0 :
    # look at A(Q)
    p1=js.mplot()
    Aqa = Aq(a)
    p1.Plot(Aqa, sy=0, li=1)
    p1.Yaxis(min=0, max=0.8)

#2 -----------------------------------------------------------------------------
# A fit model to fit Iqt from NSE measurements
# Include H(Q) and S(Q)
# and repat what we need from above

%matplotlib
import jscatter as js
import numpy as np

# create universe
u = js.bio.scatteringUniverse(adhmerged)
u.setSolvent('1d2o1')
u.qlist = js.loglist(0.1, 5, 100)
u.atoms.deuteration = 0
protein = u.select_atoms('protein')
S0 = js.bio.nscatIntUniv(protein, cubesize=0.5, getVolume='once')


# structure factor Sq and hydrodynamic function Hq
# This should be determined from SAXS/SANS measurements at same concentration like NSE
# and maybe fit including concentration dependence
mol = 0.0003
R=4
def Sqbeta(q, R, molarity):
    # this function should be used for structure factor fitting of experiemntal data
    # as it contains the shape correction from Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983)
    # structure factor without correction
    Sq = js.sf.PercusYevick(q=q, R=R, molarity=molarity)  # about 50mg/ml protein like experiemtnal data
    # factor beta from formfactor calculation
    beta = S0.interp(q, col='beta')
    # correct Sq for beta
    Sq.Y = 1 + beta * (Sq.Y-1)
    return Sq

# Hq can be determined by fitting Rh or be determined by other measurements
# We assume here larger hydrodynamic interaction
# The Kotlarchyk correction from above is included by using Sqbeta
Hq = js.sf.hydrodynamicFunct(Sq.X, Rh=R*1.1, molarity=mol,
                             structureFactor=Sqbeta,
                             structureFactorArgs={'R': R}, )


# look at the  D_t = D_0 H(Q)/S(Q) correction for translational diffusion
p3 = js.mplot()
p3.plot(Sq, le='S(Q)')
p3.plot(Hq,le='H(Q)')
p3.plot(Sq.X, Hq.Y/Sq.Y,le='H(Q)/S(Q)')
p3.Yaxis(label='S(Q), H(Q), H(Q)/S(Q)')
p3.Xaxis(min=0.,max=4,label='$Q / nm^-1$')
p3.Title('structure factor and hydrodynamic function\n for translational diffusion')
p3.Text('$H(Q=\infty)/S(Q=\infty)$ can be estimated \nfrom viscosity measurements \nor PFG-NMR.',x=2,y=0.8)
p3.Text('$H(Q=0)/S(Q=0)$ can be measured by DLS.',x=0.8,y=0.95)
p3.Legend()
# p3.savefig(js.examples.imagepath+'/ADHNM_SqHq.jpg', dpi=100)


# make normal modes and calc A(Q)
ca = u.residues
nm = js.bio.vibNM(ca)
Ph678 = js.dL()
for NN in [6,7,8]:
   Ph = js.bio.intScatFuncPMode(nm, NN, output=0, qlist=Deff.X)
   Ph678.append(Ph)
sumP = Ph678.Y.array.sum(axis=0)


def Aq(a):
    aq = a**2*sumP / (Ph678[0]._Fq + a**2*sumP)
    A = js.dA(np.c_[Ph678[0].X, aq].T)
    A.rmsdNM = a * Ph678.kTrmsdNM.array.sum()
    return A


def transRotModes(t, q, Dt, Dr, Rhf=1, R=4, a=1000, l=10, mol=0.0003):
    # trans rot diffusion including H(Q)/S(Q)
    # default values for R, mol are determined from preparation or experiments

    Sq = Sqbeta(q=q, R=R, molarity=mol)
    # assume a factor between the interaction radius R and hydrodynamic radius Rh
    Hq = js.sf.hydrodynamicFunct(q, Rh=R*Rhf, molarity=mol, structureFactor=Sqbeta,
                                structureFactorArgs={'R': R}, )

    Dth = Dt * Hq.interp(q) / Sq.interp(q)
    # assume Hr =1-(1-DsoverD0)/3 for rotational diffusion
    Drh = Dr*(1-(1-Hq.DsoverD0)/3)
    Iqt = js.bio.intScatFuncYlm(u.residues, qlist=np.r_[q],tlist=t, Dtrans=Dth, Drot=Drh, cubesize=1)[0]
    
    # add Pmode relaxation
    Aqa = Aq(a)
    diff = Iqt.Y *(1-Aqa.interp(q))
    Iqt.Y = Iqt.Y *((1-Aqa.interp(q)) + Aqa.interp(q)*np.exp(-1/(l*1000)*Iqt.X))
    Iqt2 = Iqt.addColumn(1,diff)
    
    # for later reference save parameters
    Iqt2.Dt = Dt
    Iqt2.Dr = Dr
    Iqt2.H0= Hq.DsoverD0
    Iqt2.R = R
    Iqt2.Rh = R * Rhf
    Iqt2.rmsdNM = Aqa.rmsdNM

    return Iqt2

tlist = np.r_[1, 10:1e5:50]
sim = js.dL()
for q in np.r_[0.25,0.5,0.9,1.2,2]:
    sim.append(transRotModes(t=tlist, q=q, Dt=Dt, Dr=Dr,a=1000,l=10))

p4=js.mplot()
for c, si in enumerate(sim,1):
    p4.plot(si,sy=0,li=[1,2,c],le=f'$Q={si.q} nm^{-1}$')
    p4.plot(si.X,si[2], sy=0, li=[3,2,c ])
p4.Yaxis(min=0.01,max=1,label='I(Q,t)/I(Q,0)',scale='log')
p4.Xaxis(min=0.1,max=100000,label='t / ps')
p4.Title('Intermediate scattering function')
p4.Subtitle(f'rmsd = {si.rmsdNM:.2f} nm')
p4.Legend()
# p4.savefig(js.examples.imagepath+'/ADHNM_IQTsim.jpg', dpi=100)

# A fit to exp. NSE data might be done like this (using sim as measurd data)
# fixpar are determined from from other experiments (e.g. Dt0 extrapolating DLS to zero conc.)
# or Dr0 from calculation from structure, mol from sample preparation
Dt0 = 4.83e-05   #  nm²/ps
Dr0 = 1.64e-06  #  1/ps
sim.fit(model=transRotModes,
            freepar={'Rhf':1, 'a':1000, 'l':10},
            fixpar={'Dt':Dt0, 'Dr':Dr0,'R':4, 'mol':0.0003 },
            mapNames={'t':'X'})
