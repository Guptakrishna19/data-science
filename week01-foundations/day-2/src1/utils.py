
#Flatten 

from importlib.resources.readers import remove_duplicates


flatten ([[1, 2], [3, 4]])
# Output: [1, 2, 3, 4]

flatten ([[1, 2], [3, [4, 5]]])
# Output: [1, 2, 3, 4, 5]   

flatten ([[1, 2], [3, [4, [5, 6]]]])
# Output: [1, 2, 3, 4, 5, 6]    

#chunk list into smaller lists of a specified size
chunk([1, 2, 3, 4, 5], 2)
# Output: [[1, 2], [3, 4], [5]] 

chunk([1,4,6,7,3,8,4,2,0],3)
# Output: [[1, 4, 6], [7, 3, 8], [4, 2, 0]]

#remove_duplicate list elements
remove_duplicates([1, 2, 3, 2, 1])
# Output: [1, 2, 3] 

remove_duplicates([1,2,4,2,5,6,8,4,7])
# Output: [1, 2, 4, 5, 6, 8, 7] 

word_count("hello hello world")
# Output: {'hello': 2, 'world': 1}  

word_count("chandu ki mummy ne chandu ko chandni raat ko chandi ki chamach se chutney chatai ")
# Output: {'chandu': 2, 'ki': 3, 'mummy': 1, 'ne': 1, 'ko': 2, 'chandni': 1, 'raat': 1, 'chandi': 1, 'chamach': 1, 'se': 1, 'chutney': 1, 'chatai': 1}  

snake_to_title
snake_to_title("hello_world")
# "Hello World"
snake_to_title("chandu_ki_mummy_ne_chandu_ko_chandni_raat_ko_chandi_ki_chamach_se_chutney_chatai")
# "Chandu Ki Mummy Ne Chandu Ko Chandni Raat Ko Chandi Ki Chamach Se Chutney Chatai"

Truncate text to a specified length and add "..." if it exceeds that length
truncate_text("This is a long sentence", 10)
# "This is..."

truncate_text("chandu ki mummy ne chandu ko chandni raat ko chandi ki chamach se chutney chatai",26)
# "chandu ki mummy ne chandu ko chandni..." 


#dictionary 
invert_dict({"a": 1, "b": 2})
{1: "a", 2: "b"}

merge_dicts({"a": 1}, {"b": 2})
# {"a": 1, "b": 2}

#safe_division
safe division(10, 2)
# 5.0

safe_division(17, 3)
# 5.666666666666667

#Average 
average(10, 20, 30)
# 20.0
average(5, 10, 15, 20, 21, 17,41,30)
# 20.5

#Testing 
chunk_list([1, 2, 3], 0)
# Output: ValueError: Chunk size must be greater than 0

safe_divide(5, 0)
# Output: ValueError: Cannot divide by zero

