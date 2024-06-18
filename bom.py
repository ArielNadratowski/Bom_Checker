
class Bom:
    def __init__(self, window, bom, status):       
        self.name = window.input_storage[0].input.get('1.0', 'end').strip()
        self.description = window.input_storage[1].input.get('1.0', 'end').strip()
        self.quantity = window.input_storage[2].input.get('1.0', 'end').strip()
        self.reference_designator = window.input_storage[3].input.get('1.0', 'end').strip()
        self.manufacturer = window.input_storage[4].input.get('1.0', 'end').strip()
        self.manufacturer_part_number = window.input_storage[5].input.get('1.0', 'end').strip()
        self.header = window.input_storage[6].input.get('1.0', 'end').strip()
        self.bom = bom
        self.bom_status = status

