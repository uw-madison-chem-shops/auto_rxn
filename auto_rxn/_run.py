__all__ = ["run"]


def run(recipe):
    from ._happi import happi_client
    devices = dict()
    for id in recipe.control_point_ids:
        device = happi_client.load_device(name=id)
        devices[id] = device
