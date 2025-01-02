import pytest
from base_utils import run_command


def test_run_command_wait_true(mocker):
    # Arrange
    command = "echo 'Hello, World!'"
    mock_run = mocker.patch("base_utils.subprocess.run")
    mock_print = mocker.patch("builtins.print")

    # Act
    run_command(command, wait=True)

    # Assert
    mock_run.assert_called_once_with(command, shell=True)
    mock_print.assert_called_with("\nCommand completed.\n")


def test_run_command_wait_false(mocker):
    # Arrange
    command = "echo 'Hello, World!'"
    mock_popen = mocker.patch("base_utils.subprocess.Popen")
    mock_print = mocker.patch("builtins.print")
    mock_process = mocker.MagicMock()
    mock_popen.return_value = mock_process

    # Act
    result = run_command(command, wait=False)

    # Assert
    mock_popen.assert_called_once_with(command, shell=True)
    mock_print.assert_called_with(
        "\nCommand started, not waiting for it to complete.\n"
    )
    assert result == mock_process
