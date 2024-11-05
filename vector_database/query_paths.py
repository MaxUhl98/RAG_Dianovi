from enum import Enum
class QueryPaths(Enum):
    INIT = 'vector_database/queries/init.sql'
    INSERT = 'vector_database/queries/insert.sql'
    RETRIEVE = 'vector_database/queries/retrieve.sql'


    def get_query(self) -> str:
        """Read and return the SQL query from the file associated with the enum member."""
        # Check if the query content is already cached
        if not hasattr(self, '_content'):
            try:
                # Read the file content and cache it
                with open(self.value, 'r', encoding='utf-8') as f:
                    self._content = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"The file '{self.value}' does not exist.")
            except IOError as e:
                raise IOError(f"An error occurred while reading '{self.value}': {e}")

        return self._content

