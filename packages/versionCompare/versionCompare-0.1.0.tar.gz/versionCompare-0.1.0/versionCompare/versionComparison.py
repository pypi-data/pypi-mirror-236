def validate_version(version):
    """
    Validate if the version string is in the correct format.
    """
    parts = version.split('.')
    if not all(part.isdigit() for part in parts):
        raise ValueError("Invalid version format")
    return tuple(map(int, parts))


def compare_versions(version1, version2):
    """
    Compare two version strings and return:
    - 1 if version1 > version2
    - 0 if version1 == version2
    - -1 if version1 < version2
    """
    v1 = validate_version(version1)
    v2 = validate_version(version2)

    if v1 > v2:
        return 1
    elif v1 < v2:
        return -1
    else:
        return 0
