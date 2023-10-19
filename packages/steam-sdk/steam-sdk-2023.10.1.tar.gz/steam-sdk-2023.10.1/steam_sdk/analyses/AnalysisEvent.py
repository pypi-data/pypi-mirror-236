import csv
import os
import re

import pandas as pd

'''
This file contains helper functions for certain analyses of steam-models-dev that:
 - do not need an instance but are static
 - do not fit in the AnalysisSTEAM.py because their use-case is not as general usable as the functions in the AnalysisSTEAM.py
'''

#TODO: Include further functions from AnalysisSteam.py here and maybe try to summarize some of them as the functionality is concruent for some of them
def find_n_magnets_in_circuit(filename: str, circuit_name: str):
    '''
    ** Find the number of magnets present in the current circuit by reading the value from a csv file **
    :param filename: path to the input csv file
    :param circuit_name: string that defines the name of the circuit (the code will look into the row that bears this name)
    :return string defining the number of magnets in the circuit
    '''
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['circuit'] == circuit_name:
                return row['NumberOfMagnets']
        return None


def find_IPQ_circuit_type_from_IPQ_parameters_table(filename: str , circuit_name: str):
    '''
    ** This function returns the circuit type e.g. IPQ_RQ4_4_2xRPHH_4xMQY for a specific circuitname e.g. RQ4.L8 from a table
    :param filename: path to the IPQ_circuit_parameters.csv file
    :param circuit_name: string that defines the name of the circuit (the code will look into the row that bears this name)
    '''
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['circuit'] == circuit_name:
                return row['circuit_type']
        return None


def get_circuit_name_from_eventfile(event_file: str):
    '''
    ** This function returns the circuit name for a given event file by opening it and reading the entry "Circuit Name"
    :param event_file: eventfile from the LHC postmortem database e.g. ROD.A23B1_FPA-2022-04-14-10h39-2022-04-14-11h04.csv
    '''
    with open(event_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_entry = row.get("Circuit Name")
            if first_entry:
                return first_entry


def get_circuit_family_from_circuit_name(circuit_name: str):
    '''
    ** This function returns the the circuit family for a given circuit name by a simple logic without any additional files necessary
    :param circuit_name: name of the circuit e.g. RQ.A12
    '''
    if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
        return "60A"
    elif circuit_name.startswith("RD"):
        return "IPD"
    elif circuit_name.startswith("RQX"):
        return "RQX"
    elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
        return "IPQ"
    elif circuit_name.startswith(("RQT12", "RQT13", "RQS", "RSS", "RQTL7", "RQTL8", "RQTL10", "RQTL11", "RCBX", "RQSX3", "RCS", "ROD", "ROF", "RSD", "RSF", "RQTL9", "RQTD", "RQTF", "RCD", "RCO", "RC.")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 8):
        return "600A"
    elif circuit_name.startswith("RQ"):
        return "RQ"
    elif circuit_name.startswith(("RCBY", "RCBC", "RCTX")):
        return "80-120A"
    elif circuit_name.startswith("RB"):
        return "RB"


def create_two_csvs_from_odd_and_even_rows(input_file_name, output_odd_file_name: str = 'output_odd.csv', output_even_file_name:str = 'output_even.csv'):
    '''
    ** This function creates two csv files from the odd and the even rows of a given csv file and returns the filenames of the respective files created
    :param imput_file_name: path of the input csv file
    '''
    # Create empty lists to hold the odd and even rows
    odd_rows = []
    even_rows = []

    # Open the input CSV file and read in the rows
    with open(input_file_name, 'r') as input_file:
        reader = csv.reader(input_file)

        # Save the header row
        header = next(reader)

        # Loop over the remaining rows and append them to the odd or even list
        for i, row in enumerate(reader):
            if i % 2 == 0:
                even_rows.append(row)
            else:
                odd_rows.append(row)

    # Write the odd and even rows to separate output files'
    with open(output_odd_file_name, 'w', newline='') as output_odd_file:
        writer_odd = csv.writer(output_odd_file)
        writer_odd.writerow(header)
        writer_odd.writerows(odd_rows)

    with open(output_even_file_name, 'w', newline='') as output_even_file:
        writer_even = csv.writer(output_even_file)
        writer_even.writerow(header)
        writer_even.writerows(even_rows)

    # Return a list of the output file names
    return [output_even_file_name, output_odd_file_name]

def get_number_of_apertures_from_circuit_family_name(circuit_family_name: str):
    '''
    **This function returns the number of apertures for a given circuit name by a simple logic
    :param circuit_family_name: This parameter defines the circuit family name which determines the number apertures
    '''
    #circuit_family_name = get_circuit_family_from_circuit_name(circuit_name)
    if circuit_family_name in ["IPQ", "RB"]:
        return 2
    else:
        return 1

def get_number_of_quenching_magnets_from_layoutdetails(position: str, circuit_family_name: str,library_path):
    '''
    **This function returns the #Electric_circuit value of a magnet based on its position argument which is the text
    **after the dot in the entries of the 'Magnet' column of  the LayoutDetails.csv
    :param position: position of the magnet
    :param circuit_family_name: family name of the circuit
    :library_path: absolute path of steam_models
    '''
    df = pd.read_csv(
        os.path.join(library_path, 'circuits', 'circuit_parameters', f"{circuit_family_name}_LayoutDetails.csv"))
    mask = df['Magnet'].str.split('.').str[1] == position
    result = df.loc[mask, '#Electric_circuit'].iloc[0]
    return result

def get_magnet_types_list(number_of_magnets: int, simulation_name: str):
    """
    **Generates a list representing types of magnets based on simulation parameters.
    :param number_of_magnets: The total number of magnets in the simulation.
    :param simulation_name: The name of the simulation.

    Explanation:
        - If the simulation involves 4 magnets and starts with "RQX", the list
          will be [1, 2, 2, 1]. This pattern is specific to this simulation case.
        - If the simulation starts with "IPQ" and involves 2 magnets, the list
          will be [1, 2].
        - If the simulation starts with "RB", all magnets will be of type 1.
        - If the simulation name is not "RQX", "IPQ" or "RB", For specific numbers of magnets (154, 13, 8, 77, 6, 12, 11, 10, 9, 4, 2),
          the list will consist of one type 1 magnet followed by (number_of_magnets - 1)
          type 2 magnets.
        - For all other cases, the default magnet type is 1 for all magnets.
    Returns:
            List[int]: A list representing types of magnets, where each element indicates the type of the corresponding magnet in the simulation.
    """
    if number_of_magnets == 4 and simulation_name.startswith("RQX"): #to be improved
        return [1, 2, 2, 1]
    elif simulation_name.startswith("IPQ") and number_of_magnets == 2:
        return [1, 2]
    elif simulation_name.startswith("RB"):
        return [1] * number_of_magnets
    elif number_of_magnets in [154, 13, 8, 77, 6, 12, 11, 10, 9, 4, 2]:
        return [1] + [2] * (number_of_magnets - 1)
    else:
        return [1] * number_of_magnets

def get_number_of_magnets(circuit_name: str, simulation_name: str, circuit_type: str):
    """
    **Determines the number of magnets in a specific circuit based on circuit name and type, and simulation name.
    :param circuit_name: The name of the circuit.
    :param simulation_name: The name of the simulation.
    :param circuit_type: The type of the circuit.

    Returns:
        int: The number of magnets in the specified circuit.

    Algorithm:
        - If the circuit type is "RCS" or "RB", returns 154.
        - If the circuit type is "RCD" or "RCO", returns 77.
        - If the circuit name starts with "RQ6." and has a length of 8, returns 6.
        - If the circuit name starts with "RQS.R", "RQS.L", or "RQTL9", returns 2.
        - If the circuit name starts with "RQS.A", "RSS", or "RQX", returns 4.
        - If the circuit name starts with "RQTD" or "RQTF", returns 8.
        - If the circuit family name is "60A", "IPD", "80-120A", or "600A", returns 1.
        - If the circuit type is "RQ_47magnets", returns 47.
        - If the circuit type is "RQ_51magnets", returns 51.
        - If the circuit family name is "IPQ", calculates the number of magnets based on the simulation name.

    Note:
        - For "IPQ" circuits, the function extracts a numeric value from the simulation name and divides it by 2 to determine the number of magnets.
    """
    circuit_family_name = get_circuit_family_from_circuit_name(circuit_name)
    #circuit_type = self.__get_circuit_type(circuit_name, self.library_path)
    if circuit_type in ["RCS", "RB"]:
        return 154
    elif circuit_type in ["RCD", "RCO"]:
        return 77
    elif circuit_name.startswith("RQ6.") and len(circuit_name) == 8:
        return 6
    elif circuit_name.startswith(("RQS.R", "RQS.L", "RQTL9")):
        return 2
    elif circuit_name.startswith(("RQS.A", "RSS", "RQX")):
        return 4
    elif circuit_name.startswith(("RQTD", "RQTF")):
        return 8
    elif circuit_family_name in ["60A", "IPD", "80-120A", "600A"]:
        return 1
    elif circuit_type == "RQ_47magnets":
        return 47
    elif circuit_type == "RQ_51magnets":
        return 51
    elif circuit_family_name == "IPQ":
        return int(int(re.search(r'_(\d+)_', simulation_name).group(1))/2)

def get_magnet_name(circuit_name: str, simulation_name: str, circuit_type: str):
    '''
    **Function that determines the magnet name(s) based on the provided circuit name, simulation name, and circuit type.
    :param circuit_name: The name of the circuit.
    :param simulation_name: The name of the simulation.
    :param circuit_type: The type of the circuit.

    Returns:
        str or list: The name of the magnet(s) corresponding to the given circuit and simulation.
        If multiple magnet names are possible, a list is returned.
    '''
    #assert (simulation_name == self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_name)
    #assert (circuit_type == self.__get_circuit_type(circuit_name, self.library_path))
    #assert (True == False)

    if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
        return "MCBH"
    elif circuit_name.startswith("RD"):
        #circuit_type = self.__get_circuit_type(circuit_name, self.library_path)
        magnet_dict = {"RD1": "MBX", "RD2": "MBRC", "RD3": "MBRS", "RD4": "MBRB"}
        return magnet_dict.get(circuit_type, "")
    elif circuit_name.startswith("RQX"):
        return ["MQXA", "MQXB"]
    elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
        magnet_dict = {"IPQ_RQ4_2_2xRPHH_2xMQY": "MQY", "IPQ_RQ4_4_2xRPHH_4xMQY": ["MQY", "MQY"], "IPQ_RQ5_2_2xRPHGB_2xMQML": "MQML", "IPQ_RQ5_2_2xRPHH_2xMQY": "MQY", "IPQ_RQ5_4_2xRPHGB_4xMQM": ["MQM", "MQM"], "IPQ_RQ5_4_2xRPHH_4xMQY": ["MQY", "MQY"], "IPQ_RQ6_2_2xRPHGB_2xMQML": "MQML", "IPQ_RQ6_2_2xRPHGB_2xMQY": "MQY", "IPQ_RQ6_4_2xRPHGB_2xMQM_2xMQML": ["MQM", "MQML"], "IPQ_RQ7_2_2xRPHGA_2xMQM": "MQM", "IPQ_RQ7_4_2xRPHGA_4xMQM": ["MQM", "MQM"], "IPQ_RQ8_2_2xRPHGA_2xMQML": "MQML", "IPQ_RQ9_4_2xRPHGA_2xMQM_2xMQMC": ["MQM", "MQMC"], "IPQ_RQ10_2_2xRPHGA_2xMQML": "MQML"}
        return magnet_dict.get(simulation_name, "")
    elif circuit_name.startswith("RQ6.") and len(circuit_name) == 8:
        return ["MQTLH", "MQTLH_quenchback"]
    elif circuit_name.startswith(("RQTL7", "RQTL8", "RQTL10", "RQTL11")):
        return "MQTLI"
    elif circuit_name.startswith("RQTL9"):
        return ["MQTLI", "MQTLI_quenchback"]
    elif circuit_name.startswith("RQSX3"):
        return "MQSX"
    elif circuit_name.startswith("RQS"):
        return ["MQS", "MQS_quenchback"]
    elif circuit_name.startswith(("RQT12", "RQT13")):
        return "MQT"
    elif circuit_name.startswith(("RQTD", "RQTF")):
        return ["MQT", "MQT_quenchback"]
    elif circuit_name.startswith("RQ"):
        return "MQ"
    elif circuit_name.startswith("RCBY"):
        return "MCBYH"
    elif circuit_name.startswith("RCBC"):
        return "MCBCH"
    elif circuit_name.startswith("RCS"):
        return ["MCS", "MCS_quenchback"]
    elif circuit_name.startswith("RB"):
        return "MB"
    elif circuit_name.startswith("RCBX"):
        return ["MCBXH", "MCBXV"]
    elif circuit_name.startswith("RSS"):
        return ["MSS", "MSS_quenchback"]
    elif circuit_name.startswith(("ROD", "ROF")):
        return ["MO", "MO_quenchback"]
    elif circuit_name.startswith(("RSD", "RSF")):
        return ["MS", "MS_quenchback"]
    elif simulation_name == "RCD":
        return ["MCD", "MCD_quenchback"]
    elif simulation_name == "RCO":
        return ["MCO", "MCO_quenchback"]

def get_circuit_type(circuit_name: str, library_path, simulation_name: str = None):
    """
    Determines the circuit type based on the provided circuit name, library path, and optional simulation name.
    The simulation name is only needed in case of RCD and RCO magnets

    :param circuit_name: The name of the circuit.
    :param library_path: The path to the steam models.
    :param simulation_name: The name of the simulation (optional).
    :return: The determined circuit type as a string.
    """
    # if simulation_name:
    #     assert(self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_name == simulation_name)
    #     #assert(True == False)
    if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
        return "RCB"
    elif circuit_name.startswith(("RD1", "RD2", "RD3", "RD4")):
        return {"RD1": "RD1", "RD2": "RD2", "RD3": "RD3", "RD4": "RD4"}.get(circuit_name[:3], "No match found")
    elif circuit_name.startswith("RQX"):
        return "RQX"
    elif circuit_name.startswith(("RQ4", "RQ5", "RQ6", "RQ7", "RQ8", "RQ9", "RQ10")):
        return circuit_name.split(".")[0]
    elif circuit_name.startswith(("RQT12", "RQT13")):
        return "RQT_12_13"
    elif circuit_name.startswith(("RQTL7", "RQTL8", "RQTL10", "RQTL11")):
        return "RQTL_7_8_10_11"
    elif circuit_name.startswith("RQTL9"):
        return "RQTL9"
    elif circuit_name.startswith(("RQTD", "RQTF")):
        return "RQT"
    elif circuit_name.startswith("RQSX3"):
        return "RQSX3"
    elif circuit_name.startswith("RQS"):
        return "RQS"
    elif circuit_name.startswith("RQ."):
        circuit_name_temp = circuit_name.replace(".", "D_")
        magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/RQ_circuit_parameters.csv"), circuit_name_temp)
        return f"RQ_{magnet_number}magnets"
    elif circuit_name.startswith("RCS"):
        return "RCS"
    elif circuit_name.startswith("RB"):
        return "RB"
    elif circuit_name.startswith("RCBX"):
        return "RCBX"
    elif circuit_name.startswith("RCBC"):
        return "RCBC"
    elif circuit_name.startswith("RCBY"):
        return "RCBY"
    elif circuit_name.startswith("RSS"):
        return "RSS"
    elif circuit_name.startswith(("RSD")):
        magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
        return f"RSD_{magnet_number}magnets"
    elif circuit_name.startswith(("RSF")):
        magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
        return f"RSF_{magnet_number}magnets"
    elif circuit_name.startswith(("RO")):
        magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
        return f"RO_{magnet_number}magnets"
    elif simulation_name == "RCD": #improvement pending
        return "RCD"
    elif simulation_name == "RCO": #improvement pending
        return "RCO"