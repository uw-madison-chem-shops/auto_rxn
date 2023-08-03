__all__ = ["with_limit_set_to"]


import auto_rxn


def with_limit_set_to(id, limit, value):
    def decorator(function):
        def wrapper():
            if id in auto_rxn.limits._state:
                original = auto_rxn.limits._state[id][limit]
                auto_rxn.limits._state[id][limit] = value
                function()
                auto_rxn.limits._state[id][limit] = original
            else:
                auto_rxn.limits._state[id] = dict()
                auto_rxn.limits._state[id][limit] = value
                function()
                del auto_rxn.limits._state[id]

        return wrapper

    return decorator
