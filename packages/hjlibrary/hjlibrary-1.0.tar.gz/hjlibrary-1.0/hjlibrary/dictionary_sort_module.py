#!/use/bin/python3
"""
dictionary sort
@sortdictionary

methods for sorting a dictionary
"""
import common_module

class SortDictionaryModule:
  """
  """
  def __init__(self):
    pass
  
  def sort_dictionary_by_value(self, in_dict: dict) -> dict:
    """
    @sort a dictionary by value
    @param in_dict: dict
    @return sorted_dict: dict
    """
    common_module.print_function(self.sort_dictionary_by_value)
    mylist = sorted(in_dict.items(), key=lambda x:x[1])
    sorted_dict = dict(mylist)

    return sorted_dict
  
  def sort_dictionary_by_key(self, in_dict) -> dict:
    """
    @sort a dictionary by key
    @param in_dict: dict
    @return sorted_dict: dict    
    """
    common_module.print_function(self.sort_dictionary_by_key)
    mylist = sorted(in_dict.items())
    sorted_dict = dict(mylist)

    return sorted_dict
  
if __name__ == '__main__':
    print('module only, not main')