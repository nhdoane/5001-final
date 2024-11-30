def convert_for_storage(amt: float):
  """
  changes a floating point currency value to an int for easier storage
  I read somewhere that this is usually how currency is stored in applications, so I mimicked it
  :param amt: The amount to be converted from a float to an int
  :return: the converted amount
  """
  return amt * 100


def convert_from_storage(amt: int):
  """
  changes an int to a float to represent currency
  :param amt: The amount to be converted from an int to a float
  :return: the converted amount
  """
  amt = amt * 0.01
  return amt