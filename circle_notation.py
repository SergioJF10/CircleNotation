# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, execute
#from qiskit.tools.jupyter import *
#from qiskit.visualization import *
#from ibm_quantum_widgets import *
from qiskit.providers.aer import AerSimulator
from qiskit.quantum_info import Statevector

# Impoting other necessary libraries
import math
import cmath
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.colorbar as clb


def get_amplitudes(sv):
    '''Extract and normalize the data structure with the amplitudes'''
    sv_dict = sv.to_dict()

    # Standardization I (include all amplitudes)
    if '0' not in sv_dict.keys(): sv_dict['0'] = 0.0
    if '1' not in sv_dict.keys(): sv_dict['1'] = 0.0

    # Standardization II (first |0> then |1>)
    sorted_dict = {}
    for key in sorted(sv_dict.keys()):
        sorted_dict[key] = sv_dict[key]
    
    sv_dict = sorted_dict
    
    return tuple(sv_dict.values())

def plot_initial_circles(ax, padding):
    '''Plotting the empty white initial circles per each component'''
    # Initial circles radius calculation
    initial_radius = 1 / math.sqrt(math.pi)
    
    # Initial circles centers calculation
    centers = ((0, 0), ((2 * initial_radius) + padding, 0))

    # Compontent |0> circle plotting
    circulo_0 = plt.Circle(centers[0], initial_radius, color='black', fill=False)
    ax.add_patch(circulo_0)

    # Compontent |1> circle plotting
    circulo_1 = plt.Circle(centers[1], initial_radius, color='black', fill=False)
    ax.add_patch(circulo_1)

    # Plot labels
    ax.text(0, -1.5 * initial_radius, '|0>', ha='center', va='center')
    ax.text((2 * initial_radius) + 0.25, -1.5 * initial_radius, '|1>', ha='center', va='center')

    # Return centers and initial radius for later computations
    return centers, initial_radius

def pick_normalized_color(phase):
    '''Get a color corresponding to the given phase'''
    norm = clr.Normalize(0, 2*math.pi)
    custom_cmap = plt.get_cmap('hsv')
    return clr.to_hex(custom_cmap(norm(phase)))

def plot_inner_circles(ax, centers, amplitudes, relative_phase):
    '''Plotting the inner circles with area propotional to the amplitude'''
    # Inner circles radius calculation
    inner_radius = (abs(amplitudes[0]) / math.sqrt(math.pi), abs(amplitudes[1]) / math.sqrt(math.pi))

    # Compontent |0> inner circle plotting in adequate center
    circulo_0 = plt.Circle(centers[0], inner_radius[0], color=pick_normalized_color(0))
    ax.add_patch(circulo_0)

    # Compontent |1> inner circle plotting in adequate center
    circulo_1 = plt.Circle(centers[1], inner_radius[1], color=pick_normalized_color(relative_phase))
    ax.add_patch(circulo_1)

def get_relative_phase(amplitudes):
    '''Calculates and standardices the relative phase for the amplitudes'''
    # Previous reasoning computation
    relative_phase = cmath.phase(amplitudes[1]) - cmath.phase(amplitudes[0])

    # Counterclockwise angle rotation
    if relative_phase < 0: 
        relative_phase += (2 * math.pi)

    return relative_phase

def plot_radius(ax, centers, amplitudes, initial_radius):
    '''Plotting both radios representing the relative phase'''
    # Calculate relative phase
    relative_phase = get_relative_phase(amplitudes)
    
    # Component |0> radius plotting
    ax.plot([centers[0][0], centers[0][0] + initial_radius], [centers[0][1], centers[0][1]], color='black')
    
    # Component |1> radius plotting
    a = centers[1][0] + (initial_radius * math.cos(relative_phase))
    b = centers[1][1] + (initial_radius * math.sin(relative_phase))
    ax.plot([centers[1][0], a], [centers[1][1], b], color='black')

    return relative_phase

def prepare_statevector():
    '''Method for preparing state i|1> (phase)'''
    qc = QuantumCircuit(1,1)
    qc.y(0)
    qc.save_statevector()
    qc.measure(0,0)

    sim = AerSimulator()
    job = execute(qc, sim, shots=1024)
    results = job.result()
    return results.get_statevector()

def circle_notation(sv):
    '''Main method with the final algorithm for plotting'''
    # Set the figure
    fig, ax = plt.subplots(figsize=(3,1.5))
    ax.set_axis_off()
    padding = 0.25

    # Main steps
    amplitudes = get_amplitudes(sv)
    centers, initial_radius = plot_initial_circles(ax, padding)
    relative_phase = plot_radius(ax, centers, amplitudes, initial_radius)
    plot_inner_circles(ax, centers, amplitudes, relative_phase)

    # Adjust figure limits and circles padding
    ax.set_xlim(-(initial_radius) , 3 * initial_radius + padding)
    ax.set_ylim(-initial_radius, initial_radius)
    plt.show()

if __name__ == '__main__':
    sv = prepare_statevector()
    circle_notation(sv)
