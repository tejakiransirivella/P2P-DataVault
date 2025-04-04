import os
import wx
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 25*1024

aes_key = b'\xc2\xc4\xaa\x10K\xdd7\xac\xb7\xa5^\xb2\x98\xd0"\xcc'
hmac_key = b'\x97qW\x05T\x10\x9b,\x1c\xdah\xe6\xa8Y\xb6\xc7'
aes_iv = b"l~\xe4\x1ax'\xcf\xa0q\x9e;Z\xa9\nF$"

class FileStore:

    __slots__ = ("path", "file", "metadata", "BLOCK_SIZE")

    def __init__(self, path) -> None:
        self.path = path
        # if not os.path.exists(path):
        self.file = open(self.path, 'w+b')
        self.BLOCK_SIZE = 25648
        pass

    def read_block(self, block_id):
        # use python open.seek to skip to the given block id and return data
        self.file.seek((block_id)*self.BLOCK_SIZE)
        data = self.file.read(self.BLOCK_SIZE)
        return data

    def write_block(self, data):
        # write binary data to block and append id to metadata
        # return confirmation of successful write and id
        block_id = os.path.getsize(self.path)//self.BLOCK_SIZE
        self.file.seek(0, 2)
        self.file.write(data)
        return block_id

    def close(self):
        self.file.close()


class FileStorageFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.aes_key = kwargs.get("aes_key")
        self.hmac_key = kwargs.get("hmac_key")
        self.aes_iv = kwargs.get("aes_iv")
        del kwargs["aes_key"]
        del kwargs["hmac_key"]
        del kwargs["aes_iv"]
        super(FileStorageFrame, self).__init__(*args, **kwargs)
        self.connect = FileStore('datastore')
        self.files = {}
        self.InitUI()
        self.Centre()

    def OnUpload(self, event):
        dlg = wx.FileDialog(self, "Choose a file", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            selected_file = dlg.GetPath()
            print(f"Selected file: {selected_file}")
            blocks = self.encrypt_and_send(selected_file)
            filename = os.path.basename(selected_file)
            self.files[filename] = blocks
            self.updateList()
        dlg.Destroy()

    def OnDownload(self, event):
        index = self.selectedElement
        self.receive_and_decrypt(self.fileList.GetItemText(index))
        pass

    def encrypt_and_send(self, path):

        filepath = path
        testfile = open(filepath, 'rb')

        # https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
        aes_key = self.aes_key
        hmac_key = self.hmac_key
        aes_iv = self.aes_iv
        blocks = []

        for i in range(0, os.path.getsize(filepath) // BLOCK_SIZE):
            testfile.seek(i * BLOCK_SIZE)
            data = testfile.read(BLOCK_SIZE)
            cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            ciphertext = cipher.encrypt(data)
            tag = hmac.update(cipher.iv + ciphertext).digest()
            send_data = tag + cipher.iv + ciphertext
            # TODO : send data to wherever
            # recv_data.append(send_data)
            blocks.append(self.connect.write_block(send_data))
        else:
            data = testfile.read()
            data += (BLOCK_SIZE - len(data)) * '\0'.encode('utf-8')
            cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            ciphertext = cipher.encrypt(data)
            tag = hmac.update(cipher.iv + ciphertext).digest()
            send_data = tag + cipher.iv + ciphertext
            # TODO : send data to wherever
            # recv_data.append(send_data)
            blocks.append(self.connect.write_block(send_data))

        return blocks

    def receive_and_decrypt(self, filename):
        blocks = self.files[filename]
        recv_data = [self.connect.read_block(b) for b in blocks]
        aes_key = self.aes_key
        hmac_key = self.hmac_key
        reconstruct = b""
        for f in recv_data:
            tag1 = f[:32]
            iv1 = f[32:48]
            ciphertext1 = f[48:]
            try:
                hmac1 = HMAC.new(hmac_key, digestmod=SHA256)
                tag1 = hmac1.update(iv1 + ciphertext1).verify(tag1)
            except ValueError:
                print("The message was modified!")
            cipher1 = AES.new(aes_key, AES.MODE_CBC, iv=iv1)
            message = cipher1.decrypt(ciphertext1)
            reconstruct += message
        f = open("downloads/" + filename, 'wb', encoding=None)
        f.write(reconstruct.strip('\0'.encode('utf-8')))
        f.close()

    def add_file_to_list(self, filename, blocks):
        index = self.fileList.InsertItem(0, filename)  # Insert at the top (index 0)

        self.fileList.SetItem(index, 1, str(blocks))

    def updateList(self):
        self.fileList.DeleteAllItems()
        for key, value in self.files.items():
            self.add_file_to_list(key, value)

    def updateSelected(self, event):
        self.selectedElement = event.GetIndex()

    def InitUI(self):
        panel = wx.Panel(self)

        # File list display
        self.fileList = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.fileList.InsertColumn(0, "Filename", width=250)
        self.fileList.InsertColumn(1, "Blocks", width=100)
        self.fileList.InsertColumn(2, "Last Modified", width=150)

        # Buttons
        uploadBtn = wx.Button(panel, label="Upload")
        downloadBtn = wx.Button(panel, label="Download")
        deleteBtn = wx.Button(panel, label="Delete")

        # Sizers (for layout)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.fileList, proportion=1, flag=wx.EXPAND)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(uploadBtn, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        btnSizer.Add(downloadBtn, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        btnSizer.Add(deleteBtn, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        mainSizer.Add(btnSizer, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(mainSizer)

        # TODO : plan and add events for buttons
        uploadBtn.Bind(wx.EVT_BUTTON, self.OnUpload)
        downloadBtn.Bind(wx.EVT_BUTTON, self.OnDownload)
        self.fileList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.updateSelected)

        self.SetTitle("Distributed Storage")
        self.SetSize(600, 400)


def main():
    app = wx.App(
    )
    frame = FileStorageFrame(None,
                             aes_key=aes_key,
                             hmac_key=hmac_key,
                             aes_iv=aes_iv)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()