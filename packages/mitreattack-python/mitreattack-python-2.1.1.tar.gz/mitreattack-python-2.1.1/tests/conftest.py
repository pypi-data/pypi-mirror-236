import shutil
from pathlib import Path

import pytest
from loguru import logger
from stix2 import MemoryStore

from mitreattack.download_stix import download_domains
from mitreattack.navlayers import Layer
from mitreattack.release_info import LATEST_VERSION

from .resources.testing_data import example_layer_v3_all, example_layer_v43_dict


@pytest.fixture(autouse=True, scope="session")
def attack_stix_dir():
    logger.debug("Downloading the ATT&CK STIX!!!")
    download_dir = "attack-releases"
    download_domains(
        domains=["enterprise", "mobile", "ics"],
        download_dir=download_dir,
        all_versions=False,
        stix_version="2.0",
    )

    yield download_dir

    shutil.rmtree(download_dir)


@pytest.fixture(scope="session")
def stix_file_enterprise_latest(attack_stix_dir):
    return f"{attack_stix_dir}/v{LATEST_VERSION}/enterprise-attack.json"


@pytest.fixture(scope="session")
def stix_file_mobile_latest(attack_stix_dir):
    return f"{attack_stix_dir}/v{LATEST_VERSION}/mobile-attack.json"


@pytest.fixture(scope="session")
def stix_file_ics_latest(attack_stix_dir):
    return f"{attack_stix_dir}/v{LATEST_VERSION}/ics-attack.json"


@pytest.fixture(scope="session")
def memstore_enterprise_latest(attack_stix_dir):
    logger.debug("Loading STIX memstore for Enterprise ATT&CK")
    stix_file = f"{attack_stix_dir}/v{LATEST_VERSION}/enterprise-attack.json"
    mem_store = MemoryStore()
    mem_store.load_from_file(stix_file)
    return mem_store


@pytest.fixture(scope="session")
def memstore_mobile_latest(attack_stix_dir):
    logger.debug("Loading STIX memstore for Mobile ATT&CK")
    stix_file = f"{Path.cwd()}/{attack_stix_dir}/v{LATEST_VERSION}/mobile-attack.json"
    mem_store = MemoryStore()
    mem_store.load_from_file(stix_file)
    return mem_store


@pytest.fixture(scope="session")
def memstore_ics_latest(attack_stix_dir):
    logger.debug("Loading STIX memstore for ICS ATT&CK")
    stix_file = f"{attack_stix_dir}/v{LATEST_VERSION}/ics-attack.json"
    mem_store = MemoryStore()
    mem_store.load_from_file(stix_file)
    return mem_store


@pytest.fixture()
def layer_v3_all():
    layer = Layer()
    layer.from_str(example_layer_v3_all)
    return layer


@pytest.fixture()
def layer_v43():
    layer = Layer()
    layer.from_dict(example_layer_v43_dict)
    return layer
