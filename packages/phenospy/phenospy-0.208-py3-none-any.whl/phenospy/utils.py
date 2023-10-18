
import os
import requests
import yaml

from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

#----------- Download Ontologies from YAML file
# yaml_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/phenotypes/phs-config.yaml'
# save_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/source_ontologies'
# download_ontologies_from_yaml(yaml_file, save_dir)

def download_ontologies_from_yaml(yaml_file, save_dir):
    # -----------------------------------------
    # Read configuration yaml
    # -----------------------------------------
    print(f"{Fore.BLUE}Reading yaml file: {Style.RESET_ALL}{yaml_file}")
    with open(yaml_file, 'r') as f_yaml:
        phs_yaml = yaml.safe_load(f_yaml)
    # print(phs_yaml)
    print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

    # Create a directory to store downloaded ontologies
    os.makedirs(save_dir, exist_ok=True)
    print(f"{Fore.BLUE}Downloading ontologies to: {Style.RESET_ALL}{save_dir}")

    # Iterate over the ontologies and download them
    for ontology_url in phs_yaml['importOntologies']:
        # Get the filename from the URL
        filename = os.path.basename(ontology_url)
        file_path = os.path.join(save_dir, filename)

        # Download the ontology
        response = requests.get(ontology_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as ontology_file:
                ontology_file.write(response.content)
            print(f"{Fore.BLUE}Downloaded: {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to download: {filename}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}All ontologies downloaded.{Style.RESET_ALL}")