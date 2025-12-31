export interface ILogger {
  debug(message: string, meta?: unknown): void;
  info(message: string, meta?: unknown): void;
  warn(message: string, meta?: unknown): void;
  error(message: string, meta?: unknown): void;
}

export class ConsoleLogger implements ILogger {
  debug(message: string, meta?: unknown): void {
    console.debug(message, meta ?? "");
  }

  info(message: string, meta?: unknown): void {
    console.info(message, meta ?? "");
  }

  warn(message: string, meta?: unknown): void {
    console.warn(message, meta ?? "");
  }

  error(message: string, meta?: unknown): void {
    console.error(message, meta ?? "");
  }
}

export class NullLogger implements ILogger {
  debug(): void {}
  info(): void {}
  warn(): void {}
  error(): void {}
}
