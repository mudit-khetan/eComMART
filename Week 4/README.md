# Week 4: Object-Oriented Programming and File Handling

## eCOMMart AI Squad | Python Fundamentals

Welcome to Week 4. This week moves from functions and dictionaries to building
programs around objects, then teaches you how to read, write, and configure
applications with files.

## Learning Goals

By the end of this week, you will be able to:

- Explain when object-oriented programming (OOP) helps organize an application.
- Design classes with attributes, methods, and clear responsibilities.
- Use encapsulation, properties, inheritance, and composition appropriately.
- Read and write text, JSON, and CSV files safely.
- Load configuration and save application data.
- Combine these skills in a small product-catalog application.

## Learning Path

Work through the sections in order. The first section reviews concepts from
earlier weeks before introducing OOP.

### 01 - Getting Ready for OOP

| Lesson | What you will learn |
|---|---|
| [Reviewing Python Functions and Dictionaries](01_Getting_Ready_for_OOP/01_Reviewing_Python_Functions_and_Dicts.md) | Recognize where functions and dictionaries work well and where they become difficult to manage. |
| [What Is OOP and Why It Matters](01_Getting_Ready_for_OOP/02_What_is_OOP_and_Why_It_Matters.md) | Understand the purpose of OOP and how it organizes related data and behavior. |
| [Thinking in Objects](01_Getting_Ready_for_OOP/03_Thinking_in_Objects.md) | Identify objects and responsibilities when breaking down a problem. |

### 02 - Classes and Objects

| Lesson | What you will learn |
|---|---|
| [What Are Classes and Objects](02_Classes_and_Objects/01_What_Are_Classes_and_Objects.md) | Distinguish a class blueprint from the objects created from it. |
| [Building a Class Step by Step](02_Classes_and_Objects/02_Building_a_Class_Step_by_Step.md) | Construct a useful class incrementally. |
| [The `__init__` Method and `self`](02_Classes_and_Objects/03_The_init_Method_and_self.md) | Initialize objects and understand how instance methods receive their object. |
| [Instance Attributes and Class Attributes](02_Classes_and_Objects/04_Instance_Attributes_and_Class_Attributes.md) | Choose between per-object data and data shared by a class. |
| [Methods](02_Classes_and_Objects/05_Methods.md) | Add behavior to classes with instance, class, and static methods. |
| [`__str__` and `__repr__`](02_Classes_and_Objects/06_str_and_repr.md) | Make objects readable for users and useful for debugging. |
| [Encapsulation and Properties](02_Classes_and_Objects/07_Encapsulation_and_Properties.md) | Protect object rules and validate access to attributes. |
| [Inheritance](02_Classes_and_Objects/08_Inheritance.md) | Reuse and specialize behavior in related classes. |
| [Composition](02_Classes_and_Objects/09_Composition.md) | Build objects from other collaborating objects. |

### 03 - File Handling

| Lesson | What you will learn |
|---|---|
| [Reading Files and Iterating Lines](03_File_Handling/01_Reading_Files_and_Iterating_Lines.md) | Open text files and process their contents line by line. |
| [Writing and Appending Files](03_File_Handling/02_Writing_and_Appending_Files.md) | Save new content or add content to an existing file. |
| [`with open()` and File Modes](03_File_Handling/03_with_open_and_File_Modes.md) | Manage file lifetimes and select the appropriate mode. |
| [Working with CSV](03_File_Handling/05_Working_with_CSV.md) | Read and write row-and-column data in CSV format. |
| [Working with JSON](03_File_Handling/04_Working_with_JSON.md) | Store and load structured data as JSON. |

### 04 - Configuration and Data

| Lesson | What you will learn |
|---|---|
| [File Paths and `os.path`](04_Configuration_and_Data/01_File_Paths_and_os_path.md) | Build and check file paths reliably. |
| [Loading Configuration from JSON](04_Configuration_and_Data/02_Loading_Config_from_JSON.md) | Keep application settings outside the program code. |
| [Saving Application Output](04_Configuration_and_Data/03_Saving_Application_Output.md) | Persist the results of an application run. |
| [File Error Handling](04_Configuration_and_Data/04_File_Error_Handling.md) | Handle missing files and invalid or unexpected file data. |

### 05 - Worked Examples

Follow the examples to see the week's concepts used in complete applications:

1. [Product Class from Scratch](05_Worked_Examples/01_Product_Class_From_Scratch.md)
2. [Catalog Manager with Inheritance](05_Worked_Examples/02_Catalog_Manager_with_Inheritance.md)
3. [Reading and Writing Product Data](05_Worked_Examples/03_Reading_and_Writing_Product_Data.md)
4. [Config-Driven Application](05_Worked_Examples/04_Config_Driven_Application.md)
5. [Mini OOP Agent Tool](05_Worked_Examples/05_Mini_OOP_Agent_Tool.md)

### 06 - Practice

- [Exercises](06_Exercises/exercises.md) - Apply the concepts from the lessons.
- [Solutions](06_Exercises/solutions.md) - Check your work after attempting the exercises.

## Suggested Study Routine

1. Read each lesson and type out the examples yourself.
2. Run the code and inspect how objects and files behave.
3. Complete the worked examples before moving on to the exercises.
4. Try the exercises without looking at the solutions first.

> The examples use eCOMMart products and catalogs to connect OOP and file
> handling to a practical application.
