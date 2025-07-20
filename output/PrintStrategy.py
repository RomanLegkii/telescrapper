from output.printRaw import printRaw
from output.printDefault import printDefault
from output.printId import printId


class Output():
    printType = {}
    def __init__(self):
        self.printType['raw'] = printRaw
        self.printType['username_bio'] = printDefault
        self.printType['id_name_username_bio'] = printId
    
    def getOutput(self, requestedPrint: str) -> dict:
        result_filters = {key: filter_func for key, filter_func in self.printType.items() if key == requestedPrint} #smash or pass?
        return result_filters
    
    def registerPrintType(self, key: str, print_func: callable):
        self.printType[key] = print_func