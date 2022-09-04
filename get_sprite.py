def get_sprite(sprite_route, *names):
    sprites = []
    for name in names:
        file_path = f"{sprite_route}{name}.txt"
        with open(file_path, "r") as file:
            sprites.append(file.read())
    return sprites
