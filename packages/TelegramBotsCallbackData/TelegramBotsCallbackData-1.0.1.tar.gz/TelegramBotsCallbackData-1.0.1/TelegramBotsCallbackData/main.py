"""
Copyright 2023 Wintreist

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from  hashlib import sha256
from pathlib import Path
import pickle as pkl


class CallbackData(object):
    def __init__(self, file_path=Path.cwd().joinpath("./.callback_lib/data.pkl")):
        self.file_path = Path(file_path)
        self.create_dir()
        self.data:dict = self.read()

    def create_dir(self):
        self.file_path.parent.mkdir(exist_ok=True)
        if not self.file_path.is_file():
            with open(self.file_path, 'wb') as file:
                pkl.dump({}, file, protocol=pkl.HIGHEST_PROTOCOL)
        
    def read(self):
        with open(self.file_path, 'rb') as file:
            data = pkl.load(file)
        return data
    
    def update_data(self):
        with open(self.file_path, 'wb') as file:
            pkl.dump(self.data, file, protocol=pkl.HIGHEST_PROTOCOL)

    def new(self, callback_data:dict, just_once = False):
        callback_data['just_once'] = just_once
        if callback_data in self.data.values():
            return list(self.data.keys())[list(self.data.values()).index(callback_data)]
        callback_data_bytes = pkl.dumps(callback_data, protocol=pkl.HIGHEST_PROTOCOL)
        hash = sha256(callback_data_bytes).hexdigest()
        self.data[hash] = callback_data
        self.update_data()
        return hash

    def restore(self, callback_data:str):
        if callback_data in self.data:
            data:dict = self.data[callback_data]
            just_once:bool = data.pop('just_once')
            if just_once:
                del self.data[callback_data]
                self.update_data()
            return data
        else:
            raise KeyError("This hash doesn't exist in callback lib")
