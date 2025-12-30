# typescript-lab

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

## References

- [Typescript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

