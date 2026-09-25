def AABB(object1, object2):
    xOne = object1.get_x() + object1.get_width() > object2.get_x()
    xTwo = object2.get_x() + object2.get_width() > object1.get_x()
    yOne = object1.get_y() + object1.get_height() > object2.get_y()
    yTwo = object2.get_y() + object2.get_height() > object1.get_y()

    return xOne and xTwo and yOne and yTwo
