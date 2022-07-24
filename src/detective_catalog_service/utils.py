# import project related modules
from detective_catalog_service.settings import dgraph_client


def test_dgraph_connection() -> bool:
    try:
        dgraph_client.check_version()
        return True
    except Exception:
        return False
