
def calc_resize(original_width, original_height, desired_width, desired_height):
    """
    Calculate new image size to fit new dimension. It keeps the original image proportions.
    :param original_width:
    :param original_height:
    :param desired_width:
    :param desired_height:
    :return: new width, new height
    """
    if original_width <= desired_width and original_height <= desired_height:
        return original_width, original_height
    proportion = original_width / original_height
    if desired_width > desired_height:
        new_width = desired_height * proportion
        return new_width, desired_height

    # if desired_width < desired_height:
    new_height = desired_width / proportion
    return desired_width, new_height
