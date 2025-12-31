import type { IUserBuilder } from "./builder";
import type { IUser } from "./model";

export interface IUserFactory {
  user(id: number, name: string): IUser;
  admin(id: number, name: string): IUser;
}

export class UserFactory {
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
