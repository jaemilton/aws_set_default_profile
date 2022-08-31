#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import subprocess
from typing import List

class OsProcessHelper(object):
    """
    Call in a loop to create terminal progress bar
    @params:
        command       - Required  : command
        args       - Optional  : with interation number is the start interation
    """

    def __init__(self, 
                    command:str,
                    args:List[str]) -> None:
        self.command:str = command
        self.args:List[str] = args
        self.monitoring_data = []
        self.max_cpu_percentage=0
        self.max_memory=0

    def start(self):
        command_params = [self.command]
        command_params.extend(self.args)
        self.process = subprocess.Popen(command_params)
        

    def get_pid(self):
        return self.process.pid
    
    def wait(self) -> None:
        self.process.wait()

