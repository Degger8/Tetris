def AABB(object1, object2):
    xOne = object1.x + object1.width > object2.x
    xTwo = object2.x + object2.width > object1.x
    yOne = object1.y + object1.height > object2.y
    yTwo = object2.y + object2.height > object1.y

    return xOne and xTwo and yOne and yTwo
