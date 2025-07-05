
class note_saver:
    def __init__(self, note_name: str, length:int, bar_idx:int, volume = 1) -> None:
        self.note_name=note_name
        self.length=length
        self.bar_idx=bar_idx
        self.volume=volume
    def get_information(self) -> tuple:
        """
        获取音符信息 

        return:
            tuple: (note_name, length, bar_idx, volume)
        """
        return (self.note_name, self.length, self.bar_idx, self.volume)

class track_saver:
    def __init__(self,  track_id:int, timbre = "piano", bpm = 120) -> None:
        self.timbre=timbre
        self.bpm=bpm
        self.track_id=track_id
        self.note_savers = []  # 存储音符信息的列表

    def add_note(self, note_saver: note_saver):
        """
        添加音符信息到列表中
        """
        self.note_savers.append(note_saver)
    def get_note_information(self) -> list:
        """
        获取音符信息

        return:
            list: [(note_name, length, bar_idx, volume), ...]
        """
        note_information = []
        for note_saver in self.note_savers:
            note_information.append(note_saver.get_information())
        return note_information