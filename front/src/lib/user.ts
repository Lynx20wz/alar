import { publicRouter } from "./config";
import type { User } from "./types/User";

export async function getUser(): Promise<User|undefined> {
  const token = localStorage.getItem("auth_token");
  const username = localStorage.getItem("username");

  if (!token && !username && !publicRouter.includes(window.location.pathname)) {
    window.location.href = "/login";
  }

  const user = await fetch(`/api/user/${username}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }).then((res) => res.json());
  return user as User;
}

export async function getAvatarUrl(): Promise<string|undefined> {
  const username = localStorage.getItem("username");

  if (!username && !publicRouter.includes(window.location.pathname)) {
    return;
  }
  
  return '/api/avatar/' + username
}
