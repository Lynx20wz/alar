<script lang="ts">
  import type { UserShortInfo } from "$lib/types/User";
  
  export let user: UserShortInfo;

  export function setDefaultAvatar(event: Event) {
    const img = event.currentTarget as HTMLImageElement;
    img.src =
      "data:image/svg+xml;utf8," +
      encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="#333333"/></svg>`
      );
  }
</script>

<a href="/{user.username}" class="user-card df">
  <img
    class="user-card__avatar"
    src={`/api/user/avatar/${user.username}`}
    alt="user avatar"
    onerror={setDefaultAvatar}
  />
  <h5 class="user-card__username">{user.username}</h5>
</a>

<style lang="scss">
  .user-card {
    gap: 5px;
    text-decoration: none;
    &__avatar {
      border-radius: 50%;
      height: 40px;
    }
  }
</style>
