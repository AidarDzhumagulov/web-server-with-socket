from typing import List
import os


class Handler:
    DATABASE_DIR = 'data'
    RCSOC_OK = 'НОРМАЛДЫКС РКСОК/1.0'
    RCSOC_NOT_OK = 'НИНАШОЛ РКСОК/1.0'
    RCSOC_DO_NOT_UNDERSTAND = "НИПОНЯЛ РКСОК/1.0"
    RKSOK_DO_NOT = 'НИЛЬЗЯ РКСОК/1.0'

    def __init__(self, method: str, request: List[str]):
        self.method = method
        self.request = request
        self.check = 'vragi-vezde.to.digital:51624'

    def handle(self) -> str:

        if self.method == "ОТДОВАЙ":
            return self._get()

        if self.method == "УДОЛИ":
            return self._delete()

        if self.method == "ЗОПИШИ":
            return self._write()

    def _get(self) -> str:
        first_name, last_name = self.request[0].split()[1:3:]
        file_name = self._get_filename(first_name, last_name)

        with open(self.DATABASE_DIR + file_name, 'r') as f:
            file_size = os.path.getsize(self.DATABASE_DIR + f"/{file_name}")

            if file_size == 0:
                return self.RCSOC_NOT_OK

            phone = f.read()

        return f'{self.RCSOC_OK}\r\n{phone}'

    def _delete(self) -> str:
        first_name, last_name = self.request[0].split()[1:3:]
        file_name = self._get_filename(first_name, last_name)

        if os.path.exists(self.DATABASE_DIR + file_name):
            os.remove(self.DATABASE_DIR + file_name)
            return self.RCSOC_OK

        else:
            return self.RCSOC_NOT_OK

    def _write(self) -> str:
        first_name, last_name = self.request[0].split()[1:3:]
        phone = self.request[1]
        file_name = self._get_filename(first_name, last_name)

        if len(first_name) < 30:
            if not os.path.exists(self.DATABASE_DIR + file_name):
                with open(file_name, 'w') as file:
                    file.write(phone)
                return self.RCSOC_OK
            else:
                with open(self.DATABASE_DIR + file_name, 'r+') as file:
                    already_exists = False
                    for row in file:
                        if row.strip() == phone:
                            already_exists = True
                            break
                    if not already_exists:
                        file.write('\n' + phone)
                        return self.RCSOC_OK
                    return self.RKSOK_DO_NOT
        return self.RCSOC_DO_NOT_UNDERSTAND

    @staticmethod
    def _get_filename(first_name: str, last_name: str) -> str:
        return f'/{first_name.lower()}_{last_name.lower()}.txt'

    def _check(self) -> str:
        return self.request[0]
