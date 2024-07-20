from collections import deque

from temporal.util import LimitedDict


class TemporalBuffer:
    """
    A buffer designed for storing and managing states in a temporal sequence.

    This class utilizes a deque with a fixed maximum length (maxlen) to maintain
    a rolling buffer of states.

    Each state can be indexed by an integer, a string ID, or a slice. The class
    also tracks the current state index within the buffer.

    Parameters
    ----------
    temporal_depth : int
        The maximum number of states to store.

    Attributes
    ----------
    buffer : deque
        A deque with a maxlen.
    id_index : LimitedDict
        A dictionary with a limit on the number of items it can store.
    current_index : int
        The index of the current state.

    Methods
    -------
    add(id: str, state: dict) -> None:
        Appends a state to the buffer.
    update(object) -> None:
        Adds the object's state to the buffer.
    get_last_n_states(n: int) -> list[dict]:
        Returns the last n states from the buffer.
    get_state_at_index(index: int) -> dict:
        Returns the state at the given index.
    move_forward() -> dict:
        Moves the current index forward by 1 step.
    move_backward() -> dict:
        Moves the current index backward by 1 step.
    current() -> dict:
        Returns the current state.
    """

    def __init__(self, temporal_depth: int = 100) -> None:
        """
        Parameters
        ----------
        size : int
            The maximum number of states to store.
        """
        self.buffer = deque(maxlen=temporal_depth)
        self.id_index = LimitedDict(temporal_depth)
        self.current_index = -1  # Initialize to -1 to indicate no states yet

    def add(self, id: str, state: dict) -> None:
        """
        Appends a state to the buffer.

        Parameters
        ----------
        id : str
            The ID of the state.
        state : dict
            The state to add to the buffer.
        """
        self.id_index[id] = state
        if len(self.buffer) == self.buffer.maxlen:
            self.current_index = (self.current_index + 1) % self.buffer.maxlen
        else:
            self.current_index += 1
        self.buffer.append(state)

    def update(self, object_state: dict) -> None:
        """
        Adds the object's state to the buffer.

        Parameters
        ----------
        object_state : dict
            The object's state to add to the buffer.
        """
        self.add(object_state.temporal_id, object_state)

    def get_last_n_states(self, n: int) -> list[dict]:
        """
        Returns the last n states from the buffer.

        Parameters
        ----------
        n : int
            The number of states to return.

        Returns
        -------
        list[dict]
            The last n states from the buffer.
        """
        return list(self.buffer)[-n:]

    def get_state_at_index(self, index: int) -> dict:
        """
        Returns the state at the given index.

        Parameters
        ----------
        index : int
            The index of the state to return.

        Returns
        -------
        dict
            The state at the given index.
        """
        return self[index]

    def move_forward(self) -> dict:
        """
        Moves the current index forward by 1 step.

        Returns
        -------
        dict
            The state at the new index.
        """
        raise NotImplementedError("Forward traversal not implemented")

    def move_backward(self) -> dict:
        """
        Moves the current index backward by 1 step.

        Returns
        -------
        dict
            The state at the new index.
        """
        raise NotImplementedError("Backward traversal not implemented")

    def _get_by_temporal_id(self, temporal_id):
        return self.id_index.get(temporal_id, None)

    def __len__(self) -> int:
        """
        Returns the number of states in the buffer.

        Returns
        -------
        int
            The number of states in the buffer.
        """
        return len(self.buffer)

    def __call__(self, index: int | slice | str = 0) -> dict:
        """
        Returns the state at the given index.
        """
        if len(self.buffer) == 0:
            raise IndexError("No states in the buffer")
        return self.buffer[index]

    def __contains__(self, key: str) -> bool:
        """
        Returns whether the temporal ID is in the buffer.
        """
        return key in self.id_index

    def __setitem__(self, key: str, value: dict) -> None:
        """
        Sets the value of the key.
        """
        self.id_index[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Deletes the value of the key.
        """
        del self.id_index[key]

    def __iter__(self) -> dict:
        """
        Returns an iterator over the states in the buffer.
        """
        return iter(self.buffer)

    def __getitem__(self, index: int | slice | str) -> dict:
        """
        Returns the state at the given index.

        Parameters
        ----------
        index : int | slice | str
            The index of the state to return. Can be by position (int),
            by temporal ID (str), or by slice.

        Returns
        -------
        dict
            The state at the given index.
        """
        # If index is an integer, return the state at the given index
        if isinstance(index, int):
            # If index is negative
            if index < 0:
                index = abs(index)
            # Check if the index is within the valid range
            if index < 0 or index >= len(self.buffer):
                raise IndexError("Index out of range")
            # Return the state at the given index
            return self.buffer[-1 - index]

        # If index is a slice, return the states in the given range
        elif isinstance(index, slice):
            raise NotImplementedError("Haven't implemented slicing yet")
            #! Highlighted out until implemented
            # # Convert the slice to a list of indices
            # start, stop, step = index.indices(len(self.buffer))
            # # Return the states at the given indices
            # return [self[i] for i in range(start, stop, step)]

        elif isinstance(index, str):
            return self._get_by_temporal_id(index)
        else:
            raise TypeError("Invalid argument type")

    @property
    def current(self) -> dict:
        """
        Returns the current state.

        Returns
        -------
        dict
            The current state.
        """
        return self.buffer[-1]
