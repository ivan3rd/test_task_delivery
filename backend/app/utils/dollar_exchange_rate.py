import logging
import requests

from app.cache import RedisCache


logger = logging.getLogger('uvicorn.error')


async def get_dollar_exchange_rate() -> float | None:
    logger.info('get_dollar_exchage_rate(). Started')
    cache = RedisCache()
    der = None
    try:
        logger.info('get_dollar_exchage_rate(). Requesting exchange rate from redis cache')
        der: bytes | None = await cache.get('der_value')
        if der is None:
            logger.info('get_dollar_exchage_rate(). Cache appeared to be empty. Getting new value for dollar exchange rate')
            der_service_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
            response = requests.get(der_service_url)
            if response.status_code == 200:
                logger.info(f'get_dollar_exchage_rate(). Successeful request to {der_service_url}')
                der = response.json().get('Valute', {}).get('USD', {}).get('Value', 0.0)
                await cache.set('der_value', der)
            else:
                logger.error('get_dollar_exchage_rate(). Got unexpected answer from foreing service.')
                logger.error(f'get_dollar_exchage_rate(). Status_code: {response.status_code}. json: {response.json()}')
        logger.info('get_dollar_exchage_rate(). Got exchange rate.')
    except Exception as e:
        logger.error(f'get_dollar_exchage_rate(). Error occurred while executing. Exception: {e}')
    await cache.connection_close()
    if der is not None:
        der = float(der)
    return der

