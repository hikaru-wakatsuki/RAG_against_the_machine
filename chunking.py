def read_file(file_path: str) -> str:
	"""Read and return the contents of a UTF-8 text file."""
	try:
		with open(file_path, encoding="utf-8") as file:
			content = file.read()
			return content
	except (OSError, UnicodeError) as error:
		raise RuntimeError(
			f"Failed to read file '{file_path}': {error}") from error


