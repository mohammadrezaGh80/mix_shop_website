def is_access_to_rosetta_views(user):
    return user.is_admin if user.is_authenticated else False
