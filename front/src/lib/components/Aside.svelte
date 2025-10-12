<script lang="ts">
  import UserCard from "$lib/components/UserCard.svelte";
  import { getTranslate } from "@tolgee/svelte";
  import { page } from "$app/state";

  const user = page.data.user;
  const { t } = getTranslate();
</script>

<aside class="aside df">
  <h5 class="aside__header">{$t("favorites")}</h5>
  <ul class="aside__items df">
    {#each user.follows.objects as follow}
      <li class="aside__item df">
        <UserCard user={follow} />
      </li>
    {/each}
  </ul>
</aside>

<style lang="scss">
  .aside {
    height: 500px;
    width: 250px;
    background-color: var(--primary);
    padding: 10px;
    border-radius: 10px;
    flex-direction: column;
    justify-content: flex-start;
    align-items: start;
    gap: 10px;
    flex-shrink: 0;

    &__header {
      width: 100%;
      text-align: center;
    }

    &__items {
      flex-direction: column;
      gap: 10px;
      align-self: stretch;
      align-items: flex-start;
    }
    &__item {
      padding: 5px;
      border-radius: 10px;
      align-self: stretch;
      transition: background-color 0.1s ease-in-out;
      justify-content: flex-start;
      &:hover {
        background-color: rgba(#fff, 0.15);
      }
    }
  }
</style>
