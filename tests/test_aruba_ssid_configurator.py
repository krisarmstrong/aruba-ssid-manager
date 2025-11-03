"""
Test suite for Aruba SSID Configurator

Author: Kris Armstrong
"""


def test_version():
    import aruba_ssid_configurator as mod
    assert hasattr(mod, "__version__")
    assert mod.__version__ == "1.1.0"
