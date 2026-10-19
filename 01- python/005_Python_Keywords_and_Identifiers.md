# Python Keywords and Identifiers

In this class, you will learn about keywords (reserved words in Python) and identifiers (names given to variables, functions, etc.).

# 1. Python Keywords

Keywords are the reserved words in Python.

We cannot use a keyword as a **variable** name, **function** name or any other identifier. They are used to define the syntax and structure of the Python language.

In Python, keywords are **case sensitive**.

There are **36** keywords in Python 3.9. This number can vary slightly over the course of time.
![Figure: All Python Keywords](../../img/k1.png)


All the keywords except **`True`**, **`False`** and **`None`** are in lowercase and they must be written as they are. The **list of all the keywords** is given below.

**Keywords in Python**

|     |     |     |     |
|:----|:----|:----|:----|
| **`False`** | **`break`** | **`for`** | **`not`** |
| **`None`**  | **`class`** | **`from`** | **`or`** |
| **`True`**  | **`continue`** | **`global`** | **`pass`** |
| **`__peg_parser__`** |**`def`** | **`if`** | **`raise`** |
| **`and`** | **`del`** | **`import`** | **`return`** |
| **`as`** | **`elif`** | **`in`** | **`try`** |
| **`assert`** | **`else`** | **`is`** | **`while`** |
| **`async`** | **`except`** | **`lambda`** | **`with`** |
| **`await`** | **`finally`** | **`nonlocal`** |  **`yield`**  |

You can see this list any time by typing help **`keywords`** to the Python interpreter.

Trying to create a variable with the same name as any reserved word results in an **error**:

```python
for = 6

File "<ipython-input-1-50b154750974>", line 1
for = 6 # It will give error becasue "for" is keyword and we cannot use as a variable name.
        ^
SyntaxError: invalid syntax
![Figure: SyntaxError when using special character in identifier](../../img/i2.png)

```


```python
for = 6 # It will give error becasue "for" is keyword and we cannot use as a variable name.
```


```python
For = 6 # "for" is keyword but "For" is not keyword so we can use it as variable name
print(For)
```


# 2. Python Identifiers

An **identifier** is a name given to entities like **class, functions, variables, etc**. It helps to differentiate one entity from another.

### Rules for writing identifiers

1. **Identifiers** can be a combination of letters in lowercase **(a to z)** or uppercase **(A to Z)** or digits **(0 to 9)** or an underscore **`_`**. Names like **`myClass`**, **`var_1`** and **`print_this_to_screen`**, all are valid example.

2. An identifier cannot start with a digit. **`1variable`** is invalid, but **`variable1`** is perfectly fine.

3. Keywords cannot be used as identifiers

```python
global = 3

File "<ipython-input-2-43186c7d3555>", line 1
    global = 3 # because "global" is a keyword
           ^
SyntaxError: invalid syntax
```


```python
global = 3 # because "global" is a keyword
```


4. We cannot use special symbols like **!**, **@**, **#**,<b> $, % </b>, etc. in our identifier.

```python
m@ = 3

File "<ipython-input-3-4d4a0e714c73>", line 1
    m@ = 3
       ^
SyntaxError: invalid syntax
```


```python
print(m@ = 3)
```


## Things to Remember

Python is a case-sensitive language. This means, **`Variable`** and **`variable`** are not the same.

Always give the identifiers a name that makes sense. While **`c = 10`** is a valid name, writing **`count = 10`** would make more sense, and it would be easier to figure out what it represents when you look at your code after a long gap.

Multiple words can be separated using an underscore, like **`this_is_a_long_variable`**.

```python
this_is_a_long_variable = 6+3
print(this_is_a_long_variable)
```


```python
add_6_and_3 = 6+3
print(add_6_and_3)
```


### **Task: Organizing library database**
You are tasked with creating a simple Python script to manage a library database. In the library, books are categorized as either available or issued. Each book has the following attributes:
- **title:** The title of the book.
- **author:** The name of the author.
- **is_available:** A status indicating whether the book is available (True) or issued (False).

You must use appropriate keywords and identifiers to create this script and meet the requirements.

**Instructions:**
Write a Python script to perform the following:
- Create two books using valid identifiers:
  - The first book is titled "Python Basics," written by "John Doe," and is available
  - The second book is titled "Data Science 101," written by "Jane Smith," and is currently issued
  - Display the details of each book using meaningful identifiers and the print() function
- Use the not keyword to toggle the availability status of the second book and update its is_available attribute to True (marking it as returned)
- Print a summary that shows the updated availability status of the second book


> **Hints:**
  - Use identifiers like `book1_title`, `book1_author`, and `book1_is_available` for the attributes.
  - Use keywords like `True`, `False`, and `not` to manage the book's availability status
  - Remember to use valid identifiers that follow Python's naming rules. Avoid using reserved keywords like class or for as variable names



