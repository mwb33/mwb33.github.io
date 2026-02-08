#Mark Boady - 2026
#The four main positions of the qubit

#Import the Libraries
from qiskit import *
#For simulations:
from qiskit_aer import Aer
#For the Bloch Sphere
from qiskit.visualization import plot_bloch_multivector

#Make a trivial Bloch Sphere
def blochMe(qc,name):
    #Use a State Vector Back end
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(qc)
    results = job.result()
    #Get the state vector to 3 decminal places
    SV=results.get_statevector(qc,decimals=3)
    fig = plot_bloch_multivector(SV)
    fig.savefig(name)


qc = QuantumCircuit(1,1)
blochMe(qc,"comp_zero.png")

qc = QuantumCircuit(1,1)
qc.x(0)
blochMe(qc,"comp_one.png")

qc = QuantumCircuit(1,1)
qc.h(0)
blochMe(qc,"phase_plus.png")

qc = QuantumCircuit(1,1)
qc.x(0)
qc.h(0)
blochMe(qc,"phase_minus.png")



