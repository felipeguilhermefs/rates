def create_insert_prices(datasource):

    # As price is a integer in db, and convertion is a float
    # some money would be lost. But it is ok as a toy project
    def build_insert(record):
        orig_code, dest_code, day, price = record
        return f"""
        INSERT INTO prices (orig_code, dest_code, day, price)
        VALUES ('{orig_code}','{dest_code}', '{day}', {price});
        """

    def insert_prices(new_records):
        inserts = map(build_insert, new_records)
        datasource(inserts)

    return insert_prices
