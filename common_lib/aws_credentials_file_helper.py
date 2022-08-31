#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
from pick import pick
from pathlib import Path
from common_lib.common_error import BadUserInputError
from common_lib.os_process_helper import OsProcessHelper

# sample adapted from https://stackoverflow.com/questions/56723852/console-select-menu-in-python
class AwsCredentialsFileHelper(object):
  
  def __init__(self,
               aws_configure_sso_accounts_python_script_path:str,
               aws_sso_start_url:str) -> None:
    
    self.aws_configure_sso_accounts_python_script_path = aws_configure_sso_accounts_python_script_path
    if not os.path.exists(self.aws_configure_sso_accounts_python_script_path):
      raise BadUserInputError(f"Python script {self.aws_configure_sso_accounts_python_script_path} not found.")
    self.aws_sso_start_url = aws_sso_start_url
    
    self.profiles:list[str] = []
    self.current_credentials_file_lines:list[str] = []
    self.__read_current_credentials_file_lines()
    self.__get_profile_list()
    
  def __read_current_credentials_file_lines(self):
    home = str(Path.home())
    aws_config_path = os.path.join(home, ".aws")
    if not os.path.exists(aws_config_path):
      os.makedirs(aws_config_path)
    
    aws_config_file_path = os.path.join(aws_config_path, "credentials")
    if not os.path.exists(aws_config_file_path):
        open(aws_config_file_path, 'a').close()
    
    with open(aws_config_file_path,'r') as current_file:
      self.current_credentials_file_lines.extend(current_file.readlines())
  
  def __get_profile_list(self):
    for line in self.current_credentials_file_lines:
      if line.startswith("[") and line.endswith("]\n"):
        profile_name = line[1:-2]
        if profile_name != "default":
          self.profiles.append(profile_name)
    
  def set_default_profile(self):
   
    profile_name_filter = input("Profile name filter, if not set will show all available profiles: ")
    if profile_name_filter:
      profiles = [k for k in self.profiles if profile_name_filter in k]
    else:
      profiles = self.profiles
      
    profiles.sort()
    if len(profiles)> 0: 
      title = 'Please choose the default profile: '
      profile_name, index = pick(profiles, title, indicator='=>', default_index=0) 
    
      print(f"Profile [{profile_name}] selected.")
    else:
        print("There wasn`t profiles on ~/.aws/credentials file")
        profile_name = input("Please, set de full Profile name that should be ser as default:\n")
    
    os_process_helper = OsProcessHelper(command="python", 
                                        args=[self.aws_configure_sso_accounts_python_script_path,
                                              "-url",
                                              self.aws_sso_start_url,
                                              "-d",
                                              profile_name])
    print(f"Starting default credentials update.")
    os_process_helper.start()
    os_process_helper.wait()
    print(f"default credentials updated")
      
    

  