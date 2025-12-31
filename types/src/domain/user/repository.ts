import type { IUser, IUserSerializer } from "./model";
import type { ILogger } from "../../logging";

export interface IUserRepository {
  delete(user: IUser): void;
}

export class UserRepository {
  private serializer: IUserSerializer;
  private logger: ILogger;

  constructor(serializer: IUserSerializer, logger: ILogger) {
    this.serializer = serializer;
    this.logger = logger;
  }

  delete(user: IUser): void {
    this.logger.debug("Todo: delete " + this.serializer.serialize(user));
  }
}
