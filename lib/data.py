import json

def get_samples(index):
  """
  Get the number of samples for the given participant index
  """
  samples_list = json.load(open('public/submission_mockup_samples.json'))
  index = index % len(samples_list)
  samples = samples_list[index]["samples"]
  return samples