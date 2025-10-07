import type { User } from "$lib/types/User";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params }) => {
  const username = params.username;

  let visited_user: User | undefined = undefined;
  try {
    const response = await fetch(`/api/user/${username}`);
    const json = await response.json();
    if (json.success) {
      visited_user = json.user as User;
    }
  } catch (error) {
    console.error(error);
  }

  return { visited_user };
};
