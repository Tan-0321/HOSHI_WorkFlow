import subprocess
import sys
from pathlib import Path
from datetime import datetime
import argparse



class HoshiModel:
    """Represents a HOSHI model directory containing an `evol` executable."""
    DIR = None
    PROGRAM_EXEC = None
    henyey_params = None

    def __init__(self, model_dir):
        self.DIR = Path(model_dir)
        self.PROGRAM_EXEC = self.DIR / "evol"
        if not self.DIR.exists():
            raise FileNotFoundError(f"Model directory not found: {self.DIR}")
        if not self.PROGRAM_EXEC.exists():
            raise FileNotFoundError(f"Executable not found: {self.PROGRAM_EXEC}")
        self.henyey_params = self._read_henyey_params()

    def run(self, log_file: Path | str | None = None, check: bool = False) -> int:
        """Run the `evol` program and capture output to log_file.

        Args:
            log_file: path to write output. If None, a timestamped .log file
                will be created inside the model directory.
            check: if True, raise CalledProcessError on non-zero exit code.

        Returns:
            The subprocess return code.
        """
        if log_file is None:
            s = datetime.now().strftime("%y_%m%d_%H%M%S")
            log_file = self.DIR / f"run_{s}.log"
        else:
            log_file = Path(log_file)
            if not log_file.is_absolute():
                # relative paths are created relative to the model dir
                log_file = self.DIR / log_file

        # Ensure parent directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, "wb") as f:
            # Run the executable and capture both stdout and stderr
            proc = subprocess.run([str(self.PROGRAM_EXEC)], stdout=f, stderr=subprocess.STDOUT)

        if check and proc.returncode != 0:
            # Re-raise as CalledProcessError for callers who want an exception
            raise subprocess.CalledProcessError(proc.returncode, str(self.PROGRAM_EXEC))

        return proc.returncode

    def _read_henyey_params(self) -> dict:
        """Read and return parameters from the self.DIR/param/files.henyey file.

        Returns:
            A dictionary of parameter names and their values.
        """
        input_file = self.DIR / "param" / "files.henyey"
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        params = {
            "input_structure_dir": None,
            "output_summary_dir": None,
            "input_structure_file": None,
            "output_structure_file": None,
            "NAME_IN": None,
            "NAME_OUT": None,
            "NSTG_max": None,
            "MAXQTY": None,
            "FLAG_reduce_D_and_Li": None,
            "relative_metallicity": None,
            "FLAG_change_mass": None,
            "new_mass": None,
        }
        values = []
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                line = line.split(":", 1)[0].strip()
                if line and not (line.startswith("*") or line.startswith("#")):
                    values.append(line)
        #print(values)
        
        keys = list(params.keys())
        for i, key in enumerate(keys):
            if i < len(values):
                params[key] = values[i]
        # parts = params['MAXQTY'].split()
        # if len(parts) == 2:
        #     params['MAXQTY'] = (parts[0], parts[1])
        return params

    def modify_input_henyey(self, new_params: dict) -> None:
        """Modify the self.DIR/param/files.henyey file with new parameters.

        Args:
            new_params: dictionary of parameter names and their new values.
        """
        input_file = self.DIR / "param" / "files.henyey"
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        for key in new_params.keys():
            if key not in self.henyey_params:
                raise KeyError(f"Key '{key}' not found in Henyey parameters.\n"
                               f"Available keys are: {list(self.henyey_params.keys())}")

        keys_def = list(self.henyey_params.keys())
        i_key_def = 0
        keys_new = list(new_params.keys())
        lines = []
        with open(input_file, "r") as f:
            for line in f:
                if not (new_params == {}):
                    line = line.rstrip()
                    val = line.split(":", 1)[0].strip()
                    if val and not (val.startswith("*") or val.startswith("#")):
                        i_key_def += 1
                        key = keys_def[i_key_def - 1]
                        new_val = None
                        print(f"matching new values for '{key}'......")
                        for k in keys_new:
                            
                            if k == key:
                                new_val = new_params.pop(k)
                                print(f'\tnew_val found: {new_val}')
                                break
                        if new_val is not None:
                            if line.count(':') >= 1:
                                new_line = f" {new_val} \t\t: {line.split(':')[1].strip()}"
                            else:
                                new_line = f" {new_val}"
                            lines.append(new_line+'\n')
                        else:
                            lines.append(line+'\n')
                    else:
                        lines.append(line+'\n')
                else:
                    lines.append(line)

        with open("test.txt", "w") as f:
            f.writelines(lines)
        return None





