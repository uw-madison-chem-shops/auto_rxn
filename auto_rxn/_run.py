__all__ = ["run"]


from ._happi import happi_client


def run(recipe):
    devices = dict()
    for id in recipe.control_point_ids:
        device = happi_client.load_device(name=id)
        devices[id] = device
