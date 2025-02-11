import pytest
from unittest.mock import patch, MagicMock
from ui import ShellUI

@pytest.fixture
def shell_ui():
    return ShellUI()

def test_run_exit(shell_ui):
    with patch('builtins.input', side_effect=['exit']), patch('sys.exit') as mock_exit:
        shell_ui.run()
        mock_exit.assert_called_once()

def test_run_clear(shell_ui):
    with patch('builtins.input', side_effect=['clear', 'exit']), patch('builtins.print') as mock_print, patch('sys.exit'):
        shell_ui.run()
        mock_print.assert_any_call("\033c")

def test_run_history(shell_ui):
    with patch('builtins.input', side_effect=['history', 'exit']), patch('sys.exit'), patch.object(shell_ui.command_manager, 'show_history') as mock_show_history:
        shell_ui.run()
        mock_show_history.assert_called_once()

def test_run_previous_command(shell_ui):
    with patch('builtins.input', side_effect=['\x1b[A', 'exit']), patch('sys.exit'), patch.object(shell_ui.command_manager, 'get_previous_command', return_value='previous_command') as mock_get_previous_command, patch('builtins.print') as mock_print:
        shell_ui.run()
        mock_get_previous_command.assert_called_once()
        mock_print.assert_any_call('previous_command')

def test_run_next_command(shell_ui):
    with patch('builtins.input', side_effect=['\x1b[B', 'exit']), patch('sys.exit'), patch.object(shell_ui.command_manager, 'get_next_command', return_value='next_command') as mock_get_next_command, patch('builtins.print') as mock_print:
        shell_ui.run()
        mock_get_next_command.assert_called_once()
        mock_print.assert_any_call('next_command')

def test_run_handle_command(shell_ui):
    with patch('builtins.input', side_effect=['some_command', 'exit']), patch('sys.exit'), patch('src.ui.get_unix_command', return_value=('command', 'reason', 'note')), patch.object(shell_ui.command_manager, 'handle_command', return_value='result') as mock_handle_command, patch('builtins.print') as mock_print:
        shell_ui.run()
        mock_handle_command.assert_called_once_with('some_command', 'command')
        mock_print.assert_any_call('command')
        mock_print.assert_any_call('result')
        mock_print.assert_any_call('note')