import httpx


def send_request(url, method, params=None, data=None, json=None, **kwargs):
    with httpx.Client(timeout=None) as session:
        res = session.request(method=method.upper(), url=url, params=params, data=data, json=json, **kwargs)
        return res


async def async_send_request(url, method, params=None, data=None, json=None, **kwargs):
    with httpx.AsyncClient(timeout=None) as session:
        async with session.request(method.upper(), url=url, params=params, json=json, data=data,
                                   **kwargs) as resp:
            return resp
