from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_recaptcha():
    with patch('main.mixins.validate_recaptcha', return_value={ 'success': True }) as m:
        yield m

@pytest.fixture()
def mock_recaptcha_fail():
    with patch('main.mixins.validate_recaptcha', return_value={ 'success': False, 'error-codes': 1 }) as m:
        yield m

