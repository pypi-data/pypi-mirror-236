import os
import re
import subprocess
import sys
import logging
import typing
import datetime
import asyncio
import pyaware
from packaging.version import Version
import bs4
from typing import List, Iterable, Optional
import requests
import pathlib
import shutil
import stat

log = logging.getLogger(__file__)


def pip_update_pip_subprocess() -> str:
    process = subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "pip"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    if process.returncode:
        raise IOError(
            f"Pip update failed Return code {process.returncode}\n{stderr.decode('utf-8')}"
        )
    return stdout.decode("utf-8")


def urlread(url: str) -> str:
    req = requests.get(url)
    # Check for good or bad data
    if req.status_code == 200:
        # Good request
        return req.content.decode("utf-8")
    else:
        req.raise_for_status()


def list_releases(response_html: str) -> List[Version]:
    """
    Lists releases of pyaware wheels for python 3 from the response.html
    :param response_html: Response from a search of https://pypi.org/simple/pyaware or equivalent
    :return:
    """
    versions = []
    anchors = bs4.BeautifulSoup(response_html, "html.parser").find_all("a")
    for anchor in anchors:
        try:
            if anchor.text:
                match = re.match(r"pyaware-([\w\d.]+)-py3", anchor.text)
                versions.append(Version(match.group(1)))
        except BaseException:
            continue
    if not versions:
        raise ValueError("No valid pyaware versions found")
    return versions


def determine_latest(version_list: Iterable[Version]) -> Optional[Version]:
    """
    Find the latest version, ignoring developmental and pre-release versions.

    If there is no valid version in the list, return None
    """
    valid_releases = [
        release
        for release in version_list
        if not (release.is_devrelease or release.is_prerelease)
    ]
    if valid_releases:
        return max(valid_releases)
    else:
        return None


def pip_install_subprocess(version: str) -> str:
    config = pyaware.config.load_yaml_config(pyaware.config.config_main_path)
    index_url = config.get("package_index", "https://www.pypi.org/simple")
    if version:
        str_pyaware = f"pyaware=={version}"
    else:
        str_pyaware = f"pyaware"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            str_pyaware,
            "--index-url",
            index_url,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    if process.returncode:
        raise IOError(
            f"Pip install failed Return code {process.returncode}\n{stderr.decode('utf-8')}"
        )
    return stdout.decode("utf-8")


def find_latest_version() -> str:
    config = pyaware.config.load_yaml_config(pyaware.config.config_main_path)
    index = config.get("package_index", "https://www.pypi.org/simple")
    resp = urlread(f"{index}/pyaware")
    return determine_latest(list_releases(resp)).public


def should_update(spec_version: str, latest_version: bool) -> bool:
    from packaging import version

    try:
        installed_version = version.parse(pyaware.__version__)
    except (TypeError, NameError):
        log.warning(f"Installed pyaware version is an invalid version")
        installed_version = version.parse("")
    if spec_version == "manual":
        log.info("Skipping auto update as version is set to manual")
        return False

    spec_version = version.parse(spec_version)

    if latest_version:
        if installed_version > spec_version:
            log.warning("Installed version is greater than latest version in pypi")
            return False
        if installed_version == spec_version:
            log.info("Installation up to date")
            return False
        return True
    else:
        if installed_version == spec_version:
            log.info("Installation up to date")
            return False
        else:
            return True


def get_versions(version: str):
    if version == "latest":
        spec_version = find_latest_version()
        latest = True
    else:
        latest = False
        spec_version = version
    return spec_version, latest


def check_for_updates() -> typing.Optional[str]:
    config = pyaware.config.load_yaml_config(pyaware.config.config_main_path)
    version = config.get("aware_version", "latest")
    spec_version, latest = get_versions(version)
    if should_update(spec_version, latest):
        return spec_version


def bootstrap_updater():
    bin_dir = pathlib.Path(sys.executable).parent
    log.info("Bootstrapping updater")
    try:
        shutil.copy(
            bin_dir / "pyaware_updater.py",
            pathlib.Path("/usr/local/bin/pyaware_updater.py"),
        )
        log.info("Updater script bootstrapped")
    except Exception as e:
        log.error("Failed to bootstrap updater python script")
        log.exception(e)
    try:
        cron_path = pathlib.Path("/etc/cron.hourly/pyaware-updater")
        shutil.copy(bin_dir / "pyaware-cron.sh", cron_path)
        st = os.stat(cron_path)
        os.chmod(cron_path, st.st_mode | stat.S_IEXEC)
        log.info("Cron job scheduled")
    except Exception as e:
        log.error("Failed to bootstrap cron job")
        log.exception(e)
    try:
        if not check_cron_scheduled():
            log.info(
                "Cron hourlies are not enabled. Updating crontab to schedule updater"
            )
            schedule_cron()
    except Exception as e:
        log.exception(e)


def check_cron_scheduled():
    crontab = pathlib.Path("/etc/crontab")
    if not crontab.exists():
        log.error("No crontab found, skipping cron")
        return
    with crontab.open("r") as f:
        crontab_contents = f.readlines()
    for line in crontab_contents:
        if "run-parts /etc/cron." in line:
            if line.startswith("#"):
                return False
    return True


def schedule_cron():
    crontab = pathlib.Path("/etc/crontab")
    if not crontab.exists():
        log.error("No crontab found, skipping cron")
        return
    with crontab.open("r") as f:
        crontab_contents = f.readlines()
    with crontab.open("w") as f:
        for line in crontab_contents:
            if "run-parts /etc/cron." in line:
                line = line.lstrip("#").lstrip()
            f.writelines([line])


def do_updates():
    config = pyaware.config.load_yaml_config(pyaware.config.config_main_path)
    if config.get("aware_version", "latest") == "manual":
        log.info("Version set to manual, skipping bootstrap")
    else:
        bootstrap_updater()
    version = check_for_updates()
    if version:
        update_pyaware(version)


def update_pyaware(version):
    log.info(f"Updating pyaware to {version}")
    try:
        pip_update_pip_subprocess()
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess(version)
        log.info(f"Successfully updated pyaware to {version}")
        log.info("Stopping pyaware to launch updated version")
        pyaware.stop()
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess("")
        log.error(
            "Updated to latest pyaware version after failed specific version update"
        )
        log.info("Stopping pyaware to launch updated version")
        pyaware.stop()
    except IOError as e:
        log.exception(e)
        log.info(f"Failed to update pyaware to latest version. Continuing execution")
        return


def scheduled_restart(hour, **kwargs):
    now = datetime.datetime.now()
    restart_time = datetime.datetime.now().replace(
        hour=hour, minute=0, second=0, microsecond=0
    )
    if restart_time - now < datetime.timedelta(seconds=0):
        restart_time = restart_time + datetime.timedelta(days=1)
    loop = asyncio.get_event_loop()
    return loop.create_task(_restart((restart_time - now).seconds))


async def _restart(seconds):
    await asyncio.sleep(seconds)
    pyaware.stop()
