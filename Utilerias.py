from PySFML import sf

class Utilerias(object):

    @staticmethod
    def area_to_tuple(area):
        left = area.Left
        top = area.Top
        right = area.Right
        bottom = area.Bottom
        width = area.GetWidth()
        height = area.GetHeight()
        return (left, top, right, bottom, width, height)
