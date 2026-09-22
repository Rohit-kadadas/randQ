import random

def rand_draw(n_list, q_list, rng=None, excluded_pairs=None):
  chooser = rng or random
  if excluded_pairs is not None:
    available_pairs = [
      (name, question)
      for name in n_list
      for question in q_list
      if (name, question) not in excluded_pairs
    ]
    if not available_pairs:
      raise ValueError("No unused name-question pairs remain.")
    return chooser.choice(available_pairs)

  chosen_name = chooser.choice(n_list)
  chosen_question = chooser.choice(q_list)

  return (chosen_name ,chosen_question)