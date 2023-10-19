from pyoptquest import OptQuestOptimizer
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# precompute constants that we'll use in the optimize loop

# length of the rod
D = 12 * 2.54
print('rod length (D) =', D)

# thickness of the weights
d = 0.635
print('weight thickness (d) =', d)

# weight of the bolt
# the next 5 lines were copied from the fortran code, the I just reassign it to wb for my notation
bl = 5.0  # ! cm , bolt length
blh = 0.4  # ! cm , bolt length head
bd = 0.425  # ! cm , bolt diameter
den = 7.874  # ! g/cm^3 , bolt density (iron)
bm = math.pi * (0.5 * bd)**2 * bl * den  # ! g , bolt mass
wb = bm
print('bolt weight (wb) =', wb)

# db distance of com of bolt from the end of the rod
db = 2.1175
print('bolt com offset (db) =', db)

#number of test points
ntest=10000
Ttest=None

# create a vector of the permutation indices
perm_idx = []
for n in [1, 2, 3, 4]:
    for p in permutations((1, 2, 3, 4), n):
        perm_idx.append(list(p) + [0] * (4 - n))
perm_idx = np.array(perm_idx)
# at this point perm_idx contains 64 entries from [1,0,0,0] to [4,3,2,1]

# this is the distance each weight will be from the axis
d1 = D + 1 * d / 2
d2 = D + 3 * d / 2
d3 = D + 5 * d / 2
d4 = D + 7 * d / 2
dist = np.array([d1, d2, d3, d4])
print('distance of each weight com (dist)=', dist)

# This loops through perm_idx, adds up how many non-zero terms are to find out how
# far way the bolt is.
# For [1,0,0,0], there is 1 non-zero term, so the bolt will be D+1*d away
# For [1,2,0,0], there are 2 non-zero terms, so the bolt will be D+2*d away
# For [1,2,3,4], there are 4 non-zero terms, so the bolt will be D+4*d away
# bcom will be 64-length vector parallel to perm_idx for distances
bcom = D + np.sum(perm_idx > 0, axis=1) * d - db
# and now the additional torque the the bolt adds
# btorque is a 64-length vector parallel to perm_idx for torque
btorque = wb * bcom

# this is the distance the bolt will com will be when there are 1 and 4 wights (used in constraints)
db1 = D + 1 * d - db
db4 = D + 4 * d - db
print('bolt distances at extrema (db1, db4) =', db1, db4)


def get_torques(w1, w2, w3, w4):
    # a little cheat here to pull in the precomputed values
    global perm_idx
    global dist
    global btorque

    # make an array that allow us to turn indices into weights
    wts = np.array([0, w1, w2, w3, w4])

    # this does the torque calculation like in the I wrote, plus it adds in the bolt torque
    T = np.dot(dist, wts[perm_idx].T) + btorque
    return T


def get_test_torques(T, Ttest):
    return np.abs(T.reshape(-1,1)-Ttest.reshape(1,-1)).argmin(axis=0)

# def objective_evaluator(inputs):
# # this is the call back function that evaluates our objective

#     # get the weights that come from the optmizer
#     w1 = inputs['w1']
#     w2 = inputs['w2']
#     w3 = inputs['w3']
#     w4 = inputs['w4']

#     # compute the torques
#     T = get_torques(w1, w2, w3, w4)

#     # sort the torques in place
#     T.sort()

#     # compute the adjacent spacing
#     delta = T[1:] - T[0:-1]

#     # comptue the variance
#     v = np.var(delta)

#     return v

def objective_evaluator(inputs):
# this is the call back function that evaluates our objective
    global TTest

    # get the weights that come from the optmizer
    w1 = inputs['w1']
    w2 = inputs['w2']
    w3 = inputs['w3']
    w4 = inputs['w4']
    phi = inputs['phi']

    # phi=1.6180339887498948
    w1=10*phi**w1
    w2=10*phi**w2
    w3=10*phi**w3
    w4=10*phi**w4

    # compute the torques
    T = get_torques(w1, w2, w3, w4)

    idx=get_test_torques(T,Ttest)

    T=T[idx]

    delta=(T-Ttest)**2

    return delta.sum()

best=None

def status_monitor(inputs, outputs, objectives, iteration, replication):
# optional, monitors the status of the optimization
    global best
    if best is None or objectives['var'] < best:
        improvement = ''
        if best is not None:
            improvement = best - objectives['var']
        print(iteration, improvement, inputs, objectives)
        best = objectives['var']

def do_optimization(wref):
    global Ttest
    # reference weight
    # wref = 120
    # print('reference weight (wref) =', wref)
    Tref = wref * D
    # print('reference torque (Tref) =', Tref)
    # get bounds
    wmin = wref / 2
    wmax = 3 * wref / 2
    Tmin = wmin * D
    Tmax = wmax * D
    print('Trange = ',Tmin, Tmax)
    Ttest = np.linspace(Tmin,Tmax,ntest)
    # print('lower bound (wmin, Tmin) =', wmin, Tmin)
    # print('upper bound (wmax, Tmax) =', wmax, Tmax)
    # precompute w1, since we know what that is
    #w1 = (Tmin - wb*db1)/d1
    #print('w1 =',w1)

    # keep track of the best known for status monitoring
    best = None

    # define the inputs that we'll be optimizing on
    # search_space = {
    #     'w1': {'type': 'continuous', 'min': 0, 'max': wref},
    #     'w2': {'type': 'continuous', 'min': 0, 'max': wref},
    #     'w3': {'type': 'continuous', 'min': 0, 'max': wref},
    #     'w4': {'type': 'continuous', 'min': 0, 'max': wref}
    # }

    # phi=1.6180339887498948
    # grscale=[10]
    # while grscale[-1]<200:
    #     grscale.append(grscale[-1]*phi)

    search_space = {
        'w1': {'type': 'integer', 'min': 0, 'max': 10},
        'w2': {'type': 'integer', 'min': 0, 'max': 10},
        'w3': {'type': 'integer', 'min': 0, 'max': 10},
        'w4': {'type': 'integer', 'min': 0, 'max': 10},
        'phi': {'type': 'continuous', 'min':1, 'max':2}
    }

    print(search_space)

    # build up the constraints, this is the same as the paper
    # constraints = {
    #     'c1': {'expression': 'w1<w2'},
    #     'c2': {'expression': 'w2<w3'},
    #     'c3': {'expression': 'w3<w4'},
    #     'c4a': {'expression': str(Tmin) + '<w1*' + str(d1) + '+w2*' + str(d2) + '+w3*' + str(d3) + '+w4*' + str(d4) + '+' + str(wb * db1)},
    #     'c4b': {'expression': str(Tmax) + '=w1*' + str(d1) + '+w2*' + str(d2) + '+w3*' + str(d3) + '+w4*' + str(d4) + '+' + str(wb * db4)}
    # }


    # build up the constraints, this is the same as the paper
    constraints = {
        'c1': {'expression': 'w1<w2'},
        'c2': {'expression': 'w2<w3'},
        'c3': {'expression': 'w3<w4'}
        # 'c4a': {'expression': str(Tmin) + '=w1*' + str(d1) + '+' + str(wb * db1)},
        #'c4b': {'expression': str(Tmax) + '=w1*' + str(d1) + '+w2*' + str(d2) + '+w3*' + str(d3) + '+w4*' + str(d4) + '+' + str(wb * db4)}
    }
    # print(constraints)

    # define the objective
    objectives = {
        'var': {'type': 'min', 'evaluator': objective_evaluator}  # specify the evaluator
    }

    # define the optimization
    opt = OptQuestOptimizer(
        search_space,
        objectives,
        status_monitor=status_monitor,
        constraints=constraints,
        license_id=515692303,
        optquest_jar=r'OptQuest.jar')

    # call the optimizer
    opt.search(n_iter=10000)
    wts=[opt.best_para['w1'],opt.best_para['w2'],opt.best_para['w3'],opt.best_para['w4'],opt.best_para['phi']]
    wts.sort()
    return tuple(wts)


all_refs=[]
all_w1=[]
all_w2=[]
all_w3=[]
all_w4=[]

for wref in range(120,121):
    (w1,w2,w3,w4,phi)=do_optimization(wref)

    # phi = 1.6180339887498948
    w1 = 10 * phi**w1
    w2 = 10 * phi**w2
    w3 = 10 * phi**w3
    w4 = 10 * phi**w4


    all_refs.append(wref)
    all_w1.append(w1)
    all_w2.append(w2)
    all_w3.append(w3)
    all_w4.append(w4)

    print('w1',w1,'w2',w2,'w3',w3,'w4',w4)
    T = get_torques(w1, w2, w3, w4)
    ST = list(zip(T, range(len(T))))
    ST.sort()
    (T, sorted_idx) = zip(*ST)
    T=np.array(T)
    test_idx=get_test_torques(T,Ttest)
    test_idx=np.unique(test_idx)
    # print(test_idx)
    for i in range(len(test_idx)):
        print(T[test_idx[i]], perm_idx[sorted_idx[test_idx[i]]])

    # lr=LinearRegression().fit(test_idx.reshape(-1,1),T[test_idx].reshape(-1,1))
    # xp=np.array([0,64]).reshape(-1,1)
    # yp=lr.predict(xp)


    plt.plot(T, 'C0.')
    plt.plot(test_idx,T[test_idx],'C1.')
    # plt.plot(xp,yp,'C1--')
    plt.show()

    x1=np.arange(len(test_idx)).reshape(-1,1)
    y1=T[test_idx].reshape(-1,1)
    lr=LinearRegression().fit(x1,y1)
    xp=np.array([0,len(test_idx)]).reshape(-1,1)
    yp=lr.predict(xp)
    print('r-squared', lr.score(x1,y1))
    plt.clf()
    plt.plot(x1,y1,'C1.')
    plt.plot(xp,yp,'C1--')
    plt.show()

exit(0)
plt.plot(all_refs,all_w1,'.')
plt.plot(all_refs,all_w2,'.')
plt.plot(all_refs,all_w3,'.')
plt.plot(all_refs,all_w4,'.')
plt.show()

plt.clf()
all_weights=all_w1+all_w2+all_w3+all_w4
plt.hist(all_weights,bins=range(int(min(all_weights)),int(max(all_weights)+1)))
plt.show()

km=KMeans(n_clusters=20).fit(np.array(all_weights).reshape(-1,1))
wlist=km.cluster_centers_

(w1, w2, w3, w4) = do_optimization(120)
nw1=wlist[np.abs(wlist-w1).argmin()]
nw2=wlist[np.abs(wlist-w2).argmin()]
nw3=wlist[np.abs(wlist-w3).argmin()]
nw4=wlist[np.abs(wlist-w4).argmin()]

print(w1,nw1)
print(w2,nw2)
print(w3,nw3)
print(w4,nw4)

T1=get_torques(w1,w2,w3,w4)
T1.sort()
T2=get_torques(nw1,nw2,nw3,nw4)
T2.sort()

print('best weights:',wlist.flatten())

plt.clf()
plt.plot(T1, '.')
plt.plot(T2, '.')
plt.show()
