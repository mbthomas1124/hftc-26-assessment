class StreamProcessor:
    def __init__(self):
        """
        Initialize the processor state.
        """
        # TODO
        pass

    def add_message(self, message: dict):
        """
        Processes an incoming message dictionary.

        Args:
            message (dict): {
                "seq": int,
                "val": Any (optional),
                "action": str (optional)
            }
        """
        # TODO
        pass

    def get_clean_stream(self) -> list:
        """
        Returns the processed values.

        Returns:
            list: A list of values (Any) sorted by their 'seq' ID.
        """
        # TODO
        pass
