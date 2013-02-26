class Statics:
    client = None
    @staticmethod
    def SetClient(cliente):
        Statics.client = cliente

    @staticmethod
    def GetClient():
        return Statics.client
