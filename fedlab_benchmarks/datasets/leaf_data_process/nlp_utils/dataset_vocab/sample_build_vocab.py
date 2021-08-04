# Copyright 2021 Peng Cheng Laboratory (http://www.szpclab.com/) and FedLab Authors (smilelab.group)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import math
import random
import pickle
from ...data_read_util import read_dir
from ...nlp_utils.tokenizer import Tokenizer
from ...nlp_utils.vocab import Vocab


class DataSample:
    def __init__(self, dataset:str, data_path: str, select_ratio: float, is_to_tokens=True, tokenizer=None):
        self.dataset = dataset
        self.data_path = data_path  # for train data
        self.select_ratio = select_ratio
        self.select_client, self.data = self.choose_client_data()
        self.data_token = []
        self.tokenizer = tokenizer if tokenizer else Tokenizer('normal')

        if is_to_tokens:
            self.data2token()

    def choose_client_data(self):
        client_id_name_dict, client_groups, client_name_data_dict = read_dir(data_dir=self.data_path)

        client_num = len(client_id_name_dict)
        random.seed(0)
        select_client = random.sample(range(client_num), math.floor(self.select_ratio * client_num))
        data = []

        for client_id in select_client:
            client_name = client_id_name_dict[client_id]
            # choose the first data to build vocab
            data.append(self.__process_x(client_name_data_dict[client_name]['x'][0]))

        return select_client, data

    def data2token(self):
        assert self.data is not None
        for sen in self.data:
            self.data_token.append(self.tokenizer(sen))

    def __process_x(self, raw_x):
        if self.dataset == 'sent140':
            raw_x = raw_x[4]
        return raw_x


def build_vocab(dataset: str, vocab_limit_size: int):
    data_path = '../leaf_data/' + dataset + '/data/train'
    data_sample = DataSample(dataset='sent140', data_path=data_path, select_ratio=0.25)
    vocab = Vocab(origin_data_tokens=data_sample.data_token, vocab_limit_size=vocab_limit_size)
    save_file_path = dataset + '_vocab.pck'
    pickle.dump(vocab, open(save_file_path, 'wb'))
    print('sample data to build vocab for {} dataset is completed!'.format(dataset))


if __name__ == '__main__':
    build_vocab(dataset='sent140', vocab_limit_size=30000)
