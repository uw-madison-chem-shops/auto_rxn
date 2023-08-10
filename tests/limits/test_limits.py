import numpy as np

import auto_rxn


def test_set_get_atol():
    value = np.random.uniform(0, 100)
    auto_rxn.limits.set_atol("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_atol("limits_test_device"), value)


def test_set_get_deadband():
    value = np.random.uniform(0, 100)
    auto_rxn.limits.set_deadband("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_deadband("limits_test_device"), value)


def test_set_get_delay():
    value = np.random.uniform(0, 100)
    auto_rxn.limits.set_delay("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_delay("limits_test_device"), value)


def test_set_get_fallback():
    value = np.random.uniform(-100, 100)
    auto_rxn.limits.set_fallback("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_fallback("limits_test_device"), value)


def test_set_get_lower():
    value = np.random.uniform(-100, 100)
    auto_rxn.limits.set_lower("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_lower("limits_test_device"), value)


def test_set_get_rtol():
    value = np.random.uniform(0, 100)
    auto_rxn.limits.set_rtol("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_rtol("limits_test_device"), value)


def test_set_get_upper():
    value = np.random.uniform(-100, 100)
    auto_rxn.limits.set_upper("limits_test_device", value)
    assert np.isclose(auto_rxn.limits.get_upper("limits_test_device"), value)
