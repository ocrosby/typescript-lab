export type Role = "user" | "admin" | "moderator";

export interface IUser {
  name: string;
  id: number;
  role: Role;
}

class User {
  name: string;
  id: number;
  role: Role;

  constructor() {
    this.name = "";
    this.id = 0;
    this.role = "user";
  }
}

export interface IUserBuilder {
  build(): this;
  id(value: number): this;
  name(value: string): this;
  role(value: Role): this;
  getInstance(): IUser;
}

class UserBuilder {
  private user: IUser | undefined;

  constructor() {
    this.user = undefined;
  }

  build(): UserBuilder {
    this.user = new User();
    return this;
  }

  name(value: string): this {
    if (!this.user) {
      throw new Error("User not initialized");
    }

    this.user.name = value;
    return this;
  }

  id(value: number): this {
    if (!this.user) {
      throw new Error("User not initialized");
    }

    this.user.id = value;
    return this;
  }

  role(value: Role): this {
    if (!this.user) {
      throw new Error("User not initialized");
    }

    this.user.role = value;
    return this;
  }

  getInstance(): IUser {
    if (!this.user) {
      throw new Error("User not initialized");
    }

    return this.user;
  }
}

class UserFactory {
  private builder: IUserBuilder;

  constructor(builder: IUserBuilder) {
    this.builder = builder;
  }

  user(id: number, name: string): IUser {
    this.builder.build();
    this.builder.id(id);
    this.builder.name(name);
    this.builder.role("user");

    return this.builder.getInstance();
  }

  admin(id: number, name: string): IUser {
    this.builder.build();
    this.builder.id(id);
    this.builder.name(name);
    this.builder.role("admin");

    return this.builder.getInstance();
  }
}

const builder: UserBuilder = new UserBuilder();
const factory: UserFactory = new UserFactory(builder);
const user1: IUser = factory.user(2, "Murphy");
const user2: IUser = factory.admin(1, "Root");

function stringifyUser(user: IUser): string {
  return `User(id=${user.id}, name=${user.name}, role=${user.role})`;
}

function deleteUser(user: IUser) {
  console.log("Todo: Delete " + stringifyUser(user));
}

console.log(stringifyUser(user1));
console.log(stringifyUser(user2));

deleteUser(user1);
