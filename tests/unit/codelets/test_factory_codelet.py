from homer.codelets.factory_codelet import FactoryCodelet


def test_select_action():
    factory_codelet = FactoryCodelet(1)
    factory_codelet._select_action()
