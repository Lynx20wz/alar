import { redirect } from "@sveltejs/kit";
import { isPublicRoute } from "$lib/config";
import type { User } from "$lib/types/User";

export const handle = async ({ event, resolve }) => {
  if (isPublicRoute(event.url.pathname)) {
    return resolve(event);
  }
  
  const token = event.cookies.get("token");
  const username = event.cookies.get("username");

  console.log(token, username);
  if (!username || !token) {
    throw redirect(302, "/login");
  }

  let userDB;

  try {
    const response = await fetch(`http://localhost:8000/user/${username}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const json = await response.json();

    if (!response.ok) {
      throw new Error(
        `HTTP error! status: ${response.status} | ${json.detail}`
      );
    }

    console.log(json);
    userDB = json.user as User;
  } catch (error) {
    console.log(error);
    console.error("Failed to fetch user:", error);
  }

  if (!userDB) {
    throw redirect(302, "/login");
  }

  console.log("Authenticated: ", userDB);

  event.locals.user = userDB;

  return resolve(event);
};

declare global {
  namespace App {
    interface Locals {
      user: User;
    }
  }
}
