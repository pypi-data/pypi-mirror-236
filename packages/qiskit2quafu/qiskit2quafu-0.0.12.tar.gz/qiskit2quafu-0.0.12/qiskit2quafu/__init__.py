from quafu import QuantumCircuit as quafuQC
import re
from qiskit import transpile, QuantumCircuit
from quafu import User, Task
import numpy as np
import scipy.optimize as opt
from qiskit import *
import mthree
from qiskit.providers.fake_provider import FakeAthens
import json
import matplotlib.pyplot as plt
import time
import os

name = "qiskit2quafu"


def qiskit2quafu(qc: QuantumCircuit, regName='iii', basis_gates=['cx', 'cy', 'cz', 'cp', 'u1', 'u2', 'u3', 'h', 'id', 'swap', 'cswap', 'p', 'rx', 'ry',
                                                                 'rz', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg', 'sx', 'ccx', 'rxx', 'ryy', 'rzz'], optimization_level=0):

    def regMerge(qstring: str, regName=regName):
        regList = []
        t = qstring.splitlines()
        for a in t:
            if (re.search('qreg', a)):
                asp = a.split(' ')
                regList.append(asp[-1][:-1])

        mlist = []  # MiddleList

        for a in regList:
            b = a.split('[')
            b[-1] = int(b[-1][:-1])
            mlist.append(b)

        addDict = {}
        base = 0
        for a in mlist:
            addDict[a[0]] = base
            base = base+a[1]

        repDict = {}  # Replace Dictionary
        mv = 0
        currAdd = 0
        for a in mlist:
            name = a[0]
            bit = a[1]
            while mv < bit:
                repDict[name+'['+str(mv)+']'] = regName+'['+str(currAdd)+']'
                mv += 1
                currAdd += 1
            mv = 0

        ts = qstring

        for old, new in repDict.items():
            ts = ts.replace(old, new)

        rm_reg_list = []
        for a in regList:
            rm_reg_list.append('qreg '+a+';\n')

        replace_str = ''
        for a in rm_reg_list:
            replace_str += a

        ts = ts.replace(replace_str, 'qreg '+regName+'['+str(currAdd)+'];\n')
        return ts

    qc_new = transpile(qc, basis_gates=basis_gates,
                       optimization_level=optimization_level)
    qc_merge = regMerge(qc_new.qasm(), regName=regName)
    quafu_qc = quafuQC(qc_new.num_qubits)
    quafu_qc.from_openqasm(qc_merge)
    return quafu_qc, qc_merge

def hamilton2circ(hamList: list, reverse=True):
    """
    生成哈密顿量对应的测量电路
    输入: 待测哈密顿量列表
    返回: 对应测量电路
    """
    num_qubits = len(hamList[0])
    circs = []
    for op in hamList:
        if reverse:
            op = reversed(op)
        qc = QuantumCircuit(num_qubits)
        for idx, item in enumerate(op):
            if item == 'X':
                qc.h(num_qubits-idx-1)
            elif item == 'Y':
                qc.sdg(num_qubits-idx-1)
                qc.h(num_qubits-idx-1)
        circs.append(qc)
    return circs

def hamilton2quafu(i: list, reverse=True):
    '''
    对指定的哈密顿量生成测量电路,并与ansatz电路拼接
    输入格式: [ [ansatz:qiskitQuantumCircuit, H:string, coefficient:list] ]
    [[ansatz1, H1, coefficientList1], [ansatz2, H2, coefficientList2], ...] 
    例如: [ [ansatz, 'XYZ', [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0]] ]   
    reverse: 默认为True, 根据个人习惯调整
    设置为True时: 哈密顿量字符串的左起第一个对应测量结果的左起第一位
    设置为False时: 哈密顿量字符串的左起第一个对应测量结果的右起第一位
    '''
    # Steps:
    # 0. 格式化输入
    # 输入格式: [ [ansatz:qiskitQuantumCircuit, H:string, coefficient:list] ]
    resultList = []

    ansatzList = []
    for a in i:
        ansatzList.append(a[0])

    HList = []
    for a in i:
        HList.append(a[1])

    coeffList = []
    for a in i:
        coeffList.append(a[2])
    # 1. 哈密顿转换
    # Imp: hamilton2circ
    HcircuitList = hamilton2circ(HList, reverse=reverse)

    # 2. 拼接 ansatz
    # qiskit_meas_circuits = [ansatz.compose(circ).measure_all(inplace=False) for circ in meas_circuits]
    for a in range(len(i)):
        resultList.append(ansatzList[a].compose(
            HcircuitList[a].measure_all(inplace=False)))

    # 3. 赋值
    for a in range(len(i)):
        paras = resultList[a].parameters
        b = 0
        for para in paras:
            resultList[a] = resultList[a].bind_parameters(
                {para: coeffList[a][b]})
            b += 1

    outList = []
    # 4. qiskit2quafu
    for a in resultList:
        rc, _ = qiskit2quafu(a)
        outList.append(rc)

    return outList

def get_expect_value(dic: dict):
    '''
    Dict Format:
    {向量值1:频率1, 向量值2:频率2}
    向量值以str格式输入
    '''
    t = 0
    e_sum = 0
    for key, value in dic.items():
        if (key.count('1') % 2):
            e_sum -= value
        elif (key.count('1') % 2) == 0:
            e_sum += value
        t += value

    e = e_sum/t
    return e

def quafuVQE(H_op, ansatz, api_token, params, random_param=False, tol=None, maxiter=None, backend = "ScQ-P10", cpPath='checkpoint.txt', logJson='log.json'):
    # Initialize Quafu
    # 从 "ScQ-P10", "ScQ-P18", "ScQ-P136" 选择一台
    # 创建用户对象
    user = User()
    user.save_apitoken(api_token)
    # 返回任务id，测试结果和期望值
    task = Task()
    task.config(backend=backend, shots=3000, compile=True)
    print("Quafu initialized.")
    
    folder=str(time.time())
    os.mkdir(folder)
    cpPath = folder+'/'+cpPath
    logJson = folder + '/'+logJson
    
    coeffs = np.array([item[0] for item in H_op], dtype=float)
    op_strings = [item[1] for item in H_op]
    
    meas_circs = hamilton2circ(op_strings,reverse=False)
    full_circs = [ansatz.compose(meas_circs[kk]).measure_all(
    inplace=False) for kk in range(len(meas_circs))]
    
    meas_strings = [string.replace('X', 'Z').replace('Y', 'Z')
                for string in op_strings]
        
    backend = FakeAthens()
    # Insert some value temproraly
    if random_param:
        params = np.random.rand(1,len(ansatz.parameters))
        params += 0.05*(np.random.random(params.shape[0])-0.5)
    else:
        params = params
    
    mit = mthree.M3Mitigation(backend)
    mit.cals_from_system([0, 1])
    paramsProcess = []
    energyProcess = []
    def vqe_func(params, *args):
        # Attach parameters to the transpiled circuit variables
        bound_circs = [circ.bind_parameters(params) for circ in full_circs]    
        # Submit the job and get the resultant counts back
        if not isinstance(bound_circs,list):
            bound_circs = [bound_circs]
            
        result=[]
        
        for a in bound_circs:
            upload , _ = qiskit2quafu(a)
            
            res_single=task.send(upload, wait=True, name='', group='g').res
            while not(res_single):
                res_single=task.send(upload, wait=True, name='', group='g').res
                
            with open(cpPath,'w+') as f:
                f.writelines(str(params))
            result.append(res_single)
            
        # Apply mitigation to get quasi-probabilities
        quasis = mit.apply_correction(result, [0, 1])
        # Evaluate the coefficients times each expectation value obtained from quasi-probabilities and sum.
        energy = np.sum(coeffs*quasis.expval(meas_strings))
        paramsProcess.append(params.tolist())
        energyProcess.append(energy)
        with open(logJson,'w+') as l:
            json.dump({'energy':energyProcess,'params':paramsProcess},fp=l,sort_keys=True, indent=4, separators=(',', ': '))
        return energy
    
    res = opt.minimize(vqe_func, params, method='COBYLA',options={'maxiter':maxiter},tol=tol)
    return res.fun , np.mod(res.x, 2*np.pi)

def draw_plot(logpath):
    with open(logpath,'r') as f:
        data = json.load(f)['energy']
        x = range(len(data))
        y = data
        plt.plot(x,y)
        plt.grid(linestyle="--", alpha=0.4)
        plt.show()