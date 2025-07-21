from decorators.checkBio import checkBio
from decorators.checkBioFuzzy import  checkBioFuzzy 
from decorators.checkBioContains import  checkBioContains 
from decorators.checkPhoto import  checkPhoto 
from decorators.checkChannel import  checkChannel 
from typing import List


class Filter():
    filters = {}
    def __init__(self):
        self.filters ['bio']  = checkBio
        self.filters ['channel']  = checkChannel
        self.filters ['photo']  = checkPhoto
        self.filters ['bio_contains']  = checkBioContains
        self.filters ['bio_fuzzy']  = checkBioFuzzy
    
    def getFilters(self, requestedFilters: List[str]):
        result_filters = {key: filter_func for key, filter_func in self.filters.items() if key in requestedFilters} #smash or pass?
        return result_filters