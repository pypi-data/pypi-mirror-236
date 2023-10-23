from strengths.rdsystem import RDSystem, rdsystem_from_dict, rdsystem_to_dict
from strengths.units import *
from strengths.rdscript import RDScript
from strengths import engine_collection

def simulate_script(
        script,
        engine = engine_collection.euler_engine(),
        print_progress=False,
        ) :
    """
    Simulates the evolution in time of a reaction diffusion system.
    it wraps the reaction-diffusion simulation process using a RDSimulationEngine.

    :param script: the script of the simulation to be run.
    :type script: RDScript

    :param engine: the simulation engine that should handle the simulation.
        see the documentation or the engine_collection submodule for more information
        on the engines preinstalled with strengths. (default = engine_collection.euler_engine())
    :type engine: RDSimulationEngineBase derived class

    :param print_progress: if true, the progression of the simulation (percentage) is printed
        at frequently.
    :type print_progress: bool
    
    :return: simulation output.
    :rtype: RDSimulationOutput
    """

    #initialization phase
    res = engine.setup(script)

    if res == 1 :
        raise Exception("Invalid option argument : \""+engine.get_option()+"\".")
    elif res == 2 :
        raise Exception("Invalid boundary conditions.")
        
    if print_progress :
        print("0 %", end="")

    # loop phase
    continue_simulation = True
    while continue_simulation :
        continue_simulation = engine.run(1000)
        if print_progress :
            print("\r" + str(engine.get_progress()) + " %", end="")

    # output phase
    output = engine.get_output()

    # finalize
    engine.finalize()
        
    return output


def simulate(
        system,
        t_sample,
        engine = engine_collection.euler_engine(),
        print_progress=False,
        **keyword_arguments
        ) :
    """
    Simulates the evolution in time of a reaction diffusion system.
    it wraps the reaction-diffusion simulation process using a RDSimulationEngine.

    :param engine: the simulation engine that should handle the simulation.
        see the documentation or the engine_collection submodule for more information
        on the engines preinstalled with strengths. (default = engine_collection.euler_engine())
    :type engine: RDSimulationEngineBase derived class

    :param print_progress: if true, the progression of the simulation (percentage) is printed
        at frequently.
    :type print_progress: bool
    
    Other parameters corresond to the remaining RDScript properties, and have the same default values :
        
    * time_step = 1e-3
    * sampling_policy = "on_t_sample"
    * sampling_interval = 1
    * t_max = "default"
    * rng_seed = None
    * units_system = UnitsSystem()

    :return: simulation output
    :rtype: RDSimulationOutput
    """

    d = dict(keyword_arguments)
    d["system"] = system
    d["t_sample"] = t_sample
    
    script = RDScript(**d)

    output = simulate_script(script = script, 
                             engine = engine, 
                             print_progress = print_progress)
        
    return output
