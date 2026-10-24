"""GUI-owned table model: update data, never recreate all cells or auto-size every tick."""
from datetime import datetime, timezone
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot


class HardwareTableModel(QAbstractTableModel):
    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.headers = tuple(headers)
        self.rows = ()
        self._expired = set()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal and 0 <= section < len(self.headers):
            return self.headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.rows):
            return None
        row = self.rows[index.row()]
        if role == Qt.ToolTipRole:
            return row.tooltip or row.values[index.column()]
        if role == Qt.DisplayRole:
            if row.key in self._expired:
                if index.column() == 2:
                    return "—"
                if index.column() == 6:
                    return "Caducada"
            return row.values[index.column()]
        return None

    @Slot(object)
    def set_rows(self, rows):
        if self.rows == rows:
            return
        if tuple(r.key for r in self.rows) != tuple(r.key for r in rows):
            self.beginResetModel()
            self.rows = rows
            self._expired.clear()
            self.endResetModel()
        else:
            changed = [i for i, (old, new) in enumerate(zip(self.rows, rows)) if old != new]
            self.rows = rows
            self._expired.clear()
            if changed:
                self.dataChanged.emit(self.index(changed[0], 0), self.index(changed[-1], len(self.headers) - 1), [Qt.DisplayRole, Qt.ToolTipRole])
        self.expire()

    def expire(self, now=None):
        now = now or datetime.now(timezone.utc)
        expired = {row.key for row in self.rows if row.expires_at is not None and now > row.expires_at}
        changed = expired ^ self._expired
        self._expired = expired
        if changed:
            indices = [i for i, row in enumerate(self.rows) if row.key in changed]
            self.dataChanged.emit(self.index(indices[0], 2), self.index(indices[-1], len(self.headers) - 1), [Qt.DisplayRole])
