class versionComparison():

    def __init__(self, version1, version2):
        self.version1 = version1
        self.version2 = version2

    def validate_version(self, version):
        """
        Validate if the version string is in the correct format.
        """
        parts = version.split('.')
        if not all(part.isdigit() for part in parts):
            raise ValueError("Invalid version format")
        return tuple(map(int, parts))

    def compare_versions(self):
        """
        Compare two version strings and return:
        - 1 if version1 > version2
        - 0 if version1 == version2
        - -1 if version1 < version2
        """
        v1 = self.validate_version(self.version1)
        v2 = self.validate_version(self.version2)

        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
        else:
            return 0
