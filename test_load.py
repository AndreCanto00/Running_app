import math
import pytest
from click.testing import CliRunner
from loadCLI import cli
from mylib.load import trimp, trimp_lt, hrrs
from fastapi.testclient import TestClient
from main import app


# Fixtures 1
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
    (150, 180, 60, 60, 121.56),
    (120, 180, 30, 45, 54.68),
    (130, 190, 45, 50, 57.81),
]

test_trimp_lt_data = [
    (150, 180, 60, 121.56),
    (120, 180, 30, 72.91),
    (130, 190, 45, 69.37),
]

test_hrrs_data = [
    (150, 180, 60, 60, 150, 100.0),
    (120, 180, 30, 45, 130, 59.39),
    (130, 190, 45, 50, 140, 65.31),
]


# TRIMP function tests
@pytest.mark.parametrize("hr,hr_max,rest_hr,duration,expected", test_trimp_data)
def test_trimp_parametrized(hr, hr_max, rest_hr, duration, expected):
    """Test TRIMP calculation with various input combinations"""
    assert math.isclose(trimp(hr, hr_max, rest_hr, duration), expected, rel_tol=1e-2)


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
@pytest.mark.parametrize("hr,hr_max,rest_hr,expected", test_trimp_lt_data)
def test_trimp_lt_parametrized(hr, hr_max, rest_hr, expected):
    """Test TRIMP_LT calculation with various input combinations"""
    assert math.isclose(trimp_lt(hr, hr_max, rest_hr), expected, rel_tol=1e-2)


def test_trimp_lt_invalid_input():
    """Test TRIMP_LT function with invalid inputs"""
    with pytest.raises(ValueError):
        trimp_lt(-150, 180, 60)
    with pytest.raises(ValueError):
        trimp_lt(150, -180, 60)
    with pytest.raises(ValueError):
        trimp_lt(150, 180, -60)


# HRRS function tests
@pytest.mark.parametrize("hr,hr_max,rest_hr,duration,hr_lt,expected", test_hrrs_data)
def test_hrrs_parametrized(hr, hr_max, rest_hr, duration, hr_lt, expected):
    """Test HRRS calculation with various input combinations"""
    assert math.isclose(
        hrrs(hr, hr_max, rest_hr, duration, hr_lt), expected, rel_tol=1e-2
    )


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
    result = runner.invoke(cli, ["trimp"], input="150\n180\n60\n60\n")
    assert result.exit_code == 0
    assert "TRIMP value: 121.556" in result.output


def test_trimp_lt_cli_success(runner):
    """Test successful TRIMP_LT CLI command"""
    result = runner.invoke(cli, ["trimp_lt"], input="150\n180\n60\n")
    assert result.exit_code == 0
    assert "TRIMP_LT value: 121.556" in result.output


def test_hrrs_cli_success(runner):
    """Test successful HRRS CLI command"""
    result = runner.invoke(cli, ["hrrs"], input="150\n180\n60\n60\n150\n")
    assert result.exit_code == 0
    assert "HRRS value: 100.0" in result.output


def test_trimp_cli_invalid_input(runner):
    """Test TRIMP CLI command with invalid input"""
    result = runner.invoke(cli, ["trimp"], input="invalid\n180\n60\n60\n")
    assert result.exit_code != 0
    assert "Error: Input must be an integer" in result.output


def test_trimp_lt_cli_invalid_input(runner):
    """Test TRIMP_LT CLI command with invalid input"""
    result = runner.invoke(cli, ["trimp_lt"], input="invalid\n180\n60\n")
    assert result.exit_code != 0
    assert "Error: Input must be an integer" in result.output


def test_hrrs_cli_invalid_input(runner):
    """Test HRRS CLI command with invalid input"""
    result = runner.invoke(cli, ["hrrs"], input="invalid\n180\n60\n60\n150\n")
    assert result.exit_code != 0
    assert "Error: Input must be an integer" in result.output


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


### Web Application Testing


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, I am your load running calculator!"}


# Test TRIMP calculation
def test_trimp_post(client):
    response = client.post(
        "/trimp/",
        json={
            "avg_hr": 150,
            "max_hr": 180,
            "rest_hr": 60,
            "workout_duration": 60,
            "lt_hr": 150,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"TRIMP value": 121.56}


# Test TRIMP_LT calculation
def test_trimp_lt_post(client):
    response = client.post(
        "/trimp_lt/",
        json={
            "lt_hr": 150,
            "max_hr": 180,
            "rest_hr": 60,
            "workout_duration": 60,
            "avg_hr": 150,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"TRIMP_LT value": 121.56}


# Test HRRS calculation
def test_hrrs_post(client):
    response = client.post(
        "/hrrs/",
        json={
            "avg_hr": 150,
            "max_hr": 180,
            "rest_hr": 60,
            "workout_duration": 60,
            "lt_hr": 150,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"HRRS value": 100.0}
