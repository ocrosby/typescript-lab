import type { IUser, IUserSerializer } from "./model";

export interface IUserRepository {
  delete(user: IUser): void;
}

export class UserRepository {
  private serializer: IUserSerializer;

  constructor(serializer: IUserSerializer) {
    this.serializer = serializer;
  }

  delete(user: IUser): void {
    console.log("Todo: delete " + this.serializer.serialize(user));
  }
}
