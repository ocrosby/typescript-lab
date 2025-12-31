import type { Role, IUser } from "./model";
import { User } from "./model";

export interface IUserBuilder {
  build(): this;
  id(value: number): this;
  name(value: string): this;
  role(value: Role): this;
  getInstance(): IUser;
}

export class UserBuilder implements IUserBuilder {
  private user: IUser | undefined;

  build(): this {
    this.user = new User();
    return this;
  }

  name(value: string): this {
    if (!this.user) throw new Error("User not initialized");
    this.user.name = value;
    return this;
  }

  id(value: number): this {
    if (!this.user) throw new Error("User not initialized");
    this.user.id = value;
    return this;
  }

  role(value: Role): this {
    if (!this.user) throw new Error("User not initialized");
    this.user.role = value;
    return this;
  }

  getInstance(): IUser {
    if (!this.user) throw new Error("User not initialized");
    return this.user;
  }
}
