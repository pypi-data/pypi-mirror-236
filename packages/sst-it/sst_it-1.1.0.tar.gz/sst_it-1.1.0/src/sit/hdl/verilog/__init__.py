"""Implementation of the Verilog class

This class inherits from the HardwareDescriptionLanguage base class and implements its
own methods of parsing, modifying and generating boilerplate code for its
specific paradigms.
"""
from .. import HardwareDescriptionLanguage
from ...exceptions import SignalFormatException


class Verilog(HardwareDescriptionLanguage):
    def __init__(
        self,
        module_name,
        lib,
        ipc="sock",
        module_dir="",
        lib_dir="",
        desc="",
    ):
        """Constructor for Verilog HardwareDescriptionLanguage

        Parameters:
        -----------
        module : str
            SST element component and HDL module name
        lib : str
            SST element library name
        ipc : str (options: "sock", "zmq")
            method of IPC
        module_dir : str (default: "")
            directory of HDL module
        lib_dir : str (default: "")
            directory of HardwareDescriptionLanguage library
        desc : str (default: "")
            description of the SST model
        """
        super().__init__(
            module_name=module_name,
            lib=lib,
            ipc=ipc,
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
        self.paths.set_extra_file_paths({"makefile": "Makefile.config"})

    def _compute_signal_buffer_len(self, signal_type, signal_len):
        """Parse the type and computes its size from the signal

        Parameters:
        -----------
        signal : str
            signal definition

        Returns:
        --------
        int
            signal width
        """

        match signal_type:

            case "int":
                return self._get_num_digits(signal_len)

            case "bit":
                return signal_len

            case _:
                raise SignalFormatException(
                    f'Invalid signal type "{signal_type}"'
                ) from None

    def _get_driver_outputs(self):
        """Generate output bindings for both the components in the black box

        Returns:
        --------
        str
            snippet of code representing output bindings
        """
        return self._sig_fmt(
            fmt="str(dut.{sig}.value{type})",
            split_func=lambda x: {
                "sig": x["name"],
                "type": (".integer" if x["type"] == "int" else ""),
            },
            array=self._get_output_ports(),
            delim="\n" + (" " * 12) + "+ ",
        )

    def _get_driver_inputs(self):
        """Generate input bindings for the driver.

        Returns:
        --------
        str
            snippet of code representing input bindings
        """
        fmt = "dut.{sig}.value = int(signal[{sp}:{sl}])"
        start_pos = 0
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
            clock_fmt = "dut.{sig}.value = int(signal[{sp}:{sl}]) % 2"

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
        """Map definitions for the Verilog driver format string

        Returns:
        --------
        dict(str:str)
            format mapping of template Verilog driver string
        """
        return {
            "ipc": self.driver_ipc,
            "driver_bind": self.driver_bind,
            "connect": self.connect,
            "send": self.send,
            "module_name": self.module_name,
            "buf_size": self.driver_buf_size,
        }

    def _generate_extra_files(self):

        template = self.paths.read_template_str("makefile")
        template_str = self.template.render(
            template,
            dict(
                module_name=self.module_name,
                module_dir=self.paths.get_module_dir().resolve(),
            ),
        )

        with open(self.paths.get_gen("makefile"), "w") as makefile:
            makefile.write(template_str)
        print(f"Dumped Makefile to '{self.paths.get_gen('makefile')}'")
