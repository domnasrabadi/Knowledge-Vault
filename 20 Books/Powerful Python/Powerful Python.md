---
type: book
status: structured
quality:
topics: [software-engineering]
source: ""
created: 2024-12-26
published:
author: ""
flashcards: none
updated: 2024-12-26
---

> [!NOTE] This Book
> - This book is for those that want to develop a deep intuition of Python from first principles
> - Learning can occur in 2 ways
> 	- **information level** = learning through reading or memorising 
> 	- **ability level** = learning through doing without assistance, actually writing the code from scratch 
> 		- Rahul Pandey talks about "*Tutorial Hell*" where you actually get worse by doing more tutorials since you cannot code from scratch and tackle problems by yourself
> - **first principles** are the foundational concepts everything builds on - especially true in Python
> 	- the powerful distinctions, abstractions and mental models that give you 95% of the bang 
> 	- with just 5% of the key concepts 
> - some notes on what this book does and does NOT cover
> 	- mainly covers standard library 
> 	- no type hints 
> 	- no dataclasses
> 	- no concurrency 
> 	- nothing re specific python versions 
> 	- no regex, kwargs, args etc 


![[Screenshot 2024-12-26 at 12.42.07 pm.png| center | 400]]


# 1 Generators
- **iteration** = going through a collection sequentially (one element at a time)
	- `iter()` is a built in python method
		- pass in a collection, and get back an *iterator object* 
	- a `{python}for loop` actually uses `iter()` under the hood 
		- whatever object passed in the for loop gets called as an iterator
		- `iter()` actually relies on the special method `__iter__()`
			- any class can define this and is called without any args 
			- each time it's called, it produces a new iterator object 
```python
numbers = [1, 2, 3, 4, 5]

for num in numbers:
	print(num)

# is the same as ...
nums_iter = iter(numbers)
for num in nums_iter:
	print(num)
```
- note: the iterator object use is actually distinct to the collection 
	- can check this via the `id()` of each
```python
id(numbers) # 4330129862

id(nums_iter) # 4330216670
```
- 
- Python has clear distinction between iterable vs iterator 
	- <mark style="background: #FFB8EBA6;">iterable</mark> = object is iterable if you can pass it to iter() and get a ready to use iterator object
		- strings, lists, tuples are all iterable, anything you can use in a for loop is iterable
		- formally, should have `{python}__iter__()` method and also `{python}__getitem__()`
	- <mark style="background: #FFB8EBA6;">iterator</mark> = something you can pass to `next()` and follows Python's iterator protocol i.e.
		- defines special method `{python}__next__()` and `StopIteraton` and has boilerplate `{python}__iter__()` method
	- instead of using a for-loop, you can use `next()` for more fine-grained control over the iterator
		- once the iterator object gets exhausted, and you try `next()` again, you will get a special error for generators
		- known as the `StopIteration` exception 
		- this is how you know the sequence is done
```python
numbers = [1, 2, 3, 4, 5]

next(numbers)
>>> 1

next(numbers)
>>> 2

...

next(numbers)
>>> 5

next(numbers)
# >>> Traceback (most recent call last):  
# >>>   File "<stdin>", line 1, in <module>
# >>> StopIteration
```

- generators are very important when you have a very large potential memory footprint 
	- imagine calculating squared version of numbers up to some number e.g. 1000
	- if that number is massive, this can be a huge bottleneck and pointless e.g. 
```python
def fetch_squares(max_root):
	squares = []
	for n in range(max_root):
		squares.appnd(n**2)
	return squares

# this will create a massive list in line 7, use it once, then throw it away - not good practice
for square in fetch_squares(max_root = 1000):
	do_something_with(square)
```
- <mark style="background: #FFB8EBA6;">generator</mark> = **uses lazy evaluation as opposed to eager** i.e. only computes when needed/on the fly 
	- one of Python's most powerful tools, key for scalability 
	- syntactic differences between generators and loops 
		- `next()` to get the next value or iteration 
		- `yield` instead of `return` - must be used to specify it as a generator 
	- a generator function ALWAYS returns a generator object, nothing else
		- e.g. generator object below would be `sequence`
```python
# creating a generator using yield keyword
def gen_nums(): 
	n = 0 
	while n < 4: 
		yield n 
		n += 1

# when you call gen_nums like a func, it returns 'generator' type
sequence = gen_nums()
type(sequence)
# <class 'generator'>

# iterating through the generator object
for num in gen_nums():
	print(num)
# 0
# 1
# 2
# 3
```
- another big distinction in using generators is they basically use the `yield` as checkpoints
	- for exiting and re-entering into the flow of control
	- so when something is yielded, and then you use the generator again, you start exactly where you left off
- you can also have multiple yield statements in a generator
```python
def my_generator():
    print("Starting the generator...")
    yield 1  # <-- first yield

    print("Resuming after first yield...")
    yield 2  # <-- second yield

    print("Resuming after second yield...")
    yield 3  # <-- third yield

    print("Generator function is about to end.")

gen = my_generator()

print("Calling next(gen) the first time:")
value = next(gen) 
# Starting the generator...
# 1

print("Calling next(gen) the second time:")
value = next(gen) 
# Resuming after first yield...
# 2 

print("Calling next(gen) the third time:")
value = next(gen) 
# Resuming after second yield...
# 3

print("Calling next(gen) the fourth time (no more yields):")
value = next(gen)  # Raises StopIteration (end of generator)
```
- now revisiting the `fetch_squares()` example, here is the generator version 
	- which uses `range()` - this is important since if it was a function that would ruin the scalability
```python
def gen_squares(max_root):
	for num in range(max_root):
		yield num ** 2

for square in gen_squares(max_root = 1000):
	print(square)
```

>[!warning] Generators are as scalable as their least scalable line of code!

- one other benefit of generators is they are much easier to maintain compared to some custom class which tries to manage checkpoints etc 
	- they just make patterns for scalability much easier
- <mark style="background: #FFB8EBA6;">scalable composability</mark> = decomposing functionality into small re-usable blocks
	- which can then be assembled together into bigger more complex programs 
- example: reading data from a file and manipulating it, some best practices from below
	- uses context manager named as `handle` for automatic resource management 
	- uses the expression to simplify things `{python}for line in handle`
		- much more readable than `{python}line = handle.readline()...`
```python
# first function to read data from file
def matching_lines_from_file(path, pattern):
	with open(path) as handle:
		for line in handle:
			if pattern in line:
				yield line.rstrip('\n')
```

>[!danger] Least Scalable Line! Don't do this...
```python
for line in handle.readlines():
```
- now let's improve this via decomposing it
	- goal is to get strings from the file and transform them into a python dictionary 
	- this is what our input data looks like 

> *WARNING: Disk usage exceeding 85%* 
> *DEBUG: User 'tinytim' upgraded to Pro version* 
> *INFO: Sent email campaign, completed normally* 
> *WARNING: Almost out of beer*

```python
# second function to parse the data
def parse_log_records(lines):
	for line in lines():
		level, message = line.split(": ", 1)
		yield {"level": level, "message": message}
```
- now can connect both `{python}parse_log_records()` and `{python}matching_lines_from_file()`
	- these 2 functions are like building blocks 
```python
# log_lines = generator object 
log_lines = matching_lines_from_file("log.txt", "WARNING:")

for record in parse_log_records(log_lines):
	print(record) # record = dict
```
- notice both produce generators as output, but have different interfaces for inputs
	- `{python}parse_log_records()` - takes in an iterator 
	- `{python}matching_lines_from_file()` - takes in a path to read from 
	- combining functions is often good in real life, but ideally you want consistent interfaces 
	- when designing programs with decomposed functions, think through what each does
		- is the function a sink (consumes things without producing an iterator) or a source (produces an iterator)
		- or does it do filtering, or mapping or a combination of these
- 2 types of patterns for function that deal with data 
	- fanning out = read in one record, output multiple records
	- fanning in = read in multiple records, output a single record
- iterables are everywhere in python
	- almost all built-in collection types are iterable - make sure to inherit from these for custom classes for functionality
	- even `{python}dict.items()` is iterable - note: if you iter over just `{python}dict` it will just go over the keys

---
# 2 Comprehensions
---
# 3 Advanced Functions
---
# 4 Decorators
---
# 5 Exceptions & Errors
---
# 6 Classes & Objects
---
# 7 Automated Testing 
---
# 8 Module Organisation 
---
# 9 Logging 
---



