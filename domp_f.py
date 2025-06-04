import numpy as np
import gurobipy as gp
import pandas as pd

def lproot(model, where):
        """
        Gurobi callback function to add cutting planes at MIPNODE and MIPSOL nodes.
        """
        if where == gp.GRB.Callback.MIPNODE:  # Node solution
            nodecnt = model.cbGet(gp.GRB.Callback.MIPNODE_NODCNT)
            if nodecnt==0:
                model._lp=model.cbGet(gp.GRB.Callback.MIPNODE_OBJBND)


class DOMP:
    def __init__(self, file, method, time_limit, relax, p, alpha=1.0):

        self.file=file
        self.method = method
        self.time_limit = time_limit
        self.relax=relax
        self.p=p
        self.alpha=alpha
        self.solution_info = {}


    def lambda_parameter(self):

        if self.method=="sum":
            self.lamb=np.ones(self.n)
        elif self.method=="cent":
            self.lamb = self.alpha*np.ones(self.n)
            self.lamb[0]=1
        elif self.method=="ksum":
            self.lamb = np.zeros(self.n)
            for i in range(int(self.alpha*self.n)):
                self.lamb[i]=1
        elif self.method=="decreasing":
            self.lamb=np.empty(self.n)
            for i in range(self.n):
                self.lamb[i]=self.n-i
        else:
            print("Non defined method")

    def _extract_solution_info(self, model):
        
        """Extracts relevant solution information after solving the model."""
        self.solution_info = {
            "file": self.file,
            "method": self.method,
            "n": self.n,
            "relax": self.relax,
            "CPUTime": model.Runtime,
            "ObjVal": model.ObjVal if model.status != gp.GRB.INFEASIBLE else None,
            "MIPGap":  0 if self.relax else model.MIPGap,
            "LPRelaxation at Root": model._lproot,
            "Work": model.getAttr(gp.GRB.Attr.Work),
            "NodeCount": model.NodeCount,
            "NumBinVars": model.NumBinVars,
            "NumCtrs": model.NumConstrs,
            "status": model.Status,
            "iterations": model.IterCount,
            "Y": self.Y,
            "Z": self.Z
        }


    def solve_BEP(self):


        # Load data:
        X= np.loadtxt(self.file)
        n = X.shape[0]
        self.n=n
        self.lambda_parameter()

        ##Model:
        model = gp.Model("domps")
        model.setParam("Outputflag", 0)
        model.setParam("TimeLimit", 3600)

        
        
        c=np.sqrt(((X[:, np.newaxis, :] - X[np.newaxis, :, :])**2).sum(axis=2))

        N= range(n)

        u = model.addVars(N,  name="u")
        v = model.addVars(N,  name="v")
        if self.relax:
            x = model.addVars(N, N,  name="x") #vtype=gp.GRB.BINARY,
            y = model.addVars(N,  name="y")#vtype=gp.GRB.BINARY,
        else:
            x = model.addVars(N, N, vtype=gp.GRB.BINARY, name="x") #
            y = model.addVars(N, vtype=gp.GRB.BINARY, name="y")#vtype=gp.GRB.BINARY,



        model.setObjective(
            gp.quicksum(u[i]+v[i] for i in N),
            gp.GRB.MINIMIZE
        )

        for i in N:
        # Restricción 1: Cada cliente debe ser atendido completamente
            model.addConstr(gp.quicksum(x[i, j] for j in N) == 1)
            for j in N:
                model.addConstr(x[i,j] <= y[j])
        
        model.addConstr(gp.quicksum(y[j] for j in N) == self.p)

        for i in N:
            for j in N:
                if self.lamb[j]>0.001:
                    model.addConstr(u[i]+v[j] >= self.lamb[j]*gp.quicksum(x[i,l]*c[i,l] for l in N))

        for j in N:
            for i in N:
                model.addConstr(gp.quicksum(x[i,jj] for jj in N if c[i,jj]>c[i,j]) + y[j] <=1)

        model._lproot=0
        model.Params.OutputFlag=1
        model.optimize(lproot)
        
        self.Y = model.getAttr("X", y)
        self.Z = model.getAttr("X", x)

        self._extract_solution_info(model)


        return model.ObjVal
    
    