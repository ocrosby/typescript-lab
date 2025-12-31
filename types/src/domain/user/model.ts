export type Role = "user" | "admin" | "moderator";

export interface IUser {
  name: string;
  id: number;
  role: Role;
}

export interface IUserSerializer {
  serialize(user: IUser): string;
}

export class User implements IUser {
  name = "";
  id = 0;
  role: Role = "user";
}

export class UserSerializer implements IUserSerializer {
  serialize(user: IUser): string {
    return `User(id=${user.id}, name=${user.name}, role=${user.role})`;
  }
}
