import sys
from os import system

from .runnr_parser import runnr_parser
from .runnr_flags import runnr_flags
from .runnr_ver import runnr_ver

ver = runnr_ver()

#command line arguments
argc = len(sys.argv)
argv = sys.argv

class runnr():
    def __init__(self):
        self.test_argv()
        self.parser = runnr_parser()
        self.flags = runnr_flags()
        self.parser.init()
        self.setup_cli_param()
        self.split_extension()
        self.build_commands()
        exit(0)


    def test_argv(self) -> None:
        if argc <= 1:
            print('runnr: error: no input file')
            exit(1)


    def output_name(self, configs : [dict]) -> [str]:
        if configs['type'] == 'c':
            if self.flags.b_custom_output_name:
                return [f'{self.flags.s_custom_output_file_name}', f'-o {self.flags.s_custom_output_file_name}']
            

            match configs['out']:
                case '$FILE':
                    return [f'{self.flags.s_file_name}', f'-o {self.flags.s_file_name}']

                case '$NONE':
                    return ['', '']
                
                case _:
                    return [f"{configs['out']}", f"-o {configs['out']}"]
        else:
            return ['', '']
            
    def executor_param(self) -> str:
        if self.flags.b_extra_param:
            return self.flags.s_extra_param_list
        else:
            return ''
        
    def execute(self, output_name : str, status : int) -> None:
        if output_name and not status:
            if sys.platform == 'win32':
                if self.flags.b_extra_args:
                    if self.flags.b_debug_mode:
                        print(f'runnr: debug: run: .\\{output_name} {self.flags.s_extra_args_list}')

                    system(f'.\\{output_name}  {self.flags.s_extra_args_list}')
                else:
                    if self.flags.b_debug_mode:
                        print(f'runnr: debug: run: .\\{output_name}')
                    system(f'.\\{output_name}')

            elif sys.platform in ['darwin', 'linux']:
                if self.flags.b_extra_args:
                    if self.flags.b_debug_mode:
                        print(f'runnr: debug: run: ./{output_name} {self.flags.s_extra_args_list}')
                        
                    system(f'./{output_name} {self.flags.s_extra_args_list}')
                else:
                    if self.flags.b_debug_mode:
                        print(f'runnr: debug: run: ./{output_name}')
                    system(f'./{output_name}')


    def setup_cli_param(self) -> None:
        if argv[1] in ['--version', '-v']:
            print(f'{ver.ver}')
            exit(0)

        if argv[1] == '-open':
            for rows in self.parser.runnr_config_table:
                if rows['extension'] == argv[1]:
                    system(f"{rows['executor']} {argv[argc - 1]}")
                    exit(0)
                
            print(f'runnr: error: no >> -open >> config found in {self.parser.path_of_config}')
            exit(1)


        i = 1
        while(i < argc - 1):
            match argv[i]:
                case '-run':
                    if argv[i + 1] == 'Y':
                        self.flags.b_run_after_compilatiion = True
                    elif argv[i + 1] == 'N':
                        self.flags.b_run_after_compilatiion = False
                    else:
                        print('runnr: error: invalid parameter for -run');
                        exit(1)
                     
                    i += 1

                case '-debug':
                    if not self.flags.b_debug_mode:
                        self.flags.b_debug_mode = True
                    else:
                        print('runnr: error: multiple use of -debug')
                        exit(1)

                case '-out':
                    if not self.flags.b_custom_output_name:
                        self.flags.b_custom_output_name = True
                        self.flags.s_custom_output_file_name = argv[i + 1]
                        i += 1
                    else:
                        print('runnr: error: multiple use of -out')
                        exit(1)

                case '-param':
                    if not self.flags.b_extra_param:
                        self.flags.b_extra_param = True
                        self.flags.s_extra_param_list = argv[i + 1]
                        i += 1
                    else:
                        print('runnr: error: multiple use of -param')
                        exit(1)

                case '-args':
                    if not self.flags.b_extra_args:
                        self.flags.b_extra_args = True
                        self.flags.s_extra_args_list = argv[i + 1]
                        i += 1
                    else:
                        print('runnr: error: multiple use of -args')
                        exit(1)

                case _:
                    if argv[i][0] == '-':
                        print(f'runnr: error: bad option: {argv[i]}')
                        exit(1)
        
            i += 1
    

    def split_extension(self) -> None:
        index = argv[argc - 1].rfind('.')
        self.flags.s_file_name = argv[argc - 1][:index]
        self.flags.s_extension = argv[argc - 1][index:]


    def build_commands(self) -> None:
        config : dict = self.parser.runnr_get_extension_config(self.flags.s_extension)

        if not config:
            print('runnr: error: file format is not found in runnr.conf')
            exit(1)

        [output_name, output_command_w_name] = self.output_name(config)
        command = f"{config['executor']} {self.executor_param()} {argv[argc - 1]} {output_command_w_name}"

        if self.flags.b_debug_mode:
            print(f'runnr: debug: config: using config from {self.parser.path_of_config}')
            print(f'runnr: debug: executed: {command}')

        status = system(command)

        if self.flags.b_run_after_compilatiion:
            self.execute(output_name, status)