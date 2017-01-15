class FileWorker:
    out_file_name = "reservations.log"

    @classmethod
    def insert_reservation_item(cls, item, add):
        message = str(item)
        with open(cls.out_file_name, "a") as out_log:
            out_log.write(message + " add:" + add + "\n\n")


with open(FileWorker.out_file_name, "w") as out_log:
    out_log.write("")
