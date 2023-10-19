# Copyright [2023] [Arcus Inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Dict, List


class JoinKeyMetadata:
    def __init__(self, column_indices: List[int], column_headers: List[str]):
        assert len(column_indices) == len(
            column_headers
        ), "Number of column indices must match number of column headers."
        self.column_indices = column_indices
        self.column_headers = column_headers

    def get_column_indices(self) -> List[int]:
        return self.column_indices

    def get_column_headers(self) -> List[str]:
        return self.column_headers
