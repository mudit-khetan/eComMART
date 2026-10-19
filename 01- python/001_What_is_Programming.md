# What is programming?

Feel free to **skip this part** if you already know everything it's talking about.

As a computer user you know that computers don't have feelings. They don't work any faster or slower depending on if we're angry at them or if we're happy. Computers can perform millions of calculations per second, but they require us to tell them exactly what to do. If they do something else than we want them to do the problem is usually that they don't understand our instructions the way we understand them.

The only big difference between programming and what you're familiar with already is that instead of clicking buttons to do things we write the instructions using a **programming language**.
![Figure: How an Interpreter processes your Python code vs a Compiler](../../img/IvsC.png)
 Most programming languages consist of English words, digits and some characters that have special meanings.

Unlike people often think, programming is usually not complicated. Large programs are always made of small, simple pieces, and those pieces are written one by one. Programming languages are made to be used by humans, so if there's an easy way to do something and a difficult way to do something, you should use the easier way.

## What do I need?

First of all, you don't need to be good at math. Some programmers are good at math, some are not. Programming and math are two separate things and being good or bad at one doesn't mean you are automatically good or bad at the other.

You also don't need a powerful computer. I could do almost all of my programming on a 12-year-old computer if I needed to. Fast computers are nice to work with, but you don't need them.

Programming takes time like all hobbies do. Some people learn it quickly, and some people don't. I don't expect you to read this tutorial in a couple hours and then master everything it's talking about. Take your time with things, and remember that I learned to program slowly.

## Getting started

This tutorial uses a programming language called Python because it's easy to learn and we can do many different things with it. For example, we can create our own applications that have buttons that people can click instead of just using applications written by others.

In this tutorial we need to know how to type these characters. We'll learn their meanings later.

| Character | Names |
|:---: |:--- |
| **`+`** | **plus** |
| **`-`** | **minus, dash** |
| **`_`** | **underscore** |
| **`*`** | **star, asterisk** |
| **`/`** | **forwardslash (it's leaning forward)** |
| **`\`** | **backslash (it's leaning back)** |
| **`=`** | **equals sign** |
| **`%`** | **percent sign** |
| **`.`** | **dot** |
| **`,`** | **comma** |
| **`:`** | **colon** |
| **`;`** | **semi-colon** |
| **`?`** | **question mark** |
| **`!`** | **exclamation mark** |
| **`< >`** | **less-than and greater-than signs** |
| **`' "`** | **single quote and double quote** |
| **`#`** | **hashtag** |
| **`()`** | **parentheses** |
| **`[]`** | **square brackets, brackets** |
| **`{}`** | **curly braces, braces, curly brackets** |

That may seem like many characters, but you probably know many of them already so it shouldn't be a problem.

<a id="howto"></a>
## How to read this tutorial

I've done my best to make this tutorial as easy to follow as possible. Other people have commented on this and helped me improve this a lot also. But what should you do if you have a problem with the tutorial?

1. Try the example code yourself.
2. Read the code and the explanation for it again.
3. If there's something you haven't seen before in the tutorial and it's not explained, try to find it in the previous chapters.
4. If you can't find what you're looking for or you still have trouble understanding the tutorial or any other problems with the tutorial, please tell me about it by **Create an issue on GitHub**. I want to improve this tutorial so other readers won't have the same problem as you have.

One of the most important things with learning to program is to not fear mistakes. If you make a mistake, your computer will not break in any way. You'll get an error message that tells you what's wrong and where. Even professional programmers do mistakes and get error messages all the time, and there's nothing wrong with it.

If you want to know what some piece of code in this tutorial does just **try it and see**. It's practically impossible to break anything accidentally with the things you will learn by reading this tutorial, so you are free to try out all the examples however you want and change them to do whatever you want.

Even though a good tutorial is an important part about learning to program, you also need to learn to make your own things. Use what you have learned, and create something with it.

## But reading is boring!

This chapter is probably the most boring chapter in the whole tutorial. Other chapters contain much less text and much more code. You can also get pretty far by just reading the code, and then reading the text only if you don't understand the code.


## Python Operators — Quick Reference

Operators are special symbols that perform operations on values and variables.

### Arithmetic Operators
| Operator | Name | Example | Result |
|:---:|---|---|---|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | Division | `10 / 3` | `3.333...` |
| `//` | Floor Division | `10 // 3` | `3` |
| `%` | Modulus (Remainder) | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 8` | `256` |

### Comparison Operators
| Operator | Meaning | Example | Result |
|:---:|---|---|---|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `3 <= 5` | `True` |

### Assignment Operators
| Operator | Example | Equivalent to |
|:---:|---|---|
| `=` | `x = 10` | Assign 10 to x |
| `+=` | `x += 3` | `x = x + 3` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 3` | `x = x * 3` |
| `/=` | `x /= 3` | `x = x / 3` |
| `//=` | `x //= 3` | `x = x // 3` |
| `%=` | `x %= 3` | `x = x % 3` |
| `**=` | `x **= 3` | `x = x ** 3` |

### Logical Operators
| Operator | Meaning | Example | Result |
|:---:|---|---|---|
| `and` | True if both are True | `True and False` | `False` |
| `or` | True if at least one is True | `True or False` | `True` |
| `not` | Reverses the boolean | `not True` | `False` |

### Membership Operators
| Operator | Meaning | Example |
|:---:|---|---|
| `in` | True if value is in sequence | `"a" in "apple"` → `True` |
| `not in` | True if value is NOT in sequence | `5 not in [1,2,3]` → `True` |

### Identity Operators
| Operator | Meaning | Example |
|:---:|---|---|
| `is` | True if both refer to same object | `x is None` |
| `is not` | True if they refer to different objects | `x is not None` |

### Bitwise Operators
| Operator | Name | Example |
|:---:|---|---|
| `&` | AND | `6 & 3` → `2` |
| `\|` | OR | `6 \| 3` → `7` |
| `^` | XOR | `6 ^ 3` → `5` |
| `~` | NOT | `~6` → `-7` |
| `<<` | Left Shift | `6 << 1` → `12` |
| `>>` | Right Shift | `6 >> 1` → `3` |

### Operator Precedence (Grouping)
Python evaluates expressions in this order (highest to lowest):

| Priority | Operator(s) | Description |
|:---:|---|---|
| 1 | `()` | Parentheses — always evaluated first |
| 2 | `**` | Exponentiation |
| 3 | `+x`, `-x`, `~x` | Unary operators |
| 4 | `*`, `/`, `//`, `%` | Multiplication, Division |
| 5 | `+`, `-` | Addition, Subtraction |
| 6 | `<<`, `>>` | Bitwise shifts |
| 7 | `&` | Bitwise AND |
| 8 | `^` | Bitwise XOR |
| 9 | `\|` | Bitwise OR |
| 10 | `==`, `!=`, `>`, `<`, `>=`, `<=`, `is`, `in` | Comparisons |
| 11 | `not` | Logical NOT |
| 12 | `and` | Logical AND |
| 13 | `or` | Logical OR |

> **Tip:** When in doubt, use `()` parentheses to make your intent explicit.
> `2 + 3 * 4` = `14` but `(2 + 3) * 4` = `20`

## Summary

* Now you should know what programming and programming languages are.
* You don't need to be good at math and you don't need a new computer.
* Complicated programs consist of simple pieces.
* You don't need to remember how to type different characters. Just find the character on your * keyboard and press the key, holding down shift or AltGr as needed.
* Make sure you understand everything you read.
* Experiment with things freely and don't fear mistakes.
* Error messages are our friends.
* Let me know if you have trouble with this tutorial.
* Now we're ready to **install Python** and **get started** and continue with next file in the list.!
