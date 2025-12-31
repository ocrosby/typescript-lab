import type { IUserBuilder } from "./domain/user/builder";
import { UserBuilder } from "./domain/user/builder";
import type { IUser, IUserSerializer } from "./domain/user/model";
import { UserSerializer } from "./domain/user/model";
import type { IUserFactory } from "./domain/user/factory";
import { UserFactory } from "./domain/user/factory";
import type { IUserRepository } from "./domain/user/repository";
import { UserRepository } from "./domain/user/repository";
import type { ILogger } from "./logging";
import { ConsoleLogger } from "./logging";

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
