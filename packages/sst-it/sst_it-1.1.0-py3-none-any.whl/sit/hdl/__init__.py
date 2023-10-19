"""Implementation of the base class of SIT. This class generates the
boilerplate code required to build the black box interface in SST
Interoperability Toolkit.

This class is purely virtual and therefore requires a child class to inherit
and implement its protected methods. The child class must implement the
following protected methods:
- _get_driver_inputs()
- _get_driver_outputs()
- _get_driver_defs()

The following public methods are inherited by the child classes and are not
to be overridden:
- set_ports(ports)
- generate_boilerplate()
- fixed_width_float_output(precision)
- disable_runtime_warnings(warnings)
"""

import math

from ..exceptions import ConfigException, PortException, SignalFormatException
from ..files import Paths
from ..render import TemplateRenderer


class HardwareDescriptionLanguage:
    def __init__(
        self,
        module_name,
        lib,
        ipc="sock",
        module_dir="",
        lib_dir="",
        desc="",
    ):
        """Constructor for the virtual base class SIT

        Initialize all member port variables and component variables. Only the
        following methods are public:
        `set_ports(ports)`
        `generate_boilerplate()`

        Parameters:
        -----------
        module_name : str
            SST element component and HDL module name
        lib : str
            SST element library name
        ipc : str (options: "sock", "zmq")
            method of IPC
        module_dir : str (default: "")
            directory of HDL module
        lib_dir : str (default: "")
            directory of SIT library
        desc : str (default: "")
            description of the SST model

        Raises:
        -------
        ConfigException
            unsupported IPC inputted
        """
        if ipc in ("sock", "zmq"):
            self.ipc = ipc
        else:
            raise ConfigException(f"{ipc} is not a supported IPC protocol")

        self.module_name = module_name
        self.lib = lib
        self.lib_dir = lib_dir
        self.desc = desc
        self.exec_cmd = ""

        self.precision = 0
        self.extra_libs = ""
        self.disable_warning = ""

        self.hdl_str = self.__class__.__name__.lower()

        self.width_macros = {}
        self.ports: dict[str, list[dict[str, int]]] = {
            "clock": [],
            "input": [],
            "output": [],
            "inout": [],
        }

        self.driver_buf_size = 0
        self.comp_buf_size = 0
        if self.ipc == "sock":

            # component attributes
            self.sig_type = "SITSocketBuffer"

        elif self.ipc == "zmq":

            # component attributes
            self.sig_type = "SITZMQBuffer"

        # shared attributes
        self.sender = self.receiver = "sit_buf"

        self.paths = Paths(self.hdl_str, module_dir)

        self.template = TemplateRenderer()

    def _get_driver_inputs(self):
        raise NotImplementedError()

    def _get_driver_outputs(self):
        raise NotImplementedError()

    def _get_driver_defs(self):
        raise NotImplementedError()

    def _compute_signal_buffer_len(self, signal_type, signal_len):
        raise NotImplementedError()

    def _generate_extra_files(self):
        raise NotImplementedError()

    @staticmethod
    def _sig_fmt(fmt, split_func, array, delim):
        """Format lists of signals based on fixed arguments

        Parameters:
        -----------
        fmt : str
            string format
        split_func : lambda or dict(str:str)
            map to split on the signals
        array : list(str)
            list of signals
        delim : str (default: ";n    ")
            delimiter

        Returns:
        --------
        str
            string formatted signals
        """
        return delim.join(fmt.format(**split_func(i)) for i in array)

    def _get_signal_width_from_macro(self, signal_type, signal_type_macro):
        """Get width of a signal type mapped in width_macros

        Parameters:
        -----------
        signal_type : str
            signal type of port
        signal_type_macro : str
            signal type macro of port

        Raises:
        -------
        SignalFormatException
            signal width macro not found

        Returns:
        --------
        value : str
            width of signal type
        """
        if signal_type_macro_value := self.width_macros.get(
            signal_type_macro, None
        ):
            return signal_type_macro_value

        raise SignalFormatException(
            f"Invalid macro in signal: {signal_type}"
        ) from None

    def _get_all_ports(self):
        """Flatten all types of ports into a single array

        Returns:
        --------
        generator
            all ports in a single array
        """
        return [i for sig in self.ports.values() for i in sig]

    def _get_input_ports(self):
        """Flatten all types of ports into a single array

        Returns:
        --------
        generator
            all ports in a single array
        """
        return self.ports["input"]

    def _get_output_ports(self):
        """Flatten all types of ports into a single array

        Returns:
        --------
        generator
            all ports in a single array
        """
        return self.ports["output"]

    @staticmethod
    def _get_num_digits(signal):
        """Compute the minimum number of digits required to hold signal data
        type width by calculating: `floor(log2(-1 + 2^x)/log2(10)) + 1`. This
        expression is equivalent to `ceil(x / log2(10))`

        Parameters:
        -----------
        signal : int
            signal data type width

        Returns:
        --------
        int
            number of digits for signal width
        """
        # log2(10) = 3.321928094887362
        return math.ceil(signal / 3.321928094887362)

    def __get_comp_defs(self):
        """Map definitions for the component format string

        Returns:
        --------
        dict(str:str)
            format mapping of template component string
        """
        self.comp_buf_size = sum(
            output_port["len"] for output_port in self.ports["output"]
        )
        if self.precision and self.precision > self.comp_buf_size - 2:
            print(
                f"Component buffer size increased from {self.comp_buf_size} to ",
                end="",
            )
            self.comp_buf_size += self.precision - 2
            print(f"{self.comp_buf_size} to include specified precision")

        return {
            "exec_cmd": self.exec_cmd,
            "lib_dir": self.lib_dir,
            "module_name": self.module_name,
            "lib": self.lib,
            "desc": self.desc,
            "ports": self._sig_fmt(
                fmt="""{{"{link}", "{desc}", {{"sst.Interfaces.StringEvent"}}}}""",
                split_func=lambda x: {
                    "link": self.module_name + x[0],
                    "desc": self.module_name + x[-1],
                },
                array=(("_din", " data in"), ("_dout", " data out")),
                delim=",\n" + " " * 8,
            ),
            "sig_type": self.sig_type,
            "buf_size": self.comp_buf_size,
            "sender": self.sender,
            "receiver": self.receiver,
        }

    def __generate_comp_str(self):
        """Generate the black box-model code based on methods used to format
        the template file

        Raises:
        -------
        TemplateFileNotFound
            boilerplate template file not found

        Returns:
        --------
        str
            boilerplate code representing the black box-model file
        """
        template = self.paths.read_template_str("comp")
        return self.template.render(template, self.__get_comp_defs())

    def __generate_driver_str(self):
        """Generate the black box-driver code based on methods used to format
        the template file

        Raises:
        -------
        TemplateFileNotFound
            boilerplate template file not found

        Returns:
        --------
        str
            boilerplate code representing the black box-driver file
        """
        template = self.paths.read_template_str("driver")
        return self.template.render(
            template,
            dict(
                inputs=self._get_driver_inputs(),
                outputs=self._get_driver_outputs(),
                **self._get_driver_defs(),
            ),
        )

    def set_template_paths(self, dir="", driver="", comp=""):
        self.paths.set_template_paths(dir, driver, comp)

    def set_gen_paths(self, dir="", driver="", comp=""):
        self.paths.set_gen_paths(dir, driver, comp)

    def set_width_macros(self, width_macros):
        """Set width macros provided by user

        width_macros : dict(str:[str|int]) (default: dict(None:None))
            mapping of signal width macros to their integer values. An HDL
            module may declare constants or user-inputted variables in their
            implementation to determine signal widths.
            The module can only know the values of those macros by utilizing
            this parameter.
            Example:
            `width_macros = {
                "ADDRESS_WIDTH": 16,
                "DATA_WIDTH": 16,
            }`"""
        self.width_macros = width_macros

    def fixed_width_float_output(self, precision):
        """Generate additional methods to handle ports with float signals

        Parameters:
        -----------
        precision : int
            level of precision for float signals

        Raises:
        -------
        AttributeError
            method not supported
        """
        self.precision = precision
        print("Adding fixed precision for float outputs")
        try:
            self._fixed_width_float_output()
        except AttributeError:
            raise AttributeError(
                f"fixed_width_float_output() not supported with {self.module_name}"
            )

    def disable_runtime_warnings(self, warnings):
        """Generate additional methods to disable driver runtime warnings

        Parameters:
        -----------
        warnings : str|list(str)
            runtime warning or list of runtime warnings to ignore

        Raises:
        -------
        AttributeError
            method not supported
        """
        if not isinstance(warnings, list):
            warnings = [warnings]
        for warning in warnings:
            try:
                self._disable_runtime_warnings(warning)
            except AttributeError:
                raise AttributeError(
                    f"disable_runtime_warnings() not supported with {self.module_name}"
                )

    def set_ports(self, ports):
        """Assign ports to their corresponding member lists

        Parameters:
        -----------
        ports : nested dict
            type-declared signals in the form:
                {"name": <SIGNAL NAME>, "type": <SIGNAL DATA TYPE>, "len": <SIGNAL LEN>}
            The current types of signals supported are:
                ("clock", "input", "output", "inout")

        Raises:
        -------
        SignalFormatException
            invalid signal format provided
        PortException
            invalid port type provided
        """
        for port_type, signals in ports.items():

            for signal in signals:

                if len(signal) != 3:
                    raise SignalFormatException(
                        "Invalid signal format"
                    ) from None

                signal["len"] = self._compute_signal_buffer_len(
                    signal_type=signal["type"], signal_len=signal["len"]
                )

                try:
                    self.ports[port_type].append(signal)

                except KeyError:
                    raise PortException(
                        f"{signal[port_type]} is an invalid port type"
                    ) from None

    def generate_boilerplate(self):
        """Provide a high-level interface to the user to generate both the
        components of the black box and dump them to their corresponding files

        Raises:
        -------
        PortException
            no ports were provided
        """
        if not len(self.ports):
            raise PortException(
                "No ports were set. Make sure to call set_ports() before generating files."
            )

        self.paths.get_gen("dir").mkdir(exist_ok=True)

        with open(self.paths.get_gen("driver"), "w") as driver_file:
            driver_file.write(self.__generate_driver_str())

        with open(self.paths.get_gen("comp"), "w") as comp_file:
            comp_file.write(self.__generate_comp_str())

        try:
            self._generate_extra_files()
        except NotImplementedError:
            pass
