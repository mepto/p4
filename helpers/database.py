# -*- coding: utf-8 -*-
import os
from json.decoder import JSONDecodeError
from os.path import exists

from tinydb import Query, TinyDB


class Database:
    """ Database class to CRUD data and cache it"""

    def __init__(self):
        self.db = self.get_db()
        self.player_table = TinyDB.table(self.db, 'player')
        self.tournament_table = TinyDB.table(self.db, 'tournament')

    # IN INIT MUST BE CACHED  - CALLED IN
    @staticmethod
    def get_db():
        db_file_name = 'chess_db.json'

        if not exists(os.path.abspath(db_file_name)):
            file = open(db_file_name, 'w+')
            file.close()

        return TinyDB(db_file_name, sort_keys=True, indent=4,
                      separators=(',', ': '))

    def create(self, table: str, item: dict):
        table_to_update = self.get_table(table)
        table_to_update.insert(item)

    def read(self, table, **kwargs) -> list:
        if kwargs:
            current_table = self.get_table(table)
            q = Query()
            results = []
            for kw in kwargs:
                results.append(current_table.search(q[kw] == kwargs[kw]))
            return results
        return [item for item in self.get_table(table)]

    def update(self, table: str, item_id: int, **kwargs):
        table_to_update = self.get_table(table)
        # doc = Query()
        for item in kwargs:
            table_to_update.update({item: kwargs[item]}, doc_ids=[item_id])

    def get_table(self, table):
        return self.player_table if table == 'player' else self.tournament_table

    def get_next_id(self, table):
        current_table = self.get_table(table)
        q = Query()
        try:
            max_id = max(
                [res.get('id') for res in current_table.search(q.id.exists())])
            new_id = max_id + 1
        except (JSONDecodeError, ValueError):
            new_id = 1
        return new_id
