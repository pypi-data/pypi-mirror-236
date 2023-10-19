from collections.abc import MutableMapping

from graphblas import Vector, monoid

from . import _utils


class NodeMap(MutableMapping):
    def __init__(self, v, *, fill_value=None, values_are_keys=False, key_to_id=None):
        self.vector = v
        if key_to_id is None:
            self._key_to_id = {i: i for i in range(v.size)}
        else:
            self._key_to_id = key_to_id
        self._id_to_key = None
        self._fill_value = fill_value
        self._values_are_keys = values_are_keys

    id_to_key = property(_utils.id_to_key)
    # get_property = _utils.get_property
    # get_properties = _utils.get_properties
    dict_to_vector = _utils.dict_to_vector
    list_to_vector = _utils.list_to_vector
    list_to_mask = _utils.list_to_mask
    list_to_ids = _utils.list_to_ids
    list_to_keys = _utils.list_to_keys
    matrix_to_dicts = _utils.matrix_to_dicts
    set_to_vector = _utils.set_to_vector
    # to_networkx = _utils.to_networkx
    vector_to_dict = _utils.vector_to_dict
    vector_to_list = _utils.vector_to_list
    vector_to_nodemap = _utils.vector_to_nodemap
    vector_to_nodeset = _utils.vector_to_nodeset
    vector_to_set = _utils.vector_to_set
    # _cacheit = _utils._cacheit

    # Requirements for MutableMapping
    def __delitem__(self, key):
        idx = self._key_to_id[key]
        del self.vector[idx]

    def __getitem__(self, key):
        idx = self._key_to_id[key]
        if (rv := self.vector.get(idx)) is not None:
            if self._values_are_keys:
                return self.id_to_key[rv]
            return rv
        if self._fill_value is not None:
            return self._fill_value
        raise KeyError(key)

    def __iter__(self):
        if self._fill_value is not None:
            return iter(self._key_to_id)
        # Slow if we iterate over one; fast if we iterate over all
        return map(
            self.id_to_key.__getitem__, self.vector.to_coo(values=False, sort=False)[0].tolist()
        )

    def __len__(self):
        if self._fill_value is not None:
            return len(self._key_to_id)
        return self.vector.nvals

    def __setitem__(self, key, val):
        idx = self._key_to_id[key]
        if self._values_are_keys:
            val = self._key_to_id[val]
        self.vector[idx] = val

    # Override other MutableMapping methods
    def __contains__(self, key):
        idx = self._key_to_id[key]
        return self._fill_value is not None or idx in self.vector

    def __eq__(self, other):
        if isinstance(other, NodeMap):
            return (
                self._values_are_keys == other._values_are_keys
                and self._fill_value == other._fill_value
                and self.vector.isequal(other.vector)
                and self._key_to_id == other._key_to_id
            )
        return super().__eq__(other)

    def clear(self):
        self.vector.clear()
        self._fill_value = None

    def get(self, key, default=None):
        idx = self._key_to_id[key]
        rv = self.vector.get(idx)
        if rv is None:
            if self._fill_value is not None:
                return self._fill_value
            return default
        if self._values_are_keys:
            return self.id_to_key[rv]
        return rv

    # items
    # keys
    # pop

    def popitem(self):
        v = self.vector
        try:
            idx, value = next(v.ss.iteritems())
        except StopIteration:
            raise KeyError from None
        del v[idx]
        if self._values_are_keys:
            value = self.id_to_key[value]
        return self.id_to_key[idx], value

    def setdefault(self, key, default=None):
        idx = self._key_to_id[key]
        if (value := self.vector.get(idx)) is not None:
            if self._values_are_keys:
                return self.id_to_key[value]
            return value
        if self._fill_value is not None:
            return self._fill_value
        if default is not None:
            self.vector[idx] = default
        return default

    # update
    # values


class VectorMap(MutableMapping):
    def __init__(self, v):
        self.vector = v

    # Requirements for MutableMapping
    def __delitem__(self, key):
        del self.vector[key]

    def __getitem__(self, key):
        return self.vector.get(key)

    def __iter__(self):
        # Slow if we iterate over one; fast if we iterate over all
        return iter(self.vector.to_coo(values=False, sort=False)[0].tolist())

    def __len__(self):
        return self.vector.nvals

    def __setitem__(self, key, val):
        self.vector[key] = val

    # Override other MutableMapping methods
    def __contains__(self, key):
        return key in self.vector

    def __eq__(self, other):
        if isinstance(other, VectorMap):
            return self.vector.isequal(other.vector)
        if isinstance(other, Vector):
            return self.vector.isequal(other)
        if isinstance(other, NodeMap):
            return self.vector.isequal(other.vector) and other._key_to_id == {
                i: i for i in range(self.vector.size)
            }
        return super().__eq__(other)

    def clear(self):
        self.vector.clear()

    def get(self, key, default=None):
        return self.vector.get(key, default)

    # items
    # keys
    # pop

    def popitem(self):
        v = self.vector
        try:
            idx, value = next(v.ss.iteritems())
        except StopIteration:
            raise KeyError from None
        del v[idx]
        return idx, value

    def setdefault(self, key, default=None):
        if (value := self.vector.get(key)) is not None:
            return value
        self.vector[key] = default
        return default

    # update
    # values


class VectorNodeMap(MutableMapping):
    def __init__(self, A, *, key_to_id=None):
        self.matrix = A
        if key_to_id is None:
            self._key_to_id = {i: i for i in range(A.size)}
        else:
            self._key_to_id = key_to_id
        self._id_to_key = None
        self._rows = None

    def _get_rows(self):
        if self._rows is None:
            self._rows = self.matrix.reduce_rowwise(monoid.any).new()
            self._rows(self._rows.S) << 1  # Make iso-valued
        return self._rows

    id_to_key = property(_utils.id_to_key)
    # get_property = _utils.get_property
    # get_properties = _utils.get_properties
    dict_to_vector = _utils.dict_to_vector
    list_to_vector = _utils.list_to_vector
    list_to_mask = _utils.list_to_mask
    list_to_ids = _utils.list_to_ids
    list_to_keys = _utils.list_to_keys
    matrix_to_dicts = _utils.matrix_to_dicts
    set_to_vector = _utils.set_to_vector
    # to_networkx = _utils.to_networkx
    vector_to_dict = _utils.vector_to_dict
    vector_to_list = _utils.vector_to_list
    vector_to_nodemap = _utils.vector_to_nodemap
    vector_to_nodeset = _utils.vector_to_nodeset
    vector_to_set = _utils.vector_to_set
    # _cacheit = _utils._cacheit

    # Requirements for MutableMapping
    def __delitem__(self, key):
        idx = self._key_to_id[key]
        del self.matrix[idx, :]
        if self._rows is not None:
            del self._rows[idx]

    def __getitem__(self, key):
        idx = self._key_to_id[key]
        if self._get_rows().get(idx) is None:
            raise KeyError(key)
        return VectorMap(self.matrix[idx, :].new())

    def __iter__(self):
        # Slow if we iterate over one; fast if we iterate over all
        return map(
            self.id_to_key.__getitem__,
            self._get_rows().to_coo(values=False, sort=False)[0].tolist(),
        )

    def __len__(self):
        return self._get_rows().nvals

    def __setitem__(self, key, val):
        idx = self._key_to_id[key]
        if isinstance(val, VectorMap):
            val = val.vector
        elif isinstance(val, dict):
            val = Vector.from_dict(val, self.matrix.dtype, size=self.matrix.ncols)
        else:
            raise TypeError
        if val.nvals == 0:
            del self.matrix[idx, :]
            if self._rows is not None:
                del self._rows[idx]
        else:
            self.matrix[idx, :] = val
            if self._rows is not None:
                self._rows[idx] = 1

    # Override other MutableMapping methods
    def __contains__(self, key):
        idx = self._key_to_id[key]
        return idx in self._get_rows()

    def __eq__(self, other):
        if isinstance(other, VectorNodeMap):
            return self.matrix.isequal(other.matrix) and self._key_to_id == other._key_to_id
        return super().__eq__(other)

    def clear(self):
        self.matrix.clear()
        self._rows = None

    def get(self, key, default=None):
        idx = self._key_to_id[key]
        if self._get_rows().get(idx) is None:
            return default
        return VectorMap(self.matrix[idx, :].new())

    # items
    # keys
    # pop

    def popitem(self):
        rows = self._get_rows()
        try:
            idx = next(rows.ss.iterkeys())
        except StopIteration:
            raise KeyError from None
        value = VectorMap(self.matrix[idx, :].new())
        del self.matrix[idx, :]
        del rows[idx]
        return self.id_to_key[idx], value

    # setdefault
    # update
    # values


class NodeNodeMap(MutableMapping):
    def __init__(self, A, *, fill_value=None, values_are_keys=False, key_to_id=None):
        self.matrix = A
        if key_to_id is None:
            self._key_to_id = {i: i for i in range(A.size)}
        else:
            self._key_to_id = key_to_id
        self._id_to_key = None
        self._rows = None
        self._fill_value = fill_value
        self._values_are_keys = values_are_keys

    def _get_rows(self):
        if self._rows is None:
            self._rows = self.matrix.reduce_rowwise(monoid.any).new()
            self._rows(self._rows.S) << 1  # Make iso-valued
        return self._rows

    id_to_key = property(_utils.id_to_key)
    # get_property = _utils.get_property
    # get_properties = _utils.get_properties
    dict_to_vector = _utils.dict_to_vector
    list_to_vector = _utils.list_to_vector
    list_to_mask = _utils.list_to_mask
    list_to_ids = _utils.list_to_ids
    list_to_keys = _utils.list_to_keys
    matrix_to_dicts = _utils.matrix_to_dicts
    set_to_vector = _utils.set_to_vector
    # to_networkx = _utils.to_networkx
    vector_to_dict = _utils.vector_to_dict
    vector_to_list = _utils.vector_to_list
    vector_to_nodemap = _utils.vector_to_nodemap
    vector_to_nodeset = _utils.vector_to_nodeset
    vector_to_set = _utils.vector_to_set
    # _cacheit = _utils._cacheit

    # Requirements for MutableMapping
    def __delitem__(self, key):
        idx = self._key_to_id[key]
        del self.matrix[idx, :]
        if self._rows is not None:
            del self._rows[idx]

    def __getitem__(self, key):
        idx = self._key_to_id[key]
        if self._fill_value is None and self._get_rows().get(idx) is None:
            raise KeyError(key)
        return self.vector_to_nodemap(
            self.matrix[idx, :].new(),
            fill_value=self._fill_value,
            values_are_keys=self._values_are_keys,
        )

    def __iter__(self):
        if self._fill_value is not None:
            return iter(self._key_to_id)
        # Slow if we iterate over one; fast if we iterate over all
        return map(
            self.id_to_key.__getitem__,
            self._get_rows().to_coo(values=False, sort=False)[0].tolist(),
        )

    def __len__(self):
        if self._fill_value is not None:
            return len(self._key_to_id)
        return self._get_rows().nvals

    def __setitem__(self, key, val):
        idx = self._key_to_id[key]
        if isinstance(val, NodeMap):
            # TODO: check val._key_to_id?
            val = val.vector
        elif isinstance(val, dict):
            val = Vector.from_dict(val, self.matrix.dtype, size=self.matrix.ncols)
        else:
            raise TypeError
        if val.nvals == 0:
            del self.matrix[idx, :]
            if self._rows is not None:
                del self._rows[idx]
        else:
            self.matrix[idx, :] = val
            if self._rows is not None:
                self._rows[idx] = 1

    # Override other MutableMapping methods
    def __contains__(self, key):
        idx = self._key_to_id[key]
        return self._fill_value is not None or idx in self._get_rows()

    def __eq__(self, other):
        if isinstance(other, NodeNodeMap):
            return (
                self._fill_value == other._fill_value
                and self._values_are_keys == other._values_are_keys
                and self.matrix.isequal(other.matrix)
                and self._key_to_id == other._key_to_id
            )
        return super().__eq__(other)

    def clear(self):
        self.matrix.clear()
        self._rows = None
        self._fill_value = None

    def get(self, key, default=None):
        idx = self._key_to_id[key]
        if self._fill_value is None and self._get_rows().get(idx) is None:
            return default
        self.vector_to_nodemap(
            self.matrix[idx, :].new(),
            fill_value=self._fill_value,
            values_are_keys=self._values_are_keys,
        )

    # items
    # keys
    # pop

    def popitem(self):
        rows = self._get_rows()
        try:
            idx = next(rows.ss.iterkeys())
        except StopIteration:
            raise KeyError from None
        value = self.vector_to_nodemap(
            self.matrix[idx, :].new(),
            fill_value=self._fill_value,
            values_are_keys=self._values_are_keys,
        )
        del self.matrix[idx, :]
        del rows[idx]
        return self.id_to_key[idx], value

    # setdefault
    # update
    # values
