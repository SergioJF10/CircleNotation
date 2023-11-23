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

    if '0' not in sv_dict.keys(): sv_dict['0'] = 0.0
    if '1' not in sv_dict.keys(): sv_dict['1'] = 0.0
    
    sorted_dict = {}
    for key in sorted(sv_dict.keys()):
        sorted_dict[key] = sv_dict[key]
    
    sv_dict = sorted_dict
    
    return tuple(sv_dict.values())

def plot_initial_circles(ax, padding):
    '''Plotting the empty white initial circles per each component'''
    # Calculamos el radio de las circunferencias iniciales
    initial_radius = 1 / math.sqrt(math.pi)
    
    # Calculamos los centros de las circunferencias iniciales
    centers = ((0, 0), ((2 * initial_radius) + padding, 0))

    # Dibujamos el círculo del componente |0>
    circulo_0 = plt.Circle(centers[0], initial_radius, color='black', fill=False)
    ax.add_patch(circulo_0)

    # Dibujamos el círculo del componente |1>
    circulo_1 = plt.Circle(centers[1], initial_radius, color='black', fill=False)
    ax.add_patch(circulo_1)

    # Dibujamos las labels
    ax.text(0, -1.5 * initial_radius, '|0>', ha='center', va='center')
    ax.text((2 * initial_radius) + 0.25, -1.5 * initial_radius, '|1>', ha='center', va='center')
    
    return centers, initial_radius # Devolvemos los centros y el radio porque nos serán útiles después

def pick_normalized_color(phase):
    '''Get a color corresponding to the given phase'''
    norm = clr.Normalize(0, 2*math.pi)
    custom_cmap = plt.get_cmap('hsv')
    return clr.to_hex(custom_cmap(norm(phase)))

def plot_polar_colorbase():
    '''Plot a colorbase for showing the phase-color mapping'''
    display_axes = fig.add_axes([0.1,0.1,0.8,0.8], projection='polar') # polar es para que sea en círculo
    norm = clr.Normalize(0.0, 2*math.pi)
    cb = clb.ColorbarBase(display_axes, cmap=plt.get_cmap('hsv'), norm=norm, orientation='horizontal')

    # no box grid
    cb.outline.set_visible(False)
    # plot labels in radians
    ticks_position = plt.xticks()[0]
    radian_ticks = xL=['0',r'$\frac{\pi}{4}$',r'$\frac{\pi}{2}$',r'$\frac{3\pi}{4}$',\
            r'$\pi$',r'$\frac{5\pi}{4}$',r'$\frac{3\pi}{2}$',r'$\frac{7\pi}{4}$']
    plt.xticks(ticks_position, radian_ticks)
    # inner white ring
    display_axes.set_ylim(-2,1)
    plt.show()

def plot_inner_circles(ax, centers, amplitudes, relative_phase):
    '''Plotting the inner circles with area propotional to the amplitude'''
    # Calcular los radios de los círculos internos
    inner_radius = (abs(amplitudes[0]) / math.sqrt(math.pi), abs(amplitudes[1]) / math.sqrt(math.pi))

    # Dibujamos el círculo interno del componente |0> en el centro correspondiente
    circulo_0 = plt.Circle(centers[0], inner_radius[0], color=pick_normalized_color(0))
    ax.add_patch(circulo_0)

    # Dibujamos el círculo interno del componente |1> en el centro correspondiente
    circulo_1 = plt.Circle(centers[1], inner_radius[1], color=pick_normalized_color(relative_phase))
    ax.add_patch(circulo_1)

def plot_radius(ax, centers, amplitudes, initial_radius):
    '''Plotting both radios representing the relative phase'''
    # Calculamos la fase relativa
    relative_phase = abs(cmath.phase(amplitudes[0]) - cmath.phase(amplitudes[1]))
    
    # Dibujamos el radio del componente |0>
    ax.plot([centers[0][0], centers[0][0] + initial_radius], [centers[0][1], centers[0][1]], color='black')
    
    # Dibujamos el radio del componente |1>
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
    # Configuramos la figura
    fig, ax = plt.subplots(figsize=(3,1.5))
    ax.set_axis_off()
    padding = 0.25

    # Pasos principales
    amplitudes = get_amplitudes(sv)
    centers, initial_radius = plot_initial_circles(ax, padding)
    relative_phase = plot_radius(ax, centers, amplitudes, initial_radius)
    plot_inner_circles(ax, centers, amplitudes, relative_phase)

    # Ajustamos los límites de la figura a los radios y el relleno entre círculos (padding)
    ax.set_xlim(-(initial_radius) , 3 * initial_radius + padding)
    ax.set_ylim(-initial_radius, initial_radius)
    plt.show()

if __name__ == '__main__':
    sv = prepare_statevector()
    circle_notation(sv)
