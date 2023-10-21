# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name

import pytest
from quantify_scheduler.device_under_test.device_element import DeviceElement
from quantify_scheduler.device_under_test.edge import Edge
from quantify_scheduler.device_under_test.quantum_device import QuantumDevice


def test_generate_device_config(mock_setup_basic_transmon: dict) -> None:
    quantum_device = mock_setup_basic_transmon["quantum_device"]

    # N.B. the validation of the generated config is happening inside the
    # device object itself using the pydantic dataclass. Invoking the function
    # tests this directly.
    dev_cfg = quantum_device.generate_device_config()

    assert {"q0", "q1", "q2", "q3"} <= set(dev_cfg.elements.keys())
    # Ensure that we also check that the edges are being configured
    assert "q2_q3" in dev_cfg.edges


def test_generate_hardware_config(
    mock_setup_basic_transmon: dict,
) -> None:
    quantum_device = mock_setup_basic_transmon["quantum_device"]

    mock_hardware_cfg = {
        "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
        "ic_qcm0": {
            "name": "qcm0",
            "instrument_type": "Pulsar_QCM",
            "mode": "complex",
            "ref": "external",
            "IP address": "192.168.0.3",
            "complex_output_0": {
                "lo_name": "ic_lo_mw0",
                "lo_freq": None,
                "seq0": {"port": "q0:mw", "clock": "q0.01", "interm_freq": -100e6},
            },
        },
        "ic_qrm0": {
            "name": "qrm0",
            "instrument_type": "Pulsar_QRM",
            "mode": "complex",
            "ref": "external",
            "IP address": "192.168.0.2",
            "complex_output_0": {
                "lo_name": "ic_lo_ro",
                "lo_freq": None,
                "seq0": {"port": "q0:res", "clock": "q0.ro", "interm_freq": 50e6},
            },
        },
        "ic_lo_ro": {"instrument_type": "LocalOscillator", "lo_freq": None, "power": 1},
        "ic_lo_mw0": {
            "instrument_type": "LocalOscillator",
            "lo_freq": None,
            "power": 1,
        },
    }

    quantum_device.hardware_config(mock_hardware_cfg)

    _ = quantum_device.generate_hardware_config()

    # cannot validate as there is no schema exists see quantify-scheduler #181
    # validate_config(dev_cfg, scheme_fn="qblox_cfg.json")


@pytest.fixture
def dev():
    dev = QuantumDevice("dev")
    yield dev
    dev.close()


@pytest.fixture
def meas_ctrl():
    test_mc = QuantumDevice("test_mc")
    yield test_mc
    test_mc.close()


def test_adding_non_element_raises(dev, meas_ctrl):
    with pytest.raises(TypeError):
        dev.add_element(meas_ctrl)


def test_invalid_device_element_name():
    invalid_name = "q_0"
    with pytest.raises(ValueError):
        DeviceElement(invalid_name)


def test_wrong_scheduling_strategy(mock_setup_basic_transmon_with_standard_params):
    quantum_device = mock_setup_basic_transmon_with_standard_params["quantum_device"]
    # Assert that a validation error is raised for scheduling strategy other_strategy
    with pytest.raises(ValueError):
        quantum_device.scheduling_strategy("other_strategy")


def test_add_and_get_unreferenced_device_elements(dev):
    for i in range(50):
        dev.add_element(DeviceElement(f"elem{i}"))

    for i in range(50):
        dev.get_element(f"elem{i}")


def test_get_and_re_add_closed_device_element(dev):
    # Create and add a new device element
    element = DeviceElement("elem")
    dev.add_element(element)

    # Close the element
    element.close()

    # Try to get the element
    with pytest.raises(ValueError, match="not a valid device element."):
        dev.get_element("elem")

    # Re-create and re-add the element
    element = DeviceElement("elem")
    dev.add_element(element)


def test_get_and_re_add_closed_edge(dev):
    # Create and add a new edge
    edge = Edge("e1", "e2")
    dev.add_edge(edge)

    # Close the edge
    edge.close()

    # Try to get the edge
    with pytest.raises(ValueError, match="not a valid edge."):
        dev.get_edge("e1_e2")

    # Re-create and re-add the edge
    edge = Edge("e1", "e2")
    dev.add_edge(edge)
