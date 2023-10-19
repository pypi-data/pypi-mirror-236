import os 
from typing import Callable, Dict, Any, List
import EXgen.util.expression_handler as eh
import EXgen.util.solver_functions as sf
import EXgen.util.util as util 
import yaml
import shutil
import re
import numpy as np
import random
from tqdm import tqdm

######## CONST DEFS #########

TASK_SPLIT_TOKEN = "%END-PART"
EX_GROUP_TOKEN = "INSERT-GROUP"
EX_NUM_TOKEN = "INSERT-EX-NUM"
EX_NAME_TOKEN = "INSERT-EX-NAME"
TASKS_TOKEN = "INSERT-TASKS"
EX_INFOBOX_TOKEN = "INSERT-INFOBOX"
FIG_INSERT_TOKEN = "FIGPATH"
SOLUTION_TOKEN = "INSERT-SOLUTION"
TOKEN_PREFIX_LEN = len("INSERT-")
SEED_NUM_TOKEN = "seed_num"
TEMPLATE_TOKEN = "template"

TASK_KEYS_LIST = ["netlist", 
                  "var_defs",
                  "solution_gen_type"]

TEX_COMPILE_LOG = "latex_compile.log"

#############################
######## EXgen class ########

class EXgen:
    def __init__(self, args: object) -> None:
        
        # get setup info : 
        self.meta_data = self._read_yaml(args.config_file)
        self._set_defaults_meta_data()
        
        # initialize variables and functions : 
        self._init_vars()
        self._init_functions()

        # initialize function maps : 
        self._init_solution_gen_map()
        self._init_units_map()
        self._init_lcapy_maps()

        # initialize paths and dirs :
        self._init_paths_and_dirs()

        # initialize tex templates : 
        self._init_tex_templates()

        # make task list containing tasks : 
        self._extend_tasks_list()

    def _init_functions(self) -> None:
        self._set_seed = self._dummy_fun if self.seed_num is None else self._set_seed_function
        self._init_solution_functions()
        self._latex_command = util.latex_command_win if self.is_win else lambda x: util.latex_command_unix(x, TEX_COMPILE_LOG)

    def _set_defaults_meta_data(self) -> None:

        self.meta_data[SEED_NUM_TOKEN] = None if SEED_NUM_TOKEN not in self.meta_data.keys() else self.meta_data[SEED_NUM_TOKEN]
        self.meta_data[TEMPLATE_TOKEN] = "homework" if TEMPLATE_TOKEN not in self.meta_data.keys() else self.meta_data[TEMPLATE_TOKEN]

    def _init_vars(self) -> None:
        
        self.course = self.meta_data["course"]
        self.session_id = str(self.meta_data["session_id"])
        self.session = self.meta_data["session_name"]
        self.groups = self.meta_data["groups"]
        self.tasks = self.meta_data["tasks"]
        self.n_tasks = len(self.meta_data["tasks"])
        self.fig_dir_path = self.meta_data["figure_path"]
        self.generate_solution_files = self.meta_data["generate_solution_files"]
        self.seed_num = self.meta_data[SEED_NUM_TOKEN]
        self.is_win = os.name == "nt"

        self.templates_figures_dir = __file__[:-8] + "templates/figures/"
        self.main_tex_template_file = self.meta_data["template"] + "_template.tex"
        self.template_file = __file__[:-8] + "templates/" + self.main_tex_template_file
        self.tasks_tex_template_file = self.meta_data["tasks_template"]

    def _init_paths_and_dirs(self) -> None:
        
        if not os.path.exists(self.fig_dir_path):
            os.mkdir(self.fig_dir_path)

    def _init_units_map(self) -> None:
        self.units_map = {'U': 'V', 'V': 'V', 
                          'I': 'A', 
                          'R': '\Omega',
                          'E': 'V/m',
                          'F': 'N',
                          'P': 'm',
                          'Q': 'As'}

    def _init_lcapy_maps(self) -> None:
        self.lcapy_symbol_map = {'U': 'V', 
                                 'R': 'R',
                                 'I': 'I',
                                 'C': 'C',
                                 'L': 'L'}
    
    def _init_solution_functions(self) -> None:
        self.task_solver_functions = {"resistor-network" : lambda x: eh.solve(x, draw=True),
                                   "electric-field-1" : sf.electric_field_1, 
                                   "electric-field-2" : sf.electric_field_2, 
                                   "electric-field-mpq-1" : sf.electric_field_mpq_1, 
                                   }

    def _init_solution_gen_map(self) -> None:
        self.solution_gen_map = {"list-results": self._list_results_tex,}

    def _init_task_variables(self) -> None:
        for i_task in range(self.n_tasks):
            # nsubtasks = self.tasks[i_task].get("num_subtasks", 1)

            self.tasks[i_task]["solution-figpaths"] = []
            self.tasks[i_task]["variables"] = util.init_var_vals(self.tasks[i_task]["var_defs"], 
                                                                      self.tasks[i_task]["round_precision"])
    def _extend_tasks_list(self) -> None:

        for i_task in range(self.n_tasks):

            self.tasks[i_task]["inserts"] = self._get_inserts_for_task(i_task)
            self.tasks[i_task]["solution_gen_fun"] = self.solution_gen_map[self.tasks[i_task]["solution_gen_type"]]
            self.tasks[i_task]["insert_figpaths"] = self._get_insert_figpaths(self.tasks[i_task]["inserts"])
            self.tasks[i_task]["solver_fun"] = self.task_solver_functions[self.tasks[i_task]["task_solver"]]

    def _get_insert_figpaths(self, inserts: Dict[str, str]) -> List[str]:
        
        figpaths = []
        for key, val in inserts.items():
            if FIG_INSERT_TOKEN in key:
                figpaths.append(val)

        return figpaths

    def _get_inserts_for_task(self, i_task: int) -> Dict[str, str]:
        
        inserts_list = re.findall("(INSERT-[\w.-]*)\s", self.tasks_tex_list[i_task])

        return {key: self._get_insert_value(key) for key in inserts_list}

    def _get_insert_value(self, key: str) -> str:
        
        key_part = key.split('-')[1] 
        key_out = key_part
        
        if FIG_INSERT_TOKEN in key_part:
            key_out = f"{self.fig_dir_path}/figure_{key_part[len(FIG_INSERT_TOKEN):]}.pdf"
        elif SOLUTION_TOKEN in key:
            key_out = SOLUTION_TOKEN[TOKEN_PREFIX_LEN:]
        elif key_part in self.lcapy_symbol_map.keys():
            key_out = self.lcapy_symbol_map[key_part[0]] + key_part[1:]    

        return key_out

    def _generate_document_for_group(self, group: str) -> None:

        # fill template with meta data 
        tex_content = self._fill_meta_data(group)
        tex_tasks = ''
        tex_solved_tasks = ''

        # initialize variables for each new group separately : 
        self._init_task_variables()

        # add tasks : 
        for i_task, task in enumerate(self.tasks):

            # set seed for each task :
            self._set_seed() 
            
            # solve task and get results : 
            task["result"] = task["solver_fun"](task)

            task["result"][SOLUTION_TOKEN[TOKEN_PREFIX_LEN:]] = task["solution_gen_fun"](task)

            # write task to template : 
            tex_task, tex_solved_task = self._write_task(task, i_task)

            tex_tasks += tex_task
            tex_solved_tasks += tex_solved_task

        tex_tasks = self._update_if_biomed(tex_tasks, group)
        tex_solved_tasks = self._update_if_biomed(tex_solved_tasks, group)

        tex_content_tasks = tex_content.replace(TASKS_TOKEN, tex_tasks)
        tex_content_solution = tex_content.replace(TASKS_TOKEN, tex_solved_tasks)

        self._tex_to_pdf(tex_content_tasks, group, clean=True)
    
        if self.generate_solution_files:
            self._tex_to_pdf(tex_content_solution, group, clean=True, is_solution=True)

    
    def generate(self) -> None:

        tgroups = tqdm(self.groups)
        for group in tgroups:
            tgroups.set_description(f" > Generating : {group} ")
            self._generate_document_for_group(group)

        self._clean_templates()

    #####################################
    ######## Tex - functions : ##########

    def _init_tex_templates(self) -> None:

        shutil.copytree(self.templates_figures_dir, "./figures/", symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        shutil.copy(self.template_file, "./")

        self.main_tex = self._read_tex(self.main_tex_template_file)
        
        tasks_tex_template = self._read_tex(self.tasks_tex_template_file).split(TASK_SPLIT_TOKEN)
        
        self.infobox_tex = tasks_tex_template[0]
        self.tasks_tex_list = tasks_tex_template[1:]

    def _fill_meta_data(self, group: str) -> str:

        tex_str = self.main_tex

        tex_str = tex_str.replace(EX_GROUP_TOKEN, group)
        tex_str = tex_str.replace(EX_NUM_TOKEN, self.session_id)
        tex_str = tex_str.replace(EX_NAME_TOKEN, self.session)
        tex_str = tex_str.replace(EX_INFOBOX_TOKEN, self.infobox_tex)

        return tex_str
    
    def _ndarray_to_latex(self, arr):
        elems = ''.join([f"{format(x, 'e')} \\\\" for x in arr])
        return "\\begin{bmatrix}" + elems + "\\end{bmatrix}"

    def _val_to_latex(self, val, precision):
        tex_str = ''

        if type(val) in [int, float, np.int64, np.float64]:
            tex_str = str(round(val, precision))
        elif type(val) == np.ndarray:
            tex_str = self._ndarray_to_latex(val)

        return tex_str
    
    def _get_task_varkeys(self, task):
        if type(task["variables"]) == list:
            return task["variables"][0].keys()
        else:
            return task["variables"].keys()
    
    def _add_newpage_command_to_tex(self, tex_string, at_start=True):
        return "\\newpage" + tex_string if at_start else tex_string + "\\newpage"
        
    def _write_task(self, task: Dict[str, Any], i_task: int) -> str:
        
        tex_task = self.tasks_tex_list[i_task]

        task["result"] = {x.replace('V', 'U'):y for x,y in task["result"].items()}
        corrected_res_keys = list(task["result"].keys())
        corrected_res_keys.remove(SOLUTION_TOKEN[TOKEN_PREFIX_LEN:])

        var_keys = list(self._get_task_varkeys(task))
        var_keys.remove(SOLUTION_TOKEN[TOKEN_PREFIX_LEN:])

        for key, val in task["inserts"].items():

            if key[TOKEN_PREFIX_LEN:] in corrected_res_keys:
                res_val = task["result"][val]
                tex_task = tex_task.replace(key, self._val_to_latex(res_val, task["round_precision"]))
            elif key[TOKEN_PREFIX_LEN:] in var_keys:
                res_val = task["variables"][val]
                tex_task = tex_task.replace(key, self._val_to_latex(res_val, task["round_precision"]))
            elif FIG_INSERT_TOKEN in key:
                tex_task = tex_task.replace(key, val)

        solution_key = task["inserts"][SOLUTION_TOKEN]
        tex_task_solution = tex_task.replace(SOLUTION_TOKEN, task["result"][solution_key])
        # tex_task_solution = self._add_newpage_command_to_tex(tex_task_solution, at_start=True)
        tex_task = tex_task.replace(SOLUTION_TOKEN, '')

        return tex_task, tex_task_solution        

    def _tex_to_pdf(self, tex_content: str, group: str, clean: bool=False, is_solution: bool=False) -> None:
        
        ext = "_solution" if is_solution else ''

        tex_filename = self.course.replace(' ', '_') + '_' + self.session_id + f"_{group}{ext}.tex"
        fid = open(tex_filename, 'w') 
        fid.write(tex_content)
        fid.close()

        os.system(self._latex_command(tex_filename))

        if clean:
            os.remove(f"{tex_filename[:-4]}.aux")
            os.remove(f"{tex_filename[:-4]}.log")
            os.remove(f"{tex_filename[:-4]}.tex")
            # os.remove(TEX_COMPILE_LOG)

    def _list_results_tex(self, task: Dict[str, Any]) -> str:
        template = "\\newpage \n \\section*{Solution :} \\ \n INSERT-ITEMIZE \n INSERT-FIGS"

        itemize = "\\begin{itemize}\n INSERT-ITEMS \n \end{itemize}"
        items = ''
        for key, val in task["result"].items():
            unit_id = key.replace("V", "U")

            if type(val) in [int, float, np.float64, np.float32]:
                if val > 1e-3:
                    items += "\item $" + unit_id[0] + "_{" + unit_id[1:] + "} = " + str(round(val, task["round_precision"])) + ' ' + self.units_map[key[0]] + "$ \n"
                else : 
                    items += "\item $" + unit_id[0] + "_{" + unit_id[1:] + "} = " + format(val, 'e') + ' ' + self.units_map[key[0]] + "$ \n"
            elif type(val) == np.ndarray:
                items += "\item $" + "\\vec{" + f"{unit_id[0]}" "}_{" + unit_id[1:] + "} =" + self._ndarray_to_latex(val) + self.units_map[key[0]] + "$ \n"

        figs = ''
        for figpth in task["solution-figpaths"]:
            figs += "\\includegraphics[scale=1.0]{" + f"{figpth}" + "} \n"
        
        itemize = '' if items == '' else itemize.replace("INSERT-ITEMS", items) 
        template = template.replace("INSERT-ITEMIZE", itemize)
        template = template.replace("INSERT-FIGS", figs)

        return template

    def _update_if_biomed(self, tex: str, group: str) -> str:
        
        if "BME" in group:
            tex = tex.replace("%INSERT-BME", '')
        else : 
            tex = tex.replace("%INSERT-NOTBME", '')

        return tex
    #####################################
    ######## Utility functions ##########

    def _dummy_fun(self, dummy_var: Any=None) -> None:
        pass

    def _set_seed_function(self):
        np.random.seed(self.seed_num)
        random.seed(self.seed_num)
        self.seed_num += 1

    def _clean_templates(self) -> None:
        shutil.rmtree("./figures/")
        shutil.rmtree(self.fig_dir_path )
        os.remove(self.main_tex_template_file)

    def _read_tex(self, fname: str) -> str:
        
        fid = open(fname)
        contents = fid.read()
        fid.close()

        return contents

    def _read_yaml(self, fpath: str) -> Dict[str, Any]:
    
        with open(fpath) as f:
            contents = yaml.load(f, Loader=yaml.FullLoader)

        return contents
    
    #####################################

# def main() -> None:
#     myGen = EXgen("UE1_config.yaml")
#     myGen.generate()
#     print("finished")

# if __name__ == "__main__":
#     main()
    