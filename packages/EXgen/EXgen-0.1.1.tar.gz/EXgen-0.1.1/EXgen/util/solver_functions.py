import numpy as np
import matplotlib.pyplot as plt

# consts : 
EPS0 = 8.854e-12

MSH_PTS = 9
FIG_DPI = 100

#################################################
#* util functions : 
#################################################

def construct_points_list(variables):
    Plist = []
    Qlist = []

    var_keys = list(variables.keys())
    P_keys = [x for x in var_keys if x[0] == 'P']
    n = len(P_keys)
    for ind in range(1, n+1):

        Q = variables[f"Q{ind}"]
        P = variables[f"P{ind}"]

        Qlist.append(Q)
        Plist.append(P)

    return Qlist, Plist

def construct_points_list_from_inserts(task):

    Plist = []
    Qlist = []

    var_keys = list(task["variables"].keys())
    P_keys = [x for x in var_keys if x[0] == 'P']
    n = len(P_keys) // 2
    for ind in range(1, n+1):

        Q = task["variables"][f"Q{ind}"]
        Px = task["variables"][f"P{ind}x"]
        Py = task["variables"][f"P{ind}y"]

        Qlist.append(Q)
        Plist.append(np.array([Px, Py]))

    return Qlist, Plist

#################################################
#* field calc helper functions : 
#################################################

def calc_dir_vec(Pq, Pa):
    rQA = Pa - Pq
    r = np.sqrt(sum(rQA**2))
    e_rQA = rQA/r

    return e_rQA, r

def calc_e_field_in_point(Q, Pq, Pa):
    e_rQA, r = calc_dir_vec(Pq, Pa)
    return Q/(4*np.pi*EPS0*r**2) * e_rQA

def calc_e_field_in_region(Q, Pq, rng, N:int=20):
    x = np.linspace(rng[0,0],rng[0,1],N)
    y = np.linspace(rng[1,0],rng[1,1],N)

    xx, yy = np.meshgrid(x, y)

    rx = xx - Pq[0]
    ry = yy - Pq[1]

    rr = np.sqrt(rx**2 + ry**2)
    notzero = rr > 1e-16

    erx = np.zeros_like(rr)
    ery = np.zeros_like(rr)
    
    erx[notzero] = rx[notzero] / rr[notzero]
    ery[notzero] = ry[notzero] / rr[notzero]

    E = np.zeros((2, *xx.shape), dtype=np.float64)
    E[0, notzero] = Q/(4*np.pi*EPS0*rr[notzero]**2) * erx[notzero]
    E[1, notzero] = Q/(4*np.pi*EPS0*rr[notzero]**2) * ery[notzero]

    Enorm = np.zeros((2, *xx.shape), dtype=np.float64)
    Eabs = np.sqrt(E[0, :, :]**2 + E[1, :, :]**2)
    Enorm[0, notzero] = E[0, notzero]/Eabs[notzero]
    Enorm[1, notzero] = E[1, notzero]/Eabs[notzero]

    return xx, yy, rr, E, Enorm

def calc_total_e_field(Qlist, Plist, rng, N, totnorm=False):
    
    E = np.zeros((2, N, N))
    xx = yy = []

    for Q, P in zip(Qlist, Plist):
        xx, yy, rr, Ep, Enorm = calc_e_field_in_region(Q, P, rng, N)

        if totnorm:        
            E += Ep
        else:
            E += Enorm
    
    if totnorm:
        Eabs = np.sqrt(E[0, :, :]**2 + E[1, :, :]**2)
        E /= Eabs
    else:
        E /= len(Qlist)

    return xx, yy, E

#################################################
#* plot functions : 
#################################################

def plot_e_field_and_charges(xx, yy, E, Plist, figpth:str="./task_figures/el_field_mq.pdf"):
    fig, ax = plt.subplots()
    ax.quiver(xx, yy, E[0, :, :], E[1, :, :], pivot="tail", angles="xy")
    for ind, P in enumerate(Plist):
        ax.scatter(P[0], P[1], label=f"Q{ind+1}", s=300, alpha=0.5)
        ax.text(P[0]-0.1, P[1]-0.1, f"Q{ind+1}")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    ax.set_aspect('equal', 'box')

    plt.savefig(figpth, dpi=FIG_DPI)

def plot_points_and_field_dir(E, P1, P2, Pm):
    fig, ax = plt.subplots()
    figpath = "./task_figures/el_field_1.pdf"

    ax.scatter([P1[0]], [P1[1]], label="P1")
    ax.scatter([P2[0]], [P2[1]], label="P2")
    ax.scatter([Pm[0]], [Pm[1]], label="Pm")
    ax.quiver(Pm[0], Pm[1], E[0], E[1], label="Em")
    ax.legend()
    ax.grid()
    ax.set_xlabel("x in m")
    ax.set_ylabel("y in m")
    plt.savefig(figpath, dpi=FIG_DPI)
    plt.close()

    return figpath

#################################################
#* main functions : 
#################################################

def electric_field_1(task):
    P1x = task["variables"]["P1x"]
    P1y = task["variables"]["P1y"]
    P2x = task["variables"]["P2x"]
    P2y = task["variables"]["P2y"]
    P1 = np.array([P1x, P1y])
    P2 = np.array([P2x, P2y])
    Q1 = task["variables"]["Q1"] * 1e-10
    Q2 = task["variables"]["Q2"] * 1e-10
    Q3 = task["variables"]["Q3"] * 1e-10
    
    # Task : 1.1.
    Ep1 = calc_e_field_in_point(Q1, P1, P2)
    Ep2 = calc_e_field_in_point(Q2, P2, P1)
    
    F1 = Q1 * Ep2
    F2 = Q2 * Ep1

    # Task : 1.2 
    Pm = (P1 + P2)/2
    Em1 = calc_e_field_in_point(Q1, P1, Pm)
    Em2 = calc_e_field_in_point(Q2, P2, Pm)
    Em = Em1 + Em2

    figpath = plot_points_and_field_dir(Em, P1, P2, Pm)
    task["solution-figpaths"].append(figpath)
    
    # Task : 1.3 
    F3 = Q3 * Em

    return {"F1": F1, "F2": F2, "Pm": Pm, "Em": Em, "F3": F3}

def electric_field_2(task):
    P1x = task["variables"]["P1x"]
    P1y = task["variables"]["P1y"]
    P2x = task["variables"]["P2x"]
    P2y = task["variables"]["P2y"]
    P3x = task["variables"]["P3x"]
    P3y = task["variables"]["P3y"]
    P1 = np.array([P1x, P1y])
    P2 = np.array([P2x, P2y])
    P3 = np.array([P3x, P3y])
    Q1 = task["variables"]["Q1"] * 1e-10
        
    # Task : 1.1.
    Ep1 = calc_e_field_in_point(Q1, P1, P3)
    
    e2_rQA, r2 = calc_dir_vec(P2, P3)
    Q2 = - Ep1[1]*4*EPS0*r2**2/e2_rQA[1]

    return {"Q2": Q2}

def electric_field_mpq_1(task):
    # Mutpltiple question task solver function : 
    # Given a number of point charges and a location 
    # range for the charges - this function will 
    # generate a total electric field and plot it for the 
    # given configuration for the given multiple choice 
    # question. 
    
    rng = np.array([[0, 3], [0, 3]], dtype=np.float64)
    
    Qlist, Plist = construct_points_list(task["variables"])
    xx, yy, E = calc_total_e_field(Qlist, Plist, rng, MSH_PTS, totnorm=True)
    
    plot_e_field_and_charges(xx, yy, E, Plist, task["insert_figpaths"][0])
    # task["solution-figpaths"].append(figpath)

    return {}