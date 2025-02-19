import math
import pytest
from click.testing import CliRunner
from loadCLI import cli
from mylib.load import trimp, trimp_lt, hrrs

# Fixtures
@pytest.fixture
def runner():
    """Fixture for Click CLI test runner"""
    return CliRunner()

@pytest.fixture
def mock_input(monkeypatch):
    """Fixture to mock user input"""
    def mock_input_fn(_):
        return "70"
    monkeypatch.setattr("builtins.input", mock_input_fn)

# Parametrized test data
test_trimp_data = [
    (150, 180, 60, 60, 131.47),
    (120, 180, 30, 45, 65.73),
    (130, 190, 45, 50, 98.25)
]

test_trimp_lt_data = [
    (150, 180, 60, 65.73),
    (120, 180, 30, 32.86),
    (130, 190, 45, 49.12)
]

test_hrrs_data = [
    (150, 180, 60, 60, 150, 200.0),
    (120, 180, 30, 45, 130, 150.0),
    (130, 190, 45, 50, 140, 175.0)
]

# TRIMP function tests
@pytest.mark.parametrize("hr,hr_max,time,duration,expected", test_trimp_data)
def test_trimp_parametrized(hr, hr_max, time, duration, expected):
    """Test TRIMP calculation with various input combinations"""
    assert math.isclose(trimp(hr, hr_max, time, duration), expected, rel_tol=1e-2)

def test_trimp_invalid_input():
    """Test TRIMP function with invalid inputs"""
    with pytest.raises(ValueError):
        trimp(-150, 180, 60, 60)
    with pytest.raises(ValueError):
        trimp(150, -180, 60, 60)
    with pytest.raises(ValueError):
        trimp(150, 180, -60, 60)
    with pytest.raises(ValueError):
        trimp(150, 180, 60, -60)

# TRIMP_LT function tests
@pytest.mark.parametrize("hr,hr_max,time,expected", test_trimp_lt_data)
def test_trimp_lt_parametrized(hr, hr_max, time, expected):
    """Test TRIMP_LT calculation with various input combinations"""
    assert math.isclose(trimp_lt(hr, hr_max, time), expected, rel_tol=1e-2)

def test_trimp_lt_invalid_input():
    """Test TRIMP_LT function with invalid inputs"""
    with pytest.raises(ValueError):
        trimp_lt(-150, 180, 60)
    with pytest.raises(ValueError):
        trimp_lt(150, -180, 60)
    with pytest.raises(ValueError):
        trimp_lt(150, 180, -60)

# HRRS function tests
@pytest.mark.parametrize("hr,hr_max,time,duration,resting_hr,expected", test_hrrs_data)
def test_hrrs_parametrized(hr, hr_max, time, duration, resting_hr, expected):
    """Test HRRS calculation with various input combinations"""
    assert math.isclose(hrrs(hr, hr_max, time, duration, resting_hr), expected, rel_tol=1e-2)

def test_hrrs_invalid_input():
    """Test HRRS function with invalid inputs"""
    with pytest.raises(ValueError):
        hrrs(-150, 180, 60, 60, 150)
    with pytest.raises(ValueError):
        hrrs(150, -180, 60, 60, 150)
    with pytest.raises(ValueError):
        hrrs(150, 180, -60, 60, 150)
    with pytest.raises(ValueError):
        hrrs(150, 180, 60, -60, 150)
    with pytest.raises(ValueError):
        hrrs(150, 180, 60, 60, -150)

# CLI tests
def test_trimp_cli_success(runner):
    """Test successful TRIMP CLI command"""
    result = runner.invoke(cli, input="150\n180\n60\n60\n")
    assert result.exit_code == 0
    assert "TRIMP value: 131.47" in result.output

def test_trimp_lt_cli_success(runner):
    """Test successful TRIMP_LT CLI command"""
    result = runner.invoke(cli, input="150\n180\n60\n")
    assert result.exit_code == 0
    assert "TRIMP_LT value: 65.73" in result.output

def test_hrrs_cli_success(runner):
    """Test successful HRRS CLI command"""
    result = runner.invoke(cli, input="150\n180\n60\n60\n150\n")
    assert result.exit_code == 0
    assert "HRRS value: 200.0" in result.output

def test_trimp_cli_invalid_input(runner):
    """Test TRIMP CLI command with invalid input"""
    result = runner.invoke(cli, input="invalid\n180\n60\n60\n")
    assert result.exit_code != 0
    assert "Error" in result.output

def test_trimp_lt_cli_invalid_input(runner):
    """Test TRIMP_LT CLI command with invalid input"""
    result = runner.invoke(cli, input="invalid\n180\n60\n")
    assert result.exit_code != 0
    assert "Error" in result.output

def test_hrrs_cli_invalid_input(runner):
    """Test HRRS CLI command with invalid input"""
    result = runner.invoke(cli, input="invalid\n180\n60\n60\n150\n")
    assert result.exit_code != 0
    assert "Error" in result.output

# Edge cases
def test_edge_cases():
    """Test edge cases for all functions"""
    # Test with maximum possible values
    assert trimp(220, 220, 1440, 1440) > 0  # 24 hours
    assert trimp_lt(220, 220, 1440) > 0
    assert hrrs(220, 220, 1440, 1440, 40) > 0

    # Test with minimum valid values
    assert trimp(40, 220, 1, 1) > 0
    assert trimp_lt(40, 220, 1) > 0
    assert hrrs(40, 220, 1, 1, 40) > 0

if __name__ == "__main__":
    pytest.main(["-v", "test_load.py"])


