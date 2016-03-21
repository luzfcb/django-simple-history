from __future__ import unicode_literals

__version__ = '1.8.1'

from . import utils


def register(
        model, app=None, manager_name='history', records_class=None,
        table_name=None, **records_config):
    """
    Create historical model for `model` and attach history manager to `model`.

    Keyword arguments:
    app -- App to install historical model into (defaults to model.__module__)
    manager_name -- class attribute name to use for historical manager
    records_class -- class to use for history relation (defaults to
        HistoricalRecords)
    table_name -- Custom name for history table (defaults to
        'APPNAME_historicalMODELNAME')

    This method should be used as an alternative to attaching an
    `HistoricalManager` instance directly to `model`.
    """
    from . import models

    natural_key = utils.natural_key_from_model(model)
    if natural_key not in models.registered_models:
        if records_class is None:
            records_class = models.HistoricalRecords
        records = records_class(**records_config)
        records.manager_name = manager_name
        records.module = app and ("%s.models" % app) or model.__module__
        records.add_extra_methods(model)
        
        history_name = utils.natural_key_from_model(records.finalize(model))[1]
        models.registered_models[natural_key] = history_name
        
        
        records.concrete_natural_key = utils.natural_key_from_model(model._meta.concrete_model or model)
        records.finalize(model)

