# TemporalObject

The TemporalObject is a custom implementation of an object that tracks changes over time, allowing you to access past states of the object. It is designed to provide version control for dictionary-like data structures, making it ideal for applications that require historical data tracking, state buffering, and temporal data analysis.

The primary purpose of the TemporalObject class is to enable users to record and retrieve different states of an object at various points in time. This is particularly useful for scenarios where understanding the evolution of data or the ability to revert to previous states is crucial.

## Design Requirements

- The TemporalObject class should be designed to work with any dictionary-like data structure.
- The class should provide methods for adding new states to the object, retrieving past states, and navigating through the temporal history of the object.
- The class should be flexible and allow users to customize the behavior of the temporal object by providing a custom function for merging states.
- The class should be able to handle large amounts of data efficiently, without sacrificing the ability to access past states.
- The class should be able to handle nested dictionaries, allowing users to track changes in nested data structures.
- Access values by relative position, by time index, or by absolute position.
- access value from key and index the value by time index????? maybe in the get method can provide the time index too
