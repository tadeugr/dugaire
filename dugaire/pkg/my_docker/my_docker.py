def get_image_short_id(image_id) -> str:
  """ Get 10-character image id. """
  
  short_id = image_id.replace("sha256:", "")[:12]
  if len(short_id) == 12:
    short_id = short_id[:10]
  return short_id