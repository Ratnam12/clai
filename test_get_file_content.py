from functions.get_file_content import get_file_content

# Test truncation with lorem.txt
result = get_file_content("calculator", "lorem.txt")
print(f"Lorem ipsum test:")
print(f"  Length: {len(result)} characters")
print(f"  End of content: ...{result[-80:]}")
print()

# Test main.py
print('get_file_content("calculator", "main.py"):')
print(get_file_content("calculator", "main.py"))
print()

# Test pkg/calculator.py
print('get_file_content("calculator", "pkg/calculator.py"):')
print(get_file_content("calculator", "pkg/calculator.py"))
print()

# Test outside working directory
print('get_file_content("calculator", "/bin/cat"):')
print(get_file_content("calculator", "/bin/cat"))
print()

# Test file that doesn't exist
print('get_file_content("calculator", "pkg/does_not_exist.py"):')
print(get_file_content("calculator", "pkg/does_not_exist.py"))
