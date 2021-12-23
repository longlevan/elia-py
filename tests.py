import pytest
import datetime as dt
from elia import elia
from pytz import timezone

BRU = timezone("Europe/Brussels")

start_1 = dt.datetime.today() - dt.timedelta(days=2)
end_1 = dt.datetime.today() - dt.timedelta(days=1)

start_2 = dt.datetime.now(tz=BRU) - dt.timedelta(hours=12)
end_2 = dt.datetime.now(tz=BRU)


@pytest.fixture()
def elia_client() -> elia.EliaPandasClient:
    """Creates EliaClient object"""
    return elia.EliaPandasClient()


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_forecast_wind(elia_client, start, end):
    """Testing wind query"""
    df_test = elia_client.get_forecast_wind(start, end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test.tail())
    assert(len(df_test) >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_forecast_solar(elia_client, start, end):
    """Testing solar query"""
    df_test = elia_client.get_forecast_solar(start, end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test.tail())
    assert(len(df_test) >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_forecast_load(elia_client, start, end):
    """Testing consumption query"""
    df_test = elia_client.get_forecast_load(start, end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test.tail())
    assert(len(df_test) >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_actual_imbalance_price_per_quarter(elia_client, start, end):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_quarter(start, end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test.tail())
    assert(len(df_test) >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_actual_imbalance_price_per_quarter_via_excel(elia_client, start, end):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_quarter_via_excel(start, end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test.tail())
    assert(len(df_test) >= number_of_quarter_hours)


def test_actual_imbalance_volume(elia_client):
    """Testing imbalance volume query"""
    df_test = elia_client.get_actual_imbalance_volume()
    print(df_test.tail())
    assert(len(df_test) >= 59)  # data per minute, only for the latest hour


def test_actual_imbalance_price_per_minute(elia_client):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_minute()
    print(df_test.tail())
    assert(len(df_test) >= 59)  # data per minute, only for the latest hour
