import logging
import re
import string
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, List, Union, Tuple
import io
from functools import lru_cache

log = logging.getLogger(__file__)


class VenvMissing(IOError):
    ...


class VenvCreationFailed(IOError):
    ...


STD_OUT = io.BytesIO
STD_ERR = io.BytesIO


def execute_subprocess(
    execution: List[Union[str, Path]], silent: bool = False
) -> Tuple[subprocess.Popen, STD_OUT, STD_ERR]:
    log.info(f"Executing subprocess {' '.join(str(part) for part in execution)}")
    process = subprocess.Popen(
        execution, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    std_out_full = io.BytesIO()
    std_err_full = io.BytesIO()
    if not silent:
        for line in process.stdout:
            std_out_full.write(line)
            sys.stdout.write(line.decode("utf-8"))
        for line in process.stderr:
            std_err_full.write(line)
            sys.stderr.write(line.decode("utf-8"))
    std_out, std_err = process.communicate()
    std_out_full.write(std_out)
    std_err_full.write(std_err)
    std_err_full.seek(0)
    std_out_full.seek(0)
    return process, std_out_full, std_err_full


def pip_update_pip_subprocess(executable: Path) -> None:
    execution = [executable, "-m", "pip", "install", "--upgrade", "wheel", "pip"]
    process, _, _ = execute_subprocess(execution)
    if process.returncode:
        raise IOError(f"Pip update failed Return code {process.returncode}")


def pip_install_subprocess(executable: Path, version: str) -> None:
    index_url = "https://www.pypi.org/simple"
    piwheels_url = "https://www.piwheels.org/simple"
    if version:
        str_pyaware = f"pyaware=={version}"
    else:
        str_pyaware = f"pyaware"
    execution = [
        executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        str_pyaware,
        "--index-url",
        index_url,
        "--extra-index-url",
        piwheels_url,
    ]
    process, _, _ = execute_subprocess(execution)
    if process.returncode:
        raise IOError(f"Pip install failed Return code {process.returncode}")


class ServiceType(Enum):
    SYSTEMD = "systemd"
    INITTAB = "inittab"
    DEV = "dev"


def check_service_setup() -> ServiceType:
    log.info("Checking service setup")
    if Path("/etc/inittab").exists():
        log.info("Detected service inittab")
        return ServiceType.INITTAB
    if Path("/etc/systemd").exists():
        log.info("Detected service systemd")
        return ServiceType.SYSTEMD
    return ServiceType.DEV


@lru_cache()
def get_inittab_pyaware():
    execution = ["cat", "/etc/inittab"]
    _, std_out, _ = execute_subprocess(execution, silent=True)
    matches = re.search(
        r""".*AWAR.+respawn:([\w/.]+) +-m +pyaware +([\w/]+)""",
        std_out.read().decode("utf-8"),
    )
    if matches is None:
        raise IOError("Cannot find Inittab pyaware")
    return matches.group(1), matches.group(2)


def get_inittab_pyaware_executable():
    try:
        return Path(get_inittab_pyaware()[0])
    except (IOError, FileNotFoundError):
        log.info("Could not find pyaware in inittab")
        return Path("/usr/share/aware/venv/bin/python")


def get_inittab_pyaware_config():
    try:
        return Path(get_inittab_pyaware()[1]) / "config" / "gateway.yaml"
    except (IOError, FileNotFoundError):
        log.info("Could not find pyaware in inittab")
        return Path("/etc/aware/config/gateway.yaml")


@lru_cache()
def get_systemd_pyaware():
    execution = ["cat", "/etc/systemd/system/pyaware.service"]
    _, std_out, _ = execute_subprocess(execution, silent=True)
    matches = re.search(
        r"""ExecStart=([\w/.]+) +-m +pyaware +([\w/]+)""",
        std_out.read().decode("utf-8"),
    )
    if matches is None:
        raise IOError("Cannot find Systemd pyaware")
    return matches.group(1), matches.group(2)


def get_systemd_pyaware_executable():
    try:
        return Path(get_systemd_pyaware()[0])
    except (IOError, FileNotFoundError):
        log.info("Could not find pyaware in systemd")
        return Path("/usr/share/aware/venv/bin/python")


def get_systemd_pyaware_config():
    try:
        return Path(get_systemd_pyaware()[1]) / "config" / "gateway.yaml"
    except (IOError, FileNotFoundError):
        log.info("Could not find pyaware in systemd")
        return Path("/etc/aware/config/gateway.yaml")


def get_target_version(service: ServiceType) -> str:
    log.info("Getting target version")
    if service == ServiceType.SYSTEMD:
        config = get_systemd_pyaware_config()
    elif service == ServiceType.INITTAB:
        config = get_inittab_pyaware_config()
    else:
        raise ValueError("Cannot get target version for dev mode")
    log.info(f"Getting target aware version from {config}")

    if not config.exists():
        return "latest"
    with config.open("r") as f:
        matches = re.search(f"aware_version *: *(.+) *", f.read())
    if matches is not None:
        match = matches.group(1)
        log.info(f"Found target aware version {match}")
        return match
    log.info("No target version found, defaulting to latest")
    return "latest"


def get_current_version(executable: Path) -> str:
    log.info("Getting current version")
    pyaware_path = (
        executable.parent.parent
        / "lib"
        / "python3.7"
        / "site-packages"
        / "pyaware"
        / "__init__.py"
    )
    if not pyaware_path.exists():
        log.info("Pyaware init file not found. Cannot parse version")
        return ""
    log.info(f"Getting current pyaware version from {pyaware_path}")
    try:
        with pyaware_path.open() as f:
            matches = re.search('__version__ *= *"(.+)"', f.read())
        if matches is not None:
            log.info(f"Found version {matches.group(1)}")
            return matches.group(1)
    except FileNotFoundError:
        return ""


def get_all_versions(executable: Path) -> list:
    log.info("Getting all pyaware versions")
    index_url = "https://www.pypi.org/simple"
    execution = [
        executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pyaware==",
        "--index-url",
        index_url,
    ]
    process, _, stderr = execute_subprocess(execution)
    if process.returncode != 1:
        raise IOError(f"Package search failed, Return code {process.returncode}")
    matches = re.search(r"\(from versions: (.+)\)", stderr.read().decode("utf-8"))
    if matches is None:
        return []
    return matches.group(1).split(", ")


def get_latest_version(executable: Path) -> Optional[str]:
    log.info("Getting latest version")
    for ver in get_all_versions(executable)[::-1]:
        if any(character in string.ascii_letters for character in ver):
            # Filter out dev and release candidates
            log.info(f"Filtering out {ver} as invalid prod release")
            continue
        log.info(f"Found latest version as {ver}")
        return ver


@lru_cache()
def get_python_executable(service: ServiceType) -> Path:
    log.info("Getting python executable")
    if service == ServiceType.SYSTEMD:
        path = get_systemd_pyaware_executable()
        if not path.exists():
            create_venv(path.parent.parent)
        log.info(path)
        return path
    elif service == ServiceType.INITTAB:
        path = get_inittab_pyaware_executable()
        if not path.exists():
            create_venv(path.parent.parent)
        log.info(path)
        return path
    raise ValueError(
        "Cannot have venv dir if in dev mode and not configured in your service provider such as Systemd or Inittab"
    )


def create_venv(venv_path: Path):
    log.info("Create virtual env because it doesn't exist")
    execution = ["/usr/local/bin/python3.7", "-m", "venv", venv_path]
    process, _, _ = execute_subprocess(execution)
    if process.returncode:
        raise SystemExit("Missing virtual environment and failed to create one")


def do_updates():
    service = check_service_setup()
    version = get_target_version(service)
    if version == "manual":
        log.info("Set to manual updates. Aborting update")
        return
    executable = get_python_executable(service)
    if version == "latest":
        version = get_latest_version(executable)
    if version == get_current_version(executable):
        log.info("Version currently matches, skipping update")
        return
    update_pyaware(version, get_python_executable(service))
    log.info(f"Updated to {version}")


def check_if_update_running() -> bool:
    execution = ["top", "-n", "2", "|", "grep", "pip"]
    _, std_out, _ = execute_subprocess(execution, silent=True)
    if "pip" in std_out.read().decode():
        return True
    return False


def update_pyaware(version: str, executable: Path):
    log.info(f"Updating pyaware to {version}")
    if check_if_update_running():
        log.info(f"Update already running. Potentially from pyaware source. Aborting")
        return
    try:
        pip_update_pip_subprocess(executable)
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess(executable, version)
        log.info(f"Successfully updated pyaware to {version}")
        return
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess(executable, "")
        log.error(
            "Updated to latest pyaware version after failed specific version update"
        )
    except IOError as e:
        log.exception(e)
        log.info(f"Failed to update pyaware to latest version. Continuing execution")
        return


def main():
    do_updates()


if __name__ == "__main__":
    screen_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)-8s %(lineno)-8s %(message)s")
    screen_handler.setFormatter(formatter)
    log.addHandler(screen_handler)
    screen_handler.setLevel(logging.INFO)
    log.setLevel(logging.INFO)
    log.info("Starting pyaware update checker")
    try:
        main()
    except Exception as e:
        log.exception(e)
