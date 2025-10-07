export const publicRouters = ["/login", "/registration"];

export function isPublicRoute(path: string): boolean {
  return publicRouters.includes(path);
}
