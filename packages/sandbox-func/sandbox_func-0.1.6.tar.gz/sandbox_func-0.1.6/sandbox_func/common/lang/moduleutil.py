class ModuleUtil:
    @staticmethod
    def get_func(kls):
        try:
            parts = kls.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
            return m
        except Exception:
            return None
