import { redirect } from "@sveltejs/kit";
import { isPublicRoute } from "$lib/utils";
import type { UserInfo } from "$lib/types/User";

export const handle = async ({ event, resolve }) => {
  if (isPublicRoute(event.url.pathname)) {
    return resolve(event);
  }

  const token = event.cookies.get("token");
  const username = event.cookies.get("username");

  if (!username || !token) {
    throw redirect(302, "/login");
  }

  let userDB;

  try {
    const response = await event.fetch(`http://localhost:8000/users/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const json = await response.json();

    console.log(json);
    userDB = json.user as UserInfo;
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
      user: UserInfo;
    }
  }
}
