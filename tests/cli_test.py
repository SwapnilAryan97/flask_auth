import os
from click.testing import CliRunner
from app import create_log_folder, create_database

runner = CliRunner()


def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    dbdir = os.path.join(root, '../database')
    assert os.path.exists(dbdir) == True


def test_create_log_folder():
    response = runner.invoke(create_log_folder)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, '../app/logs')
    assert os.path.exists(logdir) == True
