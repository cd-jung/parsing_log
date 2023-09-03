from abstract_data_analyser import AbstractedDataAnalyser

def excute_analysis(file_path: str, analyser: AbstractedDataAnalyser) -> str:
    # read a file and its lines 
    with open(file_path, 'r') as file:
        for line in file:
            analyser.read_a_line(line)
    
    # analyse the data
    analyser.analyse()

    # store the data
    return analyser.store()
