
from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.analyses.AnalysisEvent import find_IPQ_circuit_type_from_IPQ_parameters_table, \
    get_circuit_name_from_eventfile, get_circuit_type
from steam_sdk.data.DataAnalysis import ModifyModelMultipleVariables, SetUpFolder, MakeModel, ParsimEvent, DefaultParsimEventKeys, RunSimulation
import os
import ruamel.yaml


class AnalysisEventLHC(AnalysisSTEAM):
    '''
          ** This is a class that contains helper functions for the analysis of an LHC event**
    '''

    #AnalysisEventLHC is initialized with a dictionary that can be optionally left empy
    def __init__(self, settings_file_path, dict_settings_paths: dict = None ):
        # Define default settings paths
        super().__init__()

        # Unpack Parameters
        self.settings_file_path = settings_file_path
        self.dict_settings_paths = dict_settings_paths

        # key_template_analysis that contains only the keys needed for an LHC Event Analysis
        self.default_dict_settings_paths = {
            'library_path': os.path.abspath(os.path.join(os.getcwd(), "..", "..", "..", "steam_models")),
            'PSPICE_path': None,
            'XYCE_path': None,
            'PSPICE_library_path': None,
            'local_PSPICE_folder': None,
            'local_XYCE_folder': None,
            'output_directory_yaml_files': os.path.join(os.getcwd(), 'output', 'yaml_files'),
            'output_directory_event_files': os.path.join(os.getcwd(), 'output', 'event_files')
        }

        # If entries have been defined by the user, overwrite the default values with the dict, provided by the user
        if self.dict_settings_paths:
            for key, _ in self.dict_settings_paths.items():
                self.default_dict_settings_paths[key] = self.dict_settings_paths[key]

        # Fill up non user specific keys with keys from the settings system.yaml
        # Load YAML data from the file
        with open(self.settings_file_path, 'r') as yaml_file:
            settings_file_yaml_data = ruamel.yaml.safe_load(yaml_file)

        # Update dictionary values with loaded data
        for key, _ in self.default_dict_settings_paths.items():
            if key in settings_file_yaml_data and self.default_dict_settings_paths[key] is None:
                self.default_dict_settings_paths[key] = settings_file_yaml_data[key]
                print("Changed default dict settings with csv")

        # Now, dict_settings_paths contains the updated values from the YAML file
        print(self.default_dict_settings_paths)

        # Check and update settings
        for name, _ in self.default_dict_settings_paths.items():
            if hasattr(self.settings, name):
                print(f"Found {name} in settings")
                value = self.default_dict_settings_paths[name]
                setattr(self.settings, name, value)
                if value:
                    print('{}: {}. Added.'.format(name, value))
            elif name == 'library_path':
                self.library_path = self.default_dict_settings_paths['library_path']
            else:
                print('{}: not found in the settings. Skipped.'.format(name))

        # Update data_analysis module settings
        self.data_analysis.WorkingFolders.library_path = self.default_dict_settings_paths['library_path']
        self.data_analysis.PermanentSettings.PSPICE_path = self.default_dict_settings_paths['PSPICE_path']
        self.data_analysis.PermanentSettings.XYCE_path = self.default_dict_settings_paths['XYCE_path']
        self.data_analysis.PermanentSettings.local_PSPICE_folder = self.default_dict_settings_paths['local_PSPICE_folder']
        self.data_analysis.PermanentSettings.local_XYCE_folder = self.default_dict_settings_paths['local_XYCE_folder']



    def steam_analyze_lhc_event(self, settings_file_path:str, input_csv_file: str, flag_run_software: bool, software: str,dict_settings_paths: dict, file_counter: int):
        aSTEAM = AnalysisEventLHC(settings_file_path,dict_settings_paths)

        # # Assign the keys read either from permanent-settings or local-settings TODO: later in inititalization of subclass
        # for name, _ in dict_settings_paths.items():
        #     if name in  aSTEAM.settings.__dict__:
        #         print(f"Found {name} in settings")
        #         value = dict_settings_paths[name]
        #         aSTEAM.setAttribute(aSTEAM.settings, name, value)
        #         if value:
        #             print('{} : {}. Added.'.format(name, value))
        #     elif name == 'library_path':
        #         aSTEAM.library_path = dict_settings_paths['library_path']
        #     else:
        #         print('{}: not found in the settings. Skipped.'.format(name))
        #
        # aSTEAM.data_analysis.WorkingFolders.library_path = dict_settings_paths['library_path']
        # aSTEAM.data_analysis.PermanentSettings.PSPICE_path = dict_settings_paths['PSPICE_path']
        # aSTEAM.data_analysis.PermanentSettings.XYCE_path = dict_settings_paths['XYCE_path']
        # aSTEAM.data_analysis.PermanentSettings.local_PSPICE_folder = dict_settings_paths['local_PSPICE_folder']
        # aSTEAM.data_analysis.PermanentSettings.local_XYCE_folder = dict_settings_paths['local_XYCE_folder']
        #

        if software == 'PSPICE':
            local_folder = aSTEAM.settings.local_PSPICE_folder
            print(f"Changed local folder to {local_folder}")
        elif software == 'XYCE':
            local_folder = aSTEAM.settings.local_XYCE_folder
            print(f"Changed local folder to {local_folder}")

        #print(input_csv_file)

        circuit_name = get_circuit_name_from_eventfile(event_file=input_csv_file)
        if circuit_name.startswith("RCD"):
            aSTEAM.analyze_RCD_RCO_event(os.path.join(os.getcwd(), input_csv_file), local_folder, flag_run_software, software, file_counter)
        elif circuit_name.startswith(("RD1", "RD2", "RD3", "RD4")):
            circuit_type = "IPD"
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter)
        elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
            circuit_type = find_IPQ_circuit_type_from_IPQ_parameters_table(os.path.join( aSTEAM.library_path, f"circuits/circuit_parameters/IPQ_circuit_parameters.csv"), input_csv_file.split("\\")[-1].split("_")[0])
            print(circuit_type)
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter)
        else:
            circuit_type = get_circuit_type(circuit_name,  aSTEAM.library_path)
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter)

    def analyze_circuit_event(self, input_csv_file: str, local_folder: str,circuit_type: str, flag_run_software: bool, software: str, file_counter: int):
        #file_counter = 1
        #file_name_analysis = os.path.join(os.getcwd(), "analysisSTEAM_settings.yaml") #file containing settings paths
        unique_identifier_event = os.path.splitext(os.path.basename(input_csv_file))[0]

        output_directory_yaml_files = self.default_dict_settings_paths['output_directory_yaml_files']
        output_directory_event_files = self.default_dict_settings_paths['output_directory_event_files']

        yaml_file_name = f'Infile_{software}_{unique_identifier_event}_{file_counter}.yaml'
        event_file_name = f'Eventfile_{software}_{unique_identifier_event}_{file_counter}.csv'

        path_output_yaml_file = os.path.join(output_directory_yaml_files,yaml_file_name)
        path_output_event_csv = os.path.join(output_directory_event_files,event_file_name)

        self.data_analysis.AnalysisStepDefinition = {
            'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name=circuit_type, software=[software]),
            'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data=circuit_type,
                                       case_model='circuit', software=[software], simulation_name=None,
                                       simulation_number=None, flag_build=True, flag_dump_all=False, verbose=False,
                                       flag_plot_all=False, flag_json=False),
            'modifyModel_probe': ModifyModelMultipleVariables(type='ModifyModelMultipleVariables', model_name='BM',
                                           variables_to_change=['PostProcess.probe.probe_type'],
                                           variables_value=[['CSDF']], software=[software], simulation_name=None,
                                           simulation_numbers=[]),
            'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file,
                                          path_output_event_csv=path_output_event_csv, path_output_viewer_csv=None,
                                          simulation_numbers=[file_counter], model_name='BM', case_model='circuit',
                                          simulation_name=circuit_type, software=[software], t_PC_off=None,
                                          rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[],
                                          dict_QH_circuits_to_QH_strips={},
                                          default_keys=DefaultParsimEventKeys(local_LEDET_folder=None,
                                                                              path_config_file=None, default_configs=[],
                                                                              path_tdms_files=None,
                                                                              path_output_measurement_files=None,
                                                                              path_output=local_folder)),
            'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name=circuit_type, simulation_numbers=[file_counter])}

        self.output_path = local_folder
        if software == 'PSPICE':
            self.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            self.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software== False:
            self.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'modifyModel_probe', 'runParsimEvent']
        else:
            self.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'modifyModel_probe', 'runParsimEvent', 'run_simulation']

        if software == 'PSPICE':
            list_output_file = [os.path.join(self.settings.local_PSPICE_folder, f'{circuit_type}', f'{file_counter}',
                                         f'{circuit_type}.cir')]
        elif software == 'XYCE':
            list_output_file = [os.path.join(self.settings.local_XYCE_folder, f'{circuit_type}', f'{file_counter}',
                                         f'{circuit_type}.cir')]

        if os.path.exists(path_output_yaml_file): os.remove(path_output_yaml_file)
        for file in list_output_file:
            if os.path.exists(file): os.remove(file)

        # act
        #print(self.data_analysis.PermanentSettings.PSPICE_path)
        self.write_analysis_file(path_output_file=path_output_yaml_file)
        self.run_analysis(verbose= True)



    def analyze_RCD_RCO_event(self, input_csv_file: str, local_folder: str, flag_run_software: bool, software: str, file_counter: int):

        unique_identifier_event = os.path.splitext(os.path.basename(input_csv_file))[0]

        output_directory_yaml_files = self.default_dict_settings_paths['output_directory_yaml_files']
        output_directory_event_files = self.default_dict_settings_paths['output_directory_event_files']

        yaml_file_name = f'Infile_{software}_{unique_identifier_event}_{file_counter}.yaml'
        event_file_name_RCO = f'Eventfile_RCO_{software}_{unique_identifier_event}_{file_counter}.csv'
        event_file_name_RCD = f'Eventfile_RCD_{software}_{unique_identifier_event}_{file_counter}.csv'

        path_output_yaml_file = os.path.join(output_directory_yaml_files,yaml_file_name)
        path_output_event_RCO_csv = os.path.join(output_directory_event_files, event_file_name_RCO)
        path_output_event_RCD_csv = os.path.join(output_directory_event_files, event_file_name_RCD)

        # arrange
        file_name_analysis = os.path.join(os.getcwd(), "analysisSTEAM_settings.yaml") #file containing settings paths
        aSTEAM_1 = AnalysisSTEAM(file_name_analysis=file_name_analysis)
        if software == 'PSPICE':
            aSTEAM_1.settings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_1.settings.local_XYCE_folder = local_folder
        aSTEAM_1.data_analysis.AnalysisStepDefinition = {'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name='RCO', software=[software]), 'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data='RCO', case_model='circuit', software=[software], simulation_name=None, simulation_number=None, flag_build=True, flag_dump_all=False, verbose=False, flag_plot_all=False, flag_json=False), 'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file, path_output_event_csv=path_output_event_RCO_csv, path_output_viewer_csv=None, simulation_numbers=[file_counter], model_name='BM', case_model='circuit', simulation_name='RCO', software=[software], t_PC_off=None, rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[], dict_QH_circuits_to_QH_strips={}, default_keys=DefaultParsimEventKeys(local_LEDET_folder=None, path_config_file=None, default_configs=[], path_tdms_files=None, path_output_measurement_files=None, path_output=local_folder)), 'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name='RCO', simulation_numbers=[file_counter])}
        aSTEAM_1.output_path = local_folder
        if software == 'PSPICE':
            aSTEAM_1.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_1.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software == False:
            aSTEAM_1.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent']
        else:
            aSTEAM_1.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent', 'run_simulation']

        aSTEAM_2 = AnalysisSTEAM(file_name_analysis=file_name_analysis)
        if software == 'PSPICE':
            aSTEAM_2.settings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_2.settings.local_XYCE_folder = local_folder
        aSTEAM_2.data_analysis.AnalysisStepDefinition = {'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name='RCD', software=[software]), 'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data='RCD', case_model='circuit', software=[software], simulation_name=None, simulation_number=None, flag_build=True, flag_dump_all=False, verbose=False, flag_plot_all=False, flag_json=False), 'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file, path_output_event_csv=path_output_event_RCD_csv, path_output_viewer_csv=None, simulation_numbers=[file_counter], model_name='BM', case_model='circuit', simulation_name='RCD', software=[software], t_PC_off=None, rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[], dict_QH_circuits_to_QH_strips={}, default_keys=DefaultParsimEventKeys(local_LEDET_folder=None, path_config_file=None, default_configs=[], path_tdms_files=None, path_output_measurement_files=None, path_output=local_folder)), 'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name='RCD', simulation_numbers=[file_counter])}
        aSTEAM_2.output_path = local_folder
        if software == 'PSPICE':
            aSTEAM_2.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_2.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software == False:
            aSTEAM_2.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent']
        else:
            aSTEAM_2.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent', 'run_simulation']

        if input_csv_file.endswith('.csv'):
            outputfile_1 = os.path.join(os.getcwd(), 'output', 'run_parsim_event_circuit',
                                        f'TestFile_AnalysisSTEAM_run_parsim_event_circuit_RCO_{file_counter}.yaml')
            outputfile_2 = os.path.join(os.getcwd(), 'output', 'run_parsim_event_circuit',
                                        f'TestFile_AnalysisSTEAM_run_parsim_event_circuit_RCD_{file_counter}.yaml')
            if software == 'PSPICE':
                list_output_file = [
                    os.path.join(aSTEAM_1.settings.local_PSPICE_folder, 'RCO', f'{file_counter}', 'RCO.cir'),
                    os.path.join(aSTEAM_2.settings.local_PSPICE_folder, 'RCD', f'{file_counter}', 'RCD.cir')]
            elif software == 'XYCE':
                list_output_file = [
                    os.path.join(aSTEAM_1.settings.local_XYCE_folder, 'RCO', f'{file_counter}', 'RCO.cir'),
                    os.path.join(aSTEAM_2.settings.local_XYCE_folder, 'RCD', f'{file_counter}', 'RCD.cir')]
            if os.path.exists(outputfile_1): os.remove(outputfile_1)
            if os.path.exists(outputfile_2): os.remove(outputfile_2)
            for file in list_output_file:
                if os.path.exists(file): os.remove(file)

            # act
            aSTEAM_1.write_analysis_file(path_output_file=outputfile_1)
            aSTEAM_1.run_analysis()

            aSTEAM_2.write_analysis_file(path_output_file=outputfile_2)
            aSTEAM_2.run_analysis()