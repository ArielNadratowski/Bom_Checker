""" Stores information about an error """
class HighlightError:
    def __init__(self, reference_designator, warning, error_type, error_location):
        self.reference_designator = reference_designator
        self.warning = warning
        self.error_type = error_type
        self.error_location = error_location