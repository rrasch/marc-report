class Leader:

    record_statuses = {
        "a": "Increase in encoding level",
        "c": "Corrected or revised",
        "d": "Deleted",
        "n": "New",
        "p": "Increase in encoding level from prepublication",
    }

    record_types = {
        "a": "Language material",
        "c": "Notated music",
        "d": "Manuscript notated music",
        "e": "Cartographic material",
        "f": "Manuscript cartographic material",
        "g": "Projected medium",
        "i": "Nonmusical sound recording",
        "j": "Musical sound recording",
        "k": "Two-dimensional nonprojectable graphic",
        "m": "Computer file",
        "o": "Kit",
        "p": "Mixed materials",
        "r": "Three-dimensional artifact or naturally occurring object",
        "t": "Manuscript language material",
    }

    bib_levels = {
        "a": "Monographic component part",
        "b": "Serial component part",
        "c": "Collection",
        "d": "Subunit",
        "i": "Integrating resource",
        "m": "Monograph/Item",
        "s": "Serial",
    }

    char_coding_schemes = {
        "#": "MARCH-8",
        "a": "UCS/Unicode",
    }

    def __init__(self, ldr):
        self.record_len = int(ldr[0:5])
        self.record_status = Leader.record_statuses[ldr[5]]
        self.record_type = Leader.record_types[ldr[6]]
        self.bib_level = Leader.bib_levels[ldr[7]]
        self.control_type = ldr[8]
        self.char_coding_scheme = Leader.char_coding_schemes[ldr[9]]

    def __str__(self):
        return (
            f"record length {self.record_len}\n"
            f"record status = {self.record_status}\n"
            f"record type = {self.record_type}\n"
            f"bib level = {self.bib_level}\n"
            f"control type = {self.control_type}\n"
            f"char_coding_scheme = {self.char_coding_scheme}\n"
        )

