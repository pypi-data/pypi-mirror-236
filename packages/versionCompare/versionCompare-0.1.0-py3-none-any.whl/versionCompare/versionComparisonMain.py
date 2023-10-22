from versionComparison import compare_versions

# Main function
if __name__ == '__main__':
    version1 = input("Enter the first version string: ")
    version2 = input("Enter the second version string: ")

    """
    Compare two version strings and return:
    - 1 if version1 > version2
    - 0 if version1 == version2
    - -1 if version1 < version2
    """
    result = compare_versions(version1, version2)

    if result == 1:
        print(f"{version1} is greater than {version2}")
    elif result == -1:
        print(f"{version1} is less than {version2}")
    else:
        print(f"{version1} is equal to {version2}")
