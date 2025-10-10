import type { UserInfo } from "$lib/types/User";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params }) => {
  const username = params.username;

  let visited_user: UserInfo | undefined = undefined;
  try {
    const response = await fetch(`/api/user/${username}`);
    const json = await response.json();
    if (json.success) {
      visited_user = json.user as UserInfo;
    }
  } catch (error) {
    console.error(error);
  }

  return { visited_user };
  
};