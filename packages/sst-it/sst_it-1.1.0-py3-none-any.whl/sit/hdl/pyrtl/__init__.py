"""Implementation of the PyRTL class

This class inherits from the HardwareDescriptionLanguage base class and implements its own methods of
parsing, modifying and generating boilerplate code for its specific paradigms.
"""
from .. import HardwareDescriptionLanguage


class PyRTL(HardwareDescriptionLanguage):
    def __init__(
        self,
        module_name,
        lib,
        ipc="sock",
        module_dir="",
        lib_dir="",
        desc="",
    ):
        """Constructor for PyRTL HardwareDescriptionLanguage.

        Parameters:
        -----------
        ipc : str (options: "sock", "zmq")
            method of IPC
        module : str
            SST element component and HDL module name
        lib : str
            SST element library name
        module_dir : str (default: "")
            directory of HDL module
        lib_dir : str (default: "")
            directory of HardwareDescriptionLanguage library
        desc : str (default: "")
            description of the SST model
        driver_template_path : str (default: "")
            path to the black box-driver boilerplate
        component_template_path : str (default: "")
            path to the black box-model boilerplate
        """
        super().__init__(
            ipc=ipc,
            module_name=module_name,
            lib=lib,
            module_dir=module_dir,
            lib_dir=lib_dir,
            desc=desc,
        )

        if self.ipc == "sock":

            # driver attributes
            self.driver_ipc = "socket"
            self.driver_bind = (
                "_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)"
            )
            self.send = "sendall"
            self.connect = "connect"

        elif self.ipc == "zmq":

            # driver attributes
            self.driver_ipc = "zmq"
            self.driver_bind = """context = zmq.Context()
_sock = context.socket(zmq.REQ)"""
            self.send = "send"
            self.connect = "bind"

        self.exec_cmd = """m_output.verbose(
                CALL_INFO, 1, 0, "\\033[35m[FORK] %s\\033[0m\\n\", cmd.c_str()
            );
            char* args[8];
            int i = 0;
            args[i] = std::strtok(&cmd[0u], " ");

            while (args[i] != nullptr) {
                args[++i] = strtok(nullptr, " ");
            }
            args[i] = nullptr;"""

        self.paths.set_driver_path(f"{self.module_name}_driver.py")
        self.paths.set_comp_path(f"{self.module_name}_comp.cpp")

    def _compute_signal_buffer_len(self, signal_type, signal_len):
        """Parse the type and computes its width from the signal

        Parameters:
        -----------
        signal : str
            signal definition

        Returns:
        --------
        int
            signal width
        """
        return self._get_num_digits(signal_len)

    def _get_driver_outputs(self):
        """Generate output bindings for both the components in the black box

        Returns:
        --------
        str
            snippet of code representing output bindings
        """
        return self._sig_fmt(
            fmt="str({module_name}.sim.inspect({module_name}.{sig})).encode()",
            split_func=lambda x: {
                "module_name": self.module_name,
                "sig": x["name"],
            },
            array=self._get_output_ports(),
            delim=" +\n" + " " * 8,
        )

    def _get_driver_inputs(self):
        """Generate input bindings for the driver.

        Returns:
        --------
        str
            snippet of code representing input bindings
        """
        fmt = '"{sig}": int(signal[{sp}:{sl}]),'
        start_pos = 0
        clock_fmt = '"{sig}": int(signal[{sp}:{sl}]) % 2,'
        driver_inputs = []

        for input_port in self._get_input_ports():
            driver_inputs.append(
                fmt.format(
                    sp=start_pos,
                    sl=str(input_port["len"] + start_pos),
                    sig=input_port["name"],
                )
            )
            start_pos += input_port["len"]

        if self.ports["clock"]:
            for clock_port in self.ports["clock"]:
                driver_inputs.append(
                    clock_fmt.format(
                        sp=start_pos,
                        sl=str(input_port["len"] + start_pos),
                        sig=clock_port["name"],
                    )
                )
                start_pos += int(clock_port["len"])

        self.driver_buf_size = start_pos + 1
        return ("\n" + " " * 8).join(driver_inputs)

    def _get_driver_defs(self):
        """Map definitions for the PyRTL driver format string

        Returns:
        --------
        dict(str:str)
            format mapping of template PyRTL driver string
        """
        return {
            "ipc": self.driver_ipc,
            "driver_bind": self.driver_bind,
            "connect": self.connect,
            "send": self.send,
            "module_dir": self.paths.get_module_dir().resolve(),
            "module_name": self.module_name,
            "buf_size": self.driver_buf_size,
        }
