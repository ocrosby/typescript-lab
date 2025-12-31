import {
  UserBuilder,
  UserFactory,
  UserRepository,
  UserSerializer,
  type IUser,
  type IUserBuilder,
  type IUserFactory,
  type IUserRepository,
  type IUserSerializer,
} from "./domain";

import { ConsoleLogger, type ILogger } from "./logging";

const logger: ILogger = new ConsoleLogger();
const serializer: IUserSerializer = new UserSerializer();
const builder: IUserBuilder = new UserBuilder();
const factory: IUserFactory = new UserFactory(builder);
const repository: IUserRepository = new UserRepository(serializer, logger);

const user1: IUser = factory.user(2, "Murphy");
const user2: IUser = factory.admin(1, "Root");

console.log(serializer.serialize(user1));
console.log(serializer.serialize(user2));

repository.delete(user1);
