"""Synthetic fixture; executing this module is not discovery."""
import dlt

@dlt.resource(name="items", primary_key="item_id", write_disposition="merge")
def items():
    yield {"item_id": 1, "label": "sample"}
