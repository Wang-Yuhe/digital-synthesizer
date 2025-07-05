
class note_saver:
    def __init__(self, note_name: str, track_id:int, bar_idx:int, block_idx:int) -> None:
        self.note_name=note_name
        self.track_id=track_id
        self.bar_idx=bar_idx
        self.block_idx=block_idx
    def get_information(self) -> tuple:
        """
        获取音符信息 

        return:
            tuple: (note_name, track_id, bar_idx, block_idx)
        """
        return (self.note_name, self.track_id, self.bar_idx, self.block_idx)
    
class track_saver:
    def __init__(self, timbre: str, track_id:int) -> None:
        self.timbre=timbre
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
            list: [(note_name, track_id, bar_idx, block_idx), ...]
        """
        note_information = []
        for note_saver in self.note_savers:
            note_information.append(note_saver.get_information())
        return note_information