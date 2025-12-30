# TypeScript Lab

A repository to house typescript examples.

## Types

Primitive types available in JavaScript:

- boolean, 
- bigint, 
- null, 
- number, 
- string, 
- symbol, and 
- undefined, 

Types extended by TypeScript:

- any (allow anything), 
- unknown (ensure someone using this type declares what the type is), 
- never (it’s not possible that this type could happen), and 
- void (a function which returns undefined or has no return value).

## Defining Types

This interface explicitly defines an objects "shape".

```Typescript
interface User {
  name: string;
  id: number;
}
```

This is how you can declare that a JavaScript object conforms to the shape of the new interface.

```Typescript
const user: User = {
  name: "Hayes",
  id: 0,
};
```

If you provide an object that doesn’t match the interface you have provided, TypeScript will warn you.

```Typescript
interface User {
  name: string;
  id: number;
}
 
const user: User = {
  username: "Hayes",
  id: 0,
};
```

This will result in an error similar to the following:

`Object literal may only specify known properties, and 'username' does not exist in type 'User'.`


You can use interface declarations with classes in TypeScript:

```Typescript
interface User {
  name: string;
  id: number;
}
 
class UserAccount {
  name: string;
  id: number;
 
  constructor(name: string, id: number) {
    this.name = name;
    this.id = id;
  }
}
 
const user: User = new UserAccount("Murphy", 1);
```

You can use interfaces to annotate parameters and return values for functions:

```Typescript
function deleteUser(user: User) {
  // ...
}
 
function getAdminUser(): User {
  //...
}
```

## Composing Types

With TypeScript, you can create complex types by combining simple ones. There 
are two popular ways to do so: unions and generics.

### Unions

With a union, you can declare that a type could be one of many types. For 
example, you can describe a boolean type as being either true or false:

```Typescript
type MyBool = true | false;
```

You can use union types to describe the set of string or number literals 
that a value is allowed to be:


```Typescript
type WindowStates = "open" | "closed" | "minimized";
type LockStates = "locked" | "unlocked";
type PositiveOddNumbersUnderTen = 1 | 3 | 5 | 7 | 9;
```

To learn the type of a variable, use typeof:

string
: `typeof s === "string"`

number
: `typeof n === "number"`

boolean
: `typeof b === "boolean"`

undefined
: `typeof undefined === "undefined"`

function
: `typeof f === "function"`

array
: `Array.isArray(a)`


```Typescript
function wrapInArray(obj: string | string[]) {
  if (typeof obj === "string") {
    return [obj];
            
(parameter) obj: string
  }
  return obj;
}
```

### Generics

Generics provide variables to types. A common example is an array. 
An array without generics could contain anything. An array with 
generics can describe the values that the array contains.

```Typescript
type StringArray = Array<string>;
type NumberArray = Array<number>;
type ObjectWithNameArray = Array<{ name: string }>;
```

You can declare your own types that use generics:

```Typescript
interface Backpack<Type> {
  add: (obj: Type) => void;
  get: () => Type;
}
 
// This line is a shortcut to tell TypeScript there is a
// constant called `backpack`, and to not worry about where it came from.
declare const backpack: Backpack<string>;
 
// object is a string, because we declared it above as the variable part of Backpack.
const object = backpack.get();
 
// Since the backpack variable is a string, you can't pass a number to the add function.
backpack.add(23);
```

Since the backpack object is declared as `of type string` the addition of a number 
results in an error similar to the following:

`Argument of type 'number' is not assignable to parameter of type 'string'.`



## References

- [Typescript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

