import itertools
import os
import pickle
import sys

from typing import Optional, Callable

from ctypes import CFUNCTYPE, c_int64, POINTER, c_double, c_void_p

import numpy as np
import time
import uuid

from numba import njit, carray
import numpy.typing as npt
from numba.core.registry import CPUDispatcher

from numba.experimental import jitclass
import pandas as pd
from numerous.engine.model.aliased_dataframe import AliasedDataFrame

from numerous.engine.model.events import generate_event_action_ast, generate_event_condition_ast, replace_path_strings
from numerous.engine.model.utils import Imports
from numerous.engine.numerous_event import StateEvent, TimestampEvent, Condition, Action
from numerous.engine.system.external_mappings import ExternalMapping, EmptyMapping, ExternalMappingUnpacked

from numerous.utils.logger_levels import LoggerLevel

from numerous.utils.historian import InMemoryHistorian
from numerous.engine.model.graph_representation.mappings_graph import MappingsGraph
from numerous.engine.model.compiled_model import numba_model_spec, CompiledModel
from numerous.engine.system.connector import Connector

from numerous.engine.system.subsystem import Subsystem, ItemSet
from numerous.engine.variables import VariableType, VariableDescription, _VariableFactory

from numerous.engine.model.ast_parser.parser_ast import parse_eq
from numerous.engine.model.graph_representation.graph import Graph
from numerous.engine.model.ast_parser.parser_ast import process_mappings

from numerous.engine.model.lowering.equations_generator import EquationGenerator
from numerous.engine.system import SetNamespace

from numerous.utils import logger as log

from numerous.engine.model.lowering.llvm_initializer import ee, llvm


class ModelNamespace:

    def __init__(self, tag, outgoing_mappings, item_tag, item_indcs, path, pos, item_path):
        self.tag = tag
        self.item_tag = item_tag
        self.outgoing_mappings = outgoing_mappings
        self.equation_dict = {}
        self.eq_variables_ids = []
        ##Ordered dictionary.
        self.variables = {}
        self.set_variables = None
        self.mappings = []
        self.full_tag = item_path + '.' + tag
        self.item_indcs = item_indcs

        self.path = path
        self.is_set = pos

    def ordered_variables(self):
        """
        return variables ordered for sequential llvm addressing
        """
        variables__ = []
        for vs in self.variable_scope:
            variables___ = []
            for v in vs:
                variables___.append(v)
            variables__.append(variables___)

        variables__ = [list(x) for x in zip(*variables__)]
        variables__ = list(itertools.chain(*variables__))
        variables_ordered = [None] * len(variables__)
        if self.is_set:
            for i, v in enumerate(variables__):
                v.detailed_description.variable_idx = i
        for variable in variables__:
            variables_ordered[variable.detailed_description.variable_idx] = variable
        return variables_ordered


class ModelAssembler:

    @staticmethod
    def namespace_parser(input_namespace):
        equation_dict = {}
        tag, namespaces = input_namespace
        variables_ = {}
        for namespace in namespaces:
            for i, (eq_tag, eq_methods) in enumerate(namespace.equation_dict.items()):
                scope_id = "{0}_{1}_{2}".format(eq_tag, namespace.tag, tag, str(uuid.uuid4()))
                equation_dict.update({scope_id: (eq_methods, namespace.outgoing_mappings)})
            for v in namespace.ordered_variables():
                variables_.update({v.id: v})

        return variables_, equation_dict


class Model:
    """
     The model object traverses the system to collect all information needed to pass to the solver
     for computation – the model also back-propagates the numerical results from the solver into the system,
     so they can be accessed as variable values there.
    """

    def __init__(self, system=None,
                 logger_level: LoggerLevel = LoggerLevel.ALL,
                 assemble: bool = True,
                 imports: dict = None, historian=InMemoryHistorian(),
                 use_llvm: bool = True,
                 save_to_file: bool = False,
                 generate_graph_pdf: bool = False,
                 global_variables: dict = None,
                 export_model: bool = False,
                 clonable: bool = False):

        self.path_to_variable = {}
        self.generate_graph_pdf = generate_graph_pdf
        self.export_model = export_model

        self.logger_level = logger_level
        external_mappings_unpacked = system.get_external_mappings()
        self.system_external_mappings = external_mappings_unpacked
        self.is_external_data = True if len(external_mappings_unpacked) else False
        self.external_mappings = ExternalMapping(external_mappings_unpacked) if len(
            external_mappings_unpacked) else EmptyMapping()

        self.run_after_solve = system.get_run_after_solve()

        self.post_step = system.get_post_step()

        self.use_llvm = use_llvm
        self.save_to_file = save_to_file
        self.clonable = clonable
        self.imports = Imports()
        self.imports.add_as_import("numpy", "np")
        self.imports.add_from_import("numba", "njit")
        self.imports.add_from_import("numba", "carray")
        self.imports.add_from_import("numba", "float64")
        self.imports.add_from_import("numba", "float32")
        if imports:
            for (k, v) in imports:
                self.imports.add_from_import(k, v)

        self.numba_callbacks_init = []
        self.numba_callbacks_variables = []
        self.numba_callbacks = []
        self.numba_callbacks_init_run = []
        self.callbacks = []
        self.global_tag_vars = {}
        self.system = system
        self.event_function = None
        self.condition_function = None
        self.model_items = {}
        self.state_history = {}
        self.compiled_eq = []
        self.flat_scope_idx = None
        self.flat_scope_idx_from = None
        self.historian_df = None
        self.aliases = {}
        self.historian = historian
        self.vars_ordered_value = {}
        self.events = []
        self.timestamp_events = []
        self.global_variables_tags = ['time']
        self.global_variables = {}
        self.equation_dict = {}
        self.variables = {}
        self.name_spaces = {}
        self.flat_variables = {}
        self.period = 1
        self.mapping_from = []
        self.mapping_to = []
        self.eq_outgoing_mappings = []
        self.sum_mapping_from = []
        self.sum_mapping_to = []
        self.states_idx = []
        self.derivatives_idx = []
        self.scope_to_variables_idx = []
        self.numba_model = None

        self.info = {}
        self.add_global_variable("t", 0.0)

        if global_variables:
            for g_var in global_variables:
                self.add_global_variable(g_var[0], g_var[1])

        if assemble:
            self.assemble()

    def __add_item(self, item):
        model_namespaces = {}
        if item.id in self.model_items:
            return model_namespaces

        self.model_items.update({item.id: item})
        model_namespaces[item.id] = self._create_model_namespaces(item)
        if isinstance(item, ItemSet):
            return model_namespaces
        if isinstance(item, Connector):
            for binded_item in item.get_binded_items():
                if not binded_item.part_of_set:
                    model_namespaces.update(self.__add_item(binded_item))
        if isinstance(item, Subsystem):
            for registered_item in item.registered_items.values():
                model_namespaces.update(self.__add_item(registered_item))
        return model_namespaces

    def __get_mapping__variable(self, variable, depth):
        if variable.mapping and depth > 0:
            return self.__get_mapping__variable(variable.mapping, depth - 1)
        else:
            return variable

    def _add_global_var(self, name: str, initial_value: float):
        if name in self.global_variables:
            return self.global_variables[name]
        else:
            var_desc = VariableDescription(tag=name, initial_value=initial_value,
                                           type=VariableType.PARAMETER, global_var=True,
                                           global_var_idx=len(self.global_variables.values()))
            self.global_variables[name] = _VariableFactory._create_from_variable_desc_unbound(
                variable_description=var_desc, initial_value=initial_value)
            return self.global_variables[name]

    def add_global_variable(self, name: str, initial_value: float):
        tag = "global_vars_"
        x = self._add_global_var(tag + name, initial_value)
        self.global_tag_vars[tag + name] = x
        self.variables.update({x.id: x})

    def assemble(self):
        """
        Assembles the model.
        """
        """
        notation:
        - _idx for single integers / tuples,
        - _idxs for lists / arrays of integers
        - _pos as counterpart to _from
        -  _flat
        -  _3d
        """

        def __get_mapping__idx(variable):
            if variable.mapping:
                return __get_mapping__idx(variable.mapping)
            else:
                return variable.idx_in_scope[0]

        log.info("Assembling numerous Model")
        assemble_start = time.time()

        # 1. Create list of model namespaces
        model_namespaces = {item_id: _ns
                            for item_id, _ns in self.__add_item(self.system).items()}

        # 2. Compute dictionaries
        # equation_dict <scope_id, [Callable]>
        # scope_variables <variable_id, Variable>
        for variables, equation_dict in map(ModelAssembler.namespace_parser, model_namespaces.items()):
            self.equation_dict.update(equation_dict)
            self.variables.update(variables)

        mappings = []
        for variable in self.variables.values():
            if not (variable.global_var):
                variable.top_item = self.system.id

        for scope_var_idx, var in enumerate(self.variables.values()):
            if var.mapping:
                _from = self.__get_mapping__variable(self.variables[var.mapping.id], depth=1)
                mappings.append((var.id, [_from.id]))
            if not var.mapping and var.sum_mapping:
                sum_mapping = []
                for mapping_id in var.sum_mapping:
                    _from = self.__get_mapping__variable(self.variables[mapping_id.id], depth=1)
                    sum_mapping.append(_from.id)
                mappings.append((var.id, sum_mapping))

        self.mappings_graph = Graph(preallocate_items=1000000)

        self.equations_parsed = {}

        log.info('Parsing equations starting')

        eq_used = []
        for item_id, namespaces in model_namespaces.items():
            for ns in namespaces:
                # Key : scope.tag Value: Variable or VariableSet
                if ns.is_set:
                    tag_vars = ns.set_variables
                else:
                    tag_vars = {v.tag: v for k, v in ns.variables.items()}
                tag_vars.update(self.global_tag_vars)
                parse_eq(model_namespace=ns, item_id=item_id, mappings_graph=self.mappings_graph,
                         variables=tag_vars, parsed_eq_branches=self.equations_parsed, eq_used=eq_used)
        self.eq_used = eq_used
        log.info('Parsing equations completed')

        # Process mappings add update the global graph
        log.info('Process mappings')
        self.mappings_graph = process_mappings(mappings, self.mappings_graph, self.variables)
        self.mappings_graph.build_node_edges()

        log.info('Mappings processed')

        # Process variables
        states = []
        deriv = []
        mapping = []
        other = []

        for sv_id, sv in self.variables.items():
            if sv.logger_level is None:
                sv.logger_level = LoggerLevel.ALL
            if sv.type == VariableType.STATE:
                states.append(sv)
            elif sv.type == VariableType.DERIVATIVE:
                deriv.append(sv)
            elif sv.sum_mapping or sv.mapping:
                mapping.append(sv)
            else:
                other.append(sv)

        self.vars_ordered = states + deriv + mapping + other
        self.states_end_ix = len(states)

        self.deriv_end_ix = self.states_end_ix + len(deriv)
        self.mapping_end_ix = self.deriv_end_ix + len(mapping)

        self.special_indcs = [self.states_end_ix, self.deriv_end_ix, self.mapping_end_ix]

        log.info('Variables sorted')

        self.mappings_graph = MappingsGraph.from_graph(self.mappings_graph)
        self.mappings_graph.remove_chains()
        tmp_vars = self.mappings_graph.create_assignments(self.variables)
        self.mappings_graph.add_mappings()
        if self.generate_graph_pdf:
            self.mappings_graph.as_graphviz(self.system.tag, force=True)
        self.lower_model_codegen(tmp_vars)
        self._assembly_tail()
        self._initial_variables_dict = {k: v.value for k, v in self.variables.items() if not v.global_var}

    def _assembly_tail(self):
        self.logged_aliases = {}

        for i, variable in enumerate(self.variables.values()):
            if variable.temporary_variable:
                continue
            if variable.logger_level is None:
                variable.logger_level = LoggerLevel.ALL
            logvar = False
            if variable.logger_level.value >= self.logger_level.value:
                logvar = True
            if self.system.id in variable.path.path:
                for path in variable.path.path[self.system.id]:
                    self.aliases.update({path: variable.id})
                    if logvar:
                        self.logged_aliases.update({path: variable.id})
            if variable.alias is not None:
                self.aliases.update({variable.alias: variable.id})
                if logvar:
                    self.logged_aliases.update({variable.alias: variable.id})

        self.inverse_aliases = {v: k for k, v in self.aliases.items()}
        inverse_logged_aliases = {}  # {id: [alias1, alias2...], ...}
        for k, v in self.logged_aliases.items():
            inverse_logged_aliases[v] = inverse_logged_aliases.get(v, []) + [k]

        self.inverse_logged_aliases = inverse_logged_aliases
        self.logged_variables = {}

        for varname, ix in self.vars_ordered_values.items():  # now it's a dict...
            var = self.variables[varname]
            if var.logger_level.value >= self.logger_level.value:
                if varname in self.inverse_logged_aliases:
                    for vv in self.inverse_logged_aliases[varname]:
                        self.logged_variables.update({vv: ix})

        number_of_external_mappings = 0
        external_idx = []

        for var in self.variables.values():
            if self.external_mappings.is_mapped_var(self.variables, var.id, self.system.id):
                external_idx.append(self.vars_ordered_values[var.id])
                number_of_external_mappings += 1
                self.external_mappings.add_df_idx(self.variables, var.id, self.system.id)
        self.number_of_external_mappings = number_of_external_mappings
        self.external_mappings.store_mappings()

        self.external_idx = np.array(external_idx, dtype=np.int64)
        self.generate_path_to_varaible()

        # check for item level events
        for item in self.model_items.values():
            if item.events:
                for event in item.events:
                    if not event.compiled:
                        condition_ast, condition_closurevariables = replace_path_strings(self, event.condition.func, "var",
                                                                                         item.path)
                        event.condition = Condition(event.condition.func, condition_ast, condition_closurevariables)
                        if not event.is_external:
                            action_ast, action_closurevariables = replace_path_strings(self, event.action.func, "var",
                                                                                       item.path)
                            event.action = Action(event.action.func, action_ast, action_closurevariables)

                    self.events.append(event)
            if item.timestamp_events:
                for event in item.timestamp_events:
                    if not event.is_external:
                        action_ast, action_closurevariables = replace_path_strings(self, event.action.func, "var", item.path)
                        event.action = Action(event.action.func, action_ast, action_closurevariables)
                    self.timestamp_events.append(event)

        self.info.update({"Number of items": len(self.model_items)})
        self.info.update({"Number of variables": len(self.variables)})
        self.info.update({"Number of equation scopes": len(self.equation_dict)})
        self.info.update({"Number of equations": len(self.compiled_eq)})
        self.info.update({"Solver": {}})

    def _reset(self):
        for k, v in self._initial_variables_dict.items():
            self.variables[k].value = v
            self.var_write(v, self.vars_ordered_values[k])

    def set_variables(self, variables: dict):
        for k, v in variables.items():
            var_id = self.aliases[k]
            self.variables[var_id].value = v
            self.var_write(v, self.vars_ordered_values[var_id])

    def get_variables_initial_values(self):
        return {self.inverse_aliases[k]: v for k, v in self._initial_variables_dict.items()}

    def lower_model_codegen(self, tmp_vars):

        log.info('Lowering model')

        eq_gen = EquationGenerator(equations=self.equations_parsed, filename="kernel.py",
                                   equation_graph=self.mappings_graph,
                                   scope_variables=self.variables,
                                   temporary_variables=tmp_vars, system_tag=self.system.tag, use_llvm=self.use_llvm,
                                   imports=self.imports, eq_used=self.eq_used)

        compiled_compute, var_func, var_write, self.vars_ordered_values, self.variables, \
            self.state_idx, self.derivatives_idx = \
            eq_gen.generate_equations(export_model=self.export_model, clonable=self.clonable)

        for varname, ix in self.vars_ordered_values.items():
            var = self.variables[varname]
            var.llvm_idx = ix
            if getattr(var, 'logger_level',
                       None) is None:  # added to temporary variables - maybe put in generate_equations?
                setattr(var, 'logger_level', LoggerLevel.ALL)

        def c1(self, array_):
            return compiled_compute(array_, self.global_vars)

        def c2(self):
            return var_func()

        def c3(self, value, idx):
            return var_write(value, idx)

        setattr(CompiledModel, "compiled_compute", c1)
        setattr(CompiledModel, "read_variables", c2)
        setattr(CompiledModel, "write_variables", c3)

        self.compiled_compute, self.var_func, self.var_write = compiled_compute, var_func, var_write
        self.init_values = np.ascontiguousarray(
            [self.variables[k].value for k in self.vars_ordered_values.keys()],
            dtype=np.float64)
        self.update_all_variables()

        # values of all model variables in specific order: self.vars_ordered_values
        # full tags of all variables in the model in specific order: self.vars_ordered
        # dict with scope variable id as key and scope variable itself as value

        # Create aliases for all paths in each scope variable
        def c4(values_dict):
            return [self.var_write(v, self.vars_ordered_values[self.aliases[k]]) for k, v in values_dict.items()]

        def c5():
            vals = var_func()
            return {self.inverse_aliases[k]: v for k, v in zip(self.vars_ordered_values.keys(), vals)}

        setattr(self, "update_variables", c4)
        setattr(self, "get_variables", c5)

        self.info.update({"Solver": {}})
        if self.export_model:
            path = os.environ.get("EXPORT_MODEL_PATH", 'export_model')
            filename = os.path.join(path, f'{self.system.tag}.numerous')
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as handle:
                sys.setrecursionlimit(100000)
                pickle.dump((self.system, self.logger_level,
                             self.imports, self.use_llvm, self.vars_ordered_values, self.variables,
                             self.state_idx, self.derivatives_idx, self.init_values, self.aliases,
                             eq_gen.generated_program.equations_llvm_opt, eq_gen.generated_program.max_var,
                             eq_gen.generated_program.n_deriv), handle, protocol=pickle.HIGHEST_PROTOCOL)
            log.info('Model successfully exported to ' + filename)

        if self.clonable:
            self.equations_llvm_opt = eq_gen.generated_program.equations_llvm_opt
            self.max_var = eq_gen.generated_program.max_var
            self.n_deriv = eq_gen.generated_program.n_deriv

        # set after export (otherwise we get pickling error for var.write_variable=var_write)
        for varname, ix in self.vars_ordered_values.items():
            var = self.variables[varname]
            var.llvm_idx = ix
            var.write_variable = var_write
            if getattr(var, 'logger_level',
                       None) is None:  # added to temporary variables - maybe put in generate_equations?
                setattr(var, 'logger_level', LoggerLevel.ALL)

        log.info("Lowering model finished")

    def generate_path_to_varaible(self):
        for k, v in self.aliases.items():
            self.path_to_variable[k] = self.variables[v]

    def update_all_variables(self):
        for k, v in self.vars_ordered_values.items():
            self.var_write(self.variables[k].value, v)

    def update_local_variables(self):
        vars = self.numba_model.read_variables()
        for k, v in self.vars_ordered_values.items():
            self.variables[k].value = vars[v]


    def history_as_dataframe(self):
        time = self.data[0]
        data = {'time': time}

        for i, var in enumerate(self.var_list):
            data.update({var: self.data[i + 1]})

        self.df = pd.DataFrame(data)
        self.df = self.df.dropna(subset=['time'])
        self.df = self.df.set_index('time')
        self.df.index = pd.to_timedelta(self.df.index, unit='s')

    def validate_bindings(self):
        """
        Checks that all bindings are fulfilled.
        """
        valid = True
        for item in self.model_items.values():
            for binding in item.bindings:
                if binding.is_bindend():
                    pass
                else:
                    valid = False
        return valid

    def search_items(self, item_tag):
        """
        Search an item in items registered in the model by a tag

        Returns
        ----------
        items : list of :class:`numerous.engine.system.Item`
            set of items with given tag
        """
        return [item for item in self.model_items.values() if item.tag == item_tag]

    @property
    def states_as_vector(self):
        """
        Returns current states values.

        Returns
        -------
        state_values : array of state values

        """
        return self.var_func()[self.state_idx]

    def get_variable_path(self, id, item):
        for (variable, namespace) in item.get_variables():
            if variable.id == id:
                return "{0}.{1}".format(namespace.tag, variable.tag)
        if hasattr(item, 'registered_items'):
            for registered_item in item.registered_items.values():
                result = self.get_variable_path(id, registered_item)
                if result:
                    return "{0}.{1}".format(registered_item.tag, result)
        return ""

    def add_event(self, key, condition: Callable, action: Callable, terminal: bool = False, direction: int = -1,
                  compiled: bool = False, is_external: bool = False):
        """

        Method for adding state events on the model.

        :param key: the name of the event
        :param condition: the condition function that determines if the event takes place
        :param action: the action function that executes the event
        :param terminal: not used
        :param direction: Direction of the event that triggers it (<0 from positive to negative, and >0 from negative
        to positive)
        :param compiled: if the action and condition functions are compiled already when adding
        :param is_external: True if action function should not be compiled

        """

        condition_ast, condition_closurevariables = replace_path_strings(self, condition, "var")
        condition_ = Condition(condition, condition_ast, condition_closurevariables)
        action_closeurevariables = None
        action_ast = None
        if not is_external:
            action_ast, action_closeurevariables = replace_path_strings(self, action, "var")

        action_ = Action(action, action_ast, action_closeurevariables)
        event = StateEvent(key=key, condition=condition_, action=action_, direction=direction, compiled=compiled,
                           terminal=terminal, is_external=is_external)
        self.events.append(event)

    def add_timestamp_event(self, key: str, action: Callable[[float, dict[str, float]], None],
                            timestamps: Optional[list] = None, periodicity: Optional[float] = None,
                            is_external: bool = False):
        """
        Method for adding time stamped events, that can trigger at a specific time, either given as an explicit list of
        timestamps, or a periodic trigger time. A time event must be associated with a time event action function with
        the signature (t, variables).

        :param key: A name for the event
        :type key: str
        :param action: callable with signature (t, variables)
        :type action: Callable[[float, dict[str, float]]
        :param timestamps: an optional list of timestamps
        :type timestamps: Optional[list]
        :param periodicity: an optional time value for which the event action function is triggered at each multiple of
        :type periodicity: Optional[float]
        :param is_external: True if action function should not be compiled
        :type is_external: bool

        """
        action_closeurevariables = None
        action_ast = None
        if not is_external:
            action_ast, action_closeurevariables = replace_path_strings(self, action, "var")

        action_ = Action(action, action_ast, action_closeurevariables)
        event = TimestampEvent(key=key, action=action_, timestamps=timestamps, periodicity=periodicity,
                               is_external=is_external)
        self.timestamp_events.append(event)

    def generate_mock_event(self) -> None:
        def condition(t, v):
            return 1.0

        def action(t, v):
            i = 1

        self.add_event("mock", condition, action)

    def _generate_mock_timestamp_event(self):
        def action(t, v):
            i = 1

        self.add_timestamp_event("mock", action, [-1])

    def generate_event_condition_ast(self) -> tuple[CPUDispatcher, npt.ArrayLike]:
        if len(self.events) == 0:
            self.generate_mock_event()
        return generate_event_condition_ast(self.events, self.imports.from_imports)

    def generate_event_action_ast(self, events) -> CPUDispatcher:
        return generate_event_action_ast(events, self.imports.from_imports)

    def _get_var_idx(self, var, idx_type):
        if idx_type == "state":
            return np.where(self.state_idx == var.llvm_idx)[0]
        if idx_type == "var":
            return [var.llvm_idx]

    def _create_model_namespaces(self, item):
        namespaces_list = []
        for namespace in item.registered_namespaces.values():
            set_namespace = isinstance(namespace, SetNamespace)
            model_namespace = ModelNamespace(namespace.tag, namespace.outgoing_mappings, item.tag, namespace.items,
                                             namespace.path, set_namespace, '.'.join(item.path))
            model_namespace.variable_scope = namespace.get_flat_variables()
            model_namespace.set_variables = namespace.set_variables

            equation_dict = {}
            eq_variables_ids = []
            for eq in namespace.associated_equations.values():
                equations = []
                ids = []

                for equation in eq.equations:
                    equations.append(equation)
                for vardesc in eq.variables_descriptions:
                    if set_namespace:
                        for item in namespace.items:
                            variable = item.registered_namespaces[namespace.tag].get_variable(vardesc.tag)
                            ids.append(variable.id)
                    else:
                        variable = namespace.get_variable(vardesc.tag)
                        ids.append(variable.id)
                equation_dict.update({eq.tag: equations})
                eq_variables_ids.append(ids)
            model_namespace.equation_dict = equation_dict
            model_namespace.variables = {v.id: v for vs in model_namespace.variable_scope for v in vs}
            namespaces_list.append(model_namespace)
        return namespaces_list

    # Method that generates numba_model
    def _generate_compiled_model(self, start_time, number_of_timesteps):
        for spec_dict in self.numba_callbacks_variables:
            for item in spec_dict.items():
                numba_model_spec.append(item)

        # Creating a copy of CompiledModel class so it is possible
        # to creat instance detached from muttable type of CompiledModel
        tmp = type(f'{CompiledModel.__name__}' + self.system.id, CompiledModel.__bases__, dict(CompiledModel.__dict__))
        if self.use_llvm:
            @jitclass(numba_model_spec)
            class CompiledModel_instance(tmp):
                pass
        else:
            class CompiledModel_instance(tmp):
                pass

        NM_instance = CompiledModel_instance(self.init_values,
                                             self.derivatives_idx,
                                             self.state_idx,
                                             np.array([v.value for v in self.global_variables.values()],
                                                      dtype=np.float64),
                                             number_of_timesteps,
                                             start_time,
                                             self.historian.get_historian_max_size(number_of_timesteps,
                                                                                   len(self.events)),
                                             self.external_mappings.external_mappings_time,
                                             self.number_of_external_mappings,
                                             self.external_mappings.external_mappings_numpy,
                                             self.external_mappings.external_df_idx,
                                             self.external_mappings.interpolation_info,
                                             self.is_external_data,
                                             self.external_mappings.t_max,
                                             self.external_mappings.t_min,
                                             self.external_idx,
                                             self.post_step
                                             )

        # NM_instance.run_init_callbacks(start_time)
        NM_instance.map_external_data(start_time)

        # NM_instance.historian_update(start_time)
        self.numba_model = NM_instance
        return self.numba_model

    def _set_functions(self, equations_llvm_opt, n_deriv, max_var):
        for equation in equations_llvm_opt:
            llmod2 = llvm.parse_assembly(equation)
            ee.add_module(llmod2)
        ee.finalize_object()
        cfptr = ee.get_function_address("kernel")

        cfptr_var_r = ee.get_function_address("vars_r")
        cfptr_var_w = ee.get_function_address("vars_w")

        c_float_type = type(np.ctypeslib.as_ctypes(np.float64()))

        diff_ = CFUNCTYPE(POINTER(c_float_type), POINTER(c_float_type), POINTER(c_float_type))(cfptr)

        vars_r = CFUNCTYPE(POINTER(c_float_type), c_int64)(cfptr_var_r)

        vars_w = CFUNCTYPE(c_void_p, c_double, c_int64)(cfptr_var_w)

        n_deriv = n_deriv
        max_var = max_var

        @njit('float64[:](float64[:],float64[:])')
        def compiled_compute(y, global_vars):
            deriv_pointer = diff_(y.ctypes, global_vars.ctypes)
            return carray(deriv_pointer, (n_deriv,)).copy()

        @njit('float64[:]()')
        def var_func():
            variables_pointer = vars_r(0)
            variables_array = carray(variables_pointer, (max_var,))

            return variables_array.copy()

        @njit('void(float64,int64)')
        def var_write(var, idx):
            vars_w(var, idx)

        def c1(self, array_):
            return compiled_compute(array_, self.global_vars)

        def c2(self):
            return var_func()

        def c3(self, value, idx):
            return var_write(value, idx)

        setattr(CompiledModel, "compiled_compute", c1)
        setattr(CompiledModel, "read_variables", c2)
        setattr(CompiledModel, "write_variables", c3)

        for varname, ix in self.vars_ordered_values.items():
            var = self.variables[varname]
            var.write_variable = var_write
            if getattr(var, 'logger_level',
                       None) is None:  # added to temporary variables - maybe put in generate_equations?
                setattr(var, 'logger_level', LoggerLevel.ALL)

        self.compiled_compute, self.var_func, self.var_write = compiled_compute, var_func, var_write

        def c4(values_dict):
            return [self.var_write(v, self.vars_ordered_values[self.aliases[k]]) for k, v in values_dict.items()]

        def c5():
            vals = var_func()
            return {self.inverse_aliases[k]: v for k, v in zip(self.vars_ordered_values.keys(), vals)}

        setattr(self, "update_variables", c4)
        setattr(self, "get_variables", c5)
        self._assembly_tail()

    def create_historian_dict(self, historian_data=None):
        if historian_data is None:
            historian_data = self.numba_model.historian_data
        time = historian_data[0]

        data = {var: historian_data[i + 1] for var, i in self.logged_variables.items()}
        data.update({'time': time})
        return data

    def generate_not_nan_history_array(self):
        return self.numba_model.historian_data[:, ~np.isnan(self.numba_model.historian_data).any(axis=0)]

    def create_historian_df(self):
        if self.historian_df is not None:
            import pandas as pd
            self.historian_df = AliasedDataFrame(pd.concat([self.historian_df.df,
                                                            self._generate_history_df(
                                                                self.generate_not_nan_history_array()).df],
                                                           axis=0, sort=False, ignore_index=True),
                                                 aliases=self.aliases, rename_columns=True)

        else:
            self.historian_df = self._generate_history_df(self.generate_not_nan_history_array())
        self.historian.store(self.historian_df)

    def _generate_history_df(self, historian_data):
        data = self.create_historian_dict(historian_data)
        return AliasedDataFrame(data, aliases=self.aliases, rename_columns=True)

    def set_external_mappings(self, external_mappings, data_loader):

        external_mappings_unpacked = [ExternalMappingUnpacked(external_mappings, data_loader)]
        external_mappings_unpacked = self.system_external_mappings + external_mappings_unpacked
        self.is_external_data = True if len(external_mappings_unpacked) else False
        self.external_mappings = ExternalMapping(external_mappings_unpacked) if len(
            external_mappings_unpacked) else EmptyMapping()

        number_of_external_mappings = 0
        external_idx = []

        for var in self.variables.values():
            if self.external_mappings.is_mapped_var(self.variables, var.id, self.system.id):
                external_idx.append(self.vars_ordered_values[var.id])
                number_of_external_mappings += 1
                self.external_mappings.add_df_idx(self.variables, var.id, self.system.id)
        self.number_of_external_mappings = number_of_external_mappings
        self.external_mappings.store_mappings()

        self.external_idx = np.array(external_idx, dtype=np.int64)

        self.numba_model.external_idx = self.external_idx
        self.numba_model.external_mappings_time = self.external_mappings.external_mappings_time
        self.numba_model.number_of_external_mappings = self.number_of_external_mappings
        self.numba_model.external_mappings_numpy = self.external_mappings.external_mappings_numpy
        self.numba_model.external_df_idx = self.external_mappings.external_df_idx
        self.numba_model.approximation_type = self.external_mappings.interpolation_info
        self.numba_model.is_external_data = self.is_external_data
        self.numba_model.max_external_t = self.external_mappings.t_max
        self.numba_model.min_external_t = self.external_mappings.t_min

        self.numba_model.map_external_data(0)

        # if self.numba_model.is_external_data_update_needed(0):
        self.numba_model.is_external_data = self.external_mappings.load_new_external_data_batch(0)
        if self.numba_model.is_external_data:
            self.numba_model.update_external_data(self.external_mappings.external_mappings_numpy,
                                                  self.external_mappings.external_mappings_time,
                                                  self.external_mappings.t_max, self.external_mappings.t_min)

    @classmethod
    def from_file(cls, filename: str):

        system_, logger_level, imports, use_llvm, vars_ordered_values, variables, state_idx, \
            derivatives_idx, init_values, aliases, equations_llvm_opt, max_var, n_deriv = pickle.load(
            open(filename, "rb"))
        model = Model(system=system_, assemble=False, logger_level=logger_level,
                      use_llvm=use_llvm)
        model.variables = variables
        model.imports = imports
        model.vars_ordered_values = vars_ordered_values
        model.state_idx = state_idx
        model.derivatives_idx = derivatives_idx
        model.init_values = init_values
        model.aliases = aliases

        model._set_functions(equations_llvm_opt, n_deriv, max_var)
        return model

    def clone(self, clonable=False):

        if not self.clonable:
            raise Exception("Model isn't clonable")
        system_ = self.system
        logger_level = self.logger_level
        use_llvm = self.use_llvm
        model = Model(system=system_, assemble=False, logger_level=logger_level,
                      use_llvm=use_llvm)
        model.variables = self.variables
        model.imports = self.imports
        model.vars_ordered_values = self.vars_ordered_values
        model.state_idx = self.state_idx
        model.derivatives_idx = self.derivatives_idx
        model.init_values = self.init_values
        model.aliases = self.aliases

        model._set_functions(self.equations_llvm_opt, self.n_deriv, self.max_var)

        if clonable:
            model.clonable = True
            model.equations_llvm_opt = self.equations_llvm_opt
            model.n_deriv = self.n_deriv
            model.max_var = self.max_var

        return model
