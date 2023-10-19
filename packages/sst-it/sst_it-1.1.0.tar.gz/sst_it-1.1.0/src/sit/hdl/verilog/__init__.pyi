from typing import Literal

from .. import HardwareDescriptionLanguage

class Verilog(HardwareDescriptionLanguage):
    def __init__(
        self,
        module_name: str,
        lib: str,
        ipc: Literal["sock", "zmq"] = ...,
        module_dir: str = ...,
        lib_dir: str = ...,
        desc: str = ...,
    ) -> None: ...
    def _compute_signal_buffer_len(
        self, signal_type: str, signal_len: int
    ) -> int: ...
    def _get_driver_inputs(self) -> str: ...
    def _get_driver_outputs(self) -> str: ...
    def _get_driver_defs(self) -> dict[str, str]: ...
    def _generate_extra_files(self) -> None: ...
