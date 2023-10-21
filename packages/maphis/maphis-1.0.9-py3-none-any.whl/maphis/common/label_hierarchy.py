import dataclasses
import functools
import itertools
import json
import math
import operator
import typing
from pathlib import Path
from typing import List, Optional, Dict, Union, Any, Tuple, Set


def convert_legacy_hierarchy_to_new(lab_hier_path: Path) -> typing.Dict[str, typing.Any]:
    with open(lab_hier_path, 'r') as f:
        lab_hier_dict = json.load(f)
    new_lab_hier_dict = {'definition_file_version': '1.0',
                         'name': lab_hier_dict['name'],
                         'bits_per_label': 32}
    level_names = lab_hier_dict['mask_names']
    bit_counts = lab_hier_dict['counts_of_bits']
    level_bit_starts = list(itertools.accumulate(bit_counts, lambda a, b: a + b, initial=0))[len(level_names)-1::-1]
    new_lab_hier_dict['levels'] = [
        {
            'level_name': level_name,
            'bit_count': bit_count,
            'start': start
        } for level_name, bit_count, start in zip(level_names, bit_counts, level_bit_starts)
    ]
    new_lab_hier_dict['labels'] = [
        {
            'name': region_dict['name'],
            'code': region_dict['code'], #tuple([int(idx_at_level) for idx_at_level in region_dict['code'].split(':')]),
            'label': int(region_label),
            'color': region_dict['color'],
            'children': []
        } for region_label, region_dict in lab_hier_dict['labels'].items() if int(region_label) >= 0
    ]
    new_lab_hier_dict['labels'] = nest_regions(new_lab_hier_dict['labels'], len(level_names))
    return new_lab_hier_dict


def region_path_str_to_tuple(region_path: str) -> typing.Tuple[int, ...]:
    return tuple(int(i) for i in region_path.split(':'))


def nest_regions(region_dicts: typing.List[typing.Dict[str, typing.Any]], num_levels: int) -> typing.List[typing.Dict[str, typing.Any]]:
    region_paths_sorted: typing.List[typing.Tuple[int, ...]] = sorted([region_path_str_to_tuple(region_dict['code']) for region_dict in region_dicts])

    dict_of_regions: typing.Dict[typing.Tuple[int, ...], typing.Dict[str, typing.Any]] = {}

    for region_dict in region_dicts:
        dict_of_regions[region_path_str_to_tuple(region_dict['code'])] = region_dict

    if num_levels == 1:  # flat hierarchy
        return [dict_of_regions[region_path] for region_path in region_paths_sorted]

    zero_level_regions: typing.List[typing.Dict[str, typing.Any]] = []


    for region_path in region_paths_sorted:
        try:
            level_idx = max(region_path.index(0) - 1, 0)
            if level_idx == 0:
                zero_level_regions.append(dict_of_regions[region_path])
                continue
        except ValueError:
            level_idx = num_levels - 1
        parent_path = region_path[:level_idx] + tuple(0 for _ in region_path[level_idx:])
        dict_of_regions[parent_path]['children'].append(dict_of_regions[region_path])

    return zero_level_regions


class Node:
    """Label representation."""
    def __init__(self):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self.label: int = -1
        self.level: int = 0
        self.code: str = ''
        self.name: str = ''
        self.color: Tuple[int, int, int] = (255, 255, 255)  # for now

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'code': self.code,
            'color': {
                'red': self.color[0],
                'green': self.color[1],
                'blue': self.color[2]
            },
            'label': self.label,
            'children': [child_node.to_dict() for child_node in self.children]
        }

    @classmethod
    def from_dict(cls, node_dict: typing.Dict[str, typing.Any], parent: typing.Optional['Node']=None) -> 'Node':
        node = Node()
        node.parent = parent
        node.label = node_dict['label']
        node.code = node_dict['code']
        node.name = node_dict['name']
        node.color = tuple(node_dict['color'].values())
        node.children = [Node.from_dict(node_child_dict, node) for node_child_dict in node_dict['children']]
        return node

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(self.label)

    def __str__(self) -> str:
        return f'{self.name} ({self.code}), integer label = {self.label} (level: {self.level})\n'

    def hierarchy_str(self, indent: int=0) -> str:
        return '\t' * indent + str(self) + '\n'.join([child.hierarchy_str(indent+1) for child in self.children])

    @property
    def ancestors(self) -> typing.List['Node']:
        ancestors: typing.List[Node] = []
        curr_node = self
        while (curr_node := curr_node.parent) is not None:
            ancestors.append(curr_node)
        return ancestors


class HierarchyLevel:
    def __init__(self, name: str, bit_count: int, bit_start: int, n_bits: int=32):
        self.__nbits = n_bits
        self.name: str = name
        self.bit_count: int = bit_count
        self.bit_start: int = bit_start
        self.nodes: typing.List[Node] = []
        self.accumulated_bit_mask: int = ((2 ** self.__nbits - 1) << self.bit_start)
        self.bit_mask: int = self.accumulated_bit_mask & ((2 ** self.bit_count - 1) << self.bit_start)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "level_name": self.name,
            "bit_count": self.bit_count,
            "start": self.bit_start
        }

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, typing.Any], bits_per_label: int) -> 'HierarchyLevel':
        return HierarchyLevel(
            name=_dict['level_name'],
            bit_count=_dict['bit_count'],
            bit_start=_dict['start'],
            n_bits=bits_per_label
        )

    def __str__(self) -> str:
        return f'Level: `{self.name}`,\n\tbit mask: {bin(self.bit_mask)[2:]:0>32}'


class _LabelHierarchy:
    """Class representing a particular hierarchy of labels."""
    ROOT: int = -1

    DEFINITION_FILE_VERSION = '1.0'

    def __init__(self):
        self.masks: List[int] = []  # bit masks for all label levels, len(self.masks) = number of levels in hierarchy
        self.n_bits: int = 0  # how many bits are allocated for each label in the hierarchy
        self.mask_names: List[str] = []  # human-friendly names of masks, eg. Animal, Segments, corresponding to label levels
        self.counts_of_bits: List[int] = []  # a distribution of `n_bits` to `len(self.masks)` levels, self.counts_of_bits[i] = x means, x bits are allocated to i-th mask/level
        self.shifts: List[int] = []  # bit shifts for each mask, `self.shifts[0] = self.n_bits`, self.shifts[i] = self.shifts[i-1] - self.counts_of_bits[i-1]
        self.sep: str = ':'  # separator for code representation of labels, e.g. 1:1:2:0
        self.labels: List[int] = []  # list of labels that are defined, ie. that make sense to use for a specific case
        self.children: Dict[int, List[int]] = {}  # a mapping; label -> list of label's children
        self.parents: Dict[int, int] = {}  # a mappping; label -> label's parent

        self.hierarchy_levels: typing.Dict[str, HierarchyLevel] = {}

        self.nodes: Dict[int, Node] = {}  # a mapping; label -> label's node representation
        #self.colormap: Optional[Colormap] = None
        self.colormap: Dict[int, Tuple[int, int, int]] = {}
        self.name = ''
        self._level_groups: List[Set[int]] = []
        self.mask_label: Optional[Node] = None
        self.nodes_by_level: typing.List[typing.List[Node]] = []

    @classmethod
    def are_valid_levels(cls, levels: List[HierarchyLevel], n_bits: int = 32) -> bool:
        """
        Checks whether `masks` represents a valid distribution of masks for `n_bits`-bit labels
        For `masks` to be a valid list of masks:
        1. each mask must have only one sequence of ones, e.g. 11110000 is valid, 11110011 is not valid
        2. no two distinct masks can overlap, e.g. 11110000, 00001111 is a valid distribution;
                   11110000, 00111111  is not a valid mask distribution
        3. `masks[i]` and `masks[i+1]` must have their one-bit sequences adjacent, ie. 11110000 00001111 is valid
                    11110000, 00000111 is not valid
        4. bit-wise union of all masks must equal to `2^n_bits - 1`
        """
        masks = [level.bit_mask for level in levels]
        if not all(map(functools.partial(cls.has_unique_sequence_of_ones, n_bits=n_bits), masks)):
            return False

        return not cls.masks_overlap(list(sorted(masks))) and cls.masks_are_adjacent(masks) and cls.masks_cover_nbits(
            masks, n_bits)

    @classmethod
    def masks_overlap(cls, masks: List[int]) -> bool:
        """Checks whether the sorted masks in `masks` have nonempty bitwise intersection."""
        masks_ = list(sorted(masks))
        for i in range(len(masks_) - 1):
            if masks_[i] & masks_[i+1]:
                return True
        return False

    @classmethod
    def masks_are_adjacent(cls, masks: List[int]) -> bool:
        """Checks whether the neighboring masks in sorted(`masks`) are adjacent w.r.t. to their one-bit sequences.
        see 3. in the docstring of `are_valid_masks`"""
        masks_ = list(sorted(masks))
        for i in range(len(masks_) - 1):
            if not (masks_[i] & (masks_[i+1] >> 1)):
                return False
        return True

    @classmethod
    def has_unique_sequence_of_ones(cls, mask: int, n_bits: int = 32) -> bool:
        """Checks whether `mask` contains a single contiguous run of `1`-s."""
        found_seq_already = False  # is True when 0 bit is encountered after a sequence of 1 bits
        ones = False  # is switched to True when encountered the first 1 bit

        for i in range(n_bits):
            bit = (mask >> i) & 1
            if bit:
                if not found_seq_already: # The first 1bit encountered, marking the first sequence of 1bits
                    ones = True
                    found_seq_already = True
                else:
                    if not ones: # This means we encountered a second sequence of 1bits, making the mask an invalid one
                        return False
            else:
                ones = False
        return True

    @classmethod
    def create(cls, levels: typing.List[HierarchyLevel], n_bits: int = 32) -> \
            Optional['LabelHierarchy']:
        """Creates a new label hierarchy with the given masks in `masks`, named by `mask_names` and with a total of
        `n_bits` bits per mask."""
        masks = [level.bit_mask for level in levels]
        if not cls.are_valid_levels(masks, n_bits):
            return None  # TODO raise Exception?
        # if mask_names is None:
        #     mask_names = [f'level {i}' for i in range(len(masks))]

        hier = LabelHierarchy()
        hier.whole_mask = 2**n_bits - 1
        hier.hierarchy_levels = {level.name: level for level in levels}
        # hier.masks = list(sorted(masks, reverse=True))  # sort the masks in DESC
        hier.counts_of_bits = [level.bit_count for level in hier.hierarchy_levels]  # infer the count of bits of each mask

        start = n_bits
        for bit_count in hier.counts_of_bits:  # derive the bit shift for each mask.
            start -= bit_count
            hier.shifts.append(start)

        # hier.named_masks = {name: mask for name, mask in zip(mask_names, hier.masks)}
        hier.n_bits = n_bits
        # hier.mask_names = mask_names
        # hier.masks_names = {mask: name for name, mask in hier.named_masks.items()}

        hier.mask_to_level = {level.bit_mask: level for level in levels}

        for _ in range(len(masks)):
            hier._level_groups.append(set())

        return hier

    @classmethod
    def designate_bits(cls, counts_of_bits: List[int], mask_names: Optional[List[str]] = None, n_bits: int = 32) -> \
            Optional['LabelHierarchy']:
        """Generates `len(counts_of_bits)` masks and designates each of them its corresponding number of bits as specified
        in `counts_of_bits` out of total number of bits as specified in `n_bits`.
        Optionally gives them names as specified in `mask_names`."""
        if mask_names is None:
            mask_names = [f'level {i}' for i in range(len(counts_of_bits))]
        masks = []
        start = n_bits
        for count_of_bits in counts_of_bits:
            start -= count_of_bits
            masks.append((2**count_of_bits - 1) << start)
        return cls.create(masks, mask_names=mask_names, n_bits=n_bits)

    @classmethod
    def masks_cover_nbits(cls, masks: List[int], n_bits: int = 32) -> bool:
        """Checks whether the total number of 1-bits in all masks in `masks` is equal to `n_bits`."""
        mask = functools.reduce(operator.or_, masks)
        return mask == 2**n_bits - 1

    @classmethod
    def load(cls, path_to_json: Path) -> Optional['LabelHierarchy']:
        if not path_to_json.exists():
            return None
        with open(path_to_json) as f:
            label_hier_info = json.load(f)
        #counts_of_bits = label_hier_info['counts_of_bits']
        #mask_names = label_hier_info['mask_names']
        #return cls.designate_bits(counts_of_bits, mask_names=mask_names, n_bits=sum(counts_of_bits))
        return cls.from_dict(label_hier_info)

    def save(self, path_to_json: Path):
        with open(path_to_json, 'w') as f:
            json.dump({'counts_of_bits': self.counts_of_bits, 'mask_names': self.mask_names}, f)

    # def get_mask_name(self, label_or_code: Union[int, str]) -> str:
    #     """Returns the name of the mask that the `label` as specified by `label_or_code` belongs to.
    #
    #     `label_or_code`: int or str - either the integer representation of the label or its textual code.
    #     """
    #     if type(label_or_code) == str:
    #         label = self.label(label_or_code)
    #     else:
    #         label = label_or_code
    #     return self.mask_names[self.get_level(label)]
    #     #for level in range(len(self.masks) - 1, -1, -1):
    #     #    if label & self.masks[level]:
    #     #        return self.mask_names[level]

    def get_level(self, label: int) -> int:
        """Returns the level the label `label` belongs to in this hierarchy."""
        if label == 0:
            return 0
        if label < 0:
            return -1
        for level in range(len(self.masks) - 1, -1, -1):
            if label & self.masks[level]:
                return level

    def get_mask(self, label: int) -> int:
        """Returns the mask of the level that the `label` belongs to."""
        return self.masks[self.get_level(label)]

    def label_mask(self, label: int) -> int:
        """
        Returns the union of self.masks[0],...,self.masks[self.get_level(label)]
        """
        level = self.get_level(label)
        mask = 0
        for i in range(level+1):
            mask = mask | self.masks[i]
        return mask

    def get_parent(self, label_or_code: Union[int, str]) -> int:
        """Returns the parent label of the label represented by `label_or_code`."""
        if type(label_or_code) == str:
            label = self.label(label_or_code)
        else:
            label = label_or_code
        if label in self.parents:
            return self.parents[label]
        level = self.get_level(label)
        if level == 0:
            return -1
        parent_mask = self.get_label_mask_up_to(level - 1, label)
        # mask = self.get_mask(label)
        # index = self.masks.index(mask)
        return label & parent_mask

    def get_ancestors(self, label: int) -> List[int]:
        """Returns the list of ancestor labels for `label`."""
        parents = []
        curr_label = label
        while (parent := self.parents[curr_label]) > 0:
            parents.append(parent)
            curr_label = parent
        # parents.append(-1)
        return parents

    def code(self, label: int) -> str:
        """Returns the textual code representation of `label`."""
        str_code = str((self.masks[0] & label) >> self.shifts[0]) + self.sep
        for i in range(1, len(self.masks)):
            str_code += str((self.masks[i] & label) >> self.shifts[i]) + self.sep
        return str_code[:-1]

    def label(self, code: str) -> int:
        """Returns the `label` that is represented by `code`."""
        labels = code.split(self.sep)
        bits = [int(label) << shift for label, shift in zip(labels, self.shifts)]
        return functools.reduce(operator.or_, bits)

    def level_mask(self, level: int) -> int:
        """Returns the union of self.masks[0],...,self.masks[level]."""
        mask = 0
        for l in range(level + 1):
            mask |= self.masks[l]
        return mask

    def get_label_mask_up_to(self, level: int, label: int) -> int:
        """Returns the bitwise AND of `level_mask(level) and `label`."""
        mask = 0
        for l in range(level + 1):
            mask |= self.masks[l]
        return mask & label

    # def set_labels(self, labels: List[int]):
    #     self.labels = labels.copy()
    #
    #     self.nodes.clear()
    #     for label in self.labels:
    #         node = Node()
    #         node.label = label
    #         node.code = self.code(label)
    #         self.nodes[label] = node
    #         self._level_groups[self.get_level(label)].add(label)
    #
    #     self.compute_children()

    def compute_children(self):
        # self.nodes_by_level = [[] for _ in range(len(self.masks))]
        # for node in self.nodes.values():
        #     if node.label < 0:
        #         continue
        #     level = self.get_level(node.label)
        #     self.nodes_by_level[level].append(node)

        self._create_root_node()

        for node in sorted(self.nodes.values(), key=lambda _node: _node.label):
            if node.label < 0:
                continue
            level = self.get_level(node.label)
            if level == 0:
                self.parents[node.label] = -1
                node.parent = self.nodes[-1]
                self.children.setdefault(-1, list()).append(node.label)
                self.nodes[-1].children.append(node)
            else:
                mask = self.get_label_mask_up_to(level - 1, node.label)
                parent_label = node.label & mask
                if parent_label not in self.nodes:
                    # `node` is an orphaned node, should not happen unless the json file was modified manually
                    # TODO reject the whole label hierarchy or ignore the orphaned labels? For now, I'll adopt the second option
                    del self.nodes[node.label]
                    continue
                self.parents[node.label] = parent_label
                node.parent = self.nodes[parent_label]
                self.children.setdefault(parent_label, list()).append(node.label)
                self.nodes[parent_label].children.append(node)

    # def _compute_children(self):
    #     """Establishes descendant relations between label nodes."""
    #     self._create_root_node()
    #     if -1 in self.labels:
    #         self.labels.remove(-1)
    #     #first_idx = 1 if self.labels[0] == 0 else 0
    #     parent_label = -1
    #     label = parent_label
    #     depth = -1  # on depth 1 we look for children of `label` which is on level 0
    #     stack = [parent_label]
    #
    #     for curr_label in self.labels:
    #         curr_depth = self.get_level(curr_label)
    #         self.children.setdefault(curr_label, [])
    #         if curr_depth == depth:
    #             self.nodes[parent_label].children.append(self.nodes[curr_label])
    #             self.nodes[curr_label].parent = self.nodes[parent_label]
    #
    #             self.children.setdefault(parent_label, list()).append(curr_label)
    #             self.parents[curr_label] = parent_label
    #             label = curr_label
    #         elif curr_depth > depth:
    #             parent_label = label
    #             stack.append(parent_label)
    #
    #             self.nodes[parent_label].children.append(self.nodes[curr_label])
    #             self.nodes[curr_label].parent = self.nodes[parent_label]
    #
    #             self.children.setdefault(parent_label, list()).append(curr_label)
    #             self.parents[curr_label] = parent_label
    #             label = curr_label
    #             depth = curr_depth
    #         elif curr_depth < depth:
    #             for _ in range(depth - curr_depth):
    #                 stack.pop()
    #             parent_label = stack[-1]
    #
    #             self.nodes[parent_label].children.append(self.nodes[curr_label])
    #             self.nodes[curr_label].parent = self.nodes[parent_label]
    #
    #             self.children.setdefault(parent_label, list()).append(curr_label)
    #             self.parents[curr_label] = parent_label
    #             label = curr_label
    #             depth = curr_depth

    def _create_root_node(self):
        """Creates a root node. This label node is not used by the user and should not appear anywhere visible."""
        if -1 in self.nodes:
            return
        root = Node()
        root.label = -1
        root.code = '-1:0:0:0'  # whatever, this node won't be ever used for anything useful, just to have a proper rooted tree
        root.name = 'invalid'
        root.children = []
        root.parent = None

        self.nodes[-1] = root

        self.children[-1] = []
        self.parents[-1] = -1

    def is_descendant_of(self, desc: int, ance: int) -> bool:
        """Checks whether the label `desc` is actually a descendant of the label `ance`."""
        ance_mask = self.label_mask(ance)
        return (desc & ance_mask) == ance

    def is_ancestor_of(self, ance: int, label: int) -> bool:
        """Checks whether the label `ance` is actually the ancestor of the label `label`."""
        return self.is_descendant_of(label, ance)

    def add_label(self, label: int, name: str, color: Tuple[int, int, int] = (255, 255, 255)):
        """Adds a new label to the hierarchy."""
        # TODO check that `label` is not present already
        parent_label = self.get_parent(label)
        parent = None if parent_label == -1 else self.nodes[parent_label]

        self.children[label] = []
        self.parents[label] = parent_label

        label_node = Node()
        label_node.label = label
        label_node.parent = parent
        label_node.name = name
        label_node.code = self.code(label)
        label_node.children = []
        label_node.color = color

        if parent is not None:
            self.children[parent_label].append(label)
            parent.children.append(label_node)

        self.nodes[label] = label_node

        self.labels.append(label)
        self.labels.sort()

        self.colormap[label] = color

    def add_child_label(self, parent: int, name: str, color: Tuple[int, int, int]) -> Node:
        """Adds a new child label to the label `parent`."""
        last_child = max(self.children[parent], default=parent)
        if last_child != parent:
            level = self.get_level(last_child)
        else:
            level = self.get_level(parent) + 1
        mask = self.masks[level]
        child_num = last_child
        one = 1 << self.shifts[level]
        child_num += one
        label = child_num

        parent_node: Node = self.nodes[parent]

        self.children[label] = []
        self.parents[label] = parent

        label_node = Node()
        label_node.label = label
        label_node.parent = parent_node
        label_node.name = name
        label_node.code = self.code(label)
        label_node.children = []
        label_node.color = color

        if parent_node is not None:
            self.children[parent].append(label)
            parent_node.children.append(label_node)

        self.nodes[label] = label_node

        self.labels.append(label)
        self.labels.sort()

        self.colormap[label] = color

        return label_node

    @property
    def level_groups(self) -> List[Set[int]]:
        """
        Returns sets of labels grouped by level, so `level_groups[1]` is a set of labels that are on level 1 in the hierarchy.
        """
        return self._level_groups

    def group_by_level(self, labels: Union[List[int], Set[int]]) -> Dict[int, Set[int]]:
        """
        Groups the `labels` based on their level in the hierarchy.
        """
        groups: Dict[int, Set[int]] = {}
        for label in labels:
            groups.setdefault(self.get_level(label), set()).add(label)
        return groups

    def get_available_label(self, parent: int) -> int:
        """Returns the next available child label for `parent`."""
        last_child_node: typing.Optional[Node] = max(self.nodes[parent].children, default=None, key=lambda _node: _node.label)
        if last_child_node is None:
            last_child = 0
        else:
            last_child = last_child_node.label
        mask = self.get_mask(last_child)
        child_num = last_child & mask
        one = 1 << self.shifts[self.get_level(last_child)]
        child_num += one

        return parent | child_num

    # def get_child_labels(self, parent: typing.Union[Node, int, str]) -> typing.List[int]:
    #     if isinstance(parent, str):
    #         parent = self.label(parent)
    #     if isinstance(parent, Node):
    #         parent = self.nodes[parent]
    #     return [node.label for node in parent.children]

    def get_child_nodes(self, parent: typing.Union[Node, int, str]) -> typing.List[Node]:
        if isinstance(parent, str):
            parent = self.label(parent)
        if isinstance(parent, int):
            parent = self.nodes[parent]
        return parent.children

    @classmethod
    def _bit_count(cls, mask: int) -> int:
        """Returns the number of `1-bits` in `mask`."""
        bit = mask & 1
        while not bit:
            mask = mask >> 1
            bit = mask & 1
        return int(math.log2(mask + 1))

    @classmethod
    def from_dict(cls, label_hier_info: Dict[str, Any]) -> 'LabelHierarchy':
        counts_of_bits = label_hier_info['counts_of_bits']
        mask_names = label_hier_info['mask_names']
        lab_hier = cls.designate_bits(counts_of_bits, mask_names=mask_names, n_bits=sum(counts_of_bits))
        for label, label_dict in label_hier_info['labels'].items():
            node = Node()
            node.label = int(label)
            node.code = label_dict['code']
            node.name = label_dict['name']
            color = label_dict['color']
            node.color = (int(color['red']), int(color['green']), int(color['blue']))
            lab_hier.colormap[node.label] = node.color
            lab_hier.nodes[node.label] = node
            lab_hier.labels.append(node.label)
        lab_hier.labels.sort()
        lab_hier.compute_children()
        lab_hier.name = label_hier_info['name']
        if (mask_label := label_hier_info['constraint_mask_label']) is not None:
            lab_hier.mask_label = lab_hier.nodes[mask_label]
        return lab_hier

    def to_dict(self) -> Dict[str, Any]:
        json_dict = {
            'name': self.name,
            'counts_of_bits': self.counts_of_bits,
            'mask_names': self.mask_names,
            'constraint_mask_label': None if self.mask_label is None else self.mask_label.label,
            'labels': {
                label: node.to_dict() for label, node in self.nodes.items()
            }
        }
        return json_dict


class LabelHierarchy:

    DEFINITION_FILE_VERSION = '1.0'

    def __init__(self):
        self._fname: str = 'label_hierarchy.json'
        self.name: str = ''
        self.__bits_per_label = 32
        self.hierarchy_levels: typing.List[HierarchyLevel] = []
        self.nodes_hierarchy: typing.List[Node] = []
        self.nodes_flat: typing.List[Node] = []
        self.nodes_dict: typing.Dict[str, Node] = {}
        self.colormap: typing.Dict[int, typing.Tuple[int, int, int]] = {}

    @classmethod
    def create(cls, name: str, hierarchy_levels: typing.List[HierarchyLevel]) -> 'LabelHierarchy':
        hierarchy = LabelHierarchy()
        hierarchy.name = name
        hierarchy.hierarchy_levels = hierarchy_levels

        if not cls.are_valid_levels(hierarchy_levels):
            raise ValueError('The provided HierarchyLevels are not valid.')

        return hierarchy

    @classmethod
    def are_valid_levels(cls, levels: List[HierarchyLevel], n_bits: int = 32) -> bool:
        """
        Checks whether `masks` represents a valid distribution of masks for `n_bits`-bit labels
        For `masks` to be a valid list of masks:
        1. each mask must have only one sequence of ones, e.g. 11110000 is valid, 11110011 is not valid
        2. no two distinct masks can overlap, e.g. 11110000, 00001111 is a valid distribution;
        11110000, 00111111  is not a valid mask distribution
        3. `masks[i]` and `masks[i+1]` must have their one-bit sequences adjacent, ie. 11110000 00001111 is valid
        11110000, 00000111 is not valid
        4. bit-wise union of all masks must equal to `2^n_bits - 1`
        """

        masks = [level.bit_mask for level in levels]
        if not all(map(functools.partial(cls.has_unique_sequence_of_ones, n_bits=n_bits), masks)):
            return False

        return not cls.masks_overlap(list(sorted(masks))) and cls.masks_are_adjacent(masks) and cls.masks_cover_nbits(
            masks, n_bits)

    @classmethod
    def masks_overlap(cls, masks: List[int]) -> bool:
        """Checks whether the sorted masks in `masks` have nonempty bitwise intersection."""
        masks_ = list(sorted(masks))
        for i in range(len(masks_) - 1):
            if masks_[i] & masks_[i+1]:
                return True
        return False

    @classmethod
    def masks_are_adjacent(cls, masks: List[int]) -> bool:
        """Checks whether the neighboring masks in sorted(`masks`) are adjacent w.r.t. to their one-bit sequences.
        see 3. in the docstring of `are_valid_masks`"""
        masks_ = list(sorted(masks))
        for i in range(len(masks_) - 1):
            if not (masks_[i] & (masks_[i+1] >> 1)):
                return False
        return True

    @classmethod
    def masks_cover_nbits(cls, masks: List[int], n_bits: int = 32) -> bool:
        """Checks whether the total number of 1-bits in all masks in `masks` is equal to `n_bits`."""
        mask = functools.reduce(operator.or_, masks)
        return mask == 2**n_bits - 1

    @classmethod
    def has_unique_sequence_of_ones(cls, mask: int, n_bits: int = 32) -> bool:
        """Checks whether `mask` contains a single contiguous run of `1`-s."""
        found_seq_already = False  # is True when 0 bit is encountered after a sequence of 1 bits
        ones = False  # is switched to True when encountered the first 1 bit

        for i in range(n_bits):
            bit = (mask >> i) & 1
            if bit:
                if not found_seq_already: # The first 1bit encountered, marking the first sequence of 1bits
                    ones = True
                    found_seq_already = True
                else:
                    if not ones: # This means we encountered a second sequence of 1bits, making the mask an invalid one
                        return False
            else:
                ones = False
        return True

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, typing.Any]) -> 'LabelHierarchy':
        hier = LabelHierarchy()
        hier.name = _dict['name']
        hier.__bits_per_label = _dict['bits_per_label']
        hier.hierarchy_levels = [
            HierarchyLevel.from_dict(_level_dict, hier.__bits_per_label) for _level_dict in _dict['levels']
        ]
        hier.nodes_hierarchy = [Node.from_dict(node_dict) for node_dict in _dict['labels']]
        stack = list(hier.nodes_hierarchy)
        while len(stack) > 0:
            node = stack.pop()
            node.level = hier.get_level(node.label)
            hier.nodes_flat.append(node)
            stack.extend(node.children)
        hier.nodes_flat = sorted(hier.nodes_flat, key=lambda node: node.code)
        for node in hier.nodes_flat:
            hier.nodes_dict[node.code] = node
            hier.colormap[node.label] = node.color
        return hier

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'definition_file_version': self.DEFINITION_FILE_VERSION,
            'name': self.name,
            'bits_per_label': self.__bits_per_label,
            'levels': [level.to_dict() for level in self.hierarchy_levels],
            'labels': [node.to_dict() for node in self.nodes_hierarchy]
        }

    def save(self, fpath: Path):
        with open(fpath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        self._fname = fpath.name

    @classmethod
    def load_from(cls, file_path: Path) -> 'LabelHierarchy':
        with open(file_path, 'r') as f:
            _dict = json.load(f)
            lab_hier = LabelHierarchy.from_dict(_dict)
            lab_hier._fname = file_path.name
            return lab_hier

    def __str__(self) -> str:
        text = f'------Label hierarchy `{self.name}`------\n'
        text = text + 'Hierarchy levels:\n' + '\t\n'.join([str(level) for level in self.hierarchy_levels])
        return text + '\nNodes:\n' + '\n'.join([node.hierarchy_str(indent=1) for node in self.nodes_hierarchy])

    def get_level(self, label: int) -> int:
        """Returns the level the label `label` belongs to in this hierarchy."""
        if label == 0:
            return 0
        if label < 0:
            return -1
        for i, level in enumerate(self.hierarchy_levels[::-1]):
            if label & level.bit_mask:
                return len(self.hierarchy_levels) - i - 1

    def get_mask(self, label: int):
        return self.hierarchy_levels[self.get_level(label)].bit_mask

    def code(self, label: int) -> str:
        """Returns the textual code representation of `label`."""
        str_code = ''
        for i, level in enumerate(self.hierarchy_levels):
            str_code += str((level.bit_mask & label) >> level.bit_start) + ':'
        return str_code[:-1]

    def label(self, code: str) -> int:
        """Returns the `label` that is represented by `code`."""
        path = [int(v) for v in code.split(':')]
        label = 0
        for level, count_at_level in zip(self.hierarchy_levels, path):
            label |= (count_at_level << level.bit_start)
        return label

    def accumulate_bit_masks_for(self, label: int) -> int:
        return self.hierarchy_levels[self.get_level(label)].accumulated_bit_mask

    def get_available_label(self, parent: Node) -> int:
        last_child = max(parent.children, key=lambda node: node.label, default=parent)
        if last_child != parent:
            level = last_child.level + 1
        else:
            level = parent.level + 1

        child_label = last_child.label
        next_child_label = (child_label >> self.hierarchy_levels[level].bit_start) + 1
        next_child_label = next_child_label << self.hierarchy_levels[level].bit_start

        return next_child_label

    def add_child_label(self, parent: Node, name: str, color: Tuple[int, int, int]) -> Node:
        next_child_label = self.get_available_label(parent)

        child_node = Node()
        child_node.name = name
        child_node.color = color
        child_node.label = next_child_label
        child_node.code = self.code(next_child_label)

        return child_node

    def is_descendant_of(self, desc: int, ance: int) -> bool:
        """Checks whether the label `desc` is actually a descendant of the label `ance`."""
        ance_node = self.nodes_dict[self.code(ance)]
        ance_mask = self.hierarchy_levels[ance_node.level].accumulated_bit_mask
        return (desc & ance_mask) == ance

    def is_ancestor_of(self, ance: int, label: int) -> bool:
        return self.is_descendant_of(label, ance)

    def group_by_level(self, labels: Union[List[int], Set[int]]) -> Dict[int, Set[int]]:
        """
        Groups the `labels` based on their level in the hierarchy.
        """
        groups: Dict[int, Set[int]] = {}
        for label in labels:
            groups.setdefault(self.get_level(label), set()).add(label)
        return groups

    def get_ancestors(self, label: int) -> typing.List[int]:
        code = self.code(label)
        node = self.nodes_dict[code]

        return [_node.label for _node in node.ancestors]

    def __getitem__(self, item: typing.Union[str, int]) -> Node:
        if type(item) != str:
            item = int(item)
            item = self.code(item)
        return self.nodes_dict[item]

