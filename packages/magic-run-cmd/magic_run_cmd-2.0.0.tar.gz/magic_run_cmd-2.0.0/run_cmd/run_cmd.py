from __future__ import annotations
from typing import Union, Callable, Any 
from subprocess import Popen, PIPE as l
from pysimplelog import Logger
from inspect import getframeinfo, currentframe
logger = Logger(__name__)
logger.set_log_file_basename('run_cmd')
logger.set_minimum_level(logger.logLevels['info'])

def run_cmd(cmd:str, split:bool=False) -> Union[list[str],str]:
    """
    A simple wrapper for Popon to run shell commands from python
    
    Args:
        cmd str: The comanda you want to run
        example: ls
    Raises:
        OSError: If the command throws an error this  captures it. 
        example: ls /does_not_exist
    Returns:
        List[str] or str: This is output of the cmd, either as a string or
        as list which is the string spilt on endline.
    """    
    
    debug_msg = f"""########
                  {getframeinfo(currentframe())=}
                  {cmd=}{type(cmd)=}
                  {split=}{type(split)=}"""
    logger.debug(debug_msg)
    
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    debug_msg = f"""What is {out=}?
                    What is {err=}?"""
    logger.debug(debug_msg)
    
    if err:
        error_msg = f"""There was an error:
                        {err}
                        """
        logger.error(error_msg, stack_info= True)
        raise OSError(err)
    return [o for o in out.decode().split('\n') if o] if split else out.decode()

def shell(cmds:str,split=False):
        commmand_list: list[str] = cmds.split('\n')
        commmand_list = [cmd.strip() for cmd in commmand_list if cmd]
        return [run_cmd(cmd,split=split) for cmd in commmand_list]
    
class Script():
    
    '''
        Allows you write bash scripts in python code.
        script = Scripts()
        script.cmds = """
                        ls
                        echo "an"
                       """
        script()
    '''
    
    def __init__(self,
                 cmds:str='',
                 engine:Callable[[str,Any],Union[list[str],str]]=shell):
        self.cmds:str = cmds
        self.engine: Callable[[str],Union[list[str],str]] = engine

    def __add__(self,cmd: Union[Script,str])->str:
        match(cmd):
            case str():cmds:str =  '\n'.join([self.cmds,cmd])
            case Script() if self.engine!=cmd.engine:
                raise Exception(f'{self.engine.__name__} do not match {cmd.engine.__name__}')
            case Script():cmds:str = '\n'.join([self.cmds,cmd.cmd])
        return Script(cmds)
    
    def __iadd__(self,cmd: Union[Script,str])->Script:
        self = self + cmd
        return self
    
    def __repr__(self) -> str:
        return self.cmds
    
    def __str__(self) -> str:
        return self.cmds
     
    def __call__(self,*args,**kwargs) -> list[str]:
        return self.engine(self.cmds,*args,**kwargs) 

    def append(self,cmd:Union[Script,str])->None:
        self.cmds += cmd