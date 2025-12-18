import type { UserInfo } from "$lib/types/User";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params }) => {
  const username = params.username;

  try {
    const response = await fetch(`/api/users?u=${username}`);
    const json = await response.json();

    if (!response.ok) alert(json.detail)
    return { visited_user: json.data as UserInfo }
  } catch (error) {
    console.error(error)
  };
};
